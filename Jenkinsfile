pipeline {
    agent none

    environment {
        APP_NAME      = 'weather-dashboard'
        ENVIRONMENT   = "${params.ENVIRONMENT}"
        // Auto-generate namespace based on environment, or use custom
        NAMESPACE     = "${params.CUSTOM_NAMESPACE ?: 'weather-' + params.ENVIRONMENT}"
        MINIPC_IP     = '192.168.68.117'
        MINIKUBE_HOME = '/home/valen'
        DOCKER_BUILDKIT = '1'
        COMPOSE_DOCKER_CLI_BUILD = '1'
    }

    options {
        disableConcurrentBuilds()
        timeout(time: ENVIRONMENT == 'prod' ? 45 : 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: ENVIRONMENT == 'prod' ? '20' : '10'))
    }

    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], description: 'Target environment (auto-sets namespace)')
        string(name: 'CUSTOM_NAMESPACE', defaultValue: '', description: 'Custom K8s namespace (leave empty to use auto-generated)')
        booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Skip tests (hotfix only)')
        booleanParam(name: 'DEPLOY_ENABLED', defaultValue: true, description: 'Enable deployment to Kubernetes')
    }

    stages {
        stage('Validate Parameters') {
            steps {
                echo "🚀 Deployment Configuration:"
                echo "   Environment: ${ENVIRONMENT}"
                echo "   Namespace: ${NAMESPACE}"
                echo "   Skip Tests: ${params.SKIP_TESTS}"
                echo "   Deploy Enabled: ${params.DEPLOY_ENABLED}"
                echo "   Build: #${env.BUILD_NUMBER}"
                echo "   Commit: ${env.GIT_COMMIT.take(8)}"

                script {
                    if (ENVIRONMENT == 'prod' && !params.DEPLOY_ENABLED) {
                        echo "⚠️  WARNING: Production deployment disabled!"
                    }
                }
            }
        }

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
                    error 'Unit tests failed — deployment canceled'
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
                            --label version=${BUILD_NUMBER} \
                            --label timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ') .
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
                    error 'E2E tests failed — deployment canceled'
                }
            }
        }

        stage('Validate Manifests') {
            agent any
            steps {
                sh '''
                    kubectl apply --dry-run=client -f k8s-deployment.yaml
                    kubectl apply --dry-run=client -f k8s-service.yaml
                    echo "✓ Manifests validated"
                '''
            }
        }

        stage('Deploy') {
            agent any
            when {
                expression { params.DEPLOY_ENABLED }
            }
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
            when {
                expression { params.DEPLOY_ENABLED }
            }
            steps {
                retry(15) {
                    sh '''
                        POD=$(kubectl get pod -n ${NAMESPACE} -l app=${APP_NAME} -o jsonpath='{.items[0].metadata.name}')
                        [ -n "$POD" ] || exit 1
                        echo "Checking pod: ${POD}"

                        kubectl exec -n ${NAMESPACE} ${POD} -- \
                            python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5000').read(); print('OK')" || exit 1
                        
                        echo "✓ App responding correctly"
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
            echo "✗ Pipeline failed at: ${env.STAGE_NAME}"
            node('built-in') {
                sh '''
                    echo "=== Deployment Status ==="
                    kubectl get deployment/${APP_NAME} -n ${NAMESPACE} -o wide || true
                    
                    echo "=== Pods Status ==="
                    kubectl get pods -n ${NAMESPACE} -l app=${APP_NAME} -o wide || true
                    
                    echo "=== Latest Logs ==="
                    kubectl logs -n ${NAMESPACE} -l app=${APP_NAME} --tail=30 --timestamps=true || true
                    
                    echo "=== Pod Description ==="
                    kubectl describe pod -n ${NAMESPACE} -l app=${APP_NAME} || true
                    
                    echo "=== Rollout History ==="
                    kubectl rollout history deployment/${APP_NAME} -n ${NAMESPACE} || true
                '''
            }
        }
        unstable {
            echo "⚠ Pipeline unstable — check logs"
        }
        always {
            node('built-in') {
                sh '''
                    echo "Cleaning up workspace..."
                    docker image prune -f || true
                '''
                cleanWs()
            }
        }
    }
}