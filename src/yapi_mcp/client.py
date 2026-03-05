"""YAPI 客户端模块"""

import json
from typing import Any

from requests import Session

from .config import get_config


def _check(condition: bool, message: str) -> None:
    """条件检查辅助函数"""
    if not condition:
        raise Exception(message)


class YAPIClient:
    """YAPI 客户端类"""

    def __init__(
        self,
        base_url: str | None = None,
        email: str | None = None,
        password: str | None = None,
    ):
        """
        初始化 YAPI 客户端

        :param base_url: YAPI 服务器地址，默认从配置读取
        :param email: 登录邮箱，默认从配置读取
        :param password: 登录密码，默认从配置读取
        """
        config = get_config()
        self._session = Session()
        self.base_url = base_url or config.base_url
        self.email = email or config.email
        self.password = password or config.password

    def is_login(self) -> bool:
        """检查是否已登录"""
        resp = self._session.get(f"{self.base_url}/api/user/status")
        return resp.json()["errcode"] == 0

    def login(self) -> bool:
        """执行登录"""
        resp = self._session.post(
            f"{self.base_url}/api/user/login_by_ldap",
            json={"email": self.email, "password": self.password},
        )
        return resp.json()["errcode"] == 0

    def guarantee_login(self) -> None:
        """确保已登录"""
        if not self.is_login():
            ret = self.login()
            _check(ret, "登录失败")

    def _transform_schema(self, data: str) -> dict:
        """转换 JSON Schema 数据"""
        obj = json.loads(data)
        return obj.get("properties", {})

    # ============ 接口相关 ============

    def get_api(self, url: str) -> dict[str, Any]:
        """
        获取接口详情

        :param url: YAPI 接口地址
        :return: 接口信息
        """
        try:
            self.guarantee_login()
            api_id = url.split("/")[-1]
            real_url = f"{self.base_url}/api/interface/get?id={api_id}"
            result = self._session.get(real_url).json()
            _check(result["errcode"] == 0, "获取接口失败")

            data = result["data"]
            return {
                "title": data["title"],
                "request": self._transform_schema(data.get("req_body_other", "{}")),
                "response": self._transform_schema(data.get("res_body", "{}")),
            }
        except Exception as e:
            return {"ret_code": "400", "ret_msg": f"异常: {str(e)}"}

    # ============ 项目相关 ============

    def get_project(self, project_id: int) -> dict[str, Any]:
        """
        获取项目基本信息

        :param project_id: 项目ID
        :return: 项目信息
        """
        try:
            self.guarantee_login()
            result = self._session.get(
                f"{self.base_url}/api/project/get?id={project_id}"
            ).json()
            _check(
                result["errcode"] == 0,
                f"获取项目失败: {result.get('errmsg', '未知错误')}",
            )
            return result["data"]
        except Exception as e:
            return {"ret_code": "400", "ret_msg": f"获取项目失败: {str(e)}"}

    def get_project_list(self) -> list[dict] | dict:
        """
        获取项目列表

        :return: 项目列表
        """
        try:
            self.guarantee_login()
            result = self._session.get(f"{self.base_url}/api/project/list").json()
            _check(
                result["errcode"] == 0,
                f"获取项目列表失败: {result.get('errmsg', '未知错误')}",
            )
            return result["data"]
        except Exception as e:
            return {"ret_code": "400", "ret_msg": f"获取项目列表失败: {str(e)}"}

    def get_project_members(self, project_id: int) -> list[dict] | dict:
        """
        获取项目成员列表

        :param project_id: 项目ID
        :return: 成员列表
        """
        try:
            self.guarantee_login()
            result = self._session.get(
                f"{self.base_url}/api/project/get?id={project_id}"
            ).json()
            _check(
                result["errcode"] == 0,
                f"获取项目成员失败: {result.get('errmsg', '未知错误')}",
            )
            project_data = result["data"]
            members = project_data.get("members") or project_data.get("members_data", [])
            return members
        except Exception as e:
            return {"ret_code": "400", "ret_msg": f"获取项目成员失败: {str(e)}"}

    # ============ 接口列表相关 ============

    def get_interface_list(
        self, project_id: int, cat_id: int | None = None
    ) -> list[dict] | dict:
        """
        获取接口列表

        :param project_id: 项目ID
        :param cat_id: 分类ID（可选）
        :return: 接口列表
        """
        try:
            self.guarantee_login()
            params = {"project_id": project_id}
            if cat_id:
                params["catid"] = cat_id

            result = self._session.get(
                f"{self.base_url}/api/interface/list", params=params
            ).json()
            _check(
                result["errcode"] == 0,
                f"获取接口列表失败: {result.get('errmsg', '未知错误')}",
            )
            return result["data"]
        except Exception as e:
            return {"ret_code": "400", "ret_msg": f"获取接口列表失败: {str(e)}"}

    def get_interface_list_by_cat(self, cat_id: int) -> list[dict] | dict:
        """
        获取某分类下的接口列表

        :param cat_id: 分类ID
        :return: 接口列表
        """
        try:
            self.guarantee_login()
            result = self._session.get(
                f"{self.base_url}/api/interface/list_cat", params={"catid": cat_id}
            ).json()
            _check(
                result["errcode"] == 0,
                f"获取分类接口列表失败: {result.get('errmsg', '未知错误')}",
            )
            return result["data"]
        except Exception as e:
            return {"ret_code": "400", "ret_msg": f"获取分类接口列表失败: {str(e)}"}

    def search_interfaces(self, project_id: int, keyword: str) -> list[dict] | dict:
        """
        搜索接口

        :param project_id: 项目ID
        :param keyword: 搜索关键字
        :return: 匹配的接口列表
        """
        try:
            self.guarantee_login()
            result = self._session.get(
                f"{self.base_url}/api/interface/list",
                params={"project_id": project_id},
            ).json()
            _check(
                result["errcode"] == 0,
                f"搜索接口失败: {result.get('errmsg', '未知错误')}",
            )

            interfaces = result["data"]
            if isinstance(interfaces, list):
                keyword_lower = keyword.lower()
                filtered = [
                    iface
                    for iface in interfaces
                    if keyword_lower in iface.get("title", "").lower()
                    or keyword_lower in iface.get("path", "").lower()
                ]
                return filtered
            return []
        except Exception as e:
            return {"ret_code": "400", "ret_msg": f"搜索接口失败: {str(e)}"}

    # ============ 数据导入相关 ============

    def import_swagger(
        self,
        url: str | None = None,
        json_data: str | None = None,
        project_id: int | None = None,
        merge: str = "normal",
    ) -> dict[str, Any]:
        """
        导入 Swagger/OpenAPI 数据

        :param url: Swagger URL
        :param json_data: Swagger JSON 字符串
        :param project_id: 项目ID
        :param merge: 合并策略
        :return: 导入结果
        """
        try:
            self.guarantee_login()
            data: dict = {"type": "Swagger", "merge": merge}
            if url:
                data["url"] = url
            if json_data:
                data["json"] = json_data
            if project_id is not None:
                data["project_id"] = project_id

            result = self._session.post(
                f"{self.base_url}/api/interface/save", json=data
            ).json()
            _check(
                result["errcode"] == 0,
                f"导入Swagger失败: {result.get('errmsg', '未知错误')}",
            )
            return result["data"]
        except Exception as e:
            return {"ret_code": "400", "ret_msg": f"导入Swagger失败: {str(e)}"}

    def import_postman(
        self,
        url: str | None = None,
        json_data: str | None = None,
        project_id: int | None = None,
        merge: str = "normal",
    ) -> dict[str, Any]:
        """
        导入 Postman 数据

        :param url: Postman URL
        :param json_data: Postman JSON 字符串
        :param project_id: 项目ID
        :param merge: 合并策略
        :return: 导入结果
        """
        try:
            self.guarantee_login()
            data: dict = {"type": "Postman", "merge": merge}
            if url:
                data["url"] = url
            if json_data:
                data["json"] = json_data
            if project_id is not None:
                data["project_id"] = project_id

            result = self._session.post(
                f"{self.base_url}/api/interface/save", json=data
            ).json()
            _check(
                result["errcode"] == 0,
                f"导入Postman失败: {result.get('errmsg', '未知错误')}",
            )
            return result["data"]
        except Exception as e:
            return {"ret_code": "400", "ret_msg": f"导入Postman失败: {str(e)}"}

    def import_json(
        self, json_data: str, project_id: int, merge: str = "normal"
    ) -> dict[str, Any]:
        """
        导入 JSON 数据

        :param json_data: JSON 数据字符串
        :param project_id: 项目ID
        :param merge: 合并策略
        :return: 导入结果
        """
        try:
            self.guarantee_login()
            data = {
                "type": "json",
                "json": json_data,
                "merge": merge,
                "project_id": project_id,
            }

            result = self._session.post(
                f"{self.base_url}/api/interface/save", json=data
            ).json()
            _check(
                result["errcode"] == 0,
                f"导入JSON失败: {result.get('errmsg', '未知错误')}",
            )
            return result["data"]
        except Exception as e:
            return {"ret_code": "400", "ret_msg": f"导入JSON失败: {str(e)}"}

    # ============ 自动化测试相关 ============

    def run_auto_test(
        self,
        col_id: int,
        project_id: int,
        token: str,
        mode: str = "html",
        email: bool = False,
    ) -> dict[str, Any]:
        """
        运行自动化测试

        :param col_id: 测试集合ID
        :param project_id: 项目ID
        :param token: 项目token
        :param mode: 报告模式
        :param email: 是否发送邮件通知
        :return: 测试结果
        """
        try:
            self.guarantee_login()
            data = {
                "col_id": col_id,
                "project_id": project_id,
                "token": token,
                "mode": mode,
                "email": email,
            }

            result = self._session.post(
                f"{self.base_url}/api/open/run", json=data
            ).json()
            _check(
                result["errcode"] == 0,
                f"运行自动化测试失败: {result.get('errmsg', '未知错误')}",
            )
            return result["data"]
        except Exception as e:
            return {"ret_code": "400", "ret_msg": f"运行自动化测试失败: {str(e)}"}
