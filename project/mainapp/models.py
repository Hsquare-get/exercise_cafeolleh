from django.db import models

# Create your models here

#best9 id와 이름 테이블
class Product(models.Model):
    id=models.IntegerField(primary_key=True)
    products=models.CharField(max_length=20)

#ForeignKeyField가 바라보는 값이 삭제될 때 ForeignKeyField를 포함하는 모델 인스턴스(row)도 삭제된다.
#브랜드별 커피이름 테이블, best9의 id, 즉 Product 테이블의 primary_key와 일대일 참조, Product 테이블의 기본키 필드가 지워지면 참조하는 필드도 같이 지운다.
class Product_Bybrand(models.Model):
    product = models.OneToOneField(Product, primary_key=True, on_delete=models.CASCADE)
    Starbucks=models.CharField(max_length=30, null=True)
    Twosome=models.CharField(max_length=30, null=True)
    TomandToms=models.CharField(max_length=30, null=True)
    Ediya=models.CharField(max_length=30, null=True)
    Mega=models.CharField(max_length=30, null=True)
    Hollys=models.CharField(max_length=30, null=True)
    Coffeebean=models.CharField(max_length=30, null=True)
    Coffeebay=models.CharField(max_length=30, null=True)
    Angelinus=models.CharField(max_length=30, null=True)
    Pascucci=models.CharField(max_length=30, null=True)


class Price_Bybrand(models.Model):
    product = models.OneToOneField(Product, primary_key=True, on_delete=models.CASCADE)
    Starbucks=models.IntegerField(null=True)
    Twosome=models.IntegerField(null=True)
    TomandToms=models.IntegerField(null=True)
    Ediya=models.IntegerField(null=True)
    Mega=models.IntegerField(null=True)
    Hollys=models.IntegerField(null=True)
    Coffeebean=models.IntegerField(null=True)
    Coffeebay=models.IntegerField(null=True)
    Angelinus=models.IntegerField(null=True)
    Pascucci=models.IntegerField(null=True)