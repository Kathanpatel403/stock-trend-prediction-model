// pipeline {
//     agent any

//     stages {
//         stage('Clone Repository') {
//             steps {
//                 echo 'Cloning the repository...'
//                 checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-credentials', url: 'https://github.com/Kathanpatel403/stock-trend-prediction-model.git']])
//                 echo 'Cloned repository successfully!'
//             }
//         }
//         stage('Build Docker Image') {
//             steps {
//                 echo 'Building new Docker image...'
//                 sh 'docker build -t stock-app .'
//                 echo 'Docker image built successfully!'
//             }
//         }
//         stage('Stop running containers') {
//             steps {
//                 echo 'Stopping any running Docker containers...'
//                 sh '''
//                     running_containers=$(docker ps -q)
//                     if [ -n "$running_containers" ]; then
//                         docker stop $running_containers
//                         echo "Stopped running containers: $running_containers"
//                     else
//                         echo "No running containers to stop."
//                     fi
//                 '''
//             }
//         }
//         stage('Run Docker Image') {
//             steps {
//                 echo 'Running new Docker container...'
//                 sh 'docker run -d -p 80:5000 stock-app'
//                 echo 'Docker container started successfully!'
//             }
//         }
//     }

//     post {
//         always {
//             // Clean up workspace after build
//             cleanWs()
//         }
//     }
// }


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
        stage('Tag and Push Docker Image to Docker Hub') {
            steps {
                script {
                    def dockerImage = "kathanpatel403/stock-trend-prediction-flask-app"
                    def tag = "latest"
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        sh "docker tag stock-app ${dockerImage}:${tag}"
                        sh "docker push ${dockerImage}:${tag}"
                    }
                    echo 'Docker image pushed to Docker Hub successfully!'
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes...'
                // Ensure you have `kubectl` configured on your Jenkins machine
                sh 'kubectl apply -f deployment.yaml'
                echo 'Deployment applied to Kubernetes!'
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
