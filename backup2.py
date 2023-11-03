from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from typing import List, Optional, Union
from collections import defaultdict, ChainMap
from enum import Enum
from rest_framework import status
import json
from django.shortcuts import get_object_or_404






class ExpenseAPI(APIView):
    def __init__(self):
        self.transactions_for_users = {}

    def expense(self, amount_paid, user_owed, num_users, users, split_type, split_amount=None):
        # Implement your expense logic here
        self.validate(split_type=split_type, split_amount=split_amount, num_users=num_users, amount_paid=amount_paid)
        
        if split_type == SplitType.EQUAL:
            amount_owed = amount_paid / num_users

        for user_id in users:
            if user_id == user_owed:
                continue

            Transaction.objects.create(user_id=user_id, amount = amount_owed, type=TransactionType.LEND)
            Transaction.objects.create(user_id=user_owed, amount = amount_owed, type=TransactionType.OWE)

        if split_type == SplitType.EXACT:
            for user_id, amount_owed in zip(users, split_amount):
                if user_id == user_owed:
                    continue
            
            self.transactions_for_users[user_owed].append(Transaction(user_id=user_id, amount=amount_owed, type=TransactionType.LEND))
            self.transactions_for_users[user_id].append(Transaction(user_id=user_owed, amount=amount_owed, type=TransactionType.OWE))

        if split_type == SplitType.PERCENT:
            for user_id, owed_percent in zip(users, split_amount):
                if user_id == user_owed:
                    continue
            
            amount_owed = round((amount_paid * owed_percent / 100), 2)
            
            self.transactions_for_users[user_owed].append(Transaction(user_id=user_id, amount=amount_owed, type=TransactionType.LEND))
            self.transactions_for_users[user_id].append(Transaction(user_id=user_owed, amount=amount_owed, type=TransactionType.OWE))


    def validate(self, split_type, split_amount, num_users, amount_paid):
        if split_type == 'EQUAL':
            return

        if split_type == 'EXACT':
            if num_users != len(split_amount):
                raise Exception(f'The number of users owing {len(split_amount)}, does not equal the total number of users {num_users}')
                
            if amount_paid != sum(split_amount):
                raise Exception(f'The sum of the split amount {split_amount} = {sum(split_amount)} does not equal the total amount paid {amount_paid}')

        if split_type == 'PERCENT':
            if num_users != len(split_amount):
                raise Exception(f'The number of users owing {len(split_amount)}, does not equal the total number of users {num_users}')

            if 100 != sum(split_amount):
                raise Exception(f'The total percentage of {sum(split_amount)} does not equal 100')


    # def equal(self,amount_paid,user_owed,split_type,user_ids):



    def post(self, request, *args, **kwargs):
        amount_paid = request.data.get('amount_paid', '')
        user_owed = request.data.get('user_owed', '')
        split_type = request.data.get('split_type', '')
        user_ids = request.data.get('users', [])
        split_amount = request.data.get('split_amount', [])

        if split_type == 'exact':
            if len(user_ids) != len(split_amount):
                exception_warning =(f'The number of users owing {len(split_amount)}, does not equal the total number of users {len(user_ids)}')
            if amount_paid != sum(split_amount):
                exception_warning = (f'The sum of the split amount {split_amount} = {sum(split_amount)} does not equal the total amount paid {amount_paid}')
            return Response({'warning': str(exception_warning)}, status=status.HTTP_400_BAD_REQUEST)
        
        if split_type == 'percent':
            if len(user_ids) != len(split_amount):
                exception_warning = (f'The number of users owing {len(split_amount)}, does not equal the total number of users {len(user_ids)}')

            if 100 != sum(split_amount):
                exception_warning = (f'The total percentage of {sum(split_amount)} does not equal 100')
            return Response({'warning': str(exception_warning)}, status=status.HTTP_400_BAD_REQUEST)


        if split_type == 'equal':
            amount_owed = float(amount_paid) / len(user_ids)
            
        try:
            user_owed = User.objects.get(name=str(user_owed))
            user_objects = User.objects.filter(name__in=user_ids)
            for user_id in user_objects:
                if user_id == user_owed:
                    continue
                
                existing_owe_transcation = Transaction.objects.filter(user_obj=user_owed).first()
                existing_lend_transcation = Transaction.objects.filter(user_obj=user_id).first()
                if not existing_owe_transcation:
                    Transaction.objects.create(user_obj = user_owed,  user_transcation = [])
                if not existing_lend_transcation:
                    Transaction.objects.create(user_obj = user_id,  user_transcation = [])
               
                transaction_owed = Transaction.objects.get(user_obj = user_owed)
                transaction_owed.user_transcation.append({"user_id": str(user_id), "amount": str(amount_owed), "type": "LEND"})
                transaction_owed.save()
                transaction_lend = Transaction.objects.get(user_obj = user_id)
                transaction_lend.user_transcation.append({"user_id": str(user_owed), "amount": str(amount_owed), "type": "OWE"})
                transaction_lend.save()
                
            return Response({'message': 'Transaction updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("EXCEPTION", str(e))
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        # Retrieve balances for the specified user or for all users
        transactions = Transaction.objects.all()
        print(transactions)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        data = User.objects.all()
        serializer = UserSerializer(data, many = True)
        serialized_data = serializer.data
        return Response(serialized_data,status=status.HTTP_200_OK)
    
class ShowDetails(APIView):
    
    def calculate_transactions(self, user_id):
        
        user = get_object_or_404(User, name=user_id)
        existing_user = Transaction.objects.get(user_obj=user)
        if not existing_user:
            print(f'No balances for {user_id}')
            return {}
      
        transaction_map = {}
        users_in_debt = {}
        
        transaction_for_user_id = Transaction.objects.get(user_obj=user)
        for transaction in transaction_for_user_id.user_transcation:
            
            transaction_type = transaction.get('type')
            other_user_id = transaction.get('user_id')
            amount = transaction.get('amount')
            if transaction_type == 'OWE':
                if other_user_id in transaction_map:
                    transaction_map[other_user_id] += float(amount)
                else:
                    transaction_map[other_user_id] = float(amount)

            if transaction_type == 'LEND':
                if other_user_id in transaction_map:
                    transaction_map[other_user_id] -= float(amount)
                else:
                    transaction_map[other_user_id] = -float(amount)

        if all(amount_owed == 0 for amount_owed in transaction_map.values()):
            return {}

        for other_user_id, amount_owed in transaction_map.items():
            amount_owed = round(amount_owed, 2)

            if amount_owed < 0:
                if other_user_id in users_in_debt:
                    users_in_debt[other_user_id].append(user_id, abs(amount_owed))
                else:
                    users_in_debt[other_user_id] = [(user_id, abs(amount_owed))]

            if amount_owed > 0:
                if user_id in users_in_debt:
                    users_in_debt[user_id].append((other_user_id, amount_owed))
                else:
                    users_in_debt[user_id] = [(other_user_id, amount_owed)]
        
        return users_in_debt


    def show(self, user_id=None):
        users_in_debt = {}

        if user_id:
            print('====' * 10)
            print(f"showing transactions for user: {user_id}")

            users_in_debt = self.calculate_transactions(user_id=user_id)
            
        else:
            print('====' * 10)
            print('showing transactions for all\n')
            user_objs = User.objects.filter(transaction__isnull=False).distinct()
            for user_id in user_objs:
                for user_in_debt, owed_users in self.calculate_transactions(user_id=user_id).items():
                    if user_in_debt in users_in_debt:
                        users_in_debt[user_in_debt] = list(set(users_in_debt[user_in_debt] + owed_users))
                    else:
                        users_in_debt[user_in_debt] = owed_users

        if not users_in_debt:
            print('No balances')

        final_list = []
        for user_in_debt, users_owed in users_in_debt.items():
            for user_owed, amount_owed in users_owed:
                final_list.append(f'{user_in_debt} owes {user_owed}: {abs(amount_owed)}')
                print(f'{user_in_debt} owes {user_owed}: {abs(amount_owed)}')
        print(set(final_list))

    def get(self,request):
        all_details = self.show()
        print(all_details)
        return Response("serialized_data",status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', '')
        # all_details = self.show(user_id)
        all_details = self.show()
        # print(all_details)
        return Response("serialized_data",status=status.HTTP_200_OK)
    