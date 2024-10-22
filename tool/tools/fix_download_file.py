from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool, tool
from tool import ToolRegistry

class FixDownloadFileToolInput(BaseModel):
    """
    诊断下载文件失败的工具，需要用户提供用户的 id和服务器实例 id，和文件名字，随后该工具返回给用户需要的文件
    """
    uid: str = Field(description="用户的uid，用于标识用户，是由一串数字组成的字符串")
    bucket_id: str = Field(description="用户出错的服务器实例的id，用于标识服务器，是由一串数字+字母组成的字符串")
    file_name: str = Field(description="用户曾经尝试下载但是出错了的文件")


@ToolRegistry.register
@tool("fix_download_file", args_schema=FixDownloadFileToolInput)
def fix_doownload_file(uid=None,bucket_id=None,file_name=None) -> str:
    #三个参数必须都不为 None，否则同时返回缺失了哪些参数
    if uid and bucket_id and file_name:
        return f"用户{uid}从服务器{bucket_id}下载了文件{file_name}"
    else:
        schema_dict = FixDownloadFileToolInput.schema()['properties']
        return f"缺失参数：{[schema_dict[k].get('description') for k,v in locals().items() if v is None]}"
    
# print(doownload_file(bucket_id="123",file_name="test.txt"))