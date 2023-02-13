# Generated by Django 4.1.4 on 2023-01-29 10:43

import birthday.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_identitycard_picture_delete_collectedpassword'),
    ]

    operations = [
        migrations.AddField(
            model_name='identitycard',
            name='dob_dayofyear_internal',
            field=models.PositiveSmallIntegerField(default=None, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='identitycard',
            name='dob',
            field=birthday.fields.BirthdayField(),
        ),
       
    ]