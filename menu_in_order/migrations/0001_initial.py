# Generated by Django 4.0.1 on 2022-05-23 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='menu_in_order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('price', models.IntegerField()),
                ('is_hot', models.BooleanField(default=False)),
                ('is_small', models.BooleanField(default=False)),
                ('menu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.menu')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
    ]