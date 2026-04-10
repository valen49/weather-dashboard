FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' appuser

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY run.py .

# Switch to non-root user
USER appuser

# Document which port the app listens on
EXPOSE 5000

# Run the application
CMD ["python", "run.py"]