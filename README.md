# Stock Trend Prediction Model

## Project Overview

This project focuses on building and deploying a web application that predicts stock price trends using a machine learning model. The application combines data science, web development, containerization, and cloud deployment, resulting in a scalable and automated stock prediction system.

## Project Highlights
- ** Model development:** Trained model on XGBoost algorithm to capture complex patterns form data and saved the model for later uses.
- **Backend Integration:** Utilized Flask to power the backend, handling user requests, processing data, and predicting stock trends, with an HTML frontend for user interaction.
- **Containerization:** Dockerized the entire project, enabling seamless deployment across environments. The Docker image was pushed to Docker Hub for easy access.
- **AWS Deployment:** Deployed the project on AWS EC2 with Kubernetes for scalable and efficient hosting.
- **CI/CD Pipeline:** Set up Jenkins to automate the continuous integration and delivery process. Changes pushed to the GitHub repository automatically trigger Docker builds, push updates to Docker Hub, and deploy to the Kubernetes cluster on AWS EC2.

## Technologies Used

- Python
- Flask
- HTML, CSS
- Docker
- Kubernetes
- Jenkins
- GitHub
- AWS EC2

## Data Preprocessing

The project uses historical stock data for trend prediction. Data preprocessing steps include handling missing values, feature scaling, feature engineering and splitting data into training and test sets.

## Model Training

The machine learning model is trained using libraries like Pandas, NumPy, and Scikit-learn. The model is designed to predict stock price movements based on historical data and is integrated into the web application.

## Backend Development

The backend is powered by Flask. The `app.py` file contains the Flask application code, which handles incoming requests, processes stock data, and delivers predictions. The frontend HTML templates are stored in the `templates/` directory.

## Containerization and Deployment

- **Dockerization:** The project is containerized using Docker. The Docker image is built and pushed to Docker Hub for easy deployment.
- **AWS EC2 Deployment with Kubernetes:**
    - A Kubernetes cluster is created on AWS EC2 to manage the deployment and scaling of the application.
- **CI/CD Pipeline with Jenkins:**
    - Jenkins is used to automate the CI/CD pipeline. It fetches the latest changes from GitHub, builds new Docker images, pushes them to Docker Hub, and deploys them to the Kubernetes cluster on AWS.

## Continuous Integration & Deployment

- **Jenkins Pipeline Setup:**
    - Configured Jenkins to monitor changes in the GitHub repository.
    - Automatic Docker builds and image pushes to Docker Hub upon each commit.
    - Deployment to the Kubernetes cluster on AWS for continuous delivery.

## Conclusion

This project demonstrates the integration of machine learning, web development, containerization, and cloud-based deployment. The automated CI/CD pipeline with Jenkins, Docker, and Kubernetes ensures seamless updates and scalable deployment of the stock trend prediction application.
