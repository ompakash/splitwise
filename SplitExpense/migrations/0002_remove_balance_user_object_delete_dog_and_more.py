# Generated by Django 4.2.6 on 2023-11-03 04:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("SplitExpense", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="balance",
            name="user_object",
        ),
        migrations.DeleteModel(
            name="Dog",
        ),
        migrations.RemoveField(
            model_name="splittransaction",
            name="user_owed",
        ),
        migrations.RemoveField(
            model_name="splittransaction",
            name="users",
        ),
        migrations.DeleteModel(
            name="Balance",
        ),
        migrations.DeleteModel(
            name="SplitTransaction",
        ),
    ]