from django.db import models

# 상품 모델
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# 상품 할인 정보 - 1:1 관계
class Discount(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='discount'
    )
    discount_percentage = models.DecimalField(
        max_digits=5,       # 전체 자리수
        decimal_places=2,   # 소수점 이하 자리수
        help_text='Discount rate (e.g. 0.20 for 20%)'    
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f'{self.discount_percentage}% off for {self.product.name}'


# 상품 리뷰 - 1:N 관계
class Review(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,   # 상품 삭제 시 리뷰도 삭제 (삭제 룰)
        related_name='reviews'      # Product에서 product.reviews로 참조
    )
    # ORM스러운 방식은 아니지만 여기서는 간단히 표현(user 객체 참조 대신)
    user_id = models.PositiveIntegerField(blank=True, null=True)
    rating = models.PositiveIntegerField(default=1, help_text='Rating from 1 to 5')
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.product.name} by {self.user_id}'

# 상품 카테고리 - N:M 관계
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    products = models.ManyToManyField(
        Product,
        related_name='categories',
        blank=True
    )

    def __str__(self):
        return self.name