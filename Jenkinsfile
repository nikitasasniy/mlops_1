pipeline {
    agent any

    environment {
        VENV = ".venv"
        GITHUB_REPO = 'mlops_1'              // имя репозитория
        GITHUB_ACCOUNT = 'nikitasasniy'      // GitHub username
        GITHUB_CREDENTIALS = 'github-token-id' // Jenkins credentials ID с PAT (Secret text)
    }

    stages {
        stage('Checkout') {
            steps {
                git(
                    url: "https://github.com/${env.GITHUB_ACCOUNT}/${env.GITHUB_REPO}.git",
                    branch: 'main',
                    credentialsId: env.GITHUB_CREDENTIALS
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
                . $VENV/bin/activate
                pip install --upgrade pip --quiet
                pip install -r req.txt --quiet
                '''
            }
        }

        stage('Data creation') {
            steps {
                sh ". $VENV/bin/activate && python data_creation.py"
            }
        }

        stage('Data preprocessing') {
            steps {
                sh ". $VENV/bin/activate && python data_preprocessing.py"
            }
        }

        stage('Model training') {
            steps {
                sh ". $VENV/bin/activate && python model_preparation.py"
            }
        }

        stage('Model Testing') {
            steps {
                script {
                    def output = sh(script: ". $VENV/bin/activate && python model_testing.py", returnStdout: true).trim()
                    def rmseLine = output.readLines().find { it.contains('rmse=') }
                    def rmse = rmseLine?.split('=')[1]?.trim() ?: "N/A"
                    echo "Test RMSE: ${rmse}"

                    env.RMSE = rmse
                }
            }
        }
    }

    post {
        success {
            script {
                // GitHub Checks Plugin
                githubChecks(
                    status: 'COMPLETED',
                    conclusion: 'SUCCESS',
                    checkName: 'ML Model Test',
                    description: "Test RMSE: ${env.RMSE}",
                    githubCredentialsId: env.GITHUB_CREDENTIALS,
                    commit: env.GIT_COMMIT,
                    repo: env.GITHUB_REPO,
                    owner: env.GITHUB_ACCOUNT
                )
            }
        }
        failure {
            script {
                githubChecks(
                    status: 'COMPLETED',
                    conclusion: 'FAILURE',
                    checkName: 'ML Model Test',
                    description: "Pipeline failed",
                    githubCredentialsId: env.GITHUB_CREDENTIALS,
                    commit: env.GIT_COMMIT,
                    repo: env.GITHUB_REPO,
                    owner: env.GITHUB_ACCOUNT
                )
            }
        }
    }
}
