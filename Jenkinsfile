pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/bernakart/Streamlit_Proje.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Application') {
            steps {
                sh 'streamlit run main.py &'
            }
        }
    }
}
