pipeline {
  environment {
    DB_NAME = 'test_api'
    CI      = 'true'
  }

  agent {
    docker {
      alwaysPull true
      image "bellti9er/database-migration-build"
      args "-e MYSQL_PASSWORD=test --entrypoint=''"
    }
  }

  stages {

    stage("1. Environment Setup") {
      steps {
        echo "============Initialzing Docker Env================"

        withCredentials([usernamePassword(credentialsId: 'DockerHubCredentials', passwordVariable: 'DOCKER_HUB_PASS', usernameVariable: 'DOCKER_HUB_USER')]) {
          sh """
            echo "${DOCKER_HUB_PASS}" | docker login -u ${DOCKER_HUB_USER} --password-stdin
          """
        }
      }
    } 

    stage("2. Database Setup") {
      steps {
        echo "============Initialzing Database================"
        
        sh """
          sudo cat /etc/mysql/my.cnf
          
          sudo service mysql start
          
          sudo mysql -uroot -e "UPDATE mysql.user SET authentication_string=PASSWORD('test') WHERE User='root'; FLUSH PRIVILEGES;"
          sudo mysql -uroot -e "CREATE USER 'jenkins'@'%' IDENTIFIED BY 'test';"
          sudo mysql -uroot -e "GRANT ALL PRIVILEGES ON *.* to 'jenkins'@'%' IDENTIFIED BY 'test'; FLUSH PRIVILEGES;"
          
          sudo mysql -ujenkins -ptest -e "CREATE DATABASE api_test;"
          
          python3.8 -mpip install -r requirements.txt
        """
        
        withCredentials([sshUserPrivateKey(credentialsId: 'bellti9er_ssh', keyFileVariable: 'id_rsa')]) {
          sh """
            mkdir -p ~/.ssh
            cp ${id_rsa} ~/.ssh/id_rsa
            echo 'Host *\n    StrictHostKeyChecking no' > ~/.ssh/config
          """
        }
      }
    }

    stage('3. Staging DB Migration Apply') {
      when {
        branch 'develop'
      }
      
      steps {
        echo "============Deploying For Staging================"
        
        withCredentials([string(credentialsId: 'staging-database', variable: 'secret')]) {
          script {
            def creds = readJSON text: secret
            
            env.DB_USER     = creds['username']
            env.DB_PASSWORD = creds['password']
            env.DB_HOST     = creds['host']
            env.DB_PORT     = creds['port']
          }
          
          sh """
            ~/.local/bin/yoyo apply -v -b --database "mysql://${env.DB_USER}:${env.DB_PASSWORD}@${env.DB_HOST}:3306/staging_${DB_NAME}?charset=utf8mb4"
          """
        }
      }
    }

  }
  
  post {
    always {
      cleanWs()
      dir("${env.WORKSPACE}@tmp") {
        deleteDir()
      }
    }
  }

}
