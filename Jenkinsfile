pipeline {
    agent any

    environment {
        VENV = ".venv"
        GITHUB_REPO = 'mlops_1'
        GITHUB_ACCOUNT = 'nikitasasniy'
        REPORT_DIR = "reports"
    }

    stages {
        stage('Checkout') {
            steps {
                git(
                    url: "https://github.com/${env.GITHUB_ACCOUNT}/${GITHUB_REPO}.git",
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

        stage('Model training') {
            steps {
                sh ". $VENV/bin/activate && python model_preparation.py"
            }
        }

        stage('Model testing & reporting') {
            steps {
                script {
                    // Создаем папку для отчетов заранее
                    sh "mkdir -p ${REPORT_DIR}"

                    // Запуск тестирования и сохранение stdout
                    def output = sh(script: ". $VENV/bin/activate && python model_testing.py", returnStdout: true).trim()
                    writeFile file: "${REPORT_DIR}/model_testing_output.txt", text: output

                    // Парсинг RMSE
                    def rmseLine = output.split('\n').find { it.toLowerCase().contains('rmse') }
                    def rmse = rmseLine?.split(':')[-1]?.trim() ?: "N/A"
                    writeFile file: "${REPORT_DIR}/rmse.txt", text: rmse

                    echo "Test RMSE: ${rmse}"

                    // Архивируем все отчеты и графики
                    archiveArtifacts artifacts: "${REPORT_DIR}/**", allowEmptyArchive: true
                }
            }
        }

        stage('Publish to GitHub') {
            steps {
                withCredentials([string(credentialsId: 'github-token-id', variable: 'GITHUB_TOKEN')]) {
                    script {
                        // Собираем все отчеты и метрики в Markdown
                        def reportFiles = sh(script: "ls ${REPORT_DIR}", returnStdout: true).trim().split("\n")
                        def reportBody = "## ✅ Build Reports & Metrics\n\n"
                        reportBody += "| File | Link |\n|---|---|\n"
                        reportFiles.each { f ->
                            reportBody += "| ${f} | [artifact](${env.BUILD_URL}artifact/${REPORT_DIR}/${f}) |\n"
                        }

                        // Публикация комментария на последний коммит через GH API
                        sh '''
                        gh api repos/${GITHUB_ACCOUNT}/${GITHUB_REPO}/commits/${GIT_COMMIT}/comments \
                          -H "Authorization: token $GITHUB_TOKEN" \
                          -f body="$reportBody"
                        '''
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
