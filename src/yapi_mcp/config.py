"""配置管理模块"""

import os
from dataclasses import dataclass


@dataclass
class YAPIConfig:
    """YAPI 配置类"""
    base_url: str
    email: str
    password: str

    @classmethod
    def from_env(cls) -> "YAPIConfig":
        """
        从环境变量加载配置

        必须通过环境变量提供以下配置：
        - YAPI_BASE_URL: YAPI 服务器地址
        - YAPI_EMAIL: 登录邮箱
        - YAPI_PASSWORD: 登录密码
        """
        base_url = os.getenv("YAPI_BASE_URL")
        email = os.getenv("YAPI_EMAIL")
        password = os.getenv("YAPI_PASSWORD")

        missing = []
        if not base_url:
            missing.append("YAPI_BASE_URL")
        if not email:
            missing.append("YAPI_EMAIL")
        if not password:
            missing.append("YAPI_PASSWORD")

        if missing:
            raise ValueError(
                f"缺少必要的环境变量: {', '.join(missing)}\n"
                "请设置: YAPI_BASE_URL, YAPI_EMAIL, YAPI_PASSWORD"
            )

        return cls(
            base_url=base_url.rstrip("/"),
            email=email,
            password=password,
        )


# 全局配置实例
_config: YAPIConfig | None = None


def get_config() -> YAPIConfig:
    """获取配置实例（单例模式）"""
    global _config
    if _config is None:
        _config = YAPIConfig.from_env()
    return _config
