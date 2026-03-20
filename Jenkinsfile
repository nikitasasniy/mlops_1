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
                    echo "Commit: ${env.GIT_COMMIT}"
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

        stage('Run pipeline') {
            steps {
                script {
                    def output = sh(
                        script: ". $VENV/bin/activate && python model_preparation.py && python model_testing.py",
                        returnStdout: true
                    ).trim()

                    echo output

                    // сохраняем вывод для GitHub Checks
                    env.PIPELINE_LOG = output

                    // пробуем вытащить RMSE
                    def matcher = (output =~ /rmse=([0-9.]+)/)
                    if (matcher) {
                        env.RMSE = matcher[0][1]
                        echo "Parsed RMSE: ${env.RMSE}"
                    } else {
                        env.RMSE = "unknown"
                    }
                }
            }
        }

        stage('Publish to GitHub Checks') {
            steps {
                publishChecks name: 'ML Pipeline',
                    title: "ML Pipeline Results",
                    summary: "RMSE: ${env.RMSE}",
                    text: """
                    Commit: ${env.GIT_COMMIT}

                    Результаты пайплайна:

                    ${env.PIPELINE_LOG}
                    """,
                    conclusion: 'SUCCESS'
            }
        }
    }

    post {
        failure {
            publishChecks name: 'ML Pipeline',
                title: "ML Pipeline Failed",
                summary: "Ошибка выполнения пайплайна",
                text: "Смотри логи Jenkins",
                conclusion: 'FAILURE'
        }

        unstable {
            publishChecks name: 'ML Pipeline',
                title: "ML Pipeline Unstable",
                summary: "Метрики хуже ожидаемых",
                conclusion: 'NEUTRAL'
        }

        always {
            echo "Pipeline finished"
        }
    }
}
