# Generated by Django 4.2.2 on 2023-06-19 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('poultry', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlockInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_alive_birds', models.PositiveIntegerField(default=0)),
                ('number_of_dead_birds', models.PositiveIntegerField(default=0)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('flock', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='poultry.flock')),
            ],
            options={
                'verbose_name_plural': 'Flock Inventories',
            },
        ),
        migrations.CreateModel(
            name='FlockInventoryHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('number_of_birds', models.PositiveIntegerField()),
                ('mortality_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('flock_inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='poultry_inventory.flockinventory')),
            ],
            options={
                'verbose_name_plural': 'Flock Inventory Histories',
            },
        ),
    ]
