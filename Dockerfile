FROM python:3.9-slim
ENV PYTHONDONTWRITWBYTECODE=1
ENV PYTHONNUMBUFFERED=1
WORKDIR /app
COPY . /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","app.py"]
