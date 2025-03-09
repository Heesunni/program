# 1. Python 3.9 기반 컨테이너 사용
FROM python:3.9

WORKDIR /program
COPY . /program

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt
RUN python3 -m pip install --no-cache-dir uvicorn
RUN python3 -m pip install --no-cache-dir sqlalchemy


EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
