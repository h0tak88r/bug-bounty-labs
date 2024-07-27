FROM ubuntu:latest

# Install Python and pip
RUN apt-get update -y && apt-get install -y python3 python3-pip python3-venv

# Copy the application code
COPY . /ssrf-bug

# Set the working directory
WORKDIR /ssrf-bug

# Create a virtual environment
RUN python3 -m venv venv

# Activate the virtual environment and install dependencies
RUN /bin/bash -c "source venv/bin/activate && pip install -r requirements.txt"

# Command to run the application
CMD ["/bin/bash", "-c", "source venv/bin/activate && python app.py"]
