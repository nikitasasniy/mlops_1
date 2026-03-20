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
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: 'main']],
                    userRemoteConfigs: [[
                        url: "https://github.com/${env.GITHUB_ACCOUNT}/${env.GITHUB_REPO}.git"
                    ]]
                ])
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

        stage('Data creation & preprocessing') {
            steps {
                sh ". $VENV/bin/activate && python data_creation.py"
                sh ". $VENV/bin/activate && python data_preprocessing.py"
            }
        }

        stage('Model training & testing') {
            steps {
                sh ". $VENV/bin/activate && python model_preparation.py"
                sh '''
                mkdir -p reports
                . $VENV/bin/activate && python model_testing.py > reports/model_testing_output.txt
                '''
            }
        }

        stage('Archive reports') {
            steps {
                archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
            }
        }

        stage('Publish to GitHub') {
            steps {
                withCredentials([string(credentialsId: 'github-token-id', variable: 'GITHUB_TOKEN')]) {
                    // Здесь токен НЕ подставляется в GString, а shell сам использует переменную
                    sh '''
                    curl -s -X POST \
                        -H "Authorization: token $GITHUB_TOKEN" \
                        -H "Accept: application/vnd.github+json" \
                        https://api.github.com/repos/${GITHUB_ACCOUNT}/${GITHUB_REPO}/commits/${GIT_COMMIT}/comments \
                        -d '{"body":"✅ Jenkins build finished successfully. Все отчеты в reports/"}'
                    '''
                }
            }
        }

    }

    post {
        always {
            echo "Pipeline finished. Отчеты и графики опубликованы в GitHub к последнему коммиту."
        }
    }
}
