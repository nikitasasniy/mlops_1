pipeline {
    agent any

    environment {
        VENV = ".venv"
    }

    stages {

        stage('Setup environment') {
            steps {
                sh '''
                if [ ! -d "$VENV" ]; then
                    python3 -m venv $VENV
                fi

                . $VENV/bin/activate
                pip install --upgrade pip --quiet
                pip install -r req.txt --quiet
                '''
            }
        }

        stage('Data creation') {
            steps {
                sh '''
                . $VENV/bin/activate
                python data_creation.py
                '''
            }
        }

        stage('Data preprocessing') {
            steps {
                sh '''
                . $VENV/bin/activate
                python data_preprocessing.py
                '''
            }
        }

        stage('Model training') {
            steps {
                sh '''
                . $VENV/bin/activate
                python model_preparation.py
                '''
            }
        }

        stage('Model Testing') {
            steps {
                script {
                    // Запускаем скрипт и сохраняем вывод
                    def output = sh(script: 'python lab1/model_testing.py', returnStdout: true).trim()
                    echo "Raw output: ${output}"

                    // Ищем rmse
                    def matcher = output =~ /rmse=(\d+\.\d+)/
                    def rmse = matcher ? matcher[0][1] : "N/A"
                    echo "Model RMSE: ${rmse}"

                    // Сохраняем для post
                    currentBuild.description = "RMSE: ${rmse}"
                }
            }
        }
    }

    post {
        success {
            // Отправка статуса в GitHub
            githubNotify context: 'ML Model Test', status: 'SUCCESS', description: "RMSE: ${rmse}"
        }
        failure {
            githubNotify context: 'ML Model Test', status: 'FAILURE', description: "Pipeline failed"
        }
    }
}
