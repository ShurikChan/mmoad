# Generated by Django 4.2.14 on 2024-07-14 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adboard', '0003_alter_advertisement_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advertisement',
            options={'ordering': ['-date_in']},
        ),
    ]
