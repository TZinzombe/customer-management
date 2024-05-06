from django.db import models

# Create your models here.
class PersonalInfo(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
        ('P', 'Separated'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    cell = models.CharField(max_length=25)
    national_id = models.CharField(max_length=20)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    occupation = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=25, blank=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return self.first_name + self.last_name
    

    
class Preferences(models.Model):

    receive_news = models.BooleanField(default=True)
    receive_promotions = models.BooleanField(default=True)
    receive_alerts = models.BooleanField(default=True)
    receive_transaction_message = models.BooleanField(default=True)
    receive_pin_change_alert = models.BooleanField(default=True)

    # Communication Channels
    receive_email = models.BooleanField(default=True)
    receive_sms = models.BooleanField(default=True)
    receive_phone_call = models.BooleanField(default=True)
    
    # Promotion Types
    receive_product_recommendations = models.BooleanField(default=True)
    receive_discount_offers = models.BooleanField(default=True)
    receive_exclusive_deals = models.BooleanField(default=True)
    
    # Alert Types
    receive_account_balance_alerts = models.BooleanField(default=True)
    receive_transaction_notifications = models.BooleanField(default=True)
    receive_fraud_alerts = models.BooleanField(default=True)

    def __str__(self):
        return 'prefences' 


class Account(models.Model):
      
    ACCOUNT_TYPE_CHOICES = [
        ('savings', 'Savings'),
        ('checking', 'Checking'),
        ('investment', 'Investment'),
        ('credit', 'Credit'),
    ]

    ACCOUNT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('frozen', 'Frozen'),
        ('closed', 'Closed'),
    ]

    account_number = models.BigAutoField(primary_key=True, unique=True)
    personal_info = models.ForeignKey('PersonalInfo', on_delete=models.CASCADE)
    preference = models.ForeignKey(Preferences, on_delete=models.CASCADE, default=None)
    branch_code = models.CharField(max_length=230)
    currency = models.CharField(max_length=230)
    pin = models.CharField(max_length=4)
    balance = models.DecimalField(max_digits=50, decimal_places=2)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='checking')
    account_status = models.CharField(max_length=20, choices=ACCOUNT_STATUS_CHOICES, default='active')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.personal_info.last_name + ' ' + self.personal_info.first_name)
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        self.balance -= amount

class Transaction(models.Model):

    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    ]

    TRANSACTION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver')
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender')
    currency = models.CharField(max_length=230)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES, default='pending')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    