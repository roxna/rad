from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.fields import ToManyField, ToOneField
from tastypie.resources import ModelResource
from bills.models import Subscriber, Plan, Call, Bill, Booster, Roaming, Data


__author__ = 'roxnairani'


class BareSubscriberResource(ModelResource):
    class Meta:
        queryset = Subscriber.objects.all()
        resource_name = "bare_subscriber"


class BarePlanResource(ModelResource):
    class Meta:
        queryset = Plan.objects.all()
        resource_name = "bare_plan"


class BareBillResource(ModelResource):
    class Meta:
        queryset = Bill.objects.all()
        resource_name = "bare_bill"


class SubscriberResource(ModelResource):
    subscriber = ToManyField('bills.api.resources.BillResource', 'subscriber', full=True, null=True)

    class Meta:
        queryset = Subscriber.objects.all()
        resource_name = 'subscriber'
        authorization = Authorization()
        authentication = Authentication()


class PlanResource(ModelResource):
    plan = ToManyField('bills.api.resources.BillResource', 'plan', full=True, null=True)

    class Meta:
        queryset = Plan.objects.all()
        resource_name = 'plan'
        authorization = Authorization()
        authentication = Authentication()


class BillResource(ModelResource):
    call = ToManyField('bills.api.resources.CallResource', 'call', full=True, null=True)
    booster = ToManyField('bills.api.resources.BoosterResource', 'booster', full=True, null=True)
    data = ToManyField('bills.api.resources.DataResource', 'data', full=True, null=True)
    roaming = ToManyField('bills.api.resources.RoamingResource', 'roaming', full=True, null=True)
    subscriber = ToOneField(SubscriberResource, 'subscriber', full=False, null=True)
    plan = ToOneField(PlanResource, 'plan', full=False, null=True)

    class Meta:
        queryset = Bill.objects.all()
        resource_name = 'bill'
        authorization = Authorization()
        authentication = Authentication()


class CallResource(ModelResource):
    bill = ToOneField(BillResource, 'bill', full=False, null=True)

    class Meta:
        queryset = Call.objects.all()
        resource_name = 'call'
        authorization = Authorization()
        authentication = Authentication()


class BoosterResource(ModelResource):
    bill = ToOneField(BillResource, 'bill', full=False, null=True)

    class Meta:
        queryset = Booster.objects.all()
        resource_name = 'booster'
        authorization = Authorization()
        authentication = Authentication()


class DataResource(ModelResource):
    bill = ToOneField(BillResource, 'bill', full=False, null=True)

    class Meta:
        queryset = Data.objects.all()
        resource_name = 'data'
        authorization = Authorization()
        authentication = Authentication()


class RoamingResource(ModelResource):
    bill = ToOneField(BillResource, 'bill', full=False, null=True)

    class Meta:
        queryset = Roaming.objects.all()
        resource_name = 'roaming'
        authorization = Authorization()
        authentication = Authentication()