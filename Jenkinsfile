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
        
        stage('Docker Build') {
            agent {
                docker {
                    image 'docker:latest'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                script {
                    checkout scm
                }
                sh '''
                    docker build -t iorp/django_demo:${GIT_COMMIT} .
                '''
            }
        }
        
        stage('Send Notification / API Request') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'my_personal_token', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    script {
                        // Пример: Отправка уведомления через API с Basic Auth
                        // USERNAME и PASSWORD используются здесь для аутентификации
                        // в каком-то внешнем API (Slack, Telegram, собственный API и т.д.)
                        sh '''
                            echo "Отправка уведомления о завершении сборки..."
                            
                            # Пример 1: API запрос с Basic Auth
                            # curl -u ${USERNAME}:${PASSWORD} \
                            #   -X POST https://api.example.com/notifications \
                            #   -H "Content-Type: application/json" \
                            #   -d '{"commit":"${GIT_COMMIT}","status":"success","coverage":"91%"}'
                            
                            # Пример 2: Отправка отчета о покрытии
                            # curl -u ${USERNAME}:${PASSWORD} \
                            #   -X PUT https://api.example.com/reports/coverage \
                            #   -F "file=@htmlcov/index.html"
                            
                            # Пример 3: Регистрация деплоя в системе
                            # curl -u ${USERNAME}:${PASSWORD} \
                            #   -X POST https://deploy.example.com/api/deployments \
                            #   -d "commit=${GIT_COMMIT}&image=iorp/django_demo:${GIT_COMMIT}"
                            
                            # Для демонстрации просто показываем, что credentials доступны
                            echo "✅ Credentials загружены успешно"
                            echo "📦 Docker образ: iorp/django_demo:${GIT_COMMIT}"
                            echo "🔐 USERNAME и PASSWORD скрыты в логах Jenkins"
                        '''
                    }
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
