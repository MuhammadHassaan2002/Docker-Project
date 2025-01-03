![image](https://github.com/user-attachments/assets/3f117a3c-eb01-4575-a4fd-45a325561fa2)


My Python Flask App

This project demonstrates how to create a simple Flask application, containerize it using Docker, push the image to Docker Hub using GitHub Actions, and run it locally.

Prerequisites

- Docker installed on your local machine.
- Docker Hub account with repository access.
- GitHub repository with Actions enabled.

Steps

1. Set Up Your Flask Application

1. In the project directory, create a file named `app.py`:
    ```python
    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def hello():
        return "Hello World from Moin Tabani!"

    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000)
    ```

2. Create a Dockerfile

1. In the project directory, create a file named `Dockerfile`:
    ```dockerfile
    
    # Use the official Python image as the base image
    FROM python:3.9-slim

    # Set the working directory in the container
    WORKDIR /app

    # Copy the current directory contents into the container
    COPY . /app

    # Install any required dependencies from the requirements.txt file
    RUN pip install --no-cache-dir -r requirements.txt

    # Expose port 5000 for Flask app
    EXPOSE 5000

    # Set environment variables
    ENV FLASK_APP=app.py
    ENV FLASK_RUN_HOST=0.0.0.0
    
    # Command to run the application
    CMD ["flask", "run"]

    ```

3. Set Up GitHub Secrets for Docker Hub

1. Go to your GitHub repository on the GitHub website.
2. Navigate to Settings** > Secrets and variables > Actions > New repository secret.
3. Add the following secrets:
   - DOCKER_HUB_USERNAME: Your Docker Hub username.
   - DOCKER_HUB_ACCESS_TOKEN: Your Docker Hub access token (you can create one in your Docker Hub account settings for secure access).

4. Set Up GitHub Actions Workflow

1. In your GitHub repository, create a directory structure `.github/workflows/` and add a file named `docker-image.yml`:
    ```yaml
    
    name: Build and Deploy Docker Image
    
    on:
      push:
        branches:
          - main  # Trigger the workflow on pushes to the main branch
    
    jobs:
      build:
        runs-on: ubuntu-latest
        
        steps:
        - name: Checkout code
          uses: actions/checkout@v3
    
        - name: Log in to Docker Hub
          uses: docker/login-action@v2
          with:
            username: ${{ secrets.DOCKER_USERNAME }}  # Docker Hub username from GitHub secrets
            password: ${{ secrets.DOCKER_PASSWORD }}  # Docker Hub password from GitHub secrets
    
        - name: Build Docker image
          run: |
            docker build -t ${{ secrets.DOCKER_USERNAME }}/my-python-app:latest .
    
        - name: Push Docker image to Docker Hub
          run: |
            docker push ${{ secrets.DOCKER_USERNAME }}/my-python-app:latest
    
      deploy:
        runs-on: ubuntu-latest
        needs: build
        steps:
        - name: Log in to Docker Hub
          uses: docker/login-action@v2
          with:
            username: ${{ secrets.DOCKER_USERNAME }}
            password: ${{ secrets.DOCKER_PASSWORD }}
    
        - name: Pull and run Docker image
          run: |
            # Pull the image from Docker Hub
            docker pull ${{ secrets.DOCKER_USERNAME }}/my-python-app
            
            # Run the container on localhost on port 5000
            docker run -d --name my_local_container -p 5000:5000 ${{ secrets.DOCKER_USERNAME }}/my-python-app
    
        - name: Show running Docker containers
          run: docker ps -a

    ```

2. Commit and push these changes to trigger the GitHub Actions workflow. This workflow will:
   - Build the Docker image from your Dockerfile.
   - Push the built image to your Docker Hub repository.

5. Pull and Run the Docker Image Locally

After the GitHub Actions workflow has successfully built and pushed the image to Docker Hub:

1. Pull the image from Docker Hub to your local machine:
    ```bash
    docker pull your_dockerhub_username/my-python-app:latest
    ```

2. Run the container locally:
    ```bash
    docker run -p 5000:5000 --name my_local_container your_dockerhub_username/my-python-app:latest
    ```

3. Open a browser and visit `http://localhost:5000` to see the app running.

