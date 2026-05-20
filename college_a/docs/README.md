# College A Backend README

## 0. SQL Server 参数要求

本服务在 `sqlserver` 模式下依赖 SQL Server 配置。相关参数统一写在仓库根目录 `.env` 中，不要写死在代码里。

### 0.1 SQL Server 版本要求

推荐要求：

- SQL Server 2019 及以上版本
- 推荐使用 SQL Server Express / Developer / Standard 均可
- 需要安装 `ODBC Driver 18 for SQL Server`

当前已验证环境：

- `Microsoft SQL Server 2025 (RTM)`
- 实例名：`SQLEXPRESS`
- ODBC 驱动：`ODBC Driver 18 for SQL Server`

说明：

- 当前代码使用了 `datetime2`、外键、唯一约束、`TOP 1` 等常规 SQL Server 能力，SQL Server 2019 及以上一般都可以正常支持。
- 如果版本过旧，虽然不一定完全不能运行，但不建议作为本项目联调环境。
- 如果本机没有安装 `ODBC Driver 18 for SQL Server`，即使数据库实例正常，也可能无法通过 `pyodbc` 连接。

当前需要重点确认这些参数：

```env
COLLEGE_A_STORAGE=sqlserver

MSSQL_SERVER=localhost\SQLEXPRESS
MSSQL_HOST=
MSSQL_PORT=1433
MSSQL_DATABASE=CollegeA_DB
MSSQL_DRIVER=ODBC Driver 18 for SQL Server
MSSQL_TRUSTED_CONNECTION=true
MSSQL_USER=collegea_user
MSSQL_PASSWORD=CollegeA@123

COLLEGE_A_TEST_DATABASE=CollegeA_DB
RUN_SQLSERVER_TESTS=1
```

说明：

- `COLLEGE_A_STORAGE=sqlserver` 表示启用真实数据库模式。
- `MSSQL_SERVER` 推荐直接使用实例名，例如 `localhost\SQLEXPRESS`。
- 如果已经配置 `MSSQL_SERVER`，通常可以把 `MSSQL_HOST` 留空。
- 如果不用实例名，也可以改用 `MSSQL_HOST + MSSQL_PORT` 方式连接。
- `MSSQL_DATABASE` 是学院 A 当前使用的数据库名，这里是 `CollegeA_DB`。
- `MSSQL_DRIVER` 当前建议使用 `ODBC Driver 18 for SQL Server`。
- `MSSQL_TRUSTED_CONNECTION=true` 表示使用 Windows 身份认证。
- 如果你要改成 SQL 账号密码认证，需要把 `MSSQL_TRUSTED_CONNECTION=false`，再填写 `MSSQL_USER` 和 `MSSQL_PASSWORD`。
- `COLLEGE_A_TEST_DATABASE` 是真实写库测试使用的数据库，当前也指向 `CollegeA_DB`。
- `RUN_SQLSERVER_TESTS=1` 表示允许运行真实 SQL Server 测试。

如果缺少以下任一项，服务在 `sqlserver` 模式下可能无法启动：

- `MSSQL_SERVER` 或 `MSSQL_HOST`
- `MSSQL_DATABASE`

---

## 1. 项目说明

本目录是学院 A 后端服务实现。

当前版本基于 `Python + FastAPI`，支持两种运行模式：

- `mock`：使用内存数据，适合本地快速调试
- `sqlserver`：连接真实 SQL Server，适合联调和真实写库验证

当前已实现：

- 登录接口
- 本院课程查询接口
- 学生信息查询接口
- 共享课程查询接口
- 选课接口
- 退选接口
- 集成服务器写回接口
- 集成服务器退选写回接口

---

## 2. 目录结构

```text
college_a/
  app/
    config.py
    integration.py
    main.py
    models.py
    repository.py
    sqlserver_repository.py
    xml_utils.py
  docs/
    README.md
  tests/
    test_app.py
    test_real_sqlserver.py
  requirements.txt
```

说明：

- `main.py`：FastAPI 路由入口
- `config.py`：读取根目录 `.env`
- `repository.py`：内存 mock 仓储
- `sqlserver_repository.py`：真实 SQL Server 仓储
- `integration.py`：mock 的集成服务器调用层
- `tests/test_app.py`：mock 测试
- `tests/test_real_sqlserver.py`：真实 SQL Server 测试
- `requirements.txt`：依赖清单

