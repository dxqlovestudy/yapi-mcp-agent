# YAPI MCP Server

基于 FastMCP 的 YAPI 接口文档查询工具，让 AI 助手能够获取 YAPI 平台上的接口文档信息。

## 功能

### 项目相关
- 获取项目基本信息
- 获取项目列表
- 获取项目成员列表

### 接口管理
- 获取接口文档（请求参数和响应结构）
- 获取项目的接口列表
- 获取某个分类下的接口列表
- 按关键字搜索接口

### 数据导入
- 导入 Swagger/OpenAPI 数据
- 导入 Postman 数据
- 导入 JSON 数据

### 自动化测试
- 运行自动化测试
- 获取测试报告

### 通用功能
- 支持 LDAP 登录认证
- 自动管理登录状态
- 通过 MCP 协议与 AI 助手集成

## 安装

### 从源码安装

```bash
git clone https://github.com/yourusername/yapi-mcp.git
cd yapi-mcp
pip install -e .
```

或使用 uv：

```bash
git clone https://github.com/yourusername/yapi-mcp.git
cd yapi-mcp
uv pip install -e .
```

### 从 PyPI 安装 （暂不支持）


## 配置

通过环境变量配置 YAPI 连接信息：

```bash
export YAPI_BASE_URL="https://your-yapi-server.com"
export YAPI_EMAIL="your-email@example.com"
export YAPI_PASSWORD="your-password"
```

### 配置项说明

| 环境变量 | 说明 |
|----------|------|
| `YAPI_BASE_URL` | YAPI 服务器地址 |
| `YAPI_EMAIL` | 登录邮箱 |
| `YAPI_PASSWORD` | 登录密码 |

## 使用

### 使用 uv 运行（推荐）

```bash
uv run yapi-mcp
```

### 使用 python -m 运行

```bash
python -m yapi_mcp
```

### 直接运行命令

```bash
yapi-mcp
```

### 作为 MCP 服务器使用

#### 使用 uv 运行（推荐）

```json
{
  "mcpServers": {
    "yapi": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/yapi-mcp",
        "run",
        "yapi-mcp"
      ],
      "env": {
        "YAPI_BASE_URL": "https://your-yapi-server.com",
        "YAPI_EMAIL": "your-email@example.com",
        "YAPI_PASSWORD": "your-password"
      }
    }
  }
}
```

#### 使用 uvx 运行（暂不支持）

```json
{
  "mcpServers": {
    "yapi": {
      "command": "uvx",
      "args": [
        "yapi-mcp"
      ],
      "env": {
        "YAPI_BASE_URL": "https://your-yapi-server.com",
        "YAPI_EMAIL": "your-email@example.com",
        "YAPI_PASSWORD": "your-password"
      }
    }
  }
}
```

#### 使用 Python 直接运行

**Claude Desktop 配置**

在 Claude Desktop 的配置文件中添加：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "yapi": {
      "command": "python",
      "args": ["-m", "yapi_mcp"],
      "env": {
        "YAPI_BASE_URL": "https://your-yapi-server.com",
        "YAPI_EMAIL": "your-email@example.com",
        "YAPI_PASSWORD": "your-password"
      }
    }
  }
}
```

#### Cursor / VS Code 配置

```json
{
  "mcp": {
    "servers": {
      "yapi": {
        "command": "uv",
        "args": [
          "--directory",
          "/path/to/yapi-mcp",
          "run",
          "yapi-mcp"
        ],
        "env": {
          "YAPI_BASE_URL": "https://your-yapi-server.com",
          "YAPI_EMAIL": "your-email@example.com",
          "YAPI_PASSWORD": "your-password"
        }
      }
    }
  }
}
```

## MCP 工具

### 项目相关工具

#### 获取项目基本信息

获取 YAPI 项目的基本信息。

**参数：**
- `project_id` (int): 项目ID

**返回：** 项目基本信息字典

---

#### 获取项目列表

获取当前用户有权限访问的所有项目列表。

**返回：** 项目列表

---

#### 获取项目成员列表

获取指定项目的成员列表。

**参数：**
- `project_id` (int): 项目ID

**返回：** 成员列表

### 接口管理工具

#### 获取接口文档

获取 YAPI 接口文档信息。

**参数：**
- `url` (string): YAPI 接口地址，如 `https://yapi.example.com/project/123/interface/api/456`

