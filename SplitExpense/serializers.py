from rest_framework import serializers
from .models import *

# class SplitTransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SplitTransaction
#         fields = '__all__'

# class SplitTransactionSerializer(serializers.Serializer):
#     amount_paid = serializers.DecimalField(max_digits=10, decimal_places=2)
#     user_owed = serializers.CharField(max_length=100)
#     # num_users = serializers.IntegerField()
#     split_type = serializers.CharField(max_length=7)
#     # split_amount = serializers.CharField(default=None)  # Assuming split_amount is a string
#     users = serializers.ListField(child=serializers.CharField())


# class BalanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Balance
#         fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'