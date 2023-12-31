# Generated by Django 4.2.6 on 2023-11-02 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Dog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("data", models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("mobile_number", models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_transcation", models.JSONField(null=True)),
                (
                    "user_obj",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="SplitExpense.user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SplitTransaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount_paid", models.DecimalField(decimal_places=2, max_digits=10)),
                ("split_type", models.CharField(max_length=7)),
                (
                    "user_owed",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="SplitExpense.user",
                    ),
                ),
                (
                    "users",
                    models.ManyToManyField(
                        related_name="transactions_owed_to", to="SplitExpense.user"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Balance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("balance_activity", models.JSONField(null=True)),
                (
                    "user_object",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="SplitExpense.user",
                    ),
                ),
            ],
        ),
    ]
