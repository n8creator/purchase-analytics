# Generated by Django 5.1 on 2024-12-01 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=100, unique=True)),
                ('timestamp', models.DateTimeField()),
                ('items', models.JSONField(default=list)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('nds_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tips_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('payment_method', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'receipts',
                'indexes': [models.Index(fields=['transaction_id'], name='receipts_transac_68f3a2_idx')],
            },
        ),
    ]
