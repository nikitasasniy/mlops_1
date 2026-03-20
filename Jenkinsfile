pipeline {
    agent any

    environment {
        SCRIPT = "run_pipeline.sh"
    }

    stages {
        stage('Checkout') {
            steps {
                git(
                    url: "https://github.com/nikitasasniy/mlops_1.git",
                    branch: 'main'
                )
            }
        }

        stage('Run ML Pipeline') {
            steps {
                script {
                    try {
                        sh "chmod +x ${env.SCRIPT}"

                        def output = sh(
                            script: "./${env.SCRIPT}",
                            returnStdout: true
                        ).trim()

                        echo output

                        env.PIPELINE_LOG = output.take(4000)

                        def matcher = (output =~ /rmse=([0-9.]+)/)
                        env.RMSE = matcher ? matcher[0][1] : "unknown"

                    } catch (e) {
                        env.PIPELINE_LOG = "Pipeline failed"
                        env.RMSE = "error"
                        error("Execution failed")
                    }
                }
            }
        }

        stage('Publish Checks') {
            steps {
                script {
                    publishChecks name: 'ML Pipeline',
                        title: "ML Pipeline Results",
                        summary: "RMSE: ${env.RMSE}",
                        text: """
Logs:

${env.PIPELINE_LOG}
""",
                        detailsURL: env.BUILD_URL,
                        conclusion: currentBuild.currentResult
                }
            }
        }
    }
}
