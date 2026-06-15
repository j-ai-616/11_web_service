create user 'django'@'%' identified by 'django';

-- utf8mb4: 한글/이모지까지 저장 가능한 문자셋
-- utf8mb4_general_ci: 대소문자를 구별하지 않는 문자셋 비교/정렬 방식
create database djangodb CHARACTER set utf8mb4 collate utf8mb4_general_ci;

grant all privileges on djangodb.* to 'django'@'%';