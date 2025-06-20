# 更新日志

本文档记录了Oracle MCP服务的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 计划新增
- [ ] 数据库性能监控
- [ ] SQL查询优化建议
- [ ] 支持Oracle RAC集群连接
- [ ] PL/SQL存储过程分析
- [ ] 数据导入导出功能

## [1.0.0] - 2025-01-28

### 🎉 首次发布

#### 新增
- **🔐 安全框架**
  - 三层安全模式：只读、限制写入、完全访问
  - SQL验证器防止危险操作
  - 基于环境变量的配置管理
  
- **📋 核心功能**
  - Oracle数据库连接管理和测试
  - Schema和表结构查询分析
  - 索引和约束信息获取
  - 多Schema支持和访问控制
  
- **📊 文档生成**
  - Markdown格式表文档
  - JSON格式结构化数据
  - SQL建表语句生成
  - Schema概览文档
  
- **🔧 MCP协议支持**
  - 完整的Model Context Protocol实现
  - Cursor IDE深度集成
  - 资源和工具接口
  - 异步处理支持
  
- **📈 高级特性**
  - 连接池和超时控制
  - 查询结果限制
  - 操作日志记录
  - 错误处理和恢复

#### Oracle特性支持
- **连接方式**: SERVICE_NAME和SID双模式支持
- **数据类型**: VARCHAR2、CHAR、NUMBER、DATE、TIMESTAMP、LOB等
- **约束类型**: 主键(P)、外键(R)、唯一(U)、检查(C)约束
- **系统视图**: ALL_TABLES、ALL_TAB_COLUMNS、ALL_INDEXES等
- **字符编码**: UTF-8、GBK等多种编码支持

#### 技术规格
- **数据库支持**: Oracle 11g+, Oracle 19c+, Oracle 21c+
- **Python版本**: 3.8+
- **核心依赖**: 
  - `cx_Oracle` 8.3.0+
  - `mcp` 1.0.0+
  - `pydantic` 2.0.0+
  - `jinja2` 3.1.0+

#### 可用工具
1. `test_connection` - 测试数据库连接
2. `get_security_info` - 获取安全配置
3. `list_tables` - 列出Schema表
4. `describe_table` - 表结构详情
5. `generate_table_doc` - 生成表文档
6. `generate_database_overview` - Schema概览
7. `execute_query` - 执行SQL语句
8. `list_schemas` - 列出可用Schema

#### 配置环境变量
- **必需**: `ORACLE_HOST`, `ORACLE_PORT`, `ORACLE_USERNAME`, `ORACLE_PASSWORD`, `ORACLE_SERVICE_NAME`或`ORACLE_SID`
- **可选**: `ORACLE_SECURITY_MODE`, `ORACLE_ALLOWED_SCHEMAS`, `ORACLE_CONNECT_TIMEOUT`, `ORACLE_QUERY_TIMEOUT`, `ORACLE_MAX_RESULT_ROWS`, `ORACLE_ENABLE_QUERY_LOG`, `ORACLE_ENCODING`

#### 文件结构
```
oracle-mcp/
├── main.py                    # MCP服务器主程序
├── config.py                  # 配置管理模块
├── database.py                # 数据库操作模块
├── document_generator.py      # 文档生成器
├── requirements.txt           # Python依赖
├── README.md                  # 项目文档
├── LICENSE                    # MIT许可证
├── CHANGELOG.md              # 变更日志
├── CONTRIBUTING.md           # 贡献指南
├── Dockerfile                # 容器化支持
├── .gitignore               # Git忽略文件
└── cursor-config-example.json # Cursor配置示例
```

### 🔒 安全特性
- **只读模式**: 生产环境推荐，仅允许查询操作
- **限制写入**: 开发环境适用，禁止危险操作
- **完全访问**: 管理环境使用，需谨慎配置
- **SQL注入防护**: 参数化查询和输入验证
- **权限验证**: 基于Oracle用户权限的访问控制

### 🏛️ Oracle专项支持
- **DSN构建**: 智能构建Oracle连接字符串
- **LOB处理**: 自动处理BLOB/CLOB大对象
- **字符集**: 支持多种Oracle字符集
- **会话管理**: 优化的会话配置和管理

### 📦 部署方式
- **直接运行**: Python环境直接执行
- **容器化**: Docker支持，包含Oracle Client
- **Cursor集成**: MCP协议无缝集成

---

## 版本说明

### 版本号格式
采用语义化版本 `MAJOR.MINOR.PATCH`：
- **MAJOR**: 不兼容的API变更
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修复

### 标签说明
- 🎉 首次发布
- ✨ 新增功能  
- 🐛 错误修复
- 📝 文档更新
- 🔧 配置变更
- ⚡ 性能优化
- 🔒 安全更新
- 💥 破坏性变更
- 🗑️ 移除功能
- 🏛️ Oracle特性 