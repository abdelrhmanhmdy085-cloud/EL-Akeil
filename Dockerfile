FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variables
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0
ENV SECRET_KEY=railway_production_secret_key

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "-c", "import sys; sys.path.insert(0, 'src'); from backend.app import create_app; from backend.socket_instance import socketio; from backend import sockets; app = create_app(); socketio.init_app(app, cors_allowed_origins='*'); socketio.run(app, debug=False, port=5000, host='0.0.0.0')"]
