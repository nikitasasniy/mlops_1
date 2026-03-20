pipeline {
    agent any

    environment {
        VENV = ".venv"
        GITHUB_REPO = 'mlops_1'               // имя репозитория
        GITHUB_ACCOUNT = 'nikitasasniy'       // GitHub username
        GITHUB_TOKEN = credentials('github-token-id') // Jenkins credentials ID с PAT
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
                    // Получаем SHA последнего коммита
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
                    def rmseLine = output.split('\n').find { it.toLowerCase().contains('rmse') }
                    def rmse = rmseLine?.split('=')[-1]?.trim() ?: "N/A"
        
                    echo "Test RMSE: ${rmse}"
        
                    writeFile file: 'rmse.txt', text: rmse
                    archiveArtifacts artifacts: 'rmse.txt', allowEmptyArchive: true
        
                    // Публикация безопасно через withEnv
                    withEnv(["GITHUB_TOKEN=${GITHUB_TOKEN}"]) {
                        sh '''
                        . $VENV/bin/activate
                        gh auth login --with-token
                        gh api repos/${GITHUB_ACCOUNT}/${GITHUB_REPO}/commits/${GIT_COMMIT}/comments -f body="✅ Test RMSE: '${rmse}'"
                        '''
                    }
                }
            }
        }

    post {
        always {
            echo "Pipeline finished. RMSE сохранён в rmse.txt и комментарий добавлен к последнему коммиту."
        }
    }
}
