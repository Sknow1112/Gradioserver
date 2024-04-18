import gradio as gr
from ctransformers import AutoModelForCausalLM, AutoTokenizer
def load_llm():
    llm = AutoModelForCausalLM.from_pretrained(
        "TheBloke/xDAN-L1-Chat-RL-v1-GGUF",
        model_type='Llama',
        max_new_tokens= 512,
        temperature = 0.8
    )
    return llm

def llm_function(message, chat_history):
    llm = load_llm()
    starting_prompt = ("This is a specific context. You are a helpful ai assistant. Simply respond only with what's requested here, in english:")
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
