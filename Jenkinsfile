pipeline {
    agent none

    environment {
        APP_NAME        = 'weather-dashboard'
        NAMESPACE       = "${params.NAMESPACE}"
        ENVIRONMENT     = "${params.ENVIRONMENT}"
        MINIPC_IP       = '192.168.68.117'
        DOCKER_BUILDKIT = '1'
    }

    options {
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], description: 'Ambiente de destino')
        string(name: 'NAMESPACE', defaultValue: 'default', description: 'Kubernetes namespace')
        booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Omitir pruebas (solo hotfix)')
        booleanParam(name: 'DEPLOY_ENABLED', defaultValue: true, description: 'Habilitar despliegue en K8s')
    }

    stages {
        stage('Checkout') {
            agent any
            steps {
                script {
                    // Capturamos las variables del SCM para evitar que GIT_COMMIT sea null
                    def scmVars = checkout scm
                    env.GIT_COMMIT = scmVars.GIT_COMMIT
                    
                    // Uso de operador seguro ?. para evitar el NullPointerException
                    def shortCommit = env.GIT_COMMIT?.take(8) ?: "unknown"
                    echo "Commit: ${shortCommit} | Build: #${env.BUILD_NUMBER}"
                }
            }
        }

        stage('Unit Tests') {
            when { expression { !params.SKIP_TESTS } }
            agent {
                docker { 
                    image 'python:3.11-slim'
                    args '-u root' // Asegura permisos para instalar dependencias
                }
            }
            steps {
                sh '''
                    python -m venv /tmp/venv
                    . /tmp/venv/bin/activate
                    pip install --upgrade pip
                    pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt
                    pytest tests/ -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Build Parallel') {
            parallel {
                stage('Build E2E Image') {
                    agent any
                    steps {
                        sh "docker build -f Dockerfile.e2e -t playwright-e2e:${env.BUILD_NUMBER} -t playwright-e2e:latest ."
                    }
                }

                stage('Build App Image') {
                    agent any
                    steps {
                        sh """
                            docker build \
                            -t ${APP_NAME}:${env.BUILD_NUMBER} \
                            -t ${APP_NAME}:latest \
                            --label version=${env.BUILD_NUMBER} \
                            --label commit=${env.GIT_COMMIT?.take(8)} .
                        """
                    }
                }
            }
        }

        stage('E2E Tests') {
            when { expression { !params.SKIP_TESTS } }
            agent { docker { image "playwright-e2e:${env.BUILD_NUMBER}" } }
            steps {
                retry(2) {
                    sh 'npm ci && npx playwright test --project=chromium'
                }
            }
        }

        stage('Deploy') {
            agent any
            when { expression { params.DEPLOY_ENABLED } }
            steps {
                script {
                    sh "kubectl apply -f k8s-deployment.yaml -n ${NAMESPACE}"
                    sh "kubectl apply -f k8s-service.yaml -n ${NAMESPACE}"
                    
                    // Actualización de imagen con validación de rollout
                    sh """
                        kubectl set image deployment/${APP_NAME} ${APP_NAME}=${APP_NAME}:${env.BUILD_NUMBER} -n ${NAMESPACE}
                        kubectl rollout status deployment/${APP_NAME} -n ${NAMESPACE} --timeout=120s
                    """
                }
            }
        }

        stage('Healthcheck') {
            agent any
            when { expression { params.DEPLOY_ENABLED } }
            steps {
                retry(5) {
                    sh '''
                        POD=$(kubectl get pod -n ${NAMESPACE} -l app=${APP_NAME} --field-selector=status.phase=Running -o jsonpath='{.items[0].metadata.name}')
                        [ -n "$POD" ] || exit 1
                        kubectl exec -n ${NAMESPACE} ${POD} -- python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5000').read()"
                    '''
                    sleep 5
                }
            }
        }
    }

    post {
        success {
            script {
                def shortCommit = env.GIT_COMMIT?.take(8) ?: "N/A"
                echo "✓ Deploy OK — Build #${env.BUILD_NUMBER}"
                echo "  URL: http://${env.MINIPC_IP}:5000"
                echo "  Commit: ${shortCommit}"
            }
        }
        failure {
            echo "✗ Pipeline falló en la etapa: ${env.STAGE_NAME ?: 'Desconocida'}"
            node('built-in') {
                // Debug rápido si falla
                sh "kubectl get pods -n ${NAMESPACE} -l app=${APP_NAME} || true"
            }
        }
        always {
            node('built-in') {
                sh 'docker image prune -f || true'
                cleanWs()
            }
        }
    }
}
