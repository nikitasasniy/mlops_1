pipeline {
    agent any

    environment {
        VENV = ".venv"
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
                sh '''
                . $VENV/bin/activate
                python data_creation.py
                '''
            }
        }

        stage('Data preprocessing') {
            steps {
                sh '''
                . $VENV/bin/activate
                python data_preprocessing.py
                '''
            }
        }

        stage('Model training') {
            steps {
                sh '''
                . $VENV/bin/activate
                python model_preparation.py
                '''
            }
        }

        stage('Model testing') {
            steps {
                sh '''
                . $VENV/bin/activate
                python model_testing.py
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline finished successfully"
        }
        failure {
            echo "Pipeline failed"
        }
    }
}
