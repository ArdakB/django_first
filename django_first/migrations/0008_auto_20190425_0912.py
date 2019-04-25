# Generated by Django 2.1.7 on 2019-04-25 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_first', '0007_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='django_first.Order'),
        ),
        migrations.AlterField(
            model_name='storeitem',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='django_first.Store'),
        ),
    ]