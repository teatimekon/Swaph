from flask import Flask, request, jsonify
from swaph.swaph import Swaph

app = Flask(__name__)
swaph = Swaph()
swaph.setup()

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question')
    conversation_id = data.get('conversation_id')
    
    if not question or not conversation_id:
        return jsonify({"error": "No question or conversation_id provided"}), 400
    
    ans = swaph.invoke(question, conversation_id)
    
    # 提取 AI 的回答
    ai_responses = ans["messages"][-1].content
    
    response = {
        "answer": " ".join(ai_responses),
        "current_agent": ans["next_agent"]
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run()
