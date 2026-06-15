from product.models import Product, Category, Discount, Review
from django.db.models import Sum, Avg, Count, Max, Min
from datetime import timedelta
from django.utils import timezone

### 1:N Product-Review ###
# 1. 특정 제품(Product)의 모든 리뷰 가져오기
reviews = Review.objects.filter(product_id=1)   
for review in reviews:
    print(review.id, review.product, review.user_id, review.rating, review.comment)

product = Product.objects.get(id=1)
Review.objects.filter(product=product)

product.reviews # <django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager object at 0x0000024A37C019D0>
product.reviews.all()

# 2. 특정 제품(Product)의 평균 평점과 리뷰 개수 가져오기
product = Product.objects.get(id=1)
average_rating = product.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] # 4.0
review_count = product.reviews.count() # 4

# ORM이 생성한 SQL 쿼리 확인하기
from django.db import connection
connection.queries[-1]['sql']
import sqlparse
print(sqlparse.format(connection.queries[-1]['sql'], reindent=True))

# 3. 평점이 높은 리뷰(예: 4점 이상)만 가져오기
high_rating_reviews = product.reviews.filter(rating__gte=4)
for review in high_rating_reviews:
    print(f"[High Rating] User ID: {review.user_id}, Rating: {review.rating}, Comment: {review.comment}")

# 4. 모든 제품의 평균 평점과 리뷰 개수 가져오기
# annotate는 각 Product 객체에 avg_rating과 review_count 필드를 추가한다.
products_with_review_data = Product.objects.annotate(       
    avg_rating=Avg('reviews__rating'),
    review_count=Count('reviews')
)
for product in products_with_review_data:
    avg_rating = f"{product.avg_rating:.2f}" if product.avg_rating else "0"
    print(f"Product: {product.name}, Average Rating: {avg_rating}, Reviews: {product.review_count}")

# 5. 특정 기간 동안 작성된 리뷰 가져오기
start_date = timezone.now() - timedelta(weeks=1) # seconds, microseconds, milliseconds, minutes, hours, weeks
end_date = timezone.now()
reviews = Review.objects.filter(created_at__range=(start_date, end_date))
for review in reviews:
    print(review.id, review.product, review.user_id, review.rating, review.comment, review.created_at)


### 1:1 Product-Discount ###
# 1. 특정 제품(Product)의 할인 정보 가져오기
product_id = 3
# discount가 존재하지 않는 product의 경우 Discount.DoesNotExist 예외 발생
try:
    discount = Discount.objects.get(product_id=product_id)
    print(f"Product: {discount.product.name}, Discount: {discount.discount_percentage}%, Start: {discount.start_date}, End: {discount.end_date}")
except Discount.DoesNotExist:
    print(f"Product with ID {product_id} has no discount information.")

# 2. 할인 중인 모든 제품 가져오기
current_date = timezone.now()
current_discounts = Discount.objects.filter(start_date__lte=current_date, end_date__gte=current_date)

for discount in current_discounts:
    print(f"Product: {discount.product.name}, Discount: {discount.discount_percentage}%, Ends on: {discount.end_date}")

# 3. 특정 할인율 이상인 제품 가져오기 (예: 20% 이상)
high_discounts = Discount.objects.filter(discount_percentage__gte=0.2)

for discount in high_discounts:
    print(f"[High Discount] Product: {discount.product.name}, Discount: {discount.discount_percentage}%")

# 4. 할인 정보와 함께 모든 제품 가져오기
# - prefetch_related를 통해 지연쿼리를 제한하고, 한번의 추가쿼리로 데이터를 미리 가져와 N+1 문제 해결한다.
products = Product.objects.all()
products_with_discounts = Product.objects.prefetch_related('discount')

for product in products_with_discounts:
    if hasattr(product, 'discount'):
        print(f"Product: {product.name}, Discount: {product.discount.discount_percentage}%, Ends: {product.discount.end_date}")
    else:
        print(f"Product: {product.name}, No discount available")

# 5. 할인 기간이 지난 제품 가져오기
expired_discounts = Discount.objects.filter(end_date__lt=current_date)

