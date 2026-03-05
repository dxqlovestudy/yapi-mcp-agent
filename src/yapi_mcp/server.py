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


def run():
    """运行 MCP 服务器"""
    mcp.run()
