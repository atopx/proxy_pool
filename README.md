# proxy_pool

基于 [github.com/jhao104/proxy_pool](https://github.com/jhao104/proxy_pool)构建

# services
> 数据存储: redis(hash)
 - app/crawler: 采集器[`定时采集`, `轮训探活`]
 - app/server: api服务

## 自定义代理验证函数
> vim app/core/validator.py +69

修改函数`custom_validator_example(proxy) -> bool`

# 使用
> 安装`docker`, `docker-compose`

1. 创建`docker-compose.yaml`文件

```yaml
version: '3.7'

services:
  proxy-crawler:
    image: "itmeng2018/proxy-app:v0.1.0"
    container_name: proxy-crawler
    links:
      - proxy-redis
    entrypoint: python crawler.py
    environment:
      - "DB_CONN=redis://@proxy-redis:6379/0"
      - "HTTP_URL=http://httpbin.org"
      - "HTTPS_URL=https://www.baidu.com"

  proxy-server:
    image: "itmeng2018/proxy-app:v0.1.0"
    container_name: proxy-server
    links:
      - proxy-redis
    entrypoint: python server.py
    environment:
      - "DB_CONN=redis://@proxy-redis:6379/0"
    ports:
      - "5000:5000"

  proxy-redis:
    image: "redis"
    container_name: proxy-redis
    ports:
      - "6379:6379"

```

2. 启动服务

```
docker-compose pull
docker-compose up -d
```

