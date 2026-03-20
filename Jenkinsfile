pipeline {
    agent any

    environment {
        VENV = ".venv"  // путь к виртуальному окружению
    }

    stages {

        stage('Setup environment') {
            steps {
                sh '''
                # создаём venv, если нет
                if [ ! -d "$VENV" ]; then
                    python3 -m venv $VENV
                fi

                # активируем venv и устанавливаем зависимости
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
                    // запускаем скрипт и сохраняем вывод
                    def output = sh(script: 'python lab1/model_testing.py', returnStdout: true).trim()
                    echo "Raw output: ${output}"

                    // извлекаем RMSE
                    def matcher = output =~ /rmse=(\d+\.\d+)/
                    def rmseValue = matcher ? matcher[0][1] : "N/A"
                    echo "Model RMSE: ${rmseValue}"

                    // сохраняем для post и description
                    env.RMSE = rmseValue
                    currentBuild.description = "RMSE: ${rmseValue}"
                }
            }
        }
    }

    post {
        success {
            // отправка статуса и RMSE в GitHub
            githubNotify context: 'ML Model Test', status: 'SUCCESS', description: "RMSE: ${env.RMSE}"
        }
        failure {
            githubNotify context: 'ML Model Test', status: 'FAILURE', description: "Pipeline failed"
        }
    }
}
