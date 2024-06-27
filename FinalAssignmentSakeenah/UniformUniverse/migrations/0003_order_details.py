# Generated by Django 5.0.4 on 2024-06-23 07:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UniformUniverse', '0002_uniform'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_Details',
            fields=[
                ('OrderID', models.AutoField(primary_key=True, serialize=False)),
                ('Quantity', models.IntegerField()),
                ('Total_Price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Status', models.CharField(default='Pending', max_length=10)),
                ('CustomerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniformUniverse.customer')),
                ('UniformID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniformUniverse.uniform')),
            ],
        ),
    ]
