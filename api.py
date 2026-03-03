import os

from fastmcp import FastMCP
import asyncio
from requests import Session


def load_config():
    """
    加载配置，从环境变量读取

    必须通过环境变量提供以下配置：
    - YAPI_BASE_URL: YAPI 服务器地址
    - YAPI_EMAIL: 登录邮箱
    - YAPI_PASSWORD: 登录密码
    """
    config = {}

    # 从环境变量读取配置
    config['base_url'] = os.getenv('YAPI_BASE_URL')
    config['email'] = os.getenv('YAPI_EMAIL')
    config['password'] = os.getenv('YAPI_PASSWORD')

    # 验证必要配置
    required_keys = ['base_url', 'email', 'password']
    missing_keys = [key for key in required_keys if key not in config or not config[key]]
    if missing_keys:
        raise ValueError(
            f"缺少必要配置: {', '.join(missing_keys)}\n"
            f"请设置环境变量: YAPI_BASE_URL, YAPI_EMAIL, YAPI_PASSWORD"
        )

    return config


# 加载配置
config = load_config()


def is_true(b: bool, msg: str) -> None:
    if not b:
        raise Exception(msg)


class YAPI:

    def __init__(self, base_url: str = None, email: str = None, password: str = None):
        """
        初始化YAPI客户端
        
        :param base_url: YAPI服务器地址，默认从配置读取
        :param email: 登录邮箱，默认从配置读取
        :param password: 登录密码，默认从配置读取
        """
        self._session = Session()
        self.base_url = base_url or config['base_url']
        self.email = email or config['email']
        self.password = password or config['password']
        
        # 确保base_url不以/结尾
        self.base_url = self.base_url.rstrip('/')

    def is_login(self) -> bool:
        resp = self._session.get(f'{self.base_url}/api/user/status')
        return resp.json()['errcode'] == 0

    def login(self) -> bool:
        resp = self._session.post(f'{self.base_url}/api/user/login_by_ldap', json={
            "email": self.email,
            "password": self.password
        })
        return resp.json()['errcode'] == 0

    def guarantee_login(self) -> None:
        if not self.is_login():
            ret = self.login()
            is_true(ret, "登录失败")

    def transform(self, data: str) -> object:
        obj = json.loads(data)
        properties = obj['properties']
        # required = obj['required']
        return properties

    def get_api(self, url) -> object:
        try:
            self.guarantee_login()
            id = url.split('/')[-1]
            real_url = f'{self.base_url}/api/interface/get?id={id}'
            result = self._session.get(real_url).json()
            is_true(result['errcode'] == 0, "登录失败")
            data = result['data']
            return {
                'title': data['title'],
                'request': self.transform(data['req_body_other']),
                'response': self.transform(data['res_body'])
            }
        except Exception as e:
            print(f'捕获未知异常{e}')
            return {
                "ret_code": "400",
                "ret_msg": "异常"
            }

    # ============ 项目相关 ============

    def get_project(self, project_id: int) -> dict:
        """
        获取项目基本信息

        :param project_id: 项目ID
        :return: 项目信息字典
        """
        try:
            self.guarantee_login()
            result = self._session.get(f'{self.base_url}/api/project/get?id={project_id}').json()
            is_true(result['errcode'] == 0, f"获取项目失败: {result.get('errmsg', '未知错误')}")
            return result['data']
        except Exception as e:
            return {
                "ret_code": "400",
                "ret_msg": f"获取项目失败: {str(e)}"
            }

    def get_project_list(self) -> list:
        """
        获取项目列表

        :return: 项目列表
        """
        try:
            self.guarantee_login()
            result = self._session.get(f'{self.base_url}/api/project/list').json()
            is_true(result['errcode'] == 0, f"获取项目列表失败: {result.get('errmsg', '未知错误')}")
            return result['data']
        except Exception as e:
            return {
                "ret_code": "400",
                "ret_msg": f"获取项目列表失败: {str(e)}"
            }

    def get_project_members(self, project_id: int) -> list:
        """
        获取项目成员列表

        :param project_id: 项目ID
        :return: 成员列表
        """
        try:
            self.guarantee_login()
            result = self._session.get(f'{self.base_url}/api/project/get?id={project_id}').json()
            is_true(result['errcode'] == 0, f"获取项目成员失败: {result.get('errmsg', '未知错误')}")
            project_data = result['data']
            # 成员信息在项目的 members 或 members_data 字段中
            members = project_data.get('members') or project_data.get('members_data', [])
            return members
        except Exception as e:
            return {
                "ret_code": "400",
                "ret_msg": f"获取项目成员失败: {str(e)}"
            }

    # ============ 接口列表相关 ============

    def get_interface_list(self, project_id: int, cat_id: int = None) -> list:
        """
        获取接口列表，可选按分类过滤

        :param project_id: 项目ID
        :param cat_id: 分类ID，可选
        :return: 接口列表
        """
        try:
            self.guarantee_login()
            if cat_id:
                result = self._session.get(
                    f'{self.base_url}/api/interface/list',
                    params={'project_id': project_id, 'catid': cat_id}
                ).json()
            else:
                result = self._session.get(
                    f'{self.base_url}/api/interface/list',
                    params={'project_id': project_id}
                ).json()
            is_true(result['errcode'] == 0, f"获取接口列表失败: {result.get('errmsg', '未知错误')}")
            return result['data']
        except Exception as e:
            return {
                "ret_code": "400",
                "ret_msg": f"获取接口列表失败: {str(e)}"
            }

    def get_interface_list_by_cat(self, cat_id: int) -> list:
        """
        获取某个分类下的接口列表

        :param cat_id: 分类ID
        :return: 接口列表
        """
        try:
            self.guarantee_login()
            result = self._session.get(
                f'{self.base_url}/api/interface/list_cat',
                params={'catid': cat_id}
            ).json()
            is_true(result['errcode'] == 0, f"获取分类接口列表失败: {result.get('errmsg', '未知错误')}")
            return result['data']
        except Exception as e:
            return {
                "ret_code": "400",
                "ret_msg": f"获取分类接口列表失败: {str(e)}"
            }

    def search_interfaces(self, project_id: int, keyword: str) -> list:
        """
        按关键字搜索接口

        :param project_id: 项目ID
        :param keyword: 搜索关键字
        :return: 匹配的接口列表
        """
        try:
            self.guarantee_login()
            # 获取所有接口
            result = self._session.get(
                f'{self.base_url}/api/interface/list',
                params={'project_id': project_id}
            ).json()
            is_true(result['errcode'] == 0, f"搜索接口失败: {result.get('errmsg', '未知错误')}")

            # 过滤匹配关键字的接口
            interfaces = result['data']
            if isinstance(interfaces, list):
                filtered = [
                    iface for iface in interfaces
                    if keyword.lower() in iface.get('title', '').lower() or
                       keyword.lower() in iface.get('path', '').lower()
                ]
                return filtered
            return []
        except Exception as e:
            return {
                "ret_code": "400",
                "ret_msg": f"搜索接口失败: {str(e)}"
            }

    # ============ 数据导入相关 ============

    def import_swagger(self, url: str = None, json: str = None, project_id: int = None,
                       merge: str = 'normal') -> dict:
        """
        导入 Swagger/OpenAPI 数据

        :param url: Swagger URL
        :param json: Swagger JSON 字符串
        :param project_id: 项目ID
        :param merge: 合并策略 (normal, good, merge)
        :return: 导入结果
        """
        try:
            self.guarantee_login()
            data = {
                'type': 'Swagger',
                'merge': merge
            }
            if url:
                data['url'] = url
            if json:
                data['json'] = json
            if project_id is not None:
                data['project_id'] = project_id

            result = self._session.post(
                f'{self.base_url}/api/interface/save',
                json=data
            ).json()
            is_true(result['errcode'] == 0, f"导入Swagger失败: {result.get('errmsg', '未知错误')}")
            return result['data']
        except Exception as e:
            return {
                "ret_code": "400",
                "ret_msg": f"导入Swagger失败: {str(e)}"
            }

    def import_postman(self, url: str = None, json: str = None, project_id: int = None,
                       merge: str = 'normal') -> dict:
        """
        导入 Postman 数据

        :param url: Postman URL
        :param json: Postman JSON 字符串
        :param project_id: 项目ID
        :param merge: 合并策略 (normal, good, merge)
        :return: 导入结果
        """
        try:
            self.guarantee_login()
            data = {
                'type': 'Postman',
                'merge': merge
            }
            if url:
                data['url'] = url
            if json:
                data['json'] = json
            if project_id is not None:
                data['project_id'] = project_id

            result = self._session.post(
                f'{self.base_url}/api/interface/save',
                json=data
            ).json()
            is_true(result['errcode'] == 0, f"导入Postman失败: {result.get('errmsg', '未知错误')}")
            return result['data']
        except Exception as e:
            return {
                "ret_code": "400",
                "ret_msg": f"导入Postman失败: {str(e)}"
            }

    def import_json(self, json_data: str, project_id: int, merge: str = 'normal') -> dict:
        """
        导入 JSON 数据

        :param json_data: JSON 数据字符串
        :param project_id: 项目ID
        :param merge: 合并策略 (normal, good, merge)
        :return: 导入结果
        """
        try:
            self.guarantee_login()
            data = {
                'type': 'json',
                'json': json_data,
                'merge': merge,
                'project_id': project_id
            }

            result = self._session.post(
                f'{self.base_url}/api/interface/save',
                json=data
            ).json()
            is_true(result['errcode'] == 0, f"导入JSON失败: {result.get('errmsg', '未知错误')}")
            return result['data']
        except Exception as e:
            return {
                "ret_code": "400",
                "ret_msg": f"导入JSON失败: {str(e)}"
            }

    # ============ 自动化测试相关 ============

    def run_auto_test(self, col_id: int, project_id: int, token: str,
                      mode: str = 'html', email: bool = False) -> dict:
        """
        运行自动化测试

        :param col_id: 测试集合ID
        :param project_id: 项目ID
        :param token: 项目token
        :param mode: 报告模式 (html, json)
        :param email: 是否发送邮件通知
        :return: 测试结果
        """
        try:
            self.guarantee_login()
            data = {
                'col_id': col_id,
                'project_id': project_id,
                'token': token,
                'mode': mode,
                'email': email
            }

            result = self._session.post(
                f'{self.base_url}/api/open/run',
                json=data
            ).json()
            is_true(result['errcode'] == 0, f"运行自动化测试失败: {result.get('errmsg', '未知错误')}")
            return result['data']
        except Exception as e:
            return {
                "ret_code": "400",
                "ret_msg": f"运行自动化测试失败: {str(e)}"
            }


