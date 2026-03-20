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

        stage('Model testing & reports') {
            steps {
                script {
                    sh "mkdir -p ${REPORT_DIR}"
                    def output = sh(script: ". $VENV/bin/activate && python model_testing.py", returnStdout: true).trim()
                    writeFile file: "${REPORT_DIR}/model_testing_output.txt", text: output
                    archiveArtifacts artifacts: "${REPORT_DIR}/**", allowEmptyArchive: true
                }
            }
        }

        stage('Publish to GitHub') {
            steps {
                withCredentials([string(credentialsId: 'github-token-id', variable: 'GITHUB_TOKEN')]) {
                    script {
                        // Минимальный Check
                        sh """
                        gh api repos/${GITHUB_ACCOUNT}/${GITHUB_REPO}/check-runs \
                          -H "Authorization: token \$GITHUB_TOKEN" \
                          -F name="Jenkins CI" \
                          -F head_sha=${GIT_COMMIT} \
                          -F status="completed" \
                          -F conclusion="success" \
                          -F output.title="Build & Tests" \
                          -F output.summary="✅ Jenkins build finished successfully. Reports archived."
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Jenkins артефакты доступны, GitHub Check создан."
        }
    }
}
