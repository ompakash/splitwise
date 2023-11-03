# splitwise
Please check the below link for API end points documentation
Postman collection = https://documenter.getpostman.com/view/23574724/2s9YXe84XM



STRUCTURE TREE

├── db.sqlite3
├── manage.py
├── __pycache__
│   ├── testing3.cpython-39.pyc
│   └── testing.cpython-39.pyc
├── README.md
├── requirements.txt
├── SplitExpense
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_remove_balance_user_object_delete_dog_and_more.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-39.pyc
│   │       ├── 0002_alter_splittransaction_user_owed.cpython-39.pyc
│   │       ├── 0002_alter_transaction_user_transcation.cpython-39.pyc
│   │       ├── 0002_remove_balance_user_object_delete_dog_and_more.cpython-39.pyc
│   │       ├── 0002_remove_splittransaction_num_users.cpython-39.pyc
│   │       ├── 0002_rename_user_obj_transaction_user.cpython-39.pyc
│   │       ├── 0002_transaction_user_obj.cpython-39.pyc
│   │       ├── 0002_user.cpython-39.pyc
│   │       ├── 0003_alter_splittransaction_user_owed.cpython-39.pyc
│   │       ├── 0003_alter_transaction_user_transcation.cpython-39.pyc
│   │       ├── 0003_remove_splittransaction_split_amount.cpython-39.pyc
│   │       ├── 0003_rename__type_transaction_type.cpython-39.pyc
│   │       ├── 0004_dog.cpython-39.pyc
│   │       ├── 0004_splittransaction_users.cpython-39.pyc
│   │       ├── 0004_transaction_user_name.cpython-39.pyc
│   │       ├── 0005_alter_splittransaction_split_amount.cpython-39.pyc
│   │       ├── 0005_alter_transaction_user_transcation.cpython-39.pyc
│   │       ├── 0005_remove_transaction_amount_remove_transaction_type_and_more.cpython-39.pyc
│   │       ├── 0006_alter_splittransaction_amount_paid_and_more.cpython-39.pyc
│   │       └── __init__.cpython-39.pyc
│   ├── models.py
│   ├── __pycache__
│   │   ├── admin.cpython-39.pyc
│   │   ├── apps.cpython-39.pyc
│   │   ├── __init__.cpython-39.pyc
│   │   ├── models.cpython-39.pyc
│   │   ├── serializers.cpython-39.pyc
│   │   ├── urls.cpython-39.pyc
│   │   ├── utils.cpython-39.pyc
│   │   └── views.cpython-39.pyc
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── SplitWise
    ├── asgi.py
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-39.pyc
    │   ├── settings.cpython-39.pyc
    │   ├── urls.cpython-39.pyc
    │   └── wsgi.cpython-39.pyc
    ├── settings.py
    ├── urls.py
    └── wsgi.py

7 directories, 54 files







### Installation
*  git@github.com:ompakash/splitwise.git
*  https://github.com/ompakash/splitwise
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux) or `venv\Scripts\activate` (Windows).
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Start the development server: `python manage.py runserver`