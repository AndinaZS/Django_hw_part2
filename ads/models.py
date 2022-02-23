from django.db import models
from users.models import User


class Categories(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Advert(models.Model):
    name = models.CharField(max_length=250)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.CharField(max_length=1000, null=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', null=True)
    category_id = models.ManyToManyField(Categories)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'






