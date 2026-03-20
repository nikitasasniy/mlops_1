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
                    }
                }
            }
        }

        stage('Setup') {
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

        stage('ML Run') {
            steps {
                withChecks(name: 'ML Run', includeStage: true) {
                    script {
                        try {
                            def output = sh(
                                script: ". $VENV/bin/activate && python model_preparation.py && python model_testing.py",
                                returnStdout: true
                            ).trim()

                            env.PIPELINE_LOG = output.take(4000)

                            def matcher = (output =~ /rmse=([0-9.]+)/)
                            env.RMSE = matcher ? matcher[0][1] : "unknown"

                        } catch (e) {
                            env.RMSE = "error"
                            env.PIPELINE_LOG = "Execution failed"
                            error("ML step failed")
                        }
                    }
                }
            }
        }

        stage('Publish Checks') {
            steps {
                script {
                    def rmseValue = (env.RMSE.isNumber()) ? env.RMSE.toFloat() : null

                    // 🎯 quality gate
                    def conclusion = 'SUCCESS'
                    if (rmseValue == null) {
                        conclusion = 'FAILURE'
                    } else if (rmseValue > 1.0) {
                        conclusion = 'UNSTABLE'
                    }

                    publishChecks name: 'ML Pipeline',
                        title: "ML Pipeline Results",
                        summary: "RMSE: ${env.RMSE}",
                        text: """
                        Commit: ${env.GIT_COMMIT}
                        
                        RMSE: ${env.RMSE}
                        
                        Logs:
                        ${env.PIPELINE_LOG}
                        """,
                        detailsURL: env.BUILD_URL,   // 🔥 важно (из гайда)
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
