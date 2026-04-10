pipeline {
    agent none

    stages {
        stage('Checkout') {
            agent any
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }

        stage('Unit Tests') {
            agent {
                docker { image 'python:3.11' }
            }
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip install -r requirements-dev.txt
                    pytest tests/ -v
                '''
            }
        }

        stage('E2E Tests') {
            agent {
                docker {
                    image 'mcr.microsoft.com/playwright/python:v1.58.0-noble'
                    args '-u root'
                }
            }
            steps {
                sh '''
                    pip install -r requirements.txt --break-system-packages
                    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
                    apt-get install -y nodejs
                    npm ci
                    npx playwright test --project=chromium
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            agent any
            steps {
                sh '''
                    docker build -t weather-dashboard:latest .
                    kubectl apply -f k8s-deployment.yaml
                    kubectl apply -f k8s-service.yaml
                    kubectl rollout status deployment/weather-dashboard
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully'
        }
        failure {
            echo '❌ Pipeline failed'
        }
        always {
            echo 'Pipeline finished'
        }
    }
}