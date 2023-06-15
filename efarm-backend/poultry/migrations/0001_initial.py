# Generated by Django 4.2.2 on 2023-06-13 17:04

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_hatching', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2023, 4, 18)), django.core.validators.MaxValueValidator(datetime.date(2023, 6, 13))])),
                ('chicken_type', models.CharField(choices=[('Broiler', 'Broiler'), ('Layers', 'Layers'), ('Multi-Purpose', 'Multi Purpose')], max_length=15)),
                ('initial_number_of_birds', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(2)])),
                ('current_rearing_method', models.CharField(choices=[('Free Range', 'Free Range'), ('Cage System', 'Cage System'), ('Deep Litter', 'Deep Litter'), ('Barn System', 'Barn System'), ('Pasture Based', 'Pasture Based')], max_length=50)),
                ('date_established', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlockSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(choices=[('This Farm', 'This Farm'), ('Ken Chic', 'Ken Chic'), ('Kuku Chick', 'Kuku Chick'), ('Uzima Chick', 'Uzima Chicken'), ("Kiplel's Farm", 'Kiplels Farm')], max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='HousingStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Open-Sided Shed', 'Open Sided Shed'), ('Closed Shed', 'Closed Shed'), ('Battery Cage System', 'Battery Cage'), ('Deep Litter House', 'Deep Litter House'), ('Semi-Intensive Housing', 'Semi Intensive Housing'), ('Pasture Housing', 'Pasture Housing')], max_length=22)),
                ('category', models.CharField(choices=[('Brooder Chick House', 'Brooder Chick House'), ('Growers House', 'Growers House'), ('Layers House', 'Layers House'), ('Broilers House', 'Broilers House'), ('Breeders House', 'Breeders House')], max_length=21)),
            ],
        ),
        migrations.CreateModel(
            name='FlockMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement_date', models.DateField(auto_now_add=True)),
                ('flock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poultry.flock')),
                ('from_structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_movements', to='poultry.housingstructure')),
                ('to_structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_movements', to='poultry.housingstructure')),
            ],
        ),
        migrations.CreateModel(
            name='FlockInspectionRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('number_of_dead_birds', models.PositiveIntegerField(default=0)),
                ('flock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poultry.flock')),
            ],
        ),
        migrations.CreateModel(
            name='FlockHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rearing_method', models.CharField(choices=[('Free Range', 'Free Range'), ('Cage System', 'Cage System'), ('Deep Litter', 'Deep Litter'), ('Barn System', 'Barn System'), ('Pasture Based', 'Pasture Based')], max_length=50)),
                ('date_changed', models.DateTimeField(auto_now_add=True)),
                ('current_housing_structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poultry.housingstructure')),
                ('flock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poultry.flock')),
            ],
        ),
        migrations.AddField(
            model_name='flock',
            name='current_housing_structure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poultry.housingstructure'),
        ),
        migrations.AddField(
            model_name='flock',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poultry.flocksource'),
        ),
    ]