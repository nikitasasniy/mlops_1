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
            // Запуск теста и получение RMSE
            def output = sh(script: ". $VENV/bin/activate && python model_testing.py", returnStdout: true).trim()
            def rmseLine = output.readLines().find { it.contains('rmse=') }
            def rmse = rmseLine?.split('=')[1]?.trim() ?: "N/A"
            echo "Test RMSE: ${rmse}"

            // Сохраняем RMSE в environment, чтобы использовать в post
            env.RMSE = rmse
        }
    }
}

post {
    success {
        script {
            githubNotify(
                context: 'ML Model Test',
                status: 'SUCCESS',
                description: "RMSE: ${env.RMSE}",
                repo: 'user/repo',                 // замени на свой репозиторий
                account: 'github-account',         // твой GitHub username/organization
                credentialsId: 'github-token-id',  // ID твоего токена в Jenkins
                sha: env.GIT_COMMIT                 // текущий коммит
            )
        }
    }
    failure {
        script {
            githubNotify(
                context: 'ML Model Test',
                status: 'FAILURE',
                description: "Pipeline failed",
                repo: 'user/repo',
                account: 'github-account',
                credentialsId: 'github-token-id',
                sha: env.GIT_COMMIT
            )
        }
    }
}
