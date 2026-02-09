FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose the FASTAPI port
EXPOSE 8000

# Run the FASTAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
