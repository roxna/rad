from django.contrib import admin
from bills.models import User, Subscriber, Plan, Call, Booster, Data, Roaming, Bill

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'email']


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'relationship_num']


class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'min_rental']


class BillAdmin(admin.ModelAdmin):
    list_display = ['number', 'due_date', 'total_bill', 'subscriber', 'plan']


class UsageAdmin(admin.ModelAdmin):
    list_display = ['type', 'cost', 'date', 'time', 'recipient_number', 'bill']


admin.site.register(User, UserAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(Call, UsageAdmin)
admin.site.register(Booster, UsageAdmin)
admin.site.register(Data, UsageAdmin)
admin.site.register(Roaming, UsageAdmin)
