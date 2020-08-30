# Use an official Python runtime as a parent image
FROM python:3.8.5-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

COPY install-packages.sh .
RUN ./install-packages.sh

# Run app.py when the container launches
CMD ["python", "threadtest.py"]
