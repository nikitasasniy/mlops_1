pipeline {
    agent any

    options {
        withChecks()
    }

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
            }
        }

        stage('Run pipeline') {
            steps {
                sh ". $VENV/bin/activate && python model_preparation.py && python model_testing.py"
            }
        }

        stage('Publish results') {
            steps {
                publishChecks name: 'ML Pipeline',
                    title: "Results",
                    summary: 'Пайплайн завершён',
                    text: 'Смотри логи Jenkins для деталей',
                    conclusion: 'SUCCESS'
            }
        }
    }

    post {
        failure {
            publishChecks name: 'ML Pipeline',
                title: "Failed",
                summary: 'Ошибка в пайплайне',
                conclusion: 'FAILURE'
        }
    }
}
