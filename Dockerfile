# 使用官方Python基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖（包括构建工具）
RUN apt-get update && apt-get install -y \
    # 构建工具（用于编译cx_Oracle）
    gcc \
    g++ \
    build-essential \
    python3-dev \
    # Oracle Instant Client依赖
    wget \
    unzip \
    libaio1 \
    # 清理缓存
    && rm -rf /var/lib/apt/lists/*

# 下载并安装Oracle Instant Client
RUN mkdir -p /opt/oracle && \
    cd /opt/oracle && \
    wget https://download.oracle.com/otn_software/linux/instantclient/2113000/instantclient-basiclite-linux.x64-21.13.0.0.0dbru.zip && \
    unzip instantclient-basiclite-linux.x64-21.13.0.0.0dbru.zip && \
    rm instantclient-basiclite-linux.x64-21.13.0.0.0dbru.zip && \
    echo /opt/oracle/instantclient_21_13 > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig

# 设置Oracle环境变量
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_21_13:$LD_LIBRARY_PATH
ENV PATH=/opt/oracle/instantclient_21_13:$PATH

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖（包括编译cx_Oracle）
RUN pip install --no-cache-dir -r requirements.txt

# 安装完成后可以清理构建工具（可选，但会增加镜像层）
# RUN apt-get remove -y gcc g++ build-essential python3-dev && apt-get autoremove -y

# 复制项目文件
COPY . .

# 创建docs目录
RUN mkdir -p docs

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# 暴露端口（如果需要）
# EXPOSE 8000

# 设置默认命令
CMD ["python", "main.py"]

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "from database import get_db_instance; db = get_db_instance(); exit(0 if db.test_connection() else 1)"

# 标签
LABEL maintainer="qyue"
LABEL version="1.0.0"
LABEL description="Oracle数据库MCP服务" 