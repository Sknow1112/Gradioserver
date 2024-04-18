from gradio_client import Client
import requests

def get_description(word, node_server_url):
    # Check if the word already exists in the database
    response = requests.get(f'{node_server_url}/word/{word}')
    if response.status_code == 200:
        # If the word exists, return the stored description
        return response.json()['description']
    else:
        # If the word doesn't exist, generate a new description using ggserver.py
        client = Client("http://localhost:7860")
        try:
            result = client.predict(
                message=f'Describe the word "{word}" in a sentence.',
                api_name="/chat"
            )
            description = result['message']
        except ValueError:
            description = "Model is not loaded correctly."

        # Save the word and its description to the database
        requests.post(f'{node_server_url}/word', json={'word': word, 'description': description})

        return description

def process_word(word, node_server_url):
    word = word.strip().lower()
    description = get_description(word, node_server_url)
    print(f'Word: {word}')
    print(f'Description: {description}')

# Example usage
node_server_url = 'http://your_flutter_app_url:forwarded_port'  # Replace with the actual URL and port
word = input("Enter a word: ")
process_word(word, node_server_url)