pipeline {
    agent any

    environment {
        VENV = ".venv"
        GITHUB_REPO = 'mlops_1'
        GITHUB_ACCOUNT = 'nikitasasniy'
        GITHUB_SERVER = 'git' // имя, которое ты указал в Jenkins → Configure System → GitHub Servers
    }

    stages {
        // ===============================
        stage('Setup Environment') {
            steps {
                withChecks(name: 'Setup', includeStage: true, 
                           githubServer: env.GITHUB_SERVER, 
                           githubRepo: "${env.GITHUB_ACCOUNT}/${env.GITHUB_REPO}") {
                    script {
                        echo "Cloning repository..."
                        git(
                            url: "https://github.com/${env.GITHUB_ACCOUNT}/${env.GITHUB_REPO}.git",
                            branch: 'main',
                            credentialsId: 'github-token-id'
                        )

                        echo "Setting up Python environment..."
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
            }
        }

        // ===============================
        stage('Data Creation') {
            steps {
                withChecks(name: 'Data Creation', includeStage: true, 
                           githubServer: env.GITHUB_SERVER, 
                           githubRepo: "${env.GITHUB_ACCOUNT}/${env.GITHUB_REPO}") {
                    script {
                        sh ". $VENV/bin/activate && python data_creation.py"
                    }
                }
            }
        }

        // ===============================
        stage('Data Preprocessing') {
            steps {
                withChecks(name: 'Data Preprocessing', includeStage: true, 
                           githubServer: env.GITHUB_SERVER, 
                           githubRepo: "${env.GITHUB_ACCOUNT}/${env.GITHUB_REPO}") {
                    script {
                        sh ". $VENV/bin/activate && python data_preprocessing.py"
                    }
                }
            }
        }

        // ===============================
        stage('Model Preparation') {
            steps {
                withChecks(name: 'Model Preparation', includeStage: true, 
                           githubServer: env.GITHUB_SERVER, 
                           githubRepo: "${env.GITHUB_ACCOUNT}/${env.GITHUB_REPO}") {
                    script {
                        sh ". $VENV/bin/activate && python model_preparation.py"
                    }
                }
            }
        }

        // ===============================
        stage('Model Testing') {
            steps {
                withChecks(name: 'Model Testing', includeStage: true, 
                           githubServer: env.GITHUB_SERVER, 
                           githubRepo: "${env.GITHUB_ACCOUNT}/${env.GITHUB_REPO}") {
                    script {
                        try {
                            def output = sh(
                                script: ". $VENV/bin/activate && python model_testing.py",
                                returnStdout: true
                            ).trim()

                            echo output
                            env.PIPELINE_LOG = output.take(4000)

                            // Ищем RMSE в логах
                            def matcher = (output =~ /rmse=([0-9.]+)/)
                            env.RMSE = matcher ? matcher[0][1] : "unknown"

                        } catch (e) {
                            env.RMSE = "error"
                            env.PIPELINE_LOG = "Execution failed"
                            error("Model Testing failed")
                        }
                    }
                }
            }
        }

        // ===============================
        stage('Publish ML Pipeline Check') {
            steps {
                script {
                    def rmseValue = (env.RMSE.isNumber()) ? env.RMSE.toFloat() : null
                    def conclusion = 'SUCCESS'

                    if (rmseValue == null || env.RMSE == "error") {
                        conclusion = 'FAILURE'
                    } else if (rmseValue > 1.0) { // threshold RMSE
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
                                  githubServer: env.GITHUB_SERVER,
                                  githubRepo: "${env.GITHUB_ACCOUNT}/${env.GITHUB_REPO}",
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
                          githubServer: env.GITHUB_SERVER,
                          githubRepo: "${env.GITHUB_ACCOUNT}/${env.GITHUB_REPO}",
                          conclusion: 'FAILURE'
        }

        always {
            echo "Pipeline finished"
        }
    }
}
