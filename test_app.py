import requests
import json

def test_swaph_server():
    url = "http://localhost:5000/ask"
    headers = {"Content-Type": "application/json"}

    questions = [
        ("世界上最长的河流是什么", "conv1"),
        ("第三呢？", "conv1"),
        ("第二呢？", "conv2")
    ]

    for question, conv_id in questions:
        payload = json.dumps({"question": question, "conversation_id": conv_id})
        response = requests.post(url, headers=headers, data=payload)
        
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
