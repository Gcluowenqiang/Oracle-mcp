# Oracle数据库MCP服务
[![smithery badge](https://smithery.ai/badge/@Gcluowenqiang/oracle-mcp-qyue)](https://smithery.ai/server/@Gcluowenqiang/oracle-mcp-qyue)

专为Cursor IDE集成设计的Oracle数据库MCP（Model Context Protocol）服务，提供安全的Oracle数据库访问和管理功能。

## 🌟 功能特性

- **🔒 多层安全控制**：三种安全模式（只读、限制写入、完全访问）
- **📊 智能文档生成**：支持Markdown、JSON、SQL等多种格式
- **🎯 Cursor深度集成**：专为Cursor IDE优化的MCP协议支持
- **🛡️ SQL安全验证**：智能SQL验证器防止危险操作
- **⚡ 高性能连接**：连接池和超时控制
- **📋 完整表管理**：表结构、索引、约束等全方位信息
- **🏛️ Oracle特性支持**：Schema管理、SID/SERVICE_NAME连接、LOB处理

## 🔧 安装配置

### Installing via Smithery

To install Oracle Database Access Service for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@Gcluowenqiang/oracle-mcp-qyue):

```bash
npx -y @smithery/cli install @Gcluowenqiang/oracle-mcp-qyue --client claude
```

### 环境要求

- Python 3.8+
- Oracle Database 11g+ 或 Oracle Database 19c+
- Oracle Instant Client
- Cursor IDE

### 快速安装

```bash
# 克隆项目
git clone https://github.com/Gcluowenqiang/Oracle-mcp.git
cd oracle-mcp

# 安装依赖
pip install -r requirements.txt
```

### Oracle Client配置

```bash
# 下载并安装Oracle Instant Client
# Linux/macOS示例:
export LD_LIBRARY_PATH=/path/to/instantclient_21_8:$LD_LIBRARY_PATH

# Windows示例:
# 将 instantclient 目录添加到 PATH 环境变量
```

### Cursor MCP配置

在Cursor IDE中，添加以下配置到 MCP 设置：

```json
{
  "mcpServers": {
    "oracle-db": {
      "command": "python",
      "args": ["path/to/oracle-mcp/main.py"],
      "env": {
        "ORACLE_HOST": "localhost",
        "ORACLE_PORT": "1521",
        "ORACLE_SERVICE_NAME": "XEPDB1",
        "ORACLE_USERNAME": "your_username",
        "ORACLE_PASSWORD": "your_password",
        "ORACLE_SECURITY_MODE": "readonly",
        "ORACLE_ALLOWED_SCHEMAS": "*",
        "ORACLE_MAX_RESULT_ROWS": "1000"
      }
    }
  }
}
```

## 🚀 使用指南

### 基本操作

1. **测试连接**
   ```
   在Cursor中使用MCP工具: test_connection
   ```

2. **查看Schema概览**
   ```
   使用工具: generate_database_overview
   ```

3. **查询表结构**
   ```
   使用工具: describe_table
   参数: table_name = "EMPLOYEES"
   ```

4. **执行SQL查询**
   ```
   使用工具: execute_query
   参数: sql = "SELECT * FROM EMPLOYEES WHERE ROWNUM <= 10"
   ```

### 连接配置说明

#### Service Name连接（推荐）
```json
"ORACLE_SERVICE_NAME": "XEPDB1"
```

#### SID连接
```json
"ORACLE_SID": "XE"
```

### 安全模式说明

#### 🟢 只读模式 (readonly)
- ✅ SELECT、WITH、DESC、DESCRIBE、EXPLAIN等查询操作
- ❌ 禁止任何写入和修改操作
- 🎯 **推荐**：生产环境查询、数据分析

#### 🟡 限制写入模式 (limited_write)  
- ✅ 查询操作 + INSERT、UPDATE、MERGE
- ❌ 禁止DELETE、DROP、ALTER、PURGE等危险操作
- 🎯 **适用**：开发环境、数据维护

#### 🔴 完全访问模式 (full_access)
- ✅ 所有SQL操作
- ⚠️ **警告**：仅在完全可控的环境使用

## 📋 可用工具

| 工具名称 | 功能描述 | 主要参数 |
|---------|---------|---------|
| `test_connection` | 测试数据库连接 | - |
| `get_security_info` | 获取安全配置信息 | - |
| `list_tables` | 获取Schema表列表 | `schema`(可选) |
| `describe_table` | 获取表详细结构 | `table_name`, `schema`(可选) |
| `generate_table_doc` | 生成表文档 | `table_name`, `format`, `schema`(可选) |
| `generate_database_overview` | 生成Schema概览 | `schema`(可选) |
| `execute_query` | 执行SQL语句 | `sql` |
| `list_schemas` | 获取可用Schema列表 | - |

## ⚙️ 配置参数

### 必需环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `ORACLE_HOST` | 数据库主机地址 | `localhost` |
| `ORACLE_PORT` | 数据库端口 | `1521` |
| `ORACLE_USERNAME` | 数据库用户名 | `hr` |
| `ORACLE_PASSWORD` | 数据库密码 | `password` |
| `ORACLE_SERVICE_NAME` 或 `ORACLE_SID` | 服务名或SID | `XEPDB1` 或 `XE` |

### 可选环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `ORACLE_SECURITY_MODE` | `readonly` | 安全模式 |
| `ORACLE_ALLOWED_SCHEMAS` | `["*"]` | 允许访问的Schema列表 |
| `ORACLE_CONNECT_TIMEOUT` | `30` | 连接超时（秒） |
| `ORACLE_QUERY_TIMEOUT` | `60` | 查询超时（秒） |
| `ORACLE_MAX_RESULT_ROWS` | `1000` | 最大返回行数 |
| `ORACLE_ENABLE_QUERY_LOG` | `false` | 启用查询日志 |
| `ORACLE_ENCODING` | `UTF-8` | 字符编码 |

## 📖 文档生成

### 支持格式

- **Markdown**: 人类友好的文档格式
- **JSON**: 机器可读的结构化数据
- **SQL**: 可执行的建表语句

### 生成示例

```python
# 生成单表Markdown文档
generate_table_doc(table_name="EMPLOYEES", format="markdown")

# 生成Schema概览
generate_database_overview(schema="HR")

# 生成SQL建表语句
generate_table_doc(table_name="DEPARTMENTS", format="sql")
```

## 🏛️ Oracle特性支持

### 数据类型支持
- **字符类型**: VARCHAR2, CHAR, NVARCHAR2, NCHAR, CLOB, NCLOB
- **数值类型**: NUMBER, BINARY_FLOAT, BINARY_DOUBLE
- **日期类型**: DATE, TIMESTAMP, INTERVAL
- **LOB类型**: BLOB, CLOB, NCLOB, BFILE

### 约束类型
- **P**: 主键约束 (Primary Key)
- **R**: 外键约束 (Foreign Key) 
- **U**: 唯一约束 (Unique)
- **C**: 检查约束 (Check)

### 系统视图
- `ALL_TABLES`: 表信息
- `ALL_TAB_COLUMNS`: 列信息
- `ALL_INDEXES`: 索引信息
- `ALL_CONSTRAINTS`: 约束信息

## 🔒 安全最佳实践

1. **生产环境**：始终使用 `readonly` 模式
2. **权限最小化**：仅授予必要的Schema访问权限
3. **网络安全**：使用SSL连接，限制网络访问
4. **监控日志**：启用查询日志监控异常操作
5. **定期更新**：保持Oracle Client和依赖库版本更新

## 🔍 故障排除

### 常见问题

**Q: 连接失败 - ORA-12541?**
```
A: 检查以下项目：
   1. Oracle Listener是否运行
   2. 主机地址和端口是否正确
   3. 防火墙设置
   4. TNS配置
```

**Q: 权限不足 - ORA-00942?**
```
A: 确保数据库用户具有：
   - 目标Schema的访问权限
   - 系统视图的查询权限
   - 根据安全模式配置相应的操作权限
```

**Q: 字符编码问题?**
```
A: 检查以下设置：
   - ORACLE_ENCODING环境变量
   - Oracle客户端字符集设置
   - 数据库字符集配置
```

**Q: Oracle Client未找到?**
```
A: 确保已正确安装Oracle Instant Client：
   - Linux/macOS: 设置LD_LIBRARY_PATH
   - Windows: 添加到PATH环境变量
   - 验证cx_Oracle可以正常导入
```

## 🧪 开发测试

```bash
# 运行单元测试
pytest tests/

# 启动开发服务器
python main.py

# 检查代码质量
flake8 *.py
```

## 📝 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解版本更新信息。

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙋‍♂️ 支持

- 📧 邮箱: wxhn1217@outlook.com
- 🐛 问题反馈: [GitHub Issues](https://github.com/Gcluowenqiang/Oracle-mcp/issues)
- 📖 文档: [项目Wiki](https://github.com/Gcluowenqiang/Oracle-mcp/wiki)

---

⭐ 如果这个项目对你有帮助，请给我们一个星标！ 
