crond
crontab /home/spider/scripts/rqkscron
export LANG=en_US.utf-8
export LC_ALL=en_US.utf-8
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
python3 -m pip install --upgrade pip
pip3 install -r /home/spider/requirements.txt -i https://pypi.douban.com/simple
cd /home/spider/
uvicorn app.main:app --host 0.0.0.0