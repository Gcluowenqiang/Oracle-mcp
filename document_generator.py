"""
Oracle数据库文档生成器
支持Markdown、JSON、SQL等多种格式的数据库文档生成

Copyright (c) 2025 qyue
Licensed under the MIT License.
See LICENSE file in the project root for full license information.
"""
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from jinja2 import Template
from tabulate import tabulate

from database import get_db_instance


class OracleDocumentGenerator:
    """Oracle数据库文档生成器"""
    
    def __init__(self):
        self.db = get_db_instance()
        self.generation_time = datetime.now()
    
    def generate_table_doc(self, table_name: str, schema: str = None, format: str = "markdown") -> str:
        """生成单个表的文档"""
        try:
            # 获取表的基本信息
            tables = self.db.get_all_tables(schema)
            table_info = next((t for t in tables if t['tablename'] == table_name.upper()), None)
            
            if not table_info:
                raise ValueError(f"表 '{table_name}' 在Schema '{schema or self.db.config.username}' 中不存在")
            
            # 获取表结构
            columns = self.db.get_table_structure(table_name, schema)
            
            # 获取索引信息
            indexes = self.db.get_table_indexes(table_name, schema)
            
            # 获取约束信息
            constraints = self.db.get_table_constraints(table_name, schema)
            
            # 根据格式生成文档
            if format.lower() == "markdown":
                return self._generate_table_markdown(table_info, columns, indexes, constraints)
            elif format.lower() == "json":
                return self._generate_table_json(table_info, columns, indexes, constraints)
            elif format.lower() == "sql":
                return self._generate_table_sql(table_info, columns, indexes, constraints)
            else:
                raise ValueError(f"不支持的格式: {format}")
                
        except Exception as e:
            raise Exception(f"生成表文档失败: {e}")
    
    def generate_database_overview(self, schema: str = None) -> str:
        """生成数据库Schema概览文档（Markdown格式）"""
        try:
            if schema is None:
                schema = self.db.config.username.upper()
            
            # 获取所有表
            tables = self.db.get_all_tables(schema)
            
            # 生成概览文档
            doc = self._generate_schema_overview_markdown(schema, tables)
            
            return doc
            
        except Exception as e:
            raise Exception(f"生成Schema概览失败: {e}")
    
    def _generate_table_markdown(self, table_info: Dict, columns: List[Dict], 
                                indexes: List[Dict], constraints: List[Dict]) -> str:
        """生成表的Markdown文档"""
        template_str = """
# 表文档: {{ table_info.tablename }}

## 基本信息
- **表名**: {{ table_info.tablename }}
- **Schema**: {{ table_info.schemaname }}
- **类型**: {{ table_info.tabletype }}
- **预估行数**: {{ table_info.row_count or 0 }}
- **表注释**: {{ table_info.table_comment or '无' }}

## 字段结构
{{ columns_table }}

## 索引信息
{% if indexes %}
{{ indexes_table }}
{% else %}
*该表没有索引（除了主键）*
{% endif %}

## 约束信息
{% if constraints %}
{{ constraints_table }}
{% else %}
*该表没有约束*
{% endif %}

---
*文档生成时间: {{ generation_time }}*
*文档生成器: Oracle MCP Service*
        """.strip()
        
        template = Template(template_str)
        
        # 生成字段表格
        columns_data = []
        for col in columns:
            pk_indicator = "🔑" if col.get('is_primary_key') == 'YES' else ""
            null_indicator = "❌" if col.get('is_nullable') == 'NO' else "✅"
            
            # 构建数据类型字符串
            data_type = col['data_type']
            if col.get('character_maximum_length') and col['data_type'] in ('VARCHAR2', 'CHAR', 'NVARCHAR2', 'NCHAR'):
                data_type += f"({col['character_maximum_length']})"
            elif col.get('numeric_precision') and col.get('numeric_scale') is not None:
                data_type += f"({col['numeric_precision']},{col['numeric_scale']})"
            elif col.get('numeric_precision'):
                data_type += f"({col['numeric_precision']})"
            
            columns_data.append([
                pk_indicator,
                col['column_name'],
                data_type,
                null_indicator,
                str(col.get('column_default', ''))[:30] + ('...' if len(str(col.get('column_default', ''))) > 30 else ''),
                col.get('column_comment', '')
            ])
        
        columns_table = tabulate(
            columns_data,
            headers=["主键", "字段名", "数据类型", "允许NULL", "默认值", "注释"],
            tablefmt="pipe"
        )
        
        # 生成索引表格
        indexes_table = ""
        if indexes:
            indexes_data = []
            for idx in indexes:
                unique_indicator = "✅" if idx.get('is_unique') == 'YES' else "❌"
                indexes_data.append([
                    idx['indexname'],
                    unique_indicator,
                    idx.get('index_columns', '')
                ])
            
            indexes_table = tabulate(
                indexes_data,
                headers=["索引名", "唯一", "索引字段"],
                tablefmt="pipe"
            )
        
        # 生成约束表格
        constraints_table = ""
        if constraints:
            constraints_data = []
            for constraint in constraints:
                constraints_data.append([
                    constraint['constraint_name'],
                    constraint['constraint_type'],
                    constraint.get('column_name', ''),
                    constraint.get('foreign_key_references', '')
                ])
            
            constraints_table = tabulate(
                constraints_data,
                headers=["约束名", "约束类型", "字段", "外键引用"],
                tablefmt="pipe"
            )
        
        return template.render(
            table_info=table_info,
            columns_table=columns_table,
            indexes_table=indexes_table,
            constraints_table=constraints_table,
            indexes=indexes,
            constraints=constraints,
            generation_time=self.generation_time.strftime("%Y-%m-%d %H:%M:%S")
        )
    
    def _generate_table_json(self, table_info: Dict, columns: List[Dict], 
                           indexes: List[Dict], constraints: List[Dict]) -> str:
        """生成表的JSON文档"""
        doc = {
            "table_info": table_info,
            "columns": columns,
            "indexes": indexes,
            "constraints": constraints,
            "metadata": {
                "generation_time": self.generation_time.isoformat(),
                "generator": "Oracle MCP Service",
                "database_type": "Oracle"
            }
        }
        return json.dumps(doc, indent=2, ensure_ascii=False, default=str)
    
    def _generate_table_sql(self, table_info: Dict, columns: List[Dict], 
                          indexes: List[Dict], constraints: List[Dict]) -> str:
        """生成表的SQL创建语句"""
        sql_parts = []
        
        # 表创建语句
        sql_parts.append(f"-- 表: {table_info['tablename']}")
        sql_parts.append(f"-- Schema: {table_info['schemaname']}")
        sql_parts.append(f"-- 生成时间: {self.generation_time.strftime('%Y-%m-%d %H:%M:%S')}")
        sql_parts.append("")
        
        # CREATE TABLE 语句
        create_sql = f"CREATE TABLE {table_info['schemaname']}.{table_info['tablename']} ("
        sql_parts.append(create_sql)
        
        # 字段定义
        column_defs = []
        primary_keys = []
        
        for col in columns:
            # 构建字段定义
            col_def = f"  {col['column_name']} {col['data_type']}"
            
            # 添加长度/精度
            if col.get('character_maximum_length') and col['data_type'] in ('VARCHAR2', 'CHAR', 'NVARCHAR2', 'NCHAR'):
                col_def += f"({col['character_maximum_length']})"
            elif col.get('numeric_precision') and col.get('numeric_scale') is not None:
                col_def += f"({col['numeric_precision']},{col['numeric_scale']})"
            elif col.get('numeric_precision'):
                col_def += f"({col['numeric_precision']})"
            
            # 添加NOT NULL
            if col.get('is_nullable') == 'NO':
                col_def += " NOT NULL"
            
            # 添加默认值
            if col.get('column_default') is not None:
                col_def += f" DEFAULT {col['column_default']}"
            
            column_defs.append(col_def)
            
            # 收集主键
            if col.get('is_primary_key') == 'YES':
                primary_keys.append(col['column_name'])
        
        # 添加主键约束
        if primary_keys:
            column_defs.append(f"  CONSTRAINT PK_{table_info['tablename']} PRIMARY KEY ({', '.join(primary_keys)})")
        
        sql_parts.extend([def + "," for def in column_defs[:-1]])
        sql_parts.append(column_defs[-1])
        sql_parts.append(");")
        sql_parts.append("")
        
        # 添加表注释
        if table_info.get('table_comment'):
            sql_parts.append(f"COMMENT ON TABLE {table_info['schemaname']}.{table_info['tablename']} IS '{table_info['table_comment']}';")
            sql_parts.append("")
        
        # 添加字段注释
        for col in columns:
            if col.get('column_comment'):
                sql_parts.append(f"COMMENT ON COLUMN {table_info['schemaname']}.{table_info['tablename']}.{col['column_name']} IS '{col['column_comment']}';")
        
        if any(col.get('column_comment') for col in columns):
            sql_parts.append("")
        
        # 添加索引创建语句
        if indexes:
            sql_parts.append("-- 索引")
            for idx in indexes:
                if idx.get('index_columns'):
                    unique_str = "UNIQUE " if idx.get('is_unique') == 'YES' else ""
                    sql_parts.append(f"CREATE {unique_str}INDEX {idx['indexname']} ON {table_info['schemaname']}.{table_info['tablename']} ({idx['index_columns']});")
            sql_parts.append("")
        
        return "\n".join(sql_parts)
    
    def _generate_schema_overview_markdown(self, schema: str, tables: List[Dict]) -> str:
        """生成Schema概览的Markdown文档"""
        template_str = """
# Oracle数据库Schema概览: {{ schema }}

## 基本信息
- **Schema名**: {{ schema }}
- **表数量**: {{ tables|length }}
- **文档生成时间**: {{ generation_time }}

## Schema表列表
{{ tables_table }}

## 统计信息
- **总表数**: {{ tables|length }}
- **有数据表数**: {{ tables_with_data }}
- **空表数**: {{ empty_tables }}

## 表详细信息

{% for table in tables %}
### {{ loop.index }}. {{ table.tablename }}
- **类型**: {{ table.tabletype }}
- **预估行数**: {{ table.row_count or 0 }}
- **注释**: {{ table.table_comment or '无' }}

{% endfor %}

---
*文档生成时间: {{ generation_time }}*
*文档生成器: Oracle MCP Service*
*安全模式: {{ security_mode }}*
        """.strip()
        
        template = Template(template_str)
        
        # 生成表格数据
        tables_data = []
        tables_with_data = 0
        empty_tables = 0
        
        for i, table in enumerate(tables, 1):
            row_count = table.get('row_count', 0) or 0
            if row_count > 0:
                tables_with_data += 1
            else:
                empty_tables += 1
            
            tables_data.append([
                i,
                table['tablename'],
                table.get('tabletype', 'BASE TABLE'),
                row_count,
                (table.get('table_comment') or '')[:50] + ('...' if len(table.get('table_comment') or '') > 50 else '')
            ])
        
        tables_table = tabulate(
            tables_data,
            headers=["序号", "表名", "类型", "行数", "注释"],
            tablefmt="pipe"
        )
        
        return template.render(
            schema=schema,
            tables=tables,
            tables_table=tables_table,
            tables_with_data=tables_with_data,
            empty_tables=empty_tables,
            generation_time=self.generation_time.strftime("%Y-%m-%d %H:%M:%S"),
            security_mode=self.db.config.security_mode.value
        )
    
    def save_document(self, content: str, filename: str) -> str:
        """保存文档到文件"""
        try:
            # 确保docs目录存在
            docs_dir = "docs"
            if not os.path.exists(docs_dir):
                os.makedirs(docs_dir)
            
            # 生成完整文件路径
            filepath = os.path.join(docs_dir, filename)
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return os.path.abspath(filepath)
            
        except Exception as e:
            raise Exception(f"保存文档失败: {e}")


# 全局文档生成器实例
_doc_generator_instance = None

def get_doc_generator() -> OracleDocumentGenerator:
    """获取全局文档生成器实例"""
    global _doc_generator_instance
    if _doc_generator_instance is None:
        _doc_generator_instance = OracleDocumentGenerator()
    return _doc_generator_instance 