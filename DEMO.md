# 平台一键 Demo 接入说明

这个仓库已经改造成平台可直接构建的 Docker Compose Demo。

在平台的 Demo 设置中填写：

- 运行模式：Docker Compose
- 入口服务：web
- 入口端口：80
- 分支名：courses

平台启动后只会把 `web` 服务暴露给试用者。`web` 服务负责展示前端页面，并把接口请求转发到内部的学院 A、学院 B、学院 C 和集成服务。

内部服务说明：

- `college-a`：学院 A 后端，端口 8000
- `college-b`：学院 B 后端，端口 8001
- `college-c`：学院 C 后端，端口 8002
- `integration-server`：集成服务，端口 8081
- `web`：前端入口和反向代理，端口 80

本地验证可以运行：

```bash
docker compose up --build
```

然后在同一个 Docker 网络内访问 `web:80`，或临时给 `web` 增加本机端口映射后用浏览器访问。
