# SENTIRA PRO // Institutional Terminal Container
# Optimized for Python 3.12 + FinBERT Inference

FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

WORKDIR /app

# Install system-level dependencies for building specialized financial packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project core
COPY . .

# Create directory for model cache and output artifacts
RUN mkdir -p /root/.cache/huggingface outputs

# Expose the Streamlit instrument cluster port
EXPOSE 8501

# Healthcheck to ensure terminal is operational
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Entrypoint: Launch the Terminal Obsidian UI
CMD ["streamlit", "run", "dashboard/app.py"]