for discount in expired_discounts:
    print(f"[Expired Discount] Product: {discount.product.name}, Discount: {discount.discount_percentage}% (Ended on: {discount.end_date})")


### N:M Product-Category ###

# 1. 특정 제품(Product)이 속한 모든 카테고리 가져오기
product_id = 9  # 예시: 특정 Product ID
product = Product.objects.get(id=product_id)
categories = product.categories.all()

print(f"Product: {product.name} is in the following categories:")
for category in categories:
    print(f"- {category.name}")

# 2. 특정 카테고리(Category)에 속한 모든 제품 가져오기
category_name = "가전"  # 예시: 특정 Category 이름
try:
    category = Category.objects.get(name=category_name)
    products = category.products.all()

    print(f"Category: {category.name} contains the following products:")
    for product in products:
        print(f"- {product.name} (Price: {product.price}, Stock: {product.stock})")
except Category.DoesNotExist:
    print(f"Category '{category_name}' does not exist.")

# 3. 카테고리가 없는 제품(Product) 가져오기
products_without_category = Product.objects.filter(categories__isnull=True)

print("Products without a category:")
for product in products_without_category:
    print(f"- {product.name} (Price: {product.price}, Stock: {product.stock})")

# 4. 특정 제품(Product)에 새 카테고리 추가하기
new_category_name = "Seasonal"
new_category, created = Category.objects.get_or_create(name=new_category_name)
product.categories.add(new_category)

print(f"Added category '{new_category.name}' to product '{product.name}'.")

# 5. 모든 카테고리와 각 카테고리의 제품 수 출력하기
categories_with_product_count = Category.objects.annotate(product_count=Count('products'))

for category in categories_with_product_count:
    print(f"Category: {category.name}, Number of Products: {category.product_count}")

# 6. 여러 카테고리에 속한 제품(Product) 가져오기
multi_category_products = Product.objects.annotate(category_count=Count('categories')).filter(category_count__gt=1)

print("Products in multiple categories:")
for product in multi_category_products:
    print(f"- {product.name} (Categories: {product.categories.count()})")

### N + 1 문제 해결하기(settings.py 설정 후 테스트) ###
# - select_related: ForeignKey, OneToOneField와 같은 단일 객체 관계에서 사용한다. 
#   JOIN을 통해 관련 객체를 한번에 가져온다.
# - prefetch_related: ManyToManyField, reverse ForeignKey와 같은 다중 객체 관계에서 사용한다. 
#   별도의 쿼리를 통해 관련 객체를 미리 가져와 N+1 문제를 해결한다.

# N + 1 문제 예시 
products = Product.objects.all()
for product in products:
    # 각 Product마다 discount 정보를 가져오기 위해 추가 쿼리가 발생한다.
    if hasattr(product, 'discount'):
        print(f"Product: {product.name}, Discount: {product.discount.discount_percentage}%")
    else:
        print(f"Product: {product.name}, No discount available")

# N + 1 문제 해결(select_related 사용)
products = Product.objects.select_related('discount').all()
for product in products:
    if hasattr(product, 'discount'):
        print(f"Product: {product.name}, Discount: {product.discount.discount_percentage}%")
    else:
        print(f"Product: {product.name}, No discount available")

# N + 1 문제 예시
products = Product.objects.all()
for product in products:
    # 각 Product마다 categories 정보를 가져오기 위해 추가 쿼리가 발생한다.
    category_names = [category.name for category in product.categories.all()]  
    print(f"Product: {product.name}, Categories: {', '.join(category_names)}")

# N + 1 문제 해결(prefetch_related 사용)
products = Product.objects.prefetch_related('categories').all()
for product in products:
    category_names = [category.name for category in product.categories.all()]
    print(f"Product: {product.name}, Categories: {', '.join(category_names)}")

