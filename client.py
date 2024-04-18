import sqlite3
from gradio_client import Client

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



def get_response(message):
    # Check if the result for the current message already exists in the database
    cursor.execute("SELECT result FROM chat_log WHERE message = ?", (message,))
    row = cursor.fetchone()
    
    if row is not None:
        # If a result exists, return it without calling the AI
        return row[0]
    else:
        # If no result exists, call the AI to generate a new response
        client = Client("http://localhost:7860")
        result = client.predict(message=message, api_name="/chat")
        
        # Save the message and result to the database
        cursor.execute("INSERT INTO chat_log (message, result) VALUES (?, ?)", (message, result))
        conn.commit()
        
        return result

# Example usage
message = "Say Hello World!"
result = get_response(message)
print(result)

# Close the database connection when done
conn.close()