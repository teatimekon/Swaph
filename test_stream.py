import asyncio
from swaph.swaph import Swaph
import time

async def test_stream():
    swaph = Swaph()
    swaph.setup()
    
    questions = [
        "世界上最长的河流是什么？",
        "七大洲分别是什么？",
        "请帮我上传一个文件到kodo"
    ]
    
    for question in questions:
        print(f"\n测试问题: {question}")
        print("-" * 50)
        
        start_time = time.time()
        first_token_time = None
        token_count = 0
        
        async for token in swaph.astream(question, "test-conversation"):
            if token_count == 0:
                first_token_time = time.time()
                print(f"\n首个token耗时: {first_token_time - start_time:.2f}秒")
            
            print(token, end="", flush=True)
            token_count += 1
        
        end_time = time.time()
        print(f"\n\n总耗时: {end_time - start_time:.2f}秒")
        print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_stream())