### 집계 처리 ###
# 1.aggregate: 모든 객체에 대한 집계 처리
Product.objects.aggregate(total_count=Count('id')) 
Product.objects.aggregate(total_price=Sum('price')) 
Product.objects.aggregate(avg_price=Avg('price')) 
Product.objects.aggregate(max_price=Max('price')) 
Product.objects.aggregate(min_price=Min('price')) 

# 2.filter + aggregate: 특정 객체에 대한 집계 처리
Product.objects.filter(categories__name='가전') # <QuerySet [<Product: LG 올레드 TV 55인치>, <Product: Dyson V12 무선청소기>, <Product: Samsung Bespoke 냉장고>]>
Product.objects.filter(categories__name='가전').aggregate(avg_price=Avg('price')) # {'avg_price': 1893000.0}

# 3. 연관관계 annotate: 모든 객체에 대한 집계 처리 후 결과를 객체에 추가
# 외래 키 관계를 따라가며 데이터를 집계
# 상품별 리뷰 개수 (select product.name, count(*) from review group by product_id)
Review.objects.values('product').annotate(review_counts=Count('id'))
# <QuerySet [{'product': 1, 'review_counts': 4}, {'product': 2, 'review_counts': 2}, {'product': 3, 'review_counts': 1}, {'product': 4, 'review_cou nts': 2}, {'product': 5, 'review_counts': 3}, {'product': 6, 'review_counts': 1}, {'product': 7, 'review_counts': 2}, {'product': 9, 'review_counts': 1}, {'product': 10, 'review_counts': 2}]>
# 역방향 조회 가능하다.
Product.objects.values('id').annotate(review_counts=Count('reviews'))
# <QuerySet [{'id': 1, 'review_counts': 4}, {'id': 2, 'review_counts': 2}, {'id': 3, 'review_counts': 1}, {'id': 4, 'review_counts': 2}, {'id': 5, 'review_counts': 3}, {'id': 6, 'review_counts': 1}, {'id': 7, 'review_counts': 2}, {'id': 8, 'review_counts': 0}, {'id': 9, 'review_counts': 1}, {'id': 10, 'review_counts': 2}]>
# 이때, values는 생략할수 있고, annotate의 집계처리된 필드만 추가된다.
products = Product.objects.annotate(review_counts=Count('reviews'))
products_with_review_counts = [(product.name, product.review_counts) for product in products]
# [('iPhone 15 Pro', 4), ('Galaxy Z Flip5', 2), ('LG 올레드 TV 55인치', 1), ('Dyson V12 무선청소기', 2), ('Nintendo Switch OLED 모델', 3), ('MacBook Air 15인치 M2', 1), ('Sony WH-1000XM5', 2), ('Canon EOS R6 Mark II', 0), ('Apple Watch Series 9', 1), ('Samsung Bespoke 냉장고', 2)]

# 카테고리별 상품개수
Category.objects.values('name').annotate(product_count=Count('products'))
# <QuerySet [{'name': '가구/인테리어', 'product_count': 3}, {'name': '가전', 'product_count': 3}, {'name': '스마트폰/태블릿', 'product_count': 4}, {'name': '스포츠/레저', 'product_count': 2}, {'name': '패션/액세서리', 'product_count': 2}, {'name': '패션/의류', 'product_count': 0}]>
Product.objects.values('categories').annotate(product_count=Count('id'))
# <QuerySet [{'categories': 2, 'product_count': 4}, {'categories': 1, 'product_count': 3}, {'categories': 3, 'product_count': 3}, {'categories': 5, 'product_count': 2}, {'categories': 6, 'product_count': 2}, {'categories': None, 'product_count': 1}]>
# values 없이, annotate만 사용해도, 연관관계를 따라가며 집계처리된다.
categories = Category.objects.annotate(product_count=Count('products'), avg_product_price=Avg('products__price'))
categories_with_info = [(cate.name, cate.product_count, cate.avg_product_price) for cate in categories]
# [('가전', 3, 1893000.0), ('스마트폰/태블릿', 4, 1332250.0), ('가구/인테리어', 3, 1893000.0), ('패션/의류', 0, None), ('스포츠/레저', 2, 509000.0), ('패션/액세서리', 2, 549000.0)]
