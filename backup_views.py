

# class SplitService:
#     def __init__(self):
#         self.transactions_for_users = {}

#     def validate(self, split_type, split_amount, num_users, amount_paid):
#         if split_type == 'EQUAL':
#             return

#         if split_type == 'EXACT':
#             if num_users != len(split_amount):
#                 raise Exception(f'The number of users owing {len(split_amount)}, does not equal the total number of users {num_users}')
                
#             if amount_paid != sum(split_amount):
#                 raise Exception(f'The sum of the split amount {split_amount} = {sum(split_amount)} does not equal the total amount paid {amount_paid}')

#         if split_type == 'PERCENT':
#             if num_users != len(split_amount):
#                 raise Exception(f'The number of users owing {len(split_amount)}, does not equal the total number of users {num_users}')

#             if 100 != sum(split_amount):
#                 raise Exception(f'The total percentage of {sum(split_amount)} does not equal 100')

#     def expense(self, amount_paid, user_owed, num_users, users, split_type, split_amount=None):
#         self.validate(split_type, split_amount, num_users, amount_paid)
    
#         if split_type == 'EQUAL':
#             amount_owed = amount_paid / num_users

#             for user_id in users:
#                 if user_id == user_owed:
#                     continue
                  
#                 if user_owed not in self.transactions_for_users:
#                     self.transactions_for_users[user_owed] = []
#                 if user_id not in self.transactions_for_users:
#                     self.transactions_for_users[user_id] = []
                
#                 self.transactions_for_users[user_owed].append({'user_id': user_id, 'amount': amount_owed, 'type': 'LEND'})
#                 self.transactions_for_users[user_id].append({'user_id': user_owed, 'amount': amount_owed, 'type': 'OWE'})

#         if split_type == 'EXACT':
#             for user_id, amount_owed in zip(users, split_amount):
#                 if user_id == user_owed:
#                     continue
                  
#                 if user_owed not in self.transactions_for_users:
#                     self.transactions_for_users[user_owed] = []
#                 if user_id not in self.transactions_for_users:
#                     self.transactions_for_users[user_id] = []
                
#                 self.transactions_for_users[user_owed].append({'user_id': user_id, 'amount': amount_owed, 'type': 'LEND'})
#                 self.transactions_for_users[user_id].append({'user_id': user_owed, 'amount': amount_owed, 'type': 'OWE'})

#         if split_type == 'PERCENT':
#             for user_id, owed_percent in zip(users, split_amount):
#                 if user_id == user_owed:
#                     continue
                  
#                 amount_owed = round((amount_paid * owed_percent / 100), 2)
                
#                 if user_owed not in self.transactions_for_users:
#                     self.transactions_for_users[user_owed] = []
#                 if user_id not in self.transactions_for_users:
#                     self.transactions_for_users[user_id] = []
                
#                 self.transactions_for_users[user_owed].append({'user_id': user_id, 'amount': amount_owed, 'type': 'LEND'})
#                 self.transactions_for_users[user_id].append({'user_id': user_owed, 'amount': amount_owed, 'type': 'OWE'})

#     def calculate_transactions(self, user_id):
#         if user_id not in self.transactions_for_users:
#             print(f'No balances for {user_id}')
#             return {}
      
#         transaction_map = {}
#         users_in_debt = {}

#         for transaction in self.transactions_for_users[user_id]:
#             if transaction['type'] == 'OWE':
#                 if transaction['user_id'] in transaction_map:
#                     transaction_map[transaction['user_id']] += transaction['amount']
#                 else:
#                     transaction_map[transaction['user_id']] = transaction['amount']

#             if transaction['type'] == 'LEND':
#                 if transaction['user_id'] in transaction_map:
#                     transaction_map[transaction['user_id']] -= transaction['amount']
#                 else:
#                     transaction_map[transaction['user_id']] = -transaction['amount']

#         if all(amount_owed == 0 for amount_owed in transaction_map.values()):
#             return {}

#         for other_user_id, amount_owed in transaction_map.items():
#             amount_owed = round(amount_owed, 2)

#             if amount_owed < 0:
#                 if other_user_id in users_in_debt:
#                     users_in_debt[other_user_id].append((user_id, abs(amount_owed)))
#                 else:
#                     users_in_debt[other_user_id] = [(user_id, abs(amount_owed))]

#             if amount_owed > 0:
#                 if user_id in users_in_debt:
#                     users_in_debt[user_id].append((other_user_id, amount_owed))
#                 else:
#                     users_in_debt[user_id] = [(other_user_id, amount_owed)]

#         return users_in_debt

#     def show(self, user_id=None):
#         users_in_debt = {}

#         if user_id:
#             print('====' * 10)
#             print(f"showing transactions for user: {user_id}")

#             users_in_debt = self.calculate_transactions(user_id=user_id)
#         else:
#             print('====' * 10)
#             print('showing transactions for all\n')

#             for user_id in self.transactions_for_users.keys():
#                 for user_in_debt, owed_users in self.calculate_transactions(user_id=user_id).items():
#                     if user_in_debt in users_in_debt:
#                         users_in_debt[user_in_debt] = list(set(users_in_debt[user_in_debt] + owed_users))
#                     else:
#                         users_in_debt[user_in_debt] = owed_users

#         if not users_in_debt:
#             print('No balances')

#         for user_in_debt, users_owed in users_in_debt.items():
#             for user_owed, amount_owed in users_owed:
#                 print(f'{user_in_debt} owes {user_owed}: {abs(amount_owed)}')

