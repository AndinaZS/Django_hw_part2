from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Advert(models.Model):
    name = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    description = models.TextField(max_length=1000, null=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'






