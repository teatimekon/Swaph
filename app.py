from flask import Flask, request, jsonify, Response
from swaph.swaph import Swaph

app = Flask(__name__)
swaph = Swaph()
swaph.setup("gpt-4o-mini")
@app.route('/init', methods=['POST'])
def init():
    model = request.json.get('model')
    swaph = Swaph()
    swaph.setup(model)
    return jsonify({"message": "Model initialized"}), 200

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

@app.route('/stream', methods=['POST'])
def stream():
    data = request.json
    question = data.get('question')
    conversation_id = data.get('conversation_id')
    
    if not question or not conversation_id:
        return jsonify({"error": "No question or conversation_id provided"}), 400
    
    def generate():
        for chunk in swaph.stream(question, conversation_id):
            if chunk is not None:
                yield f"data: {chunk}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(port=5001)
    