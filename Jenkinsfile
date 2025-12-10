pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-u root -p 8000:8000'
        }
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Test + Coverage') {
            steps {
                sh '''
                    coverage run --source='.' manage.py test --verbosity=2
                    coverage report
                    coverage html
                '''
            }
        }
        
        stage('Run Application') {
            agent {
                docker {
                    image 'docker:latest'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                script {
                    checkout scm
                    def workspace = env.WORKSPACE
                    sh """
                        docker stop django_demo 2>/dev/null || true
                        docker rm django_demo 2>/dev/null || true
                        docker build -t django_demo:latest ${workspace}
                        docker run -d -p 8000:8000 --name django_demo django_demo:latest
                    """
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'htmlcov/**/*', fingerprint: true
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
 