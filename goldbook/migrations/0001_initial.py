# Generated by Django 2.1.7 on 2019-02-19 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoldenMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('message', models.TextField(null=True)),
                ('rate', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'golden message',
                'ordering': ['pk'],
            },
        ),
    ]
