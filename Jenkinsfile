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
                withChecks(name: 'Checkout', includeStage: true) {
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
        }

        stage('Setup environment') {
            steps {
                withChecks(name: 'Setup', includeStage: true) {
                    sh '''
                    if [ ! -d "$VENV" ]; then
                        python3 -m venv $VENV
                    fi
                    . $VENV/bin/activate && pip install --upgrade pip --quiet
                    . $VENV/bin/activate && pip install -r req.txt --quiet
                    '''
                }
            }
        }

        stage('Run pipeline') {
            steps {
                withChecks(name: 'ML Run', includeStage: true) {
                    script {
                        try {
                            def output = sh(
                                script: ". $VENV/bin/activate && python model_preparation.py && python model_testing.py",
                                returnStdout: true
                            ).trim()

                            echo output

                            // ограничим размер (важно для GitHub Checks)
                            env.PIPELINE_LOG = output.take(5000)

                            def matcher = (output =~ /rmse=([0-9.]+)/)
                            if (matcher) {
                                env.RMSE = matcher[0][1]
                            } else {
                                env.RMSE = "unknown"
                            }

                        } catch (err) {
                            env.PIPELINE_LOG = "Error occurred during execution"
                            env.RMSE = "error"
                            error("Pipeline execution failed")
                        }
                    }
                }
            }
        }

        stage('Publish to GitHub Checks') {
            steps {
                script {
                    def conclusion = currentBuild.currentResult

                    publishChecks name: 'ML Pipeline',
                        title: "ML Pipeline Results",
                        summary: "RMSE: ${env.RMSE}",
                        text: """
Commit: ${env.GIT_COMMIT}

Results:

${env.PIPELINE_LOG}
""",
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
                text: "Смотри логи Jenkins",
                conclusion: 'FAILURE'
        }

        unstable {
            publishChecks name: 'ML Pipeline',
                title: "ML Pipeline Unstable",
                summary: "Метрики хуже ожидаемых",
                conclusion: 'NEUTRAL'
        }

        success {
            publishChecks name: 'ML Pipeline',
                title: "ML Pipeline Success",
                summary: "RMSE: ${env.RMSE}",
                conclusion: 'SUCCESS'
        }
    }
}
