import gradio as gr
from ctransformers import AutoModelForCausalLM, AutoTokenizer
def load_llm():
    llm = AutoModelForCausalLM.from_pretrained(
        "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
        
        max_new_tokens= 512,
        temperature = 0.2
    )
    return llm

def llm_function(message, chat_history):
    llm = load_llm()
    starting_prompt = ("This is a specific context. You are a helpful assistant. Only respond with what's requested here:")
    message = starting_prompt + message  # Prepend the starting prompt to the message
    response = llm(
        message
    )
    output_texts = response
    return output_texts

title = "Silicon Chat 2.0"

examples = [
    "Say hello world!",
]
#set share=true to enable sharing
gr.ChatInterface(
    fn = llm_function,
    title=title,
    examples=examples
).launch(share=True)
