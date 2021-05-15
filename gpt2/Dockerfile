FROM python:3.7.10-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN ls -al
CMD ["python3","main.py"]