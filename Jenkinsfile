pipeline {
    agent any

    environment {
        GITHUB_REPO = 'mlops_1'
        GITHUB_ACCOUNT = 'nikitasasniy'
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

        stage('Post GitHub comment') {
            steps {
                withCredentials([string(credentialsId: 'github-token-id', variable: 'GITHUB_TOKEN')]) {
                    sh """
                    gh api repos/${GITHUB_ACCOUNT}/${GITHUB_REPO}/commits/${GIT_COMMIT}/comments \
                      -H "Authorization: token \$GITHUB_TOKEN" \
                      -f body="success"
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Проверка публикации на GitHub завершена."
        }
    }
}
