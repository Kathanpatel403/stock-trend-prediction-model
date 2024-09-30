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

    environment {
        DOCKER_IMAGE = 'kathanpatel403/stock-trend-prediction-flask-app'
        TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT[0..6]}"  // Dynamic tag with build number and git commit hash
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the repository...'
                checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-credentials', url: 'https://github.com/Kathanpatel403/stock-trend-prediction-model.git']])
                echo 'Cloned repository successfully!'
            }
        }
        stage('Build and Stop Containers') {
            parallel {
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
            }
        }
        stage('Tag and Push Docker Image to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        echo "Tagging Docker image as ${DOCKER_IMAGE}:${TAG}..."
                        sh "docker tag stock-app ${DOCKER_IMAGE}:${TAG}"
                        
                        echo "Pushing Docker image to Docker Hub..."
                        sh "docker push ${DOCKER_IMAGE}:${TAG}"
                        echo 'Docker image pushed to Docker Hub successfully!'
                    }
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes...'
                sh 'kubectl apply -f deployment.yaml'

                // Check if the deployment has been successfully rolled out
                sh 'kubectl rollout status deployment/flask-app-deployment --timeout=60s'
                echo 'Deployment applied and verified in Kubernetes!'
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully for image: ${DOCKER_IMAGE}:${TAG}"
            // Notify team of successful deployment
            mail to: 'kathanpatel403@gmail.com', 
            subject: 'Deployment Success', 
            body: "Successfully deployed ${DOCKER_IMAGE}:${TAG}. JOB '${env.JOB_NAME}' (${env.BUILD_URL}) successful."
        }
        failure {
            echo "Pipeline failed for image: ${DOCKER_IMAGE}:${TAG}"
            // Notify team of failure
            mail to: 'kathanpatel403@gmail.com', 
            subject: 'Deployment Failure', 
            body: "Failed to deploy ${DOCKER_IMAGE}:${TAG}. JOB '${env.JOB_NAME}' (${env.BUILD_URL}) failed"
        }
        always {
            // Cleaning up workspace 
            cleanWs()
            sh 'docker system prune -f'
        }
    }
}
