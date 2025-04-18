# Todo App with Django and MongoDB

This is a Todo Application built using Django, MongoDB, and Docker. The app allows users to manage tasks and subtasks through a RESTful API. It also includes a CI/CD pipeline using GitHub Actions to build and deploy the Docker image to Docker Hub.

---

## Features

- Task Management: Create, update, and delete tasks.
- Subtask Support: Add subtasks to each task and mark them as completed.
- RESTful API: Built using Django REST Framework and MongoEngine.
- Dockerized: The app is containerized using Docker for easy deployment.
- CI/CD Pipeline: Automated builds and deployments to Docker Hub via GitHub Actions.

---

## Technologies Used

- Backend Framework: Django  
- Database: MongoDB (via MongoEngine)  
- API Framework: Django REST Framework  
- Containerization: Docker  
- CI/CD: GitHub Actions  
- Container Registry: Docker Hub  

---

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker: https://www.docker.com/  
- Docker Compose: https://docs.docker.com/compose/  
- Python 3.9+ (optional, for local development): https://www.python.org/  

---

### Installation

1. Clone the Repository  
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```
2. Build and Run with Docker  
   Build and start the containers:
   ```bash
   docker-compose up --build
   ```
   The app will be available at `http://localhost:8000`.

3. Access the API  
   Use tools like Postman or `curl` to interact with the API endpoints.

---

### Running Locally (Without Docker)

1. Install Dependencies  
   ```bash
   pip install -r requirements.txt
   ```

2. Run the App  
   Since this app uses MongoDB, ensure your database connection is properly configured in `settings.py`.

3. Start the Development Server  
   ```bash
   python manage.py runserver
   ```

4. Access the API  
   The app will be available at `http://localhost:8000`.

---

## API Endpoints

The app exposes the following RESTful API endpoints:

| Method | Endpoint             | Description                   |
|--------|----------------------|-------------------------------|
| GET    | /api/tasks/          | List all tasks                |
| POST   | /api/tasks/          | Create a new task             |
| GET    | /api/tasks/:id/      | Retrieve details of a task    |
| PUT    | /api/tasks/:id/      | Update a task                 |
| DELETE | /api/tasks/:id/      | Delete a task                 |
| GET    | /api/subtasks/       | List all subtasks             |
| POST   | /api/subtasks/       | Create a new subtask          |
| GET    | /api/subtasks/:id/   | Retrieve details of a subtask |
| PUT    | /api/subtasks/:id/   | Update a subtask              |
| DELETE | /api/subtasks/:id/   | Delete a subtask              |

---

## Deployment

### Using Docker Hub

1. Pull the latest Docker image from Docker Hub:
   ```bash
   docker pull <your-dockerhub-username>/<your-repo-name>:latest
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 <your-dockerhub-username>/<your-repo-name>:latest
   ```

3. Access the app at `http://localhost:8000`.

---

### Using GitHub Actions

The app is automatically built and pushed to Docker Hub whenever changes are pushed to the `main` branch. To set up your own CI/CD pipeline:

1. Fork this repository.  
2. Add your Docker Hub credentials (`DOCKER_HUB_USERNAME` and `DOCKER_HUB_TOKEN`) as GitHub Secrets.  
3. Push changes to the `main` branch to trigger the workflow.

---
