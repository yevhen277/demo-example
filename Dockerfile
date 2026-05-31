FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UNIFOLDER_DEMO_WEB=true
ENV FLET_FORCE_WEB_SERVER=true
ENV FLET_SERVER_IP=0.0.0.0
ENV FLET_SERVER_PORT=8550
ENV UNIFOLDER_DEMO_ROOT=/app/demo-files

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/demo-files/课程作业/数据库课设 \
    /app/demo-files/课程作业/操作系统实验 \
    /app/demo-files/项目资料/UniFolder设计稿 \
    /app/demo-files/归档资料/大二下复习资料 \
    && printf "This is sample data for the UniFolder web demo.\n" > /app/demo-files/课程作业/数据库课设/README.txt \
    && printf "Container demo data only.\n" > /app/demo-files/项目资料/UniFolder设计稿/README.txt

EXPOSE 8550

CMD ["python", "main.py"]
