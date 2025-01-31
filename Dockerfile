# Use Python 3.8 as the base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Set PYTHONPATH to include the root directory
ENV PYTHONPATH=/app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "core/server.py"]