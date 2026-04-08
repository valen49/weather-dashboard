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
                docker { image 'mcr.microsoft.com/playwright/python:v1.51.0-noble' }
            }
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
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