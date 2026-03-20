pipeline {
    agent any

    environment {
        VENV = ".venv"
        GITHUB_REPO = 'mlops_1'
        GITHUB_ACCOUNT = 'nikitasasniy'
        GITHUB_TOKEN = credentials('github-token-id')
        REPORT_DIR = "reports"
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
                sh ". $VENV/bin/activate && python data_creation.py"
                sh ". $VENV/bin/activate && python data_preprocessing.py"
            }
        }

        stage('Model training & testing') {
            steps {
                sh ". $VENV/bin/activate && python model_preparation.py"
                sh ". $VENV/bin/activate && python model_testing.py > $REPORT_DIR/model_testing_output.txt"
            }
        }

        stage('Archive reports') {
            steps {
                // Сохраняем артефакты (метрики, графики)
                archiveArtifacts artifacts: "${REPORT_DIR}/**", allowEmptyArchive: true
            }
        }

        stage('Publish to GitHub') {
            steps {
                script {
                    // Собираем все отчеты и метрики в Markdown
                    def reportFiles = sh(script: "ls ${REPORT_DIR}", returnStdout: true).trim().split("\n")
                    def reportBody = "## ✅ Build Reports & Metrics\n\n"
                    reportBody += "| File | Link |\n|---|---|\n"
                    reportFiles.each { f ->
                        reportBody += "| ${f} | [artifact](${env.BUILD_URL}artifact/${REPORT_DIR}/${f}) |\n"
                    }

                    // Публикация комментария
                    withEnv(["GITHUB_TOKEN=${GITHUB_TOKEN}"]) {
                        sh """
                        . $VENV/bin/activate
                        gh api repos/${GITHUB_ACCOUNT}/${GITHUB_REPO}/commits/${GIT_COMMIT}/comments \
                            -H "Authorization: token $GITHUB_TOKEN" \
                            -f body="$reportBody"
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Все отчеты и графики опубликованы в GitHub к последнему коммиту."
        }
    }
}
