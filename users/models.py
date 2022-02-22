from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'


class User(models.Model):
    ROLE = [('member', 'участник'), ('moderator', 'модератор'), ('admin', 'админ')]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=ROLE, default='member')
    age = models.SmallIntegerField()
    location_id = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.username

    class Meta():
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

