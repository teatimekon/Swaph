import requests
import json
import time
from config.preprint import Colors

def test_swaph_server():
    url = "http://localhost:5001/ask"
    headers = {"Content-Type": "application/json"}

    questions = [
        ("世界上最长的河流是什么", "conv1"),
        ("第三呢？", "conv1"),
        ("第二呢？", "conv2")
    ]
    init_url = "http://localhost:5001/init"
    init_payload = json.dumps({"model": "gpt-4o-mini"})
    requests.post(init_url, headers=headers, data=init_payload)

    for question, conv_id in questions:
        payload = json.dumps({"question": question, "conversation_id": conv_id})
        start_time = time.time()
        response = requests.post(url, headers=headers, data=payload)
        end_time = time.time()
        print(f"{Colors.OKGREEN}请求时间: {end_time - start_time}秒{Colors.ENDC}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"问题: {question}")
            print(f"对话ID: {conv_id}")
            print(f"回答: {result['answer']}")
            print(f"下一个代理: {result['current_agent']}")
            print("-" * 50)
        else:
            print(f"请求失败: {response.status_code}")
            print(response.text)
            print("-" * 50)

def test_stream_server():
    url = "http://localhost:5001/stream"
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }
    questions = [
        ("你好", "conv1"),
    ]
    
    # init_url = "http://localhost:5001/init"
    # init_payload = json.dumps({"model": "gpt-4o-mini"})
    # requests.post(init_url, headers=headers, data=init_payload)
    
    for question, conv_id in questions:
        payload = json.dumps({
            "question": question, 
            "conversation_id": conv_id
        })
        response = requests.post(
            url, 
            headers=headers, 
            data=payload,
            stream=True
        )
        
        if response.status_code == 200:
            start_time = time.time()
            for sentence in process_stream_response(response, start_time):
                yield sentence
        else:
            print(f"请求失败: {response.status_code}")
            print(response.text)
            print("-" * 50)
        total_time = time.time() - start_time
        print(f"{Colors.OKGREEN}总请求时间: {total_time:.2f}秒{Colors.ENDC}")

def process_stream_response(response, start_time):
    """处理流式响应数据"""
    # 使用 frozenset 提升查找效率
    PUNCTUATION_MARKS = frozenset(',.;?!、，。？！；：…~:—()（）')
    
    def process_line(line: bytes) -> str:
        """处理单行数据"""
        if not line:
            return ""
        decoded_line = line.decode('utf-8')
        if not decoded_line.startswith('data: '):
            return ""
        return decoded_line[6:]  # 移除 "data: " 前缀

    def print_sentence(sentence: str, elapsed_time: float):
        """打印句子和耗时"""
        print(f"{Colors.OKGREEN}请求时间: {elapsed_time:.2f}秒{Colors.ENDC}")
        print(sentence, flush=True)

    current_sentence = []
    
    for line in response.iter_lines():
        content = process_line(line)
        if not content:
            continue
            
        for char in content:
            current_sentence.append(char)
            if char in PUNCTUATION_MARKS:
                # 使用 join 进行字符串拼接，比 += 更高效
                complete_sentence = ''.join(current_sentence)
                elapsed_time = time.time() - start_time
                # print_sentence(complete_sentence, elapsed_time)
                yield complete_sentence
                current_sentence = []

if __name__ == "__main__":
    ans = test_stream_server()
    for chunk in ans:
        print(chunk, end='\n', flush=True)
