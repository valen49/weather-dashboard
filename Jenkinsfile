pipeline {
    agent none

    stages {
        stage('Checkout') {
            agent any
            steps {
                echo 'Clonando repositorio...'
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
                    image 'mcr.microsoft.com/playwright/python:latest'
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
    }

    post {
        success {
            echo '✅ Pipeline completado exitosamente'
        }
        failure {
            echo '❌ Pipeline falló'
        }
        always {
            echo 'Pipeline finalizado'
        }
    }
}