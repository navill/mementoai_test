# MementoAI 사전 과제
- 환경 및 구성
  - 언어: python 3.10
  - 기술 스택: fastapi, mysql, celery(broker: redis), docker
- 실행 방법(docker)
  - 테스트를 위해 임의 환경변수 입력
  ```shell
    docker build --build-arg DB_USERNAME=root --build-arg DB_PASSWORD=test1234 --build-arg DB_HOST=localhost --build-arg DB_PORT=3306 --build-arg DB_NAME=mementoai_test -t mementoai_image .
    docker run -p 8000:8000 -d mementoai_image
    curl http://localhost:8000/docs # 접속
  ```
  
- 구현 내용
    - sha3-256을 이용한 url 단축키 생성
    - 요구 사항에 필요한 API 구현
    - swagger 문서화 기능 추가
    - celery를 이용한 만료 키 삭제
      - soft delete: 1시간에 한번씩 soft 삭제
      - hard delete: 매주 일요일 hard 삭제


- 데이터베이스는 mysql을 사용하였습니다. 선택한 이유는
  1. 현재 프로젝트에서 요구하는 성능을 충족함
  2. 저를 포함한 많은 사람들이 mysql에 대해 익숙하기 때문에 확장 및 문제 해결에 용이함

  