mcp = FastMCP(name="获取接口文档")


@mcp.tool("get_api_info")
def get_api_info(url: str) -> object:
    """
    获取yapi的接口文档
    :param url: yapi中接口的地址
    :return: 以json格式返回的接口信息
    """
    yapi = YAPI()
    return yapi.get_api(url)


# ============ 项目相关 MCP 工具 ============

@mcp.tool()
def get_project_info(project_id: int) -> dict:
    """
    获取 YAPI 项目的基本信息

    :param project_id: 项目ID
    :return: 项目基本信息
    """
    yapi = YAPI()
    return yapi.get_project(project_id)


@mcp.tool()
def get_project_list() -> list:
    """
    获取当前用户有权限访问的所有项目列表

    :return: 项目列表
    """
    yapi = YAPI()
    return yapi.get_project_list()


@mcp.tool()
def get_project_members(project_id: int) -> list:
    """
    获取指定项目的成员列表

    :param project_id: 项目ID
    :return: 成员列表
    """
    yapi = YAPI()
    return yapi.get_project_members(project_id)


# ============ 接口列表相关 MCP 工具 ============

@mcp.tool()
def get_interface_list(project_id: int, cat_id: int = None) -> list:
    """
    获取项目的接口列表，可指定分类ID进行过滤

    :param project_id: 项目ID
    :param cat_id: 分类ID（可选），不传则获取所有接口
    :return: 接口列表
    """
    yapi = YAPI()
    return yapi.get_interface_list(project_id, cat_id)


