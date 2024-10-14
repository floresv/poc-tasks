# Use the official Python image
FROM python:3.9-bullseye

# Install curl to download Node.js and other dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip

# Install Node.js (version 18)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Install AWS CLI using pip
RUN pip install --no-cache-dir awscli

# Install AWS CDK globally using npm
RUN npm install -g aws-cdk

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install project-specific Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install python-dotenv to load .env files
RUN pip install --no-cache-dir python-dotenv

# Set the default entry point to allow bash access
ENTRYPOINT ["/bin/bash"]
