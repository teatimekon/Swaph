import gradio as gr
from swaph.swaph import Swaph
from langchain_core.messages import AIMessageChunk
import time
swaph = Swaph()
swaph.setup()

def ask_question(question,history):
    start_time = time.time()
    ans = swaph.stream(question, "default")
    time_count = True
    show_messages = ""
    for message in ans:
        if message is not None and time_count == True:
            taken_time = time.time() - start_time
            message = f"ttf: {taken_time:.2f}秒\n" + message
            time_count = False
        show_messages += message
        yield show_messages
        
demo = gr.ChatInterface(ask_question, type="messages")

if __name__ == "__main__":
    demo.launch()
