# Use official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Use environment variables from the .env file (handled via docker-compose)
CMD ["tail", "-f", "/dev/null"]

