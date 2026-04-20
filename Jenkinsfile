pipeline {
    agent none

    environment {
        APP_NAME     = 'weather-dashboard'
        NAMESPACE    = 'default'
        MINIPC_IP    = '192.168.68.117'
        DOCKER_BUILDKIT = '1'
    }

    options {
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            agent any
            steps {
                script {
                    def scmVars = checkout scm
                    env.GIT_COMMIT = scmVars.GIT_COMMIT
                    echo "Commit: ${env.GIT_COMMIT?.take(8)} | Build: #${env.BUILD_NUMBER}"
                }
            }
        }

        stage('Unit Tests') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root'
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
            agent { docker { image "playwright-e2e:${env.BUILD_NUMBER}" } }
            steps {
                retry(2) {
                    sh 'npm ci && npx playwright test --project=chromium'
                }
            }
        }

        stage('Deploy') {
            agent any
            steps {
                sh "kubectl apply -f k8s-deployment.yaml -n ${NAMESPACE}"
                sh "kubectl apply -f k8s-service.yaml -n ${NAMESPACE}"
                sh """
                    kubectl set image deployment/${APP_NAME} ${APP_NAME}=${APP_NAME}:${env.BUILD_NUMBER} -n ${NAMESPACE}
                    kubectl rollout status deployment/${APP_NAME} -n ${NAMESPACE} --timeout=120s
                """
            }
        }

        stage('Healthcheck') {
            agent any
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
            echo "✓ Deploy OK — Build #${env.BUILD_NUMBER} | http://${MINIPC_IP}:30000"
        }
        failure {
            echo "✗ Pipeline failed at: ${env.STAGE_NAME ?: 'unknown'}"
            node('built-in') {
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
