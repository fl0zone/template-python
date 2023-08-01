# Usar una imagen base de Python
FROM python:3.8

# Establecer un directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos e instalar las dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto en el que se ejecuta la aplicación
EXPOSE 5000

# Ejecutar la aplicación
CMD ["python", "server.py"]
