# Use the official Python runtime image
FROM python:3.11-slim
 
# Create the app directory
RUN mkdir /app /app/staticfiles
 
# Set the working directory inside the container
WORKDIR /app
 
# Set environment variables 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
# install system dependencies
RUN apt-get update && apt-get install -y netcat-traditional

# Upgrade pip
RUN pip install --upgrade pip 
 
# Copy the Django project  and install dependencies
COPY requirements.txt  /app/
 
# run this command to install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# COPY entrypoint.sh /app/
 
# Copy the Django project to the container
COPY . /app/
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
 
# Expose the Django port
EXPOSE 8000

ENTRYPOINT [ "/app/entrypoint.sh" ]
