from django.db import models

# Create your models here.

class SplitType(models.TextChoices):
    EQUAL = 'equal', 'Equal'
    EXACT = 'exact', 'Exact'
    PERCENT = 'percent', 'Percent'

class TransactionType(models.TextChoices):
    OWE = 'owe', 'Owe'
    LEND = 'lend', 'Lend'

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user_transcation = models.JSONField(null=True)
    user_obj = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user_obj.name
        




# class SplitTransaction(models.Model):
#     amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
#     user_owed = models.ForeignKey(User,on_delete=models.CASCADE)
#     # user_owed = models.CharField(max_length=255)
#     # num_users = models.IntegerField()
#     users = models.ManyToManyField(User ,related_name='transactions_owed_to')  # Assuming User is a related model
#     split_type = models.CharField(max_length=7)
#     # split_amount = models.JSONField(default=None)

#     def __str__(self):
#         return f"{self.user_owed} paid {self.amount_paid}"
