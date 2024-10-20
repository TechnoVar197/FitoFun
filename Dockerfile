# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /code in the container
WORKDIR /code

# Copy the requirements file into the container at /code
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt,
# along with the necessary system packages for OpenCV and ffmpeg
RUN apt-get update -y && apt-get install -y \
    libgl1-mesa-glx \
    ffmpeg \
    libsm6 \
    libxext6 \
 && pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r /code/requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable to explicitly set Flask app
ENV FLASK_APP=app.py

# Run flask when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
