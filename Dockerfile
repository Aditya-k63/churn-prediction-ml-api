FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable stdout logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Fix line endings on start.sh (in case saved on Windows)
RUN sed -i 's/\r//' start.sh && chmod +x start.sh

# Expose both ports
EXPOSE 8000
EXPOSE 8501

# Start both services
CMD ["sh", "start.sh"]