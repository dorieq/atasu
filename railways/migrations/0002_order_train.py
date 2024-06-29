# Generated by Django 3.2.7 on 2024-06-28 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('railways', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days_until_destination', models.IntegerField()),
                ('count', models.IntegerField()),
                ('end_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='railways.station')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('count', models.IntegerField()),
                ('end_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='end', to='railways.station')),
                ('start_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start', to='railways.station')),
            ],
        ),
    ]
