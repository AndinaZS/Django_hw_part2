# Generated by Django 4.0.2 on 2022-02-22 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_alter_categories_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
