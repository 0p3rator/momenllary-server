FROM python:2.7.14-slim

WORKDIR /app

ADD . /app

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt \
&& pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn \
&& pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gevent \
&& /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo 'Asia/Shanghai' >/etc/timezone 

EXPOSE 5123

ENV NAME World

CMD ["bash", "run.sh"]
