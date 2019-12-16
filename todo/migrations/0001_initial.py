# Generated by Django 3.0 on 2019-12-16 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('color', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('completed', models.BooleanField(default=False)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('reminder_before_deadline', models.DurationField(blank=True, null=True)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.List')),
                ('tags', models.ManyToManyField(blank=True, to='todo.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='list',
            name='tags',
            field=models.ManyToManyField(blank=True, to='todo.Tag'),
        ),
    ]
