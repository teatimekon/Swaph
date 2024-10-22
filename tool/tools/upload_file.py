from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool, tool
from tool import ToolRegistry

class UploadFileToolInput(BaseModel):
    """
    上传文件的工具，用户提供用户的 id和服务器实例 id，和本地文件路径
    """
    uid: str = Field(description="用户的uid，用于标识用户，是由一串数字组成的字符串")
    bucket_id: str = Field(description="用户提供的服务器实例的id，用于标识服务器，是由一串数字+字母组成的字符串")
    file_path: str = Field(description="用户需要上传的文件路径")


@ToolRegistry.register
@tool("upload_file", args_schema=UploadFileToolInput)
def upload_file(uid="",bucket_id="",file_path="") -> str:
    #三个参数必须都不为 None，否则同时返回缺失了哪些参数
    if uid and bucket_id and file_path:
        return f"用户{uid}在服务器{bucket_id}上传了文件{file_path}，上传完成"
    else:
        schema_dict = UploadFileToolInput.schema()['properties']
        input_dict = {'uid':uid,'bucket_id':bucket_id,'file_path':file_path}
        return f"缺失参数：{[str(k) + ': ' + schema_dict[k].get('description') for k,v in input_dict.items() if not v]}"
    
# print(doownload_file(bucket_id="123",file_name="test.txt"))