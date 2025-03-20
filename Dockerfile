# Use official Python image as base
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the required files to install dependencies
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code to the container
COPY . .


# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
