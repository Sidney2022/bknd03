# Generated by Django 5.0.6 on 2024-07-07 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_organisation_org_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='firstName',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='last_name',
            new_name='lastName',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_id',
            new_name='userId',
        ),
    ]
