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
            agent {
                docker {
                    image 'docker:latest'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                script {
                    // Выполняем checkout, так как это новый агент
                    checkout scm
                }
                withCredentials([usernamePassword(credentialsId: 'my_personal_token', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                        docker build -t iorp/django_demo:${GIT_COMMIT} .
                        echo ${PASSWORD} | docker login -u ${USERNAME} --password-stdin
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
