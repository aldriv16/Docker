FROM python:3.11

WORKDIR /app

COPY requirements.txt .
<<<<<<< HEAD

RUN pip install --no-cache-dir -r requirements.txt
=======
RUN pip install -r requirements.txt
>>>>>>> 4b0bd6a80cea2db773ab1ab0adb3bd2a13ad94d3

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
