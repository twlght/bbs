# nginx-gunicorn-flask

FROM ubuntu:16.04

MAINTAINER twlght

RUN apt-get update
RUN apt-get install -y python3 python3-venv nginx supervisor zsh
RUN apt-get install -y python3-pip
RUN pip3 install setuptools
RUN pip3 install gunicorn

# Build folder
RUN mkdir -p /bbs/bbs_app

WORKDIR /bbs
# 在bbs文件夹下建立virtualenv(bbs-venv)
RUN python3 -m venv bbs-venv
RUN ls -la
# 进入虚拟环境
# bbs-venv 没有在环境变量中
# RUN source bbs-venv/bin/activate
RUN ["/bin/bash", "-c", "source bbs-venv/bin/activate"]

# only copy requirements.txt.  othors will be mounted by -v
# COPY bbs_app/requirements.txt /bbs/bbs_app/requirements.txt
# 安装python包
RUN ls -l /bbs/bbs_app/
RUN pip3 install -r /bbs/bbs_app/requirements.txt

# 设置 nginx
RUN rm /etc/nginx/sites-enabled/default
COPY bbs.nginx /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/bbs.nginx /etc/nginx/sites-enabled/bbs.nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# 配置 supervisor
RUN mkdir -p /var/log/supervisor
COPY bbs.conf /etc/supervisor/conf.d/supervisor.conf

# Start processes
CMD ["/usr/bin/supervisord"]