---

## 3. 环境准备

建议准备：

- Python 3.12
- SQL Server ODBC Driver 18
- 可用的 SQL Server 实例

依赖文件：

- [requirements.txt](/d:/All_of_mine/大学/学习/大三下/数据集成/作业三/college_a/requirements.txt)

安装命令：

```powershell
python -m pip install -r college_a/requirements.txt
```

---

## 4. 配置方式

所有运行配置统一放在仓库根目录 `.env` 中，不要硬编码到代码里。

示例文件：

- [.env.example](/d:/All_of_mine/大学/学习/大三下/数据集成/作业三/.env.example)

当前实现会在 `college_a/app/config.py` 中自动加载根目录 `.env`。

### 4.1 关键配置示例

```env
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
SECRET_KEY=changeme
LOG_LEVEL=INFO

COLLEGE_A_STORAGE=sqlserver
USE_MOCK_EXTERNALS=true
COLLEGE_ID=A
INTEGRATION_HOST=http://localhost:8081

RUN_SQLSERVER_TESTS=1

MSSQL_SERVER=localhost\SQLEXPRESS
MSSQL_HOST=
MSSQL_PORT=1433
MSSQL_DATABASE=CollegeA_DB
MSSQL_DRIVER=ODBC Driver 18 for SQL Server
MSSQL_TRUSTED_CONNECTION=true
MSSQL_USER=collegea_user
MSSQL_PASSWORD=CollegeA@123

COLLEGE_A_TEST_DATABASE=CollegeA_DB
```

### 4.2 配置项说明

- `COLLEGE_A_STORAGE`
  - `mock`：使用内存仓储
  - `sqlserver`：使用真实 SQL Server

- `USE_MOCK_EXTERNALS`
  - `true`：跨院共享课程和外部集成调用使用 mock

- `MSSQL_SERVER`
  - 推荐直接填实例名，例如 `localhost\SQLEXPRESS`

- `MSSQL_HOST + MSSQL_PORT`
  - 如果不使用实例名，可以用主机和端口组合

- `MSSQL_TRUSTED_CONNECTION`
  - `true`：Windows 身份认证
  - `false`：使用 `MSSQL_USER` / `MSSQL_PASSWORD`

- `RUN_SQLSERVER_TESTS`
  - `1`：允许运行真实 SQL Server 测试
  - `0`：跳过真实写库测试

---

## 5. 如何启动服务

### 5.1 mock 模式

先在 `.env` 中设置：

```env
COLLEGE_A_STORAGE=mock
```

启动命令：

```powershell
python -m uvicorn college_a.app.main:create_app --factory --host 0.0.0.0 --port 8000
```

### 5.2 SQL Server 模式

确认 `.env` 中已正确配置：

```env
COLLEGE_A_STORAGE=sqlserver
MSSQL_SERVER=localhost\SQLEXPRESS
MSSQL_DATABASE=CollegeA_DB
MSSQL_TRUSTED_CONNECTION=true
```

启动命令：

```powershell
python -m uvicorn college_a.app.main:create_app --factory --host 0.0.0.0 --port 8000
```

说明：

- 本项目使用 `--factory`
- 当前入口是 `create_app`

### 5.3 健康检查

```powershell
curl http://127.0.0.1:8000/health
```

预期返回：

```json
{"status":"ok"}
```

---

## 6. 接口清单

### 6.1 健康检查

- `GET /health`

### 6.2 登录

- `POST /api/v1/auth/login`

请求示例：

```xml
<LoginRequest>
  <username>a_student1</username>
  <password>123456</password>
</LoginRequest>
```

### 6.3 查询本院课程

- `GET /api/v1/courses`

### 6.4 查询学生信息

- `GET /api/v1/students/{student_id}`

示例：

- `GET /api/v1/students/S2024001`

### 6.5 查询共享课程

- `GET /api/v1/shared-courses`

可选参数：

- `collegeId`

示例：

- `GET /api/v1/shared-courses?collegeId=A`

### 6.6 发起选课

