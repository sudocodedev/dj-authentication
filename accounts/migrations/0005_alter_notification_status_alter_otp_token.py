# Generated by Django 4.2.14 on 2024-08-13 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_otp_token_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], default='pending', max_length=15),
        ),
        migrations.AlterField(
            model_name='otp',
            name='token',
            field=models.CharField(default='d63bcc5b', max_length=8),
        ),
    ]