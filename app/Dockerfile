FROM python:3.11

WORKDIR /app
# Install dependencies from requirements
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Set log file path and expose HTTP port which is 80 in our case
ENV DATA_FILE=/data/timestamps.log
EXPOSE 80

# Start API server on port 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
