import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile_pics', default='../static/img/profile_pics/default_profile_pic.png', blank=True, null=True)

    def __unicode__(self):
        return self.username


class Subscriber(models.Model):
    name = models.CharField(max_length=20, default="")
    # Phone numbers are usually better stored as a CharField since there's many different formats
    # There's also localized django libraries for phone numbers and location information
    phone_number = models.BigIntegerField(default=0)
    address = models.CharField(max_length=100, default="", null=True, blank=True)
    city = models.CharField(max_length=20, default="", null=True, blank=True)
    state = models.CharField(max_length=20, default="", null=True, blank=True)
    # zip is a reserved keyword in python, should probably be zipcode
    zip = models.IntegerField(default=00000, null=True, blank=True)
    relationship_num = models.IntegerField(default=0, null=True, blank=True)
    credit_limit = models.IntegerField(default=0, null=True, blank=True)
    security_deposit = models.IntegerField(default=0, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Plan(models.Model):
    PREPAID = 0
    POSTPAID = 1
    PLANS = (
        (POSTPAID, 'Postpaid'),
        (PREPAID, 'Prepaid')
    )
    # type's a reserved python keyword
    # You don't need a max_length here
    type = models.IntegerField(max_length=20, choices=PLANS, default=1)
    name = models.CharField(max_length=30, default="")
    min_rental = models.IntegerField(default=0, null=True, blank=True)
    # probably want to do what you did above with prepaid/postpaid and it being an IntegerField, usually best practice
    CURRENCY = (
        ('INR', 'INR'),
        ('USD', 'USD')
    )
    currency = models.CharField(max_length=10, default="INR", choices=CURRENCY)

    def __unicode__(self):
        return self.name


# BILL DETAILS - CENTRAL MODEL WITH FOREIGN/M2M KEYS TO OTHER MODELS
class Bill(models.Model):
    number = models.IntegerField(default=0)
    # Do these defaults actually work??
    start_date = models.DateField(default=2000-01-01)
    end_date = models.DateField(default=2000-01-01)
    bill_date = models.DateField(default=2000-01-01)
    due_date = models.DateField(default=2000-01-01)
    total_bill = models.DecimalField(decimal_places=3, max_digits=7, default=0.00, )
    onetime_charge = models.DecimalField(decimal_places=3, max_digits=7, default=0.00, null=True, blank=True)
    monthly_charge = models.DecimalField(decimal_places=3, max_digits=7, default=0.00, null=True, blank=True)
    call_charge = models.DecimalField(decimal_places=3, max_digits=7, default=0.00, null=True, blank=True)
    booster_charge = models.DecimalField(decimal_places=3, max_digits=7, default=0.00, null=True, blank=True)
    data_charge = models.DecimalField(decimal_places=3, max_digits=7, default=0.00, null=True, blank=True)
    roaming_charge = models.DecimalField(decimal_places=3, max_digits=7, default=0.00, null=True, blank=True)
    discount = models.DecimalField(decimal_places=3, max_digits=7, default=0.00, null=True, blank=True)
    late_fee = models.DecimalField(decimal_places=3, max_digits=7, default=0.00, null=True, blank=True)
    tax = models.DecimalField(decimal_places=3, max_digits=7, default=0.00, null=True, blank=True)

    # FOREIGN KEYS TO BILL MODEL
    subscriber = models.ForeignKey(Subscriber, related_name='bill')
    # Ignoring changes in plans for now, else M2M field
    plan = models.ForeignKey(Plan, related_name='bill')

    def __unicode__(self):
        return u"{}".format(self.number)


# PARENT CLASS
class Usage(models.Model):
    date = models.DateField(default=2000-01-01)
    time = models.TimeField(default=datetime.datetime.strptime('12:12:12', '%H:%M:%S').time())
    recipient_number = models.BigIntegerField(default=0)
    # probably want to just store it in milliseconds?
    duration = models.CharField(default='00:00', max_length=5, null=True, blank=True)
    volume = models.IntegerField(default=0, null=True, blank=True, max_length=6)
    cost = models.DecimalField(decimal_places=2, max_digits=7, default=0.00)
    bill = models.ForeignKey(Bill, related_name='%(class)s')

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"On {}, to {}".format(self.date, self.recipient_number)

# Not sure if this would give any kind of performance benefit, but you could have just had
# a Usage model with a category foreign key for Call / Booster / Data, etc. Need to see the views.py next.
# You could also store a "sub category" or the category table could have rows for each.

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
    # don't need max_length (and technically it's only 1, since it's 1-7)
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
