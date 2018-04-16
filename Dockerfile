# nginx-gunicorn-flask

FROM ubuntu:16.04

MAINTAINER twlght

RUN apt-get update
RUN apt-get install -y python3.5
RUN apt-get install -y python3-venv
RUN apt-get install -y nginx
RUN apt-get install -y supervisor
RUN apt-get install -y python3-pip
RUN apt-get install -y vim
RUN pip3 install setuptools
RUN pip3 install gunicorn
# RUN pip3 install supervisor
# Build folder
RUN mkdir -p /bbs/bbs_app

WORKDIR /bbs
# 在bbs文件夹下建立virtualenv(bbs-venv)
# RUN python3 -m venv bbs-venv
# RUN ls -la
# 进入虚拟环境
# bbs-venv 没有在环境变量中
# RUN source bbs-venv/bin/activate
# RUN ["/bin/bash", "-c", "source bbs-venv/bin/activate"]

# only copy requirements.txt.  othors will be mounted by -v
COPY bbs_app /bbs/bbs_app
# 安装python包
RUN ls -l /bbs/bbs_app/
RUN pip3 install -r /bbs/bbs_app/requirements.txt

# 设置 nginx
RUN rm /etc/nginx/sites-enabled/default
COPY bbs.nginx /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/bbs.nginx /etc/nginx/sites-enabled/bbs.nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# 配置 supervisor
# 通过supervisord管理启动和配置supervisor本身，
# 通过supervisorctl来管理使用supervisor启动和管理的自身的一些应用，如我们的这里的app.py
RUN mkdir -p /var/log/supervisor
RUN echo_supervisord_conf > /etc/supervisord.conf
COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf
RUN echo "/bbs/bbs_app" > /usr/local/lib/python3.5/bbs.pth

# Start processes
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]