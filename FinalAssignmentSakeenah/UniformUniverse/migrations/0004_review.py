# Generated by Django 5.0.4 on 2024-06-23 07:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UniformUniverse', '0003_order_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('ReviewID', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('Description', models.TextField()),
                ('Date', models.DateField()),
                ('OrderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniformUniverse.order_details')),
            ],
        ),
    ]