# Dockerfile for weather_quake_dashboard project
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# System dependencies (geopandas & folium needs)
RUN apt-get update && apt-get install -y \
    build-essential \
    gdal-bin \
    python3-dev \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Streamlit run command
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]