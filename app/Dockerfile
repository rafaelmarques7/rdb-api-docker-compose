FROM python:3.7-alpine

# Port for docker-compose
EXPOSE 5000

# Create working dir
WORKDIR /app

# Copy target files
COPY app.py /app 
COPY requirements.txt /app

# Install dependencies
RUN pip install -r requirements.txt 

# Run app 
CMD ["python", "app.py"]
