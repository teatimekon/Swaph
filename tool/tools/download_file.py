from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool, tool
from tool import ToolRegistry

class DownloadFileToolInput(BaseModel):
    """
    从云端服务器下载文件的工具，用户提供用户的 id和服务器实例 id，和文件名字，随后该工具返回给用户需要的文件
    """
    uid: str = Field(description="用户的uid，用于标识用户，是由一串数字组成的字符串")
    bucket_id: str = Field(description="用户提供的服务器实例的id，用于标识服务器，是由一串数字+字母组成的字符串")
    file_name: str = Field(description="用户需要从服务器下载的文件名字")


@ToolRegistry.register
@tool("download_file", args_schema=DownloadFileToolInput)
def doownload_file(uid="",bucket_id="",file_name="") -> str:
    #三个参数必须都不为 None，否则同时返回缺失了哪些参数
    if uid and bucket_id and file_name:
        return f"用户{uid}从服务器{bucket_id}下载了文件{file_name}，诊断完成"
    else:
        schema_dict = DownloadFileToolInput.schema()['properties']
        input_dict = {'uid':uid,'bucket_id':bucket_id,'file_name':file_name}
        return f"缺失参数：{[str(k) + ': ' + schema_dict[k].get('description') for k,v in input_dict.items() if not v]}"
    
# print(doownload_file(bucket_id="123",file_name="test.txt"))