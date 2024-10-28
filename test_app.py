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

if __name__ == "__main__":
    test_swaph_server()
