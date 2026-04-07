pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Clonando repositorio...'
                checkout scm
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Corriendo tests unitarios...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip install -r requirements-dev.txt
                    pytest tests/ -v
                '''
            }
        }

        stage('E2E Tests') {
            steps {
                echo 'Corriendo tests E2E...'
                sh '''
                    . venv/bin/activate
                    npm ci
                    npx playwright install chromium --with-deps
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