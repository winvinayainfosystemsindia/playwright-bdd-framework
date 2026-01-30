pipeline {
    agent {
        docker {
            image 'mcr.microsoft.com/playwright/python:v1.40.0-jammy'
            args '-u root:root'
        }
    }
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'qa', 'prod'], description: 'Environment to test')
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit', 'all'], description: 'Browser to use')
        choice(name: 'TEST_SUITE', choices: ['smoke', 'regression', 'all'], description: 'Test suite to run')
        booleanParam(name: 'PARALLEL', defaultValue: true, description: 'Run tests in parallel')
    }
    
    environment {
        PYTHON_VERSION = '3.11'
        HEADLESS = 'true'
        SLACK_CHANNEL = '#test-automation'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1'
            }
        }
        
        stage('Setup') {
            steps {
                sh '''
                    python --version
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    playwright install ${BROWSER == 'all' ? 'chromium firefox webkit' : BROWSER}
                '''
            }
        }
        
        stage('Code Quality') {
            parallel {
                stage('Black') {
                    steps {
                        sh 'black --check --diff . || true'
                    }
                }
                stage('Flake8') {
                    steps {
                        sh 'flake8 . || true'
                    }
                }
                stage('Pylint') {
                    steps {
                        sh 'pylint pages/ utils/ config/ || true'
                    }
                }
                stage('Bandit') {
                    steps {
                        sh 'bandit -r pages/ utils/ config/ -f json -o reports/bandit-report.json || true'
                    }
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    def marker = params.TEST_SUITE == 'all' ? '' : "-m ${params.TEST_SUITE}"
                    def parallel = params.PARALLEL ? '-n auto' : ''
                    
                    if (params.BROWSER == 'all') {
                        parallel {
                            stage('Chromium') {
                                steps {
                                    sh """
                                        ENVIRONMENT=${params.ENVIRONMENT} BROWSER=chromium \
                                        pytest ${marker} ${parallel} \
                                        --alluredir=reports/allure-results/chromium \
                                        --html=reports/report-chromium.html \
                                        --self-contained-html -v
                                    """
                                }
                            }
                            stage('Firefox') {
                                steps {
                                    sh """
                                        ENVIRONMENT=${params.ENVIRONMENT} BROWSER=firefox \
                                        pytest ${marker} ${parallel} \
                                        --alluredir=reports/allure-results/firefox \
                                        --html=reports/report-firefox.html \
                                        --self-contained-html -v
                                    """
                                }
                            }
                            stage('WebKit') {
                                steps {
                                    sh """
                                        ENVIRONMENT=${params.ENVIRONMENT} BROWSER=webkit \
                                        pytest ${marker} ${parallel} \
                                        --alluredir=reports/allure-results/webkit \
                                        --html=reports/report-webkit.html \
                                        --self-contained-html -v
                                    """
                                }
                            }
                        }
                    } else {
                        sh """
                            ENVIRONMENT=${params.ENVIRONMENT} BROWSER=${params.BROWSER} \
                            pytest ${marker} ${parallel} \
                            --alluredir=reports/allure-results \
                            --html=reports/report.html \
                            --self-contained-html -v
                        """
                    }
                }
            }
        }
        
        stage('Generate Reports') {
            steps {
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'reports/allure-results']]
                    ])
                }
            }
        }
    }
    
    post {
        always {
            // Archive test results
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
            
            // Publish HTML reports
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report*.html',
                reportName: 'Test Report'
            ])
            
            // Publish test results
            junit testResults: 'reports/junit/*.xml', allowEmptyResults: true
            
            // Clean workspace
            cleanWs()
        }
        
        success {
            slackSend(
                channel: env.SLACK_CHANNEL,
                color: 'good',
                message: "✅ Tests PASSED - ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
            )
        }
        
        failure {
            slackSend(
                channel: env.SLACK_CHANNEL,
                color: 'danger',
                message: "❌ Tests FAILED - ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
            )
            
            emailext(
                subject: "Test Failure: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <p>Test execution failed.</p>
                    <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                    <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                    <p><strong>Environment:</strong> ${params.ENVIRONMENT}</p>
                    <p><strong>Browser:</strong> ${params.BROWSER}</p>
                    <p><a href="${env.BUILD_URL}">View Build</a></p>
                """,
                to: '${DEFAULT_RECIPIENTS}',
                mimeType: 'text/html'
            )
        }
        
        unstable {
            slackSend(
                channel: env.SLACK_CHANNEL,
                color: 'warning',
                message: "⚠️ Tests UNSTABLE - ${env.JOB_NAME} #${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
            )
        }
    }
}
