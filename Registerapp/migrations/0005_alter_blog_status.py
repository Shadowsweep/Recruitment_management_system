# Generated by Django 5.0.1 on 2024-07-07 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registerapp', '0004_blog_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='status',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
