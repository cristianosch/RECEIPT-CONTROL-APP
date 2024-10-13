# Generated by Django 5.0.2 on 2024-09-24 21:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExtractingResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extracted_locale', models.CharField(max_length=10)),
                ('extracted_shop_name', models.CharField(blank=True, max_length=100, null=True)),
                ('extracted_category', models.CharField(blank=True, max_length=50, null=True)),
                ('extracted_date', models.DateField(blank=True, null=True)),
                ('extracted_total_tax', models.FloatField(blank=True, null=True)),
                ('extracted_total_amount', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='image_receipts/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExtractedLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity', models.IntegerField(blank=True, default=1, null=True)),
                ('unit_price', models.FloatField(blank=True, null=True)),
                ('total_amount', models.FloatField(blank=True, null=True)),
                ('extraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='line_items', to='receipt.extractingresults')),
            ],
        ),
        migrations.AddField(
            model_name='extractingresults',
            name='receipt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='extraction_results', to='receipt.receipt'),
        ),
    ]
