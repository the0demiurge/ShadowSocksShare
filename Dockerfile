FROM python:latest
# 把当前路径下的文件都拷贝到镜像中的 /src 目录
COPY . /src
# 安装需要的包
RUN cd /src; pip install -r requirements.txt
# 暴露 5001 端口
EXPOSE 5001
#运行脚本
ENTRYPOINT python ./.travis-test.py
