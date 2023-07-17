# database-migration-template

- database migration files의 형상 관리를 위한 레포지토리가 필요하며 MSA 구조에서는 각 service별로 관리되는 database-migration repo가 필요하기 때문에 해당 repo는 템플릿으로 활용됩니다.
- Jenkinsfile이 작성되어 있어 각 database 별로 작성된 파일들을 통해 migration이 될 때, 이를 통해 빌드, 배포 및 테스트와 같은 작업을 자동화합니다.

