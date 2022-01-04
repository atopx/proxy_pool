FROM python:3.10-alpine

WORKDIR /app

# apk repository
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

# add code
COPY . .

# timezone
RUN apk add -U tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && apk del tzdata

# runtime environment
RUN apk add musl-dev gcc libxml2-dev libxslt-dev && \
    pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ && \
    apk del gcc musl-dev
