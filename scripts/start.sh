crond
crontab /home/fastapi-templates/scripts/rqkscron
export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
pip3 install -r /home/fastapi-templates/requirements.txt -i https://pypi.douban.com/simple
cd /home/spider/
# uvicorn app.main:app --host 0.0.0.0
/bin/bash