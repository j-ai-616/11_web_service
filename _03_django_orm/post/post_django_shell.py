# python manage.py shell
# import os; os.system('cls')

from post.models import Post

print(Post) # <class 'post.models.Post'>
print(Post.objects) # <django.db.models.manager.Manager object at 0x0000020A97852FC0>
print(Post.objects.all()) # <QuerySet []>

### post 생성 ###
post = Post.objects.create(title='Hello world', content='🍭🍭🍭')
post 
post.id 
post.title 
post.content 
post.created_at 
post.updated_at 

# 메모리에서 객체를 생성한 후 save() 메소드를 호출하여 데이터베이스에 저장하는 방법도 있다.
post2 = Post(title='배고프다', content='춥고 배고프다')
post2.save() # None 반환
post2.id
post2.title
post2.content
post2.created_at
post2.updated_at

# 검색 조건 확인을 위한 추가 데이터
post3 = Post.objects.create(title='Happy New Year 2026', content='🤖🤖🤖')
post4 = Post.objects.create(title='I am so happy!', content='😊😊😊')
post5 = Post.objects.create(title='Django ORM Practice', content='filter, get, order_by 연습용 게시글')
post6 = Post.objects.create(title='수정 테스트 게시글', content='처음 저장된 내용')

# updated_at 비교 실습을 위해 한 번 수정한다.
post6.content = '수정된 내용'
post6.save()

### post 조회 ###
queryset = Post.objects.all()
queryset 

# 쿼리 확인
# 1.queryset.query
queryset.query # <django.db.models.sql.query.Query object at 0x0000020A96634AA0>
str(queryset.query)
# 'SELECT `post_post`.`id`, `post_post`.`title`, `post_post`.`content`, `post_post`.`created_at`, `post_post`.`updated_at` FROM `post_post`'

import sqlparse
print(sqlparse.format(str(queryset.query), reindent=True))
# SELECT `post_post`.`id`,
# `post_post`.`title`,
# `post_post`.`content`,
# `post_post`.`created_at`,
# `post_post`.`updated_at`
# FROM `post_post`

# 2.connection.queries
from django.db import connection

connection.queries # 실행된 모든 쿼리 출력
connection.queries[-1] # 마지막 쿼리

# where 조건검색
# 1. filter
# 2. exclude
# 3. get

# 특정 조건에 맞는 데이터 필터링
# - filter: 조건에 맞는 객체들을 QuerySet으로 반환, 0개 이상의 객체 반환 가능
# - get: 조건에 맞는 객체를 하나만 반환, 0개 또는 2개 이상의 객체 반환시 오류 발생
Post.objects.filter(title='배고프다') # <QuerySet [<Post: 배고프다>]>
Post.objects.get(title='배고프다') # <Post: 배고프다>

# 문자열 필드
Post.objects.filter(title='Hello world') # <QuerySet [<Post: Hello world>]>
Post.objects.filter(title__startswith='Hello') # <QuerySet [<Post: Hello world>]>
Post.objects.filter(title__endswith='!') # <QuerySet [<Post: I am so happy!>]>
Post.objects.filter(content__contains='🍭') # <QuerySet [<Post: Hello world>]>
Post.objects.filter(title__icontains='happy') # 대소문자구분 없음  <QuerySet [<Post: Happy New Year 2026>, <Post: I am so happy!>]>
Post.objects.filter(content__isnull=True) # <QuerySet []>

# 날짜필드
from django.utils import timezone
from datetime import timedelta

now = timezone.now()
tomorrow = now + timedelta(days=1)
yesterday = now - timedelta(days=1)

Post.objects.filter(created_at__lte=tomorrow) # 오늘 생성된 게시글 포함
Post.objects.filter(created_at__gt=yesterday) # 어제 이후 생성된 게시글
Post.objects.filter(created_at__year=now.year) # 올해 생성된 게시글

# 여러 조건 AND
Post.objects.filter(title='Hello world', created_at__year=now.year) # <QuerySet [<Post: Hello world>]>
Post.objects.filter(title='Hello world').filter(created_at__year=now.year) # <QuerySet [<Post: Hello world>]>

# 여러 조건 OR (Q 객체 필요)
from django.db.models import Q
Post.objects.filter(Q(title__icontains='happy') | Q(content__contains='🍭')) # <QuerySet [<Post: Hello world>, <Post: Happy New Year 2026>, <Post: I am so happy!>]>

# NOT 비교
# - exclude
# - filter(~Q())

# 같은 행의 다른 컬럼 비교시 F객체 사용
from django.db.models import F 
Post.objects.exclude(created_at=F('updated_at')) # 수정된 게시글 조회
Post.objects.filter(~Q(created_at=F('updated_at'))) # 수정된 게시글 조회

# 정렬
Post.objects.all().order_by('created_at')
Post.objects.all().order_by('-created_at')
Post.objects.all().order_by('title', 'id')

# 한행 조회 get
# 주로 pk컬럼 조회에 사용. 0행 또는 n행 반환시 오류
Post.objects.get(id=post.id) # <Post: Hello world>
Post.objects.get(id=100) # post.models.Post.DoesNotExist: Post matching query does not exist.
Post.objects.filter(id=post.id) # <QuerySet [<Post: Hello world>]>

# 기존 Post객체와 새롭게 질의후 반환받은 객체와 내용(pk)비교
post = Post.objects.get(id=post2.id)
# `__eq__` 내부적으로 호출, 재정의 하지않은 `__eq__`는 id함수값을 비교한다.
# Model클라스는 `__eq__`를 pk비교하도록 오버라이드함.
post == Post.objects.get(id=post2.id) # True
Post.objects.get(id=post2.id) is post # False
id(Post.objects.get(id=post2.id)), id(post)

# values
# - Model.objects.values(*fields)
# - values 메소드는 Django ORM에서 특정 필드만 선택해 쿼리셋을 생성할 때 사용한다.
# - 이를 활용하면 모델 객체 대신 필드 이름과 값으로 구성된 딕셔너리 형태의 쿼리셋을 반환한다.
Post.objects.values('title', 'content')
Post.objects.values() # 모든 필드를 key-value로 반환
Post.objects.values('title', 'content').distinct() # 중복값 제거

# values + annotate -> group by
from django.db.models.functions import ExtractYear
from django.db.models import Count
# 게시글을 작성 연도별로 묶고, 각 연도에 게시글이 몇 개 있는지 세어본다.
Post.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count_by_year=Count('year'))


#### post 수정 ####
post = Post.objects.get(id=post.id)
post.title # '배고프다'
post.title += '123'
post.title # '배고프다123'
post.save()


#### post 삭제 ####
post = Post.objects.create(title='Delete me!', content='It was nice to have you!')
post.delete() # (1, {'post.Post': 1})