from gradio_client import Client
import csv

client = Client("http://127.0.0.1:7860")
result = client.predict(
		message="Hello!!",
		api_name="/chat"
)
with open('results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Prompt", "Response"])
    writer.writerow(["Hello!!", result])
print(result)