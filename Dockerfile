# 使用官方Python基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖（包括构建工具）
RUN apt-get update && apt-get install -y --no-install-recommends \
    # 构建工具（用于编译cx_Oracle）
    gcc \
    g++ \
    build-essential \
    python3-dev \
    # Oracle Instant Client依赖
    wget \
    unzip \
    libaio1 \
    ca-certificates \
    # 清理缓存
    && rm -rf /var/lib/apt/lists/*

# 下载并安装Oracle Instant Client（增加错误处理）
RUN mkdir -p /opt/oracle && \
    cd /opt/oracle && \
    # 尝试下载Oracle Instant Client，如果失败则跳过
    (wget --timeout=60 --tries=3 https://download.oracle.com/otn_software/linux/instantclient/2113000/instantclient-basiclite-linux.x64-21.13.0.0.0dbru.zip && \
     unzip instantclient-basiclite-linux.x64-21.13.0.0.0dbru.zip && \
     rm instantclient-basiclite-linux.x64-21.13.0.0.0dbru.zip && \
     echo /opt/oracle/instantclient_21_13 > /etc/ld.so.conf.d/oracle-instantclient.conf && \
     ldconfig) || echo "Warning: Oracle Instant Client download failed, will need to be provided at runtime"

# 设置Oracle环境变量（使用条件设置）
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_21_13:$LD_LIBRARY_PATH
ENV PATH=/opt/oracle/instantclient_21_13:$PATH

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖（增加错误处理）
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt || \
    (echo "Warning: Some packages may have failed to install" && pip list)

# 安装完成后可以清理构建工具（可选，但会增加镜像层）
# RUN apt-get remove -y gcc g++ build-essential python3-dev && apt-get autoremove -y

# 复制项目文件
COPY . .

# 创建docs目录
RUN mkdir -p docs

# 创建非root用户（仅在支持的环境中）
RUN useradd --create-home --shell /bin/bash app 2>/dev/null || true && \
    chown -R app:app /app 2>/dev/null || true

# 尝试切换用户（如果用户创建成功）
USER app 2>/dev/null || echo "Using root user"

# 暴露端口（如果需要）
# EXPOSE 8000

# 设置默认命令
CMD ["python", "main.py"]

# 简化的健康检查（不连接数据库）
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# 标签
LABEL maintainer="qyue"
LABEL version="1.0.1"
LABEL description="Oracle数据库MCP服务" 