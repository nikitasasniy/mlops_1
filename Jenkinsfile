pipeline {
    agent any

    environment {
        VENV = ".venv"
        GITHUB_REPO = 'mlops_1'
        GITHUB_ACCOUNT = 'nikitasasniy'
    }

    stages {
        stage('Checkout') {
            steps {
                git(
                    url: "https://github.com/${env.GITHUB_ACCOUNT}/${env.GITHUB_REPO}.git",
                    branch: 'main',
                    credentialsId: 'github-token-id'
                )
                script {
                    env.GIT_COMMIT = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    echo "Current commit SHA: ${env.GIT_COMMIT}"
                }
            }
        }

        stage('Setup environment') {
            steps {
                sh '''
                if [ ! -d "$VENV" ]; then
                    python3 -m venv $VENV
                fi
                . $VENV/bin/activate && pip install --upgrade pip --quiet
                . $VENV/bin/activate && pip install -r req.txt --quiet
                '''
            }
        }

        stage('Data creation & preprocessing') {
            steps {
                sh ". $VENV/bin/activate && python data_creation.py && python data_preprocessing.py"
            }
        }

        stage('Model training & testing') {
            steps {
                sh ". $VENV/bin/activate && python model_preparation.py && python model_testing.py"
            }
        }

        stage('Publish results to GitHub Checks') {
            steps {
                // Используем GitHub Checks Plugin
                githubChecks name: 'ML Pipeline', title: "Pipeline results for ${env.GIT_COMMIT}", summary: 'Пайплайн завершён', status: 'COMPLETED', conclusion: 'SUCCESS', actions: [], detailsURL: '', annotations: [
                    // Можно добавить аннотации для конкретных ошибок или предупреждений
                    [path: 'model_testing.py', startLine: 1, endLine: 1, annotationLevel: 'NOTICE', message: 'Тестирование модели прошло успешно']
                ]
            }
        }
    }

    post {
        success {
            githubChecks name: 'ML Pipeline', title: "Pipeline passed", summary: 'Все шаги завершены успешно', status: 'COMPLETED', conclusion: 'SUCCESS'
        }
        failure {
            githubChecks name: 'ML Pipeline', title: "Pipeline failed", summary: 'Есть ошибки в пайплайне', status: 'COMPLETED', conclusion: 'FAILURE'
        }
        always {
            echo "Pipeline finished. Статус отображён в GitHub Checks."
        }
    }
}
