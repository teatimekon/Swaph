# Swaph

### Using swarm + LangGraph to build a workflow

python version: 3.10

#### step 1: install requirements
```
pip install -r requirements.txt
```
#### step 2: run the app
```
python app.py
```

#### step 3: test the app
```
python test_app.py
```

## 接口说明
#### POST /ask
请求参数
```
{
    question:  string,
    conversation_id: string
}
```
接口说明：
- 接收用户的问题和会话ID，返回回答
- 会话ID用于区分不同的会话，同一个会话ID的问题会共享上下文

返回参数
```
{
    answer: string
}
```