@mcp.tool()
def get_interface_list_by_cat(cat_id: int) -> list:
    """
    获取某个分类下的所有接口列表

    :param cat_id: 分类ID
    :return: 接口列表
    """
    yapi = YAPI()
    return yapi.get_interface_list_by_cat(cat_id)


@mcp.tool()
def search_interfaces(project_id: int, keyword: str) -> list:
    """
    在项目中搜索包含关键字的接口

    :param project_id: 项目ID
    :param keyword: 搜索关键字
    :return: 匹配的接口列表
    """
    yapi = YAPI()
    return yapi.search_interfaces(project_id, keyword)


# ============ 数据导入相关 MCP 工具 ============

@mcp.tool()
def import_swagger(url: str = None, json: str = None,
                   project_id: int = None, merge: str = 'normal') -> dict:
    """
    从 URL 或 JSON 导入 Swagger/OpenAPI 数据到 YAPI

    :param url: Swagger 数据的 URL（可选）
    :param json: Swagger JSON 字符串（可选）
    :param project_id: 目标项目ID（可选）
    :param merge: 合并策略，可选值: 'normal', 'good', 'merge'（默认为 'normal'）
    :return: 导入结果
    """
    yapi = YAPI()
    return yapi.import_swagger(url, json, project_id, merge)


