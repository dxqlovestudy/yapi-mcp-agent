"""MCP 服务器模块"""

from typing import Any

from fastmcp import FastMCP

from .client import YAPIClient

# 创建 MCP 服务器实例
mcp = FastMCP(name="YAPI MCP Server")


# ============ 接口相关工具 ============


@mcp.tool("get_api_info")
def get_api_info(url: str) -> dict[str, Any]:
    """
    获取 yapi 的接口文档
    :param url: yapi 中接口的地址
    :return: 以 json 格式返回的接口信息
    """
    client = YAPIClient()
    return client.get_api(url)


# ============ 项目相关工具 ============


@mcp.tool()
def get_project_info(project_id: int) -> dict[str, Any]:
    """
    获取 YAPI 项目的基本信息

    :param project_id: 项目ID
    :return: 项目基本信息
    """
    client = YAPIClient()
    return client.get_project(project_id)


@mcp.tool()
def get_project_list() -> list[dict] | dict:
    """
    获取当前用户有权限访问的所有项目列表

    :return: 项目列表
    """
    client = YAPIClient()
    return client.get_project_list()


@mcp.tool()
def get_project_members(project_id: int) -> list[dict] | dict:
    """
    获取指定项目的成员列表

    :param project_id: 项目ID
    :return: 成员列表
    """
    client = YAPIClient()
    return client.get_project_members(project_id)


# ============ 接口列表相关工具 ============


@mcp.tool()
def get_interface_list(project_id: int, cat_id: int | None = None) -> list[dict] | dict:
    """
    获取项目的接口列表，可指定分类ID进行过滤

    :param project_id: 项目ID
    :param cat_id: 分类ID（可选），不传则获取所有接口
    :return: 接口列表
    """
    client = YAPIClient()
    return client.get_interface_list(project_id, cat_id)


@mcp.tool()
def get_interface_list_by_cat(cat_id: int) -> list[dict] | dict:
    """
    获取某个分类下的所有接口列表

    :param cat_id: 分类ID
    :return: 接口列表
    """
    client = YAPIClient()
    return client.get_interface_list_by_cat(cat_id)


@mcp.tool()
def search_interfaces(project_id: int, keyword: str) -> list[dict] | dict:
    """
    在项目中搜索包含关键字的接口

    :param project_id: 项目ID
    :param keyword: 搜索关键字
    :return: 匹配的接口列表
    """
    client = YAPIClient()
    return client.search_interfaces(project_id, keyword)


# ============ 数据导入相关工具 ============


@mcp.tool()
def import_swagger(
    url: str | None = None,
    json: str | None = None,
    project_id: int | None = None,
    merge: str = "normal",
) -> dict[str, Any]:
    """
    从 URL 或 JSON 导入 Swagger/OpenAPI 数据到 YAPI

    :param url: Swagger 数据的 URL（可选）
    :param json: Swagger JSON 字符串（可选）
    :param project_id: 目标项目ID（可选）
    :param merge: 合并策略，可选值: 'normal', 'good', 'merge'（默认为 'normal'）
    :return: 导入结果
    """
    client = YAPIClient()
    return client.import_swagger(url, json, project_id, merge)


@mcp.tool()
def import_postman(
    url: str | None = None,
    json: str | None = None,
    project_id: int | None = None,
    merge: str = "normal",
) -> dict[str, Any]:
    """
    从 URL 或 JSON 导入 Postman 数据到 YAPI

    :param url: Postman 数据的 URL（可选）
    :param json: Postman JSON 字符串（可选）
    :param project_id: 目标项目ID（可选）
    :param merge: 合并策略，可选值: 'normal', 'good', 'merge'（默认为 'normal'）
    :return: 导入结果
    """
    client = YAPIClient()
    return client.import_postman(url, json, project_id, merge)


@mcp.tool()
def import_json(json: str, project_id: int, merge: str = "normal") -> dict[str, Any]:
    """
    导入 JSON 数据到 YAPI

    :param json: JSON 数据字符串
    :param project_id: 目标项目ID
    :param merge: 合并策略，可选值: 'normal', 'good', 'merge'（默认为 'normal'）
    :return: 导入结果
    """
    client = YAPIClient()
    return client.import_json(json, project_id, merge)


# ============ 自动化测试相关工具 ============


@mcp.tool()
def run_auto_test(
    col_id: int,
    project_id: int,
    token: str,
    mode: str = "html",
    email: bool = False,
) -> dict[str, Any]:
    """
    运行自动化测试并返回测试报告

    :param col_id: 测试集合ID
    :param project_id: 项目ID
    :param token: 项目token
    :param mode: 报告模式，可选值: 'html', 'json'（默认为 'html'）
    :param email: 是否发送邮件通知（默认为 False）
    :return: 测试报告
    """
    client = YAPIClient()
    return client.run_auto_test(col_id, project_id, token, mode, email)


# ============ 接口更新相关工具 ============


