### 실습문제 ###
# python manage.py shell

from product.models import Product, Review, Discount, Category
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Avg, Max

# 1. 특정 제품의 이름에 "Phone"이 포함된 제품들을 조회
products_with_phone = Product.objects.filter(name__icontains="Phone")

# 2. 특정 카테고리 이름이 "가전"인 카테고리에 속한 모든 제품을 조회
electronics_products = Product.objects.filter(categories__name="가전")

# 3. 리뷰가 없는 제품들을 조회
products_without_reviews = Product.objects.filter(reviews__isnull=True)

# 4. 평점이 4 이상인 리뷰가 달린 제품을 조회
products_with_high_reviews = Product.objects.filter(reviews__rating__gte=4).distinct()

# 5. 특정 할인율(예: 10%)보다 높은 할인을 적용받는 제품을 조회
high_discount_products = Product.objects.filter(discount__discount_percentage__gt=0.1)

# 6. 최근 2일 이내에 시작된 할인 정보를 가진 제품 조회
target_date = timezone.now() - timedelta(days=2)

products = Product.objects.filter(
    discount__start_date__gte=target_date
)

# 7. "패션"이라는 이름이 포함된 카테고리에 속한 모든 제품을 조회
fashion_products = Product.objects.filter(categories__name__icontains="패션")

# 8. 3개 이상의 카테고리에 속한 제품을 조회
multi_category_products = Product.objects.annotate(
    category_count=Count('categories', distinct=True)
).filter(category_count__gte=3)

# 9. 재고가 10이하인 제품들을 조회
low_stock_products = Product.objects.filter(stock__lte=10)

# 10. "최상"라는 단어가 설명(description)에 포함된 제품들을 조회
high_end_products = Product.objects.filter(description__icontains="최상")

# 11. 이번달에 작성된 리뷰 조회
today = timezone.localdate()

current_month_reviews = Review.objects.filter(
    created_at__year=today.year,
    created_at__month=today.month
)

# 12. 현재 할인중인 제품을 조회
# - 할인 시작 날짜와 종료 날짜 사이에 현재 날짜가 포함된 제품 조회
current_date = timezone.now()

current_discount_products = Product.objects.filter(
    discount__start_date__lte=current_date,
    discount__end_date__gte=current_date
)
# 13. 리뷰 수가 3개 이상인 제품들을 조회
products_with_many_reviews = Product.objects.annotate(
    review_count=Count('reviews')
).filter(review_count__gte=3)

# 14. 특정 사용자(user_id = 2)가 작성한 모든 리뷰를 조회
user_reviews = Review.objects.filter(user_id=2)

# 15. 평균 평점이 4.5 이상인 제품들을 조회
high_average_rating_products = Product.objects.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=4.5)

# 16. 특정 카테고리(가전)의 제품들 중 가격이 100,000원 이상인 제품을 조회
expensive_category_products = Product.objects.filter(
    categories__name="가전",
    price__gte=100000
).distinct()

# 17. 20% 이상의 할인율을 적용받는 모든 제품을 조회
products_with_high_discounts = Product.objects.filter(discount__discount_percentage__gte=0.2)

# 18. 가격이 50,000원 이상이고 재고가 10개 이상인 제품을 조회
pricey_in_stock_products = Product.objects.filter(price__gte=50000, stock__gte=10)

# 19. 5점 만점 리뷰가 하나라도 달린 제품을 조회
perfect_rating_products = Product.objects.filter(reviews__rating=5).distinct()

# 20. 가장 최근 리뷰가 작성된 제품을 조회
latest_review_date = Review.objects.aggregate(latest_date=Max('created_at'))['latest_date']
latest_reviewed_products = Product.objects.filter(reviews__created_at=latest_review_date).distinct()

for product in latest_reviewed_products:
    print(f"Product: {product.name}, Latest Review Date: {latest_review_date}")