pipeline {
    agent any

    environment {
        VENV = ".venv"
        GITHUB_REPO = 'mlops_1'
        GITHUB_ACCOUNT = 'nikitasasniy'
        GITHUB_TOKEN = credentials('github-token-id') // Jenkins credentials ID с PAT
        ARTIFACT_BRANCH = 'jenkins-artifacts'
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
                sh ". $VENV/bin/activate && python data_creation.py && python data_preprocessing.py"
            }
        }

        stage('Model training & testing') {
            steps {
                sh ". $VENV/bin/activate && python model_preparation.py && python model_testing.py"
            }
        }

        stage('Publish reports to GitHub') {
            steps {
                script {
                    sh '''
                    # Настроим git для пуша артефактов
                    git config user.name "Jenkins CI"
                    git config user.email "jenkins@example.com"

                    # Создаём отдельную ветку для артефактов
                    git checkout -B ${ARTIFACT_BRANCH}

                    # Создаём папку reports, если ещё нет
                    mkdir -p reports

                    # Копируем артефакты в папку reports
                    cp -r lab1/*.png reports/ 2>/dev/null || true
                    cp -r lab1/*.txt reports/ 2>/dev/null || true

                    # Добавляем файлы и пушим
                    git add reports
                    git commit -m "Jenkins artifacts for commit ${GIT_COMMIT}" || echo "Nothing to commit"
                    git push https://${GITHUB_ACCOUNT}:${GITHUB_TOKEN}@github.com/${GITHUB_ACCOUNT}/${GITHUB_REPO}.git ${ARTIFACT_BRANCH} --force
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Все отчеты и графики опубликованы в ветке ${ARTIFACT_BRANCH}."
        }
    }
}
