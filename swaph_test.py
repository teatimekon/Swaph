from swaph.swaph import Swaph
from langchain_core.messages import AIMessageChunk
swaph = Swaph()
swaph.setup()

while True:
    question = input("输入问题：")
    ans = swaph.stream(question, "1")
    for message in ans:
        print(message,end="｜",flush=True)
    
