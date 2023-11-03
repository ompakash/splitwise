from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings


class ExpenseAPI(APIView):
    def __init__(self):
        self.transactions_for_users = {}
    

    def equal(self,amount_paid,user_owed,user_ids):
        amount_owed = round(float(amount_paid) / len(user_ids),2)
        amount_owed = float(amount_owed)
        amount_paid = float(amount_paid)
        remain = 0
        first = True
        if (amount_owed * len(user_ids) != amount_paid):
            remain = round(amount_paid - amount_owed * len(user_ids) ,2)

        try:
            user_owed = User.objects.get(name=str(user_owed))
            user_objects = User.objects.filter(name__in=user_ids)

            all_users = User.objects.all()
            filtered_users = all_users.filter(name__in=user_ids)
            # email_list = filtered_users.values_list('email', flat=True)
            # email_list = list(email_list)
            
            amount_owed_list = []
            for user_id in user_objects:
                if user_id == user_owed:
                    continue
                if first:
                    amount_owed += remain
                    first = False
                
                existing_owe_transcation = Transaction.objects.filter(user_obj=user_owed).first()
                existing_lend_transcation = Transaction.objects.filter(user_obj=user_id).first()
                if not existing_owe_transcation:
                    Transaction.objects.create(user_obj = user_owed,  user_transcation = [])
                if not existing_lend_transcation:
                    Transaction.objects.create(user_obj = user_id,  user_transcation = [])
               
                transaction_owed = Transaction.objects.get(user_obj = user_owed)
                transaction_owed.user_transcation.append({"user_id": str(user_id), "amount": str(amount_owed), "type": "LEND"})
                transaction_owed.save()
                amount_owed_list.append(amount_owed)
                
                transaction_lend = Transaction.objects.get(user_obj = user_id)
                transaction_lend.user_transcation.append({"user_id": str(user_owed), "amount": str(amount_owed), "type": "OWE"})
                transaction_lend.save()
                amount_owed -= remain

                transaction_lend_email = transaction_lend.user_obj.email
                email_list = []
                email_list.append(transaction_lend_email)
                message = f"You been added to an expense, total amount you owe for that expense is {amount_owed} from {user_owed}"
                
                send_mail("Expense Notification",message,settings.EMAIL_HOST_USER,email_list,fail_silently=False)
            return Response({'message': 'Transaction updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def exact(self,amount_paid,user_owed,user_ids,split_amount):
        try:
            user_owed = User.objects.get(name=str(user_owed))
            user_objects = User.objects.filter(name__in=user_ids)
            # user_objects = user_objects.exclude(pk=user_owed.pk)
            for user_id, amount_owed in zip(user_objects, split_amount):
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

                transaction_lend_email = transaction_lend.user_obj.email
                email_list = []
                email_list.append(transaction_lend_email)
                message = f"You been added to an expense, total amount you owe for that expense is {amount_owed} from {user_owed}"
                
                send_mail("Expense Notification",message,settings.EMAIL_HOST_USER,email_list,fail_silently=False)
                
            return Response({'message': 'Transaction updated successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def percent(self,amount_paid,user_owed,user_ids,split_amount):
        try:
            user_owed = User.objects.get(name=str(user_owed))
            user_objects = User.objects.filter(name__in=user_ids)
            # user_objects = user_objects.exclude(pk=user_owed.pk)
            for user_id, owed_percent in zip(user_objects, split_amount):
                if user_id == user_owed:
                    continue
                
                amount_owed = round((float(amount_paid) * float(owed_percent) / 100), 2)
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

                transaction_lend_email = transaction_lend.user_obj.email
                email_list = []
                email_list.append(transaction_lend_email)
                message = f"You been added to an expense, total amount you owe for that expense is {amount_owed} from {user_owed}"
                
                send_mail("Expense Notification",message,settings.EMAIL_HOST_USER,email_list,fail_silently=False)
            return Response({'message': 'Transaction updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


        



    def post(self, request, *args, **kwargs):
        amount_paid = request.data.get('amount_paid', '')
        user_owed = request.data.get('user_owed', '')
        split_type = request.data.get('split_type', '')
        user_ids = request.data.get('users', [])
        split_amount = request.data.get('split_amount', [])
        

        if len(user_ids) > 1000 or float(amount_paid) > 10000000:
            return Response({'Expense can have maximum 1000 participants and the maximum amount for an expense can be INR 1,00,00,000/'}, status=status.HTTP_400_BAD_REQUEST)

        warn = False
        if split_type.lower() == 'exact':
            if len(user_ids) != len(split_amount):
                warn = True
                exception_warning =(f'The number of users owing {len(split_amount)}, does not equal the total number of users {len(user_ids)-1}')
            total_sum = sum(float(item) for item in split_amount if item.replace('.', '', 1).isdigit())
            if float(amount_paid) != total_sum:
                warn = True
                exception_warning = (f'The sum of the split amount {split_amount} = {sum(float(split_amount))} does not equal the total amount paid {amount_paid}')
            if warn:
                return Response({'warning': str(exception_warning)}, status=status.HTTP_400_BAD_REQUEST)
        
        if split_type.lower() == 'percent':
            if len(user_ids) != len(split_amount):
                warn = True
                exception_warning = (f'The number of users owing {len(split_amount)}, does not equal the total number of users {len(user_ids)}')
            total_sum = sum(float(item) for item in split_amount if item.replace('.', '', 1).isdigit())
            if 100 != total_sum:
                warn = True
                exception_warning = (f'The total percentage of {sum(split_amount)} does not equal 100')
            if warn:
                return Response({'warning': str(exception_warning)}, status=status.HTTP_400_BAD_REQUEST)

        try:

            if split_type.lower() == 'equal':
                return self.equal(amount_paid,user_owed,user_ids)
            
            if split_type.lower() == 'exact':
                return self.exact(amount_paid,user_owed,user_ids,split_amount)

            if split_type.lower() == 'percent':
                return self.percent(amount_paid,user_owed,user_ids,split_amount)

            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        
        transactions = Transaction.objects.all()
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

            users_in_debt = self.calculate_transactions(user_id=user_id)
            
        else:
            user_objs = User.objects.filter(transaction__isnull=False).distinct()
            for user_id in user_objs:
                for user_in_debt, owed_users in self.calculate_transactions(user_id=user_id).items():
                    if user_in_debt in users_in_debt:
                        users_in_debt[user_in_debt] = list(set(users_in_debt[user_in_debt] + owed_users))
                    else:
                        users_in_debt[user_in_debt] = owed_users

            

        final_list = []
        for user_in_debt, users_owed in users_in_debt.items():
            for user_owed, amount_owed in users_owed:
                final_list.append(f'{user_in_debt} owes {user_owed}: {abs(amount_owed)}')
        return set(final_list)

    def get(self,request):
        all_details = self.show()
        return Response(all_details,status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', '')
        all_details = self.show(user_id)    
        return Response(all_details,status=status.HTTP_200_OK)
    