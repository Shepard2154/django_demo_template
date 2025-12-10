pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-u root'
        }
    }

    environment {
        GIT_COMMIT = "${env.GIT_COMMIT}"
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
        
        stage('Docker Build and Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: '17a71590-8418-48d4-8baa-e0e2fcc19595', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                        docker build -t iorp/django_demo:${GIT_COMMIT} .
                        docker login -u ${USERNAME} -p ${PASSWORD}
                        docker push iorp/django_demo:${GIT_COMMIT}
                    '''
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
