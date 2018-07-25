FROM python:3.6.6-slim-stretch

WORKDIR /app

ADD . /app

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt \
&& /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo 'Asia/Shanghai' >/etc/timezone 

EXPOSE 5123

ENV NAME World

CMD ["bash", "run.sh"]
