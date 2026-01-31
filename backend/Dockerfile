# Dockerfile para Luz Backend con TensorFlow garantizado
FROM tensorflow/tensorflow:2.15.0-py3

LABEL maintainer="LUZ Team"
LABEL description="Backend de Luz - App de Bienestar con IA/ML completo"

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=UTC

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt requirements-ml.txt ./

# Instalar dependencias básicas
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Instalar dependencias ML (TensorFlow ya incluido en la imagen base)
RUN pip install -r requirements-ml.txt

# Copiar código del proyecto
COPY . .

# Crear directorio para base de datos
RUN mkdir -p /app/data

# Exponer puerto
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando por defecto
CMD ["python", "main.py"]

# Para desarrollo con auto-reload:
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]