# Use a lightweight Python 3.12 image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy only requirements first to leverage Docker caching
COPY requirements.txt .

# Install dependencies without cache to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port that FastAPI runs on
EXPOSE 8000

# Define the start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
