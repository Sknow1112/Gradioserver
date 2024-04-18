from gradio_client import Client
import csv

# Initialize the client
client = Client("http://127.0.0.1:7860")

# Load the CSV data into a dictionary for easy lookup
prompt_response_dict = {}
try:
    with open('results.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            prompt, response = row
            prompt_response_dict[prompt] = response
except FileNotFoundError:
    pass

# Define the prompt
prompt = "What's the capital of Venesuela?"

# Check if the prompt is already in the CSV data
if prompt in prompt_response_dict:
    result = prompt_response_dict[prompt]
    print(result)
else:
    # If not, get the response from the client and add it to the CSV file
    # Check if the file exists and has data. If it does, we want to append, not overwrite.
    try:
        with open('results.csv', 'r') as file:
            existing = csv.reader(file)
            data_exists = any(existing)
    except FileNotFoundError:
        data_exists = False

    # Open the file in append mode if data exists, otherwise write mode.
    file_mode = 'a' if data_exists else 'w'

    with open('results.csv', file_mode, newline='') as file:
        writer = csv.writer(file)
        if not data_exists:
            # Only write the header if the file didn't exist or was empty.
            writer.writerow(["Prompt", "Response"])

        result = client.predict(message=prompt, api_name="/chat")
        writer.writerow([prompt, result])
        print(result)