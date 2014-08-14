from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile_pics', default='../static/img/profile_pics/default_profile_pic.png', blank=True, null=True)

    def __unicode__(self):
        return self.username


class Subscriber(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    zip = models.IntegerField(null=True, blank=True)
    relationship_num = models.IntegerField(null=True, blank=True)
    credit_limit = models.DecimalField(default=0.00, decimal_places=2, max_digits=7)

    def __unicode__(self):
        return self.name


class Plan(models.Model):
    PREPAID = 0
    POSTPAID = 1
    PLANS = (
        (POSTPAID, 'Postpaid'),
        (PREPAID, 'Prepaid')
    )
    type = models.IntegerField(max_length=20, choices=PLANS)
    name = models.CharField(max_length=30)
    min_rental = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    CURRENCY = (
        ('INR', 'INR'),
        ('USD', 'USD')
    )
    currency = models.CharField(max_length=10, choices=CURRENCY)

    def __unicode__(self):
        return self.name


# BILL DETAILS - CENTRAL MODEL WITH FOREIGN/M2M KEYS TO OTHER MODELS
class Bill(models.Model):
    number = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    bill_date = models.DateField()
    due_date = models.DateField()
    total_bill = models.DecimalField(decimal_places=2, max_digits=7)
    onetime_charge = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    monthly_charge = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    call_charge = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    booster_charge = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    data_charge = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    roaming_charge = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    discount = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    late_fee = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True, default=0)
    tax = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)

    # FOREIGN KEYS TO BILL MODEL
    subscriber = models.ForeignKey(Subscriber, related_name='bill')
    # Ignoring changes in plans for now, else M2M field
    plan = models.ForeignKey(Plan, related_name='bill')

    def __unicode__(self):
        return "{}".format(self.number)


# PARENT CLASS
class Usage(models.Model):
    date = models.DateField()
    time = models.TimeField()
    recipient_number = models.BigIntegerField()
    volume = models.CharField(null=True, blank=True, max_length=6)
    duration = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(decimal_places=2, max_digits=7)
    bill = models.ForeignKey(Bill, related_name='%(class)s')

    class Meta:
        abstract = True

    def __unicode__(self):
        return "On {}, to {}".format(self.date, self.recipient_number)


# CHILDREN CLASSES
class Call(Usage):
    OUTGOING_LOCAL_SAME_NETWORK_MOBILE = 1
    OUTGOING_LOCAL_OTHER_NETWORK_MOBILE = 2
    OUTGOING_LOCAL_FIXED_LANDLINE = 3
    OUTGOING_STD_SAME_NETWORK_MOBILE = 4
    OUTGOING_STD_OTHER_NETWORK_MOBILE = 5
    OUTGOING_STD_FIXED_LANDLINE = 6
    OUTGOING_INTL = 7
    TYPE = (
        (OUTGOING_LOCAL_SAME_NETWORK_MOBILE, 'Outgoing Local Call to Same Network Mobile Phone'),
        (OUTGOING_LOCAL_OTHER_NETWORK_MOBILE, 'Outgoing Local Call to Other Network Mobile Phone'),
        (OUTGOING_LOCAL_FIXED_LANDLINE, 'Outgoing Local Call to Fixed Landline'),
        (OUTGOING_STD_SAME_NETWORK_MOBILE, 'Outgoing STD Call to Same Network Mobile Phone'),
        (OUTGOING_STD_OTHER_NETWORK_MOBILE, 'Outgoing STD Call to Other Network Mobile Phone'),
        (OUTGOING_STD_FIXED_LANDLINE, 'Outgoing STD to Fixed Landline'),
        (OUTGOING_INTL, 'Outgoing International Call'),
    )
    type = models.IntegerField(max_length=70, choices=TYPE)


class Booster(Usage):
    OUTGOING_LOCAL_SAME_NETWORK_MOBILE = 1
    OUTGOING_LOCAL_OTHER_NETWORK_MOBILE = 2
    OUTGOING_STD_SAME_NETWORK_MOBILE = 4
    OUTGOING_STD_OTHER_NETWORK_MOBILE = 5
    OUTGOING_INTL = 7
    TYPE = (
        (OUTGOING_LOCAL_SAME_NETWORK_MOBILE, 'Outgoing Local SMS to Same Network Mobile Phone'),
        (OUTGOING_LOCAL_OTHER_NETWORK_MOBILE, 'Outgoing Local SMS to Other Network Mobile Phone'),
        (OUTGOING_STD_SAME_NETWORK_MOBILE, 'Outgoing STD SMS to Same Network Mobile Phone'),
        (OUTGOING_STD_OTHER_NETWORK_MOBILE, 'Outgoing STD SMS to Other Network Mobile Phone'),
        (OUTGOING_INTL, 'Outgoing International SMS'),
    )
    type = models.IntegerField(max_length=70, choices=TYPE)


class Data(Usage):
    DATA_2G = 1
    DATA_3G = 2
    DATA_4G = 3
    TYPE = (
        (DATA_2G, '2G DATA'),
        (DATA_3G, '3G DATA'),
        (DATA_4G, '4G DATA'),
    )
    type = models.IntegerField(max_length=70, choices=TYPE)


class Roaming(Usage):
    NATIONAL_INCOMING_CALL = 1
    NATIONAL_OUTGOING_CALL = 2
    NATIONAL_INCOMING_SMS = 3
    NATIONAL_OUTGOING_SMS = 4
    TYPE = (
        (NATIONAL_INCOMING_CALL, 'National Incoming Voice Call'),
        (NATIONAL_OUTGOING_CALL, 'National Outgoing Voice Call'),
        (NATIONAL_INCOMING_SMS, 'National Incoming SMS'),
        (NATIONAL_OUTGOING_SMS, 'National Outgoing SMS'),
    )
    type = models.IntegerField(max_length=70, choices=TYPE)
