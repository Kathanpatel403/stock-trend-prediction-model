pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the repository...'
                checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-credentials', url: 'https://github.com/Kathanpatel403/stock-trend-prediction-model.git']])
                echo 'Cloned repository successfully!'
            }
        }
        stage('Build Docker Image') {
            steps {
                echo 'Building new Docker image...'
                sh 'docker build -t stock-app .'
                echo 'Docker image built successfully!'
            }
        }
        stage('Stop running containers') {
            steps {
                echo 'Stopping any running Docker containers...'
                sh '''
                    running_containers=$(docker ps -q)
                    if [ -n "$running_containers" ]; then
                        docker stop $running_containers
                        echo "Stopped running containers: $running_containers"
                    else
                        echo "No running containers to stop."
                    fi
                '''
            }
        }
        stage('Run Docker Image') {
            steps {
                echo 'Running new Docker container...'
                sh 'docker run -d -p 80:5000 stock-app'
                echo 'Docker container started successfully!'
            }
        }
    }

    post {
        always {
            // Clean up workspace after build
            cleanWs()
        }
    }
}
