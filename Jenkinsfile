pipeline {
    agent none

    environment {
        APP_NAME      = 'weather-dashboard'
        NAMESPACE     = 'default'
        MINIPC_IP     = '192.168.68.117'
        MINIKUBE_HOME = '/home/valen'
        DOCKER_BUILDKIT = '1'
        COMPOSE_DOCKER_CLI_BUILD = '1'
    }

    options {
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    parameters {
        booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Skip tests (solo hotfix)')
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
            when {
                expression { !params.SKIP_TESTS }
            }
            agent {
                docker { image 'python:3.11-slim' }
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
                failure {
                    error 'Unit tests fallaron — deploy cancelado'
                }
            }
        }

        stage('Build Parallel') {
            parallel {
                stage('Build E2E Image') {
                    agent any
                    steps {
                        sh '''
                            docker build -f Dockerfile.e2e \
                            --cache-from playwright-e2e:latest \
                            -t playwright-e2e:${BUILD_NUMBER} \
                            -t playwright-e2e:latest .
                        '''
                    }
                }

                stage('Build App Image') {
                    agent any
                    steps {
                        sh '''
                            docker build \
                            --cache-from ${APP_NAME}:latest \
                            -t ${APP_NAME}:${BUILD_NUMBER} \
                            -t ${APP_NAME}:latest \
                            -l version=${BUILD_NUMBER} \
                            -l timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ') .
                        '''
                    }
                }
            }
        }

        stage('E2E Tests') {
            when {
                expression { !params.SKIP_TESTS }
            }
            agent {
                docker {
                    image "playwright-e2e:${BUILD_NUMBER}"
                }
            }
            steps {
                retry(2) {
                    sh 'npm ci && npx playwright test --project=chromium --retries=1'
                }
            }
            post {
                failure {
                    error 'E2E tests fallaron — deploy cancelado'
                }
            }
        }

        stage('Validar Manifests') {
            agent any
            steps {
                sh '''
                    kubectl apply --dry-run=client -f k8s-deployment.yaml
                    kubectl apply --dry-run=client -f k8s-service.yaml
                    echo "✓ Manifiestos validados"
                '''
            }
        }

        stage('Deploy') {
            agent any
            steps {
                retry(2) {
                    sh '''
                        kubectl apply -f k8s-deployment.yaml
                        kubectl apply -f k8s-service.yaml

                        kubectl set image deployment/${APP_NAME} \
                            ${APP_NAME}=${APP_NAME}:${BUILD_NUMBER} \
                            -n ${NAMESPACE} \
                            --record

                        kubectl rollout status deployment/${APP_NAME} \
                            -n ${NAMESPACE} \
                            --timeout=300s
                    '''
                }
            }
        }

        stage('Healthcheck') {
            agent any
            steps {
                retry(15) {
                    sh '''
                        POD=$(kubectl get pod -n ${NAMESPACE} -l app=${APP_NAME} -o jsonpath='{.items[0].metadata.name}')
                        [ -n "$POD" ] || exit 1
                        echo "Verificando pod: ${POD}"

                        kubectl exec -n ${NAMESPACE} ${POD} -- \
                            curl -sf http://localhost:5000 > /dev/null || exit 1
                        
                        echo "✓ App respondiendo correctamente"
                    '''
                    sleep(time: 2, unit: 'SECONDS')
                }
            }
        }
    }

    post {
        success {
            echo "✓ Deploy OK — Build #${env.BUILD_NUMBER}"
            echo "  URL: http://${env.MINIPC_IP}:5000"
            echo "  Commit: ${env.GIT_COMMIT.take(8)}"
        }
        failure {
            echo "✗ Pipeline falló en: ${env.STAGE_NAME}"
            node('built-in') {
                sh '''
                    echo "=== Status Deployment ==="
                    kubectl get deployment/${APP_NAME} -n ${NAMESPACE} -o wide || true
                    
                    echo "=== Pods Status ==="
                    kubectl get pods -n ${NAMESPACE} -l app=${APP_NAME} -o wide || true
                    
                    echo "=== Últimos Logs ==="
                    kubectl logs -n ${NAMESPACE} -l app=${APP_NAME} --tail=30 --timestamps=true || true
                    
                    echo "=== Pod Description ==="
                    kubectl describe pod -n ${NAMESPACE} -l app=${APP_NAME} || true
                    
                    echo "=== Rollout History ==="
                    kubectl rollout history deployment/${APP_NAME} -n ${NAMESPACE} || true
                '''
            }
        }
        unstable {
            echo "⚠ Pipeline inestable — revisar logs"
        }
        always {
            node('built-in') {
                sh '''
                    echo "Limpiando espacio de trabajo..."
                    docker image prune -f || true
                '''
                cleanWs()
            }
        }
    }
}