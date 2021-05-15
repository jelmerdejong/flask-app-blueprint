FROM python:3.7.10-slim
COPY requirements.txt /tmp
RUN pip install --upgrade pip 
RUN pip install -r /tmp/requirements.txt && \
	rm /tmp/requirements.txt    
COPY . /app
WORKDIR /app
RUN ls -al
CMD ["python3","main.py"]