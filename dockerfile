FROM python:3.13-alpine

# Instala herramientas necesarias para compilar extensiones C
RUN apk add --no-cache build-base gcc musl-dev libffi-dev libc-dev

WORKDIR /app

# Instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
