#uvicorn clienthandler:app --reload --port 8000 --workers 4
import sqlite3
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from gradio_client import Client
client = Client("http://localhost:7860")
app = FastAPI()

# Connect to the SQLite database (creates a new file if it doesn't exist)
conn = sqlite3.connect('chatbot_log.db')
cursor = conn.cursor()

# Create a table to store the chat logs if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_log (
        message TEXT PRIMARY KEY,
        result TEXT
    )
''')
conn.commit()

class WordRequest(BaseModel):
    word: str

class WordResponse(BaseModel):
    description: str

@app.post("/generate_description", response_model=WordResponse)
async def generate_description(request: Request, word_request: WordRequest):
    message = word_request.word
    print("[SYSTEM] Received request for word:", message)

    try:
        # Check if the result for the current message already exists in the database
        cursor.execute("SELECT result FROM chat_log WHERE message = ?", (message,))
        row = cursor.fetchone()

        if row is not None:
            # If a result exists, return it without calling the AI
            print("[SYSTEM] Found cached description for word:", message)
            return WordResponse(description=row[0])
        else:
            # If no result exists, call the AI to generate a new response
            print("[SYSTEM] Generating new description for word:", message)
            client = Client("http://localhost:7860")
            result = client.predict(message="generate a new description for this word" + message, api_name="/chat")

            # Save the message and result to the database
            cursor.execute("INSERT INTO chat_log (message, result) VALUES (?, ?)", (message, result))
            conn.commit()
            print("[SYSTEM] Generated and cached new description for word:", message)

            return WordResponse(description=result)
    except Exception as e:
        print("[SYSTEM] Error occurred while processing request:", str(e))
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.on_event("shutdown")
def shutdown_event():
    try:
        # Close the database connection when the server is shutting down
        conn.close()
        print("[SYSTEM] Database connection closed.")
    except Exception as e:
        print("[SYSTEM] Error occurred while closing the database connection:", str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)