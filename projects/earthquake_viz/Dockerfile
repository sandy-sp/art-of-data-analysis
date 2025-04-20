# Dockerfile for Earthquake Visualization Project
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for GeoPandas and Folium
RUN apt-get update && \
    apt-get install -y gcc g++ libgdal-dev gdal-bin && \
    apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]