@mcp.tool()
def create_interface(
    title: str,
    catid: int,
    path: str,
    project_id: int | None = None,
    method: str = "GET",
    desc: str = "",
    status: str = "undone",
    req_query: list | None = None,
    req_headers: list | None = None,
    req_body_form: list | None = None,
    req_params: list | None = None,
    req_body_other: str = "",
    res_body: str = "",
    res_body_type: str = "json",
    switch_notice: bool = False,
    message: str = "",
) -> dict[str, Any]:
    """
    在 YAPI 中新增接口

    重要规范：
    - res_body 中数组类型的 items 必须定义完整的 properties，不能只写 "type": "object"
    - 如果返回数据包含 rows 字段（分页列表），必须先查找实体类获取完整字段信息
    - 详细规范请调用 get_yapi_guidelines 工具查看

    :param title: 接口标题
    :param catid: 分类ID
    :param path: 接口路径
    :param project_id: 项目ID（可选，某些YAPI版本需要）
    :param method: 请求方法，如 GET、POST、PUT、DELETE（默认为 GET）
    :param desc: 接口描述（默认为空）
    :param status: 接口状态，如 undone、done（默认为 undone）
    :param req_query: 请求查询参数列表（默认为空列表）
    :param req_headers: 请求头列表（默认包含 Content-Type）
    :param req_body_form: 表单参数列表（默认为空列表）
    :param req_params: 路径参数列表（默认为空列表）
    :param req_body_other: 请求体 JSON Schema 字符串（默认为空）
    :param res_body: 返回数据 JSON Schema 字符串（默认为空）
    :param res_body_type: 返回数据类型，如 json、raw、xml（默认为 json）
    :param switch_notice: 是否开启通知（默认为 False）
    :param message: 接口通知消息（默认为空）
    :return: 新增结果，包含接口ID
    """
    client = YAPIClient()
    return client.create_interface(
        title=title,
        catid=catid,
        path=path,
        project_id=project_id,
        method=method,
        desc=desc,
        status=status,
        req_query=req_query,
        req_headers=req_headers,
        req_body_form=req_body_form,
        req_params=req_params,
        req_body_other=req_body_other,
        res_body=res_body,
        res_body_type=res_body_type,
        switch_notice=switch_notice,
        message=message,
    )


@mcp.tool()
def update_interface(
    interface_id: int,
    title: str,
    catid: int,
    path: str,
    method: str = "GET",
    desc: str = "",
    status: str = "undone",
    req_query: list | None = None,
    req_headers: list | None = None,
    req_body_form: list | None = None,
    req_params: list | None = None,
    req_body_other: str = "",
    res_body: str = "",
    res_body_type: str = "json",
    switch_notice: bool = False,
    message: str = "",
) -> dict[str, Any]:
    """
    更新 YAPI 接口

    重要规范：
    - res_body 中数组类型的 items 必须定义完整的 properties，不能只写 "type": "object"
    - 如果返回数据包含 rows 字段（分页列表），必须先查找实体类获取完整字段信息
    - 详细规范请调用 get_yapi_guidelines 工具查看

    :param interface_id: 接口ID
    :param title: 接口标题
    :param catid: 分类ID
    :param path: 接口路径
    :param method: 请求方法，如 GET、POST、PUT、DELETE（默认为 GET）
    :param desc: 接口描述（默认为空）
    :param status: 接口状态，如 undone、done（默认为 undone）
    :param req_query: 请求查询参数列表（默认为空列表）
    :param req_headers: 请求头列表（默认包含 Content-Type）
    :param req_body_form: 表单参数列表（默认为空列表）
    :param req_params: 路径参数列表（默认为空列表）
    :param req_body_other: 请求体 JSON Schema 字符串（默认为空）
    :param res_body: 返回数据 JSON Schema 字符串（默认为空）
    :param res_body_type: 返回数据类型，如 json、raw、xml（默认为 json）
    :param switch_notice: 是否开启通知（默认为 False）
    :param message: 接口通知消息（默认为空）
    :return: 更新结果
    """
    client = YAPIClient()
    return client.update_interface(
        interface_id=interface_id,
        title=title,
        catid=catid,
        path=path,
        method=method,
        desc=desc,
        status=status,
        req_query=req_query,
        req_headers=req_headers,
        req_body_form=req_body_form,
        req_params=req_params,
        req_body_other=req_body_other,
        res_body=res_body,
        res_body_type=res_body_type,
        switch_notice=switch_notice,
        message=message,
    )


def run():
    """运行 MCP 服务器"""
    mcp.run()


# ============ MCP Resource ============

YAPI_GUIDELINES = """# YAPI 接口文档创建规范

## 问题
创建 YAPI 接口文档时，如果返回数据中的 `rows` 字段（数组类型）的 `items` 只定义 `"type": "object"` 而不定义具体的 `properties`，YAPI 页面上会显示为空，无法看到返回字段结构。

## 解决方案
在创建接口文档前，必须先查找并读取相关的实体类/DTO 类，获取完整的返回字段信息，然后在 `res_body` 中定义完整的字段结构。

## 流程
1. 根据接口路径找到对应的 Controller
2. 找到方法返回类型对应的实体类（如 `PageResponse` 中的 `rows` 对应的实体）
3. 读取实体类，提取所有字段及其描述
4. 在创建接口时，将实体类的字段完整定义到 `res_body` 的 `rows.items.properties` 中

## 示例
```json
{
  "res_body": {
    "type": "object",
    "properties": {
      "ret_code": { "type": "string", "description": "返回码" },
      "rows": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "merch_no": { "type": "string", "description": "商户号" },
            "merch_name": { "type": "string", "description": "商户名" }
          }
        }
      }
    }
  }
}
```

## 注意事项
- 所有数组类型的 items 都必须定义完整的 properties
- 字段描述应与实体类中的注释保持一致
- 常见字段类型：string、integer、number、boolean、array、object
"""


@mcp.resource("yapi://guidelines")
def get_yapi_guidelines() -> str:
    """
    获取 YAPI 接口文档创建规范

    包含完整的接口文档创建规范和示例，帮助正确创建 YAPI 接口文档。
    """
    return YAPI_GUIDELINES
