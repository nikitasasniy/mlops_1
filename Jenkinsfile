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
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                set -e

                VENV=".venv"

                python3 -m venv $VENV

                $VENV/bin/python -m ensurepip --upgrade || true
                $VENV/bin/python -m pip install --upgrade pip

                $VENV/bin/pip install -r req.txt
                '''
            }
        }

        stage('Data Creation') {
            steps {
                sh '''
                set -e
                .venv/bin/python data_creation.py
                '''
            }
        }

        stage('Data Preprocessing') {
            steps {
                sh '''
                set -e
                .venv/bin/python data_preprocessing.py
                '''
            }
        }

        stage('Model Preparation') {
            steps {
                sh '''
                set -e
                .venv/bin/python model_preparation.py
                '''
            }
        }

        stage('Model Testing') {
            steps {
                script {
                    def output = sh(
                        script: '.venv/bin/python model_testing.py',
                        returnStdout: true
                    ).trim()

                    echo output
                    env.PIPELINE_LOG = output.take(4000)

                    def matcher = (output =~ /rmse=([0-9.]+)/)
                    env.RMSE = matcher ? matcher[0][1] : "unknown"
                }
            }
        }

        stage('Publish ML Pipeline Check') {
            steps {
                script {
                    def rmseValue = (env.RMSE.isNumber()) ? env.RMSE.toFloat() : null
                    def conclusion = 'SUCCESS'

                    if (rmseValue == null || env.RMSE == "error") {
                        conclusion = 'FAILURE'
                    } else if (rmseValue > 1.0) {
                        conclusion = 'UNSTABLE'
                    }

                    publishChecks name: 'ML Pipeline',
                        title: "ML Pipeline Results",
                        summary: "RMSE: ${env.RMSE}",
                        text: """
Commit: ${env.GIT_COMMIT ?: 'unknown'}

RMSE: ${env.RMSE}

Logs:
${env.PIPELINE_LOG}
""",
                        detailsURL: env.BUILD_URL,
                        conclusion: conclusion
                }
            }
        }
    }

    post {
        failure {
            publishChecks name: 'ML Pipeline',
                title: "ML Pipeline Failed",
                summary: "Ошибка выполнения пайплайна",
                detailsURL: env.BUILD_URL,
                conclusion: 'FAILURE'
        }
    }
}
