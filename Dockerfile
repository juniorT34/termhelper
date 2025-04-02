FROM python:3.12-alpine3.19

LABEL org.opencontainers.image.source="docker.io/junior039/cmdhelper"
LABEL org.opencontainers.image.description="Command Helper CLI Tool"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY cmdhelper/ ./cmdhelper/
COPY setup.py .

# Install the package
RUN pip install -e .

# Create a non-root user
RUN adduser -D cmdhelper
USER cmdhelper

# Set environment variables
ENV FLASK_APP=cmdhelper.web.app
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

ENTRYPOINT ["cmdhelper"]
CMD ["--help"]