- `POST /api/v1/enrollments`

请求示例：

```xml
<EnrollmentRequest>
  <meta>
    <homeCollegeId>A</homeCollegeId>
    <targetCollegeId>B</targetCollegeId>
    <requestTime>2026-05-17 10:30:00</requestTime>
  </meta>
  <choices>
    <choice>
      <sid>S2024001</sid>
      <cid>B001</cid>
      <score>0</score>
    </choice>
  </choices>
</EnrollmentRequest>
```

说明：

- `targetCollegeId=A` 时，走本院本地选课
- `targetCollegeId!=A` 时，当前走 mock 集成服务器流程

### 6.7 发起退选

- `POST /api/v1/enrollments/{enrollmentId}/withdraw`

请求示例：

```xml
<WithdrawRequest>
  <enrollmentId>E202605200001</enrollmentId>
  <studentId>S2024001</studentId>
  <courseId>A001</courseId>
</WithdrawRequest>
```

### 6.8 选课写回接口

- `POST /internal/v1/enrollments/writeback`

请求示例：

```xml
<WritebackRequest>
  <meta>
    <sourceCollegeId>C</sourceCollegeId>
    <targetCollegeId>A</targetCollegeId>
    <status>ENROLLED</status>
  </meta>
  <choices>
    <choice>
      <sid>S2024001</sid>
      <cid>A001</cid>
      <score>95</score>
    </choice>
  </choices>
</WritebackRequest>
```

### 6.9 退选写回接口

- `POST /internal/v1/enrollments/withdraw`

请求示例：

```xml
<WithdrawWritebackRequest>
  <enrollmentId>E202605200001</enrollmentId>
  <studentId>S2024001</studentId>
  <courseId>A001</courseId>
</WithdrawWritebackRequest>
```

---

## 7. 如何测试

### 7.1 mock 测试

```powershell
python -m pytest college_a/tests/test_app.py -q
```

预期：

- `5 passed`

### 7.2 真实 SQL Server 测试

确认 `.env` 中：

```env
RUN_SQLSERVER_TESTS=1
COLLEGE_A_STORAGE=sqlserver
MSSQL_SERVER=localhost\SQLEXPRESS
MSSQL_DATABASE=CollegeA_DB
MSSQL_TRUSTED_CONNECTION=true
```

执行：

```powershell
python -m pytest college_a/tests/test_real_sqlserver.py -q
```

预期：

- `1 passed`

说明：

- 真实测试会写入 `Enrollment` 和 `EnrollmentLog`
- 然后执行退选，再验证状态变化

---

## 8. 推荐联调顺序

建议顺序：

1. 先用 `mock` 模式跑通健康检查和登录
2. 跑 `test_app.py`
3. 切到 `sqlserver` 模式
4. 跑 `test_real_sqlserver.py`
5. 再和集成服务器联调内部写回接口

---

## 9. 当前已验证内容

已经验证通过：

- mock 模式测试通过
- 真实 SQL Server 模式测试通过
- `.env` 配置可以驱动服务切换仓储模式

当前仍为 mock 或尚未实现：

- 真正的外部集成服务器 HTTP 调用
- 与学院 B / C 的真实联调
- 前端页面

---

## 10. 常见问题

### 10.1 服务启动报 `missing MSSQL_DATABASE in .env`

说明：

- 启用了 `sqlserver` 模式，但 `.env` 里没配 `MSSQL_DATABASE`

### 10.2 服务启动报 `missing MSSQL_SERVER or MSSQL_HOST in .env`

说明：

- `.env` 里没有提供 SQL Server 地址

### 10.3 SQL 登录失败

优先检查：

- `MSSQL_TRUSTED_CONNECTION` 是否配置正确
- SQL Server 实例是否允许 SQL 登录
- 数据库用户和登录用户映射是否正确

### 10.4 真实测试不执行

检查：

```env
RUN_SQLSERVER_TESTS=1
```

---

## 11. 后续建议

建议下一步优先做：

1. 把 `MockIntegrationGateway` 替换成真实集成服务器客户端
2. 给接口补统一鉴权
3. 增加更完整的错误码和日志
4. 增加面向前端的课程展示和选课查询接口
