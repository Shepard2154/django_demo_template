pipeline {
    agent any

    environment {
        DOCKER_HOST = "unix:///var/run/docker.sock"
    }

    stages {
        stage('Checkout and Build') {
            steps {
                script {
                    sh "docker stop django_demo 2>/dev/null || true"
                    sh "docker rm django_demo 2>/dev/null || true"
                    sh "docker build -t django_demo:latest ."
                }
            }
        }
        
        stage('Test + Coverage') {
            steps {
                script {
                    sh """
                    docker run --rm \
                        -v ${WORKSPACE}:/app \
                        -w /app \
                        python:3.11-slim \
                        bash -c "
                            pip install --upgrade pip
                            pip install -r requirements.txt
                            coverage run --source='.' manage.py test --verbosity=2
                            coverage report
                            coverage html
                        "
                    """
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    sh "docker run -d -p 8000:8000 --name django_demo django_demo:latest"
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'htmlcov/**/*', fingerprint: true
        }
        failure {
            echo 'Pipeline failed!!! :('
        }
    }
}
 