FROM python:3.9.6

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure alembic.ini is in the correct location
COPY alembic.ini .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]