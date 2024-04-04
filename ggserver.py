import gradio as gr
from ctransformers import AutoModelForCausalLM, AutoTokenizer
def load_llm():
    llm = AutoModelForCausalLM.from_pretrained(
        "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
        model_type='llama',
        max_new_tokens= 512,
        temperature = 0.2
    )
    return llm

def llm_function(message, chat_history):
    llm = load_llm()
    starting_prompt = ("You respond with what's requested here:")
    #(" This is a specific context. Please consider this while generating responses: Respond with "
                       #"creative combination of a new word from an adjective and a noun on a new line in list format like \n1. "
                       #"_____ \n2. _____ 3. ______ ")  # Add your specific starting prompt here
    message = starting_prompt + message  # Prepend the starting prompt to the message
    response = llm(
        message
    )
    output_texts = response
    return output_texts

title = "Silicon Chat 2.0"

examples = [
    "Make a list of 1-3 combinations.",
]
#set share=true to enable sharing
gr.ChatInterface(
    fn = llm_function,
    title=title,
    examples=examples
).launch(share=True)
