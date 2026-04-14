pipeline {
    agent none

    environment {
        APP_NAME     = 'weather-dashboard'
        NAMESPACE    = 'default'
        MINIPC_IP    = '192.168.68.117'
        MINIKUBE_HOME = '/home/valen'
    }

    options {
        disableConcurrentBuilds()
        timeout(time: 15, unit: 'MINUTES')
        timestamps()
    }

    stages {

        stage('Checkout') {
            agent any
            steps {
                checkout scm
                echo "Commit: ${env.GIT_COMMIT.take(8)} | Build: #${env.BUILD_NUMBER}"
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
                    pytest tests/ -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
                failure {
                    error 'Unit tests fallaron — deploy cancelado'
                }
            }
        }

        stage('Build E2E Image') {
            agent any
            steps {
                sh '''
                    docker build -f Dockerfile.e2e \
                    -t playwright-e2e:${BUILD_NUMBER} .
                '''
            }
        }

        stage('E2E Tests') {
            agent {
                docker {
                    image "playwright-e2e:${BUILD_NUMBER}"
                    reuseNode true
                }
            }
            steps {
                sh 'npx playwright test --project=chromium'
            }
            post {
                failure {
                    error 'E2E tests fallaron — deploy cancelado'
                }
            }
        }

        stage('Build imagen') {
            agent any
            steps {
                sh '''
                    docker build -t ${APP_NAME}:latest .
                    echo "Imagen lista: ${APP_NAME}:latest"
                '''
            }
        }

        stage('Validar manifests') {
            agent any
            steps {
                sh '''
                    kubectl apply --dry-run=client -f k8s-deployment.yaml
                    kubectl apply --dry-run=client -f k8s-service.yaml
                    echo "Manifiestos OK"
                '''
            }
        }

        stage('Deploy') {
            agent any
            steps {
                sh '''
                    kubectl apply -f k8s-deployment.yaml
                    kubectl apply -f k8s-service.yaml

                    kubectl set image deployment/${APP_NAME} \
                        ${APP_NAME}=${APP_NAME}:latest \
                        -n ${NAMESPACE}

                    kubectl rollout status deployment/${APP_NAME} \
                        -n ${NAMESPACE} \
                        --timeout=180s
                '''
            }
        }

        stage('Verificar') {
            agent any
            steps {
                sh '''
                    POD=$(kubectl get pod -n ${NAMESPACE} -l app=${APP_NAME} -o jsonpath='{.items[0].metadata.name}')
                    echo "Verificando pod: ${POD}"

                    for i in $(seq 1 10); do
                        HTTP_CODE=$(kubectl exec -n ${NAMESPACE} ${POD} -- \
                            python3 -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000').getcode())" 2>/dev/null || echo "000")
                        echo "Intento ${i}/10 - HTTP: ${HTTP_CODE}"
                        if [ "${HTTP_CODE}" = "200" ]; then
                            echo "App OK"
                            exit 0
                        fi
                        sleep 3
                    done

                    echo "La app no respondio correctamente"
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo "Deploy OK — Build #${env.BUILD_NUMBER} en http://${env.MINIPC_IP}:5000"
        }
        failure {
            node('built-in') {
                sh '''
                    echo "=== Pods ==="
                    kubectl get pods || true
                    echo "=== Logs ==="
                    kubectl logs -l app=weather-dashboard --tail=50 || true
                    echo "=== Describe ==="
                    kubectl describe pod -l app=weather-dashboard || true
                '''
            }
        }
        always {
            node('built-in') {
                cleanWs()
            }
        }
    }
}