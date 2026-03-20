pipeline {
    agent any

    environment {
        VENV = ".venv"  /* путь к виртуальному окружению */
        GITHUB_REPO = 'user/repo'           // заменить на свой репозиторий
        GITHUB_ACCOUNT = 'github-account'   // GitHub username/organization
        GITHUB_CREDENTIALS = 'github-token-id' // Jenkins credentials ID с PAT
    }

    stages {

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
        stage('Check credentials') {
            steps {
                script {
                    echo "Credentials ID: ${env.GITHUB_CREDENTIALS}"
        }
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
                    repo: env.GITHUB_REPO,
                    account: env.GITHUB_ACCOUNT,
                    credentialsId: env.GITHUB_CREDENTIALS,
                    sha: env.GIT_COMMIT
                )
            }
        }
        failure {
            script {
                githubNotify(
                    context: 'ML Model Test',
                    status: 'FAILURE',
                    description: "Pipeline failed",
                    repo: env.GITHUB_REPO,
                    account: env.GITHUB_ACCOUNT,
                    credentialsId: env.GITHUB_CREDENTIALS,
                    sha: env.GIT_COMMIT
                )
            }
        }
    }
}