@mcp.tool()
def import_postman(url: str = None, json: str = None,
                   project_id: int = None, merge: str = 'normal') -> dict:
    """
    从 URL 或 JSON 导入 Postman 数据到 YAPI

    :param url: Postman 数据的 URL（可选）
    :param json: Postman JSON 字符串（可选）
    :param project_id: 目标项目ID（可选）
    :param merge: 合并策略，可选值: 'normal', 'good', 'merge'（默认为 'normal'）
    :return: 导入结果
    """
    yapi = YAPI()
    return yapi.import_postman(url, json, project_id, merge)


@mcp.tool()
def import_json(json: str, project_id: int, merge: str = 'normal') -> dict:
    """
    导入 JSON 数据到 YAPI

    :param json: JSON 数据字符串
    :param project_id: 目标项目ID
    :param merge: 合并策略，可选值: 'normal', 'good', 'merge'（默认为 'normal'）
    :return: 导入结果
    """
    yapi = YAPI()
    return yapi.import_json(json, project_id, merge)


# ============ 自动化测试相关 MCP 工具 ============

@mcp.tool()
def run_auto_test(col_id: int, project_id: int, token: str,
                  mode: str = 'html', email: bool = False) -> dict:
    """
    运行自动化测试并返回测试报告

    :param col_id: 测试集合ID
    :param project_id: 项目ID
    :param token: 项目token
    :param mode: 报告模式，可选值: 'html', 'json'（默认为 'html'）
    :param email: 是否发送邮件通知（默认为 False）
    :return: 测试报告
    """
    yapi = YAPI()
    return yapi.run_auto_test(col_id, project_id, token, mode, email)


if __name__ == '__main__':
    mcp.run()


def main():
    """入口点函数，供 uvx/pip install 使用"""
    mcp.run()
#     yapi = YAPI()
#     result = yapi.get_api("https://yapi.jlpay.com/project/1646/interface/api/78406")
#     print(f'接口: {json.dumps(result, ensure_ascii=False)}')
