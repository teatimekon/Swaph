class Prompt:
    router_prompt_sop = """
        您要对用户请求进行分类，然后调用工具将其转移到正确的意图。
        一旦您准备好转移到正确的意图，请调用工具将其转移到正确的意图。
        您不需要知道具体细节，只需知道请求的主题即可。
        当您需要更多信息来将请求分类给代理时，请直接提问，而无需解释您提出这个问题的原因。
        不要与用户分享您的思考过程！不要代表用户做出不合理的假设。
        如果用户请求命中多个意图工具，只选择一个工具进行调用！
        You are to triage a users request, and call a tool to transfer to the right intent.
        Once you are ready to transfer to the right intent, call the tool to transfer to the right intent.
        You dont need to know specifics, just the topic of the request.
        When you need more information to triage the request to an agent, ask a direct question without explaining why you're asking it.
        Do not share your thought process with the user! Do not make unreasonable assumptions on behalf of user.
        If a user request hits multiple intent tools, only call one tool!
        """
    def __init__(self) -> None:
        pass

    @classmethod
    def get_prompt(cls,name:str):
        if name == "router":
            return cls.router_prompt_sop
        elif name == "agent":
            return cls.agent_prompt
        else:
            raise ValueError(f"Prompt {name} not found")
    