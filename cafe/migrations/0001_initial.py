# Generated by Django 4.0.1 on 2022-05-30 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('image', models.ImageField(upload_to='products')),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10, null=True)),
                ('available_display', models.BooleanField(default=True, verbose_name='Display')),
                ('available_order', models.BooleanField(default=True, verbose_name='Order')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created'],
                'index_together': {('id',)},
            },
        ),
    ]
