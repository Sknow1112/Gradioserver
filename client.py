from gradio_client import Client

client = Client("https://1f405b982834104160.gradio.live/")
result = client.predict(
		message="Say hello world.",
		api_name="/chat"
)
print(result)