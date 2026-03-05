"""Tests for config module"""

import os
import pytest

from yapi_mcp.config import YAPIConfig, get_config


def test_yapi_config_from_env(monkeypatch):
    """Test loading config from environment variables"""
    monkeypatch.setenv("YAPI_BASE_URL", "https://yapi.example.com/")
    monkeypatch.setenv("YAPI_EMAIL", "test@example.com")
    monkeypatch.setenv("YAPI_PASSWORD", "password123")

    config = YAPIConfig.from_env()

    assert config.base_url == "https://yapi.example.com"  # trailing slash removed
    assert config.email == "test@example.com"
    assert config.password == "password123"


def test_yapi_config_missing_env(monkeypatch):
    """Test error when required environment variables are missing"""
    monkeypatch.delenv("YAPI_BASE_URL", raising=False)
    monkeypatch.delenv("YAPI_EMAIL", raising=False)
    monkeypatch.delenv("YAPI_PASSWORD", raising=False)

    with pytest.raises(ValueError) as exc_info:
        YAPIConfig.from_env()

    assert "YAPI_BASE_URL" in str(exc_info.value)
    assert "YAPI_EMAIL" in str(exc_info.value)
    assert "YAPI_PASSWORD" in str(exc_info.value)