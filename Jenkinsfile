// Necessary plugins:
// - Docker
//
pipeline {
    agent any
    environment {
        IMAGE_BASE = "tele_bot"
        IMAGE_TAG = "v$BUILD_NUMBER"
        IMAGE_NAME = "${env.IMAGE_BASE}:${env.IMAGE_TAG}"
        }
    stages {
        stage('clone repo') {
            steps {
                checkout([
                    $class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    doGenerateSubmoduleConfigurations: false, 
                    extensions: [[$class: 'CleanCheckout']], 
                    submoduleCfg: [], 
                    userRemoteConfigs: [[credentialsId: 'git_credentials', url: 'git@github.com:ei-roslyakov/tele-boot.git']]
                ])
            }
        }
        stage('build image') {
            steps {
                script {
                    def TeleBot = docker.build("${env.IMAGE_BASE}:${env.IMAGE_TAG}", ".")
                    TeleBot.tag("latest")
                }
            }
        }
        stage('run image') {
            steps {
                withCredentials([string(credentialsId: 'telebot_api_token', variable: 'TOKEN')]) {
                    sh "docker stop ${env.IMAGE_BASE} | true"
                    sh "docker rm ${env.IMAGE_BASE} | true"
                    sh "docker run -d --restart unless-stopped --name ${env.IMAGE_BASE} -e 'SECRET_TOKEN=$TOKEN' -t ${env.IMAGE_BASE}:${env.IMAGE_TAG}"
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
