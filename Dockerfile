# Usar una imagen base de Python
FROM python:3.10-slim

# Setear el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requerimientos
COPY requirements.txt .

# Instalar las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY . .

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
