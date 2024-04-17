from gradio_client import Client

client = Client("http://127.0.0.1:7860")
## If value error is raised, result= "Model is not loaded correctly.
try:
	result = client.predict(
		message="Say hello world.",
		api_name="/chat"
	)
except ValueError:
	result = "Model is not loaded correctly."

print(result)