**返回：**
- `title`: 接口名称
- `request`: 请求参数结构
- `response`: 响应数据结构

---

#### 获取接口列表

获取项目的接口列表，可指定分类ID进行过滤。

**参数：**
- `project_id` (int): 项目ID
- `cat_id` (int, 可选): 分类ID，不传则获取所有接口

**返回：** 接口列表

---

#### 获取分类接口列表

获取某个分类下的所有接口列表。

**参数：**
- `cat_id` (int): 分类ID

**返回：** 接口列表

---

#### 搜索接口

在项目中搜索包含关键字的接口。

**参数：**
- `project_id` (int): 项目ID
- `keyword` (string): 搜索关键字

**返回：** 匹配的接口列表

### 数据导入工具

#### 导入Swagger数据

从 URL 或 JSON 导入 Swagger/OpenAPI 数据到 YAPI。

**参数：**
- `url` (string, 可选): Swagger 数据的 URL
- `json` (string, 可选): Swagger JSON 字符串
- `project_id` (int, 可选): 目标项目ID
- `merge` (string, 可选): 合并策略，可选值: `normal`、`good`、`merge`（默认为 `normal`）

**返回：** 导入结果

---

#### 导入Postman数据

从 URL 或 JSON 导入 Postman 数据到 YAPI。

**参数：**
- `url` (string, 可选): Postman 数据的 URL
- `json` (string, 可选): Postman JSON 字符串
- `project_id` (int, 可选): 目标项目ID
- `merge` (string, 可选): 合并策略，可选值: `normal`、`good`、`merge`（默认为 `normal`）

**返回：** 导入结果

---

#### 导入JSON数据

导入 JSON 数据到 YAPI。

**参数：**
- `json` (string): JSON 数据字符串
- `project_id` (int): 目标项目ID
- `merge` (string, 可选): 合并策略，可选值: `normal`、`good`、`merge`（默认为 `normal`）

**返回：** 导入结果

### 自动化测试工具

#### 运行自动化测试

运行自动化测试并返回测试报告。

**参数：**
- `col_id` (int): 测试集合ID
- `project_id` (int): 项目ID
- `token` (string): 项目token
- `mode` (string, 可选): 报告模式，可选值: `html`、`json`（默认为 `html`）
- `email` (bool, 可选): 是否发送邮件通知（默认为 `False`）

**返回：** 测试报告

## 使用示例

在 AI 助手中可以执行以下操作：

```
# 获取接口文档
请帮我获取接口 https://yapi.example.com/project/123/interface/api/456 的文档

# 获取项目列表
请获取我有权限访问的所有项目

# 获取项目成员
请获取项目 123 的成员列表

# 搜索接口
请在项目 123 中搜索包含"用户"关键字的接口

# 导入数据
请将这个 Swagger 文档导入到项目 123：https://example.com/swagger.json

# 运行测试
请为项目 123 运行自动化测试，测试集合 ID 是 456
```

## 项目结构

```
yapi-mcp/
├── src/
│   └── yapi_mcp/
│       ├── __init__.py      # 包入口，导出主要模块
│       ├── __main__.py      # 命令行入口
│       ├── server.py        # MCP 服务器和工具定义
│       ├── client.py        # YAPI 客户端类
│       └── config.py        # 配置管理
├── tests/
│   ├── __init__.py
│   └── test_config.py       # 配置测试
├── pyproject.toml           # 项目配置
├── .gitignore              # Git 忽略文件
└── README.md               # 本文档
```

## 注意事项

1. **安全性**：请勿将账号密码硬编码或提交到版本控制系统
2. **推荐使用环境变量**：在生产环境或共享环境中，使用环境变量配置敏感信息
3. **LDAP 登录**：当前仅支持 LDAP 方式登录，如需其他登录方式请修改 `login()` 方法

## 故障排除

### 登录失败

- 检查邮箱和密码是否正确
- 确认 YAPI 服务器地址是否正确（不要以 `/` 结尾）
- 确认服务器支持 LDAP 登录

### 配置未生效

- 确认环境变量是否正确设置
- 检查环境变量名称是否正确：`YAPI_BASE_URL`, `YAPI_EMAIL`, `YAPI_PASSWORD`

## License

MIT
