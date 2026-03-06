# YAPI MCP Server

[中文文档](README_CN.md) | English

A YAPI interface documentation query tool built with FastMCP, enabling AI assistants to access interface documentation from YAPI platforms.

## Features

### Project Management
- Get project basic information
- Get project list
- Get project member list

### Interface Management
- Get interface documentation (request parameters and response structure)
- Get interface list for a project
- Get interface list by category
- Search interfaces by keyword

### Data Import
- Import Swagger/OpenAPI data
- Import Postman data
- Import JSON data

### Automation Testing
- Run automation tests
- Get test reports

### General Features
- LDAP login authentication support
- Automatic login state management
- Integration with AI assistants via MCP protocol

## Installation

### Install from Source

```bash
git clone https://github.com/yourusername/yapi-mcp.git
cd yapi-mcp
pip install -e .
```

Or using uv:

```bash
git clone https://github.com/yourusername/yapi-mcp.git
cd yapi-mcp
uv pip install -e .
```

### Install from PyPI (Coming Soon)

## Configuration

Configure YAPI connection through environment variables:

```bash
export YAPI_BASE_URL="https://your-yapi-server.com"
export YAPI_EMAIL="your-email@example.com"
export YAPI_PASSWORD="your-password"
```

### Configuration Options

| Environment Variable | Description |
|---------------------|-------------|
| `YAPI_BASE_URL` | YAPI server address |
| `YAPI_EMAIL` | Login email |
| `YAPI_PASSWORD` | Login password |

## Usage

### Run with uv (Recommended)

```bash
uv run yapi-mcp
```

### Run with python -m

```bash
python -m yapi_mcp
```

### Run Directly

```bash
yapi-mcp
```

### Use as MCP Server

#### Run with uv (Recommended)

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

#### Run with uvx (Coming Soon)

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

#### Run with Python Directly

**Claude Desktop Configuration**

Add to Claude Desktop configuration file:

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

#### Cursor / VS Code Configuration

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

## MCP Tools

### Project Tools

#### Get Project Basic Information

Get basic information of a YAPI project.

**Parameters:**
- `project_id` (int): Project ID

**Returns:** Project basic information dictionary

---

#### Get Project List

Get all projects accessible by the current user.

**Returns:** Project list

---

#### Get Project Member List

Get the member list of a specified project.

**Parameters:**
- `project_id` (int): Project ID

**Returns:** Member list

### Interface Management Tools

#### Get Interface Documentation

Get YAPI interface documentation information.

**Parameters:**
- `url` (string): YAPI interface URL, e.g., `https://yapi.example.com/project/123/interface/api/456`

**Returns:**
- `title`: Interface name
- `request`: Request parameter structure
- `response`: Response data structure

---

#### Get Interface List

Get the interface list of a project, optionally filtered by category ID.

**Parameters:**
- `project_id` (int): Project ID
- `cat_id` (int, optional): Category ID, retrieves all interfaces if not provided

**Returns:** Interface list

---

#### Get Category Interface List

Get all interfaces under a specific category.

**Parameters:**
- `cat_id` (int): Category ID

**Returns:** Interface list

---

#### Search Interfaces

Search for interfaces containing a keyword in a project.

**Parameters:**
- `project_id` (int): Project ID
- `keyword` (string): Search keyword

**Returns:** Matched interface list

### Data Import Tools

#### Import Swagger Data

Import Swagger/OpenAPI data to YAPI from URL or JSON.

**Parameters:**
- `url` (string, optional): URL of Swagger data
- `json` (string, optional): Swagger JSON string
- `project_id` (int, optional): Target project ID
- `merge` (string, optional): Merge strategy, options: `normal`, `good`, `merge` (default: `normal`)

**Returns:** Import result

---

#### Import Postman Data

Import Postman data to YAPI from URL or JSON.

**Parameters:**
- `url` (string, optional): URL of Postman data
- `json` (string, optional): Postman JSON string
- `project_id` (int, optional): Target project ID
- `merge` (string, optional): Merge strategy, options: `normal`, `good`, `merge` (default: `normal`)

**Returns:** Import result

---

#### Import JSON Data

Import JSON data to YAPI.

**Parameters:**
- `json` (string): JSON data string
- `project_id` (int): Target project ID
- `merge` (string, optional): Merge strategy, options: `normal`, `good`, `merge` (default: `normal`)

**Returns:** Import result

### Automation Testing Tools

#### Run Automation Test

Run automation tests and return test reports.

**Parameters:**
- `col_id` (int): Test collection ID
- `project_id` (int): Project ID
- `token` (string): Project token
- `mode` (string, optional): Report mode, options: `html`, `json` (default: `html`)
- `email` (bool, optional): Whether to send email notification (default: `False`)

**Returns:** Test report

## Usage Examples

With AI assistants, you can perform the following operations:

```
# Get interface documentation
Please get the documentation for interface https://yapi.example.com/project/123/interface/api/456

# Get project list
Please get all projects I have access to

# Get project members
Please get the member list for project 123

# Search interfaces
Please search for interfaces containing "user" keyword in project 123

# Import data
Please import this Swagger document to project 123: https://example.com/swagger.json

# Run tests
Please run automation tests for project 123, test collection ID is 456
```

## Project Structure

```
yapi-mcp/
├── src/
│   └── yapi_mcp/
│       ├── __init__.py      # Package entry, exports main modules
│       ├── __main__.py      # CLI entry point
│       ├── server.py        # MCP server and tool definitions
│       ├── client.py        # YAPI client class
│       └── config.py        # Configuration management
├── tests/
│   ├── __init__.py
│   └── test_config.py       # Configuration tests
├── pyproject.toml           # Project configuration
├── .gitignore              # Git ignore file
└── README.md               # This document
```

## Important Notes

1. **Security**: Do not hardcode credentials or commit them to version control systems
2. **Environment Variables**: Use environment variables to configure sensitive information in production or shared environments
3. **LDAP Login**: Currently only supports LDAP login. Modify the `login()` method if other login methods are needed

## Troubleshooting

### Login Failure

- Check if email and password are correct
- Confirm the YAPI server address is correct (do not end with `/`)
- Confirm the server supports LDAP login

### Configuration Not Taking Effect

- Verify environment variables are set correctly
- Check environment variable names: `YAPI_BASE_URL`, `YAPI_EMAIL`, `YAPI_PASSWORD`

## License

MIT