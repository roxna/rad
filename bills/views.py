import cgi
import json
from decimal import Decimal
from django.contrib.auth import authenticate, REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import get_current_site
from django.core import serializers
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from bills.forms import RegistrationForm, ProfileForm, LoginForm
from bills.models import Call, Booster, Data, Roaming, Plan
from bills.utils import parse_data
from rad import settings

# Create your views here.


def home(request):
    return render(request, "home.html")


def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)
            return redirect('/dashboard')
    data = {
        'form': form
    }
    return render(request, "registration/register.html", data)


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=LoginForm,
          current_app=None, extra_context=None):

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


# @login_required
def dashboard(request):
    total_calls_cost = Call.objects.aggregate(cost=Sum('cost'))['cost']
    total_boosters_cost = Booster.objects.aggregate(cost=Sum('cost'))['cost']
    total_data_cost = Data.objects.all().aggregate(cost=Sum('cost'))['cost']
    total_cost = total_calls_cost + total_boosters_cost + total_data_cost
    data = {
        'total_cost': total_cost,
        'total_calls_cost_percent': round(total_calls_cost / total_cost * 100, 0),
        'total_boosters_cost_percent': round(total_boosters_cost / total_cost * 100),
        'total_data_cost_percent': round(total_data_cost / total_cost * 100)
    }
    return render(request, "dashboard.html", data)


# AJAX URLS
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            if form.save():
                return redirect('/dashboard')
    form = ProfileForm(instance=request.user)
    data = {
        'form': form
    }
    return render(request, "ajax/profile_template.html", data)


def upload_data(request):
    return render(request, "ajax/upload_data_template.html")


def save_uploaded_data(request):
    file_data = cgi.FieldStorage()
    file_path = file_data['uploaded_file'].value
    file_password = file_data['password'].value
    print file_path, file_password
    parse_data(file_path, file_password)


def dashboard_analysis(request):
    total_calls = Call.objects.aggregate(sum=Sum('cost'))['sum']
    total_boosters = Booster.objects.aggregate(sum=Sum('cost'))['sum']
    total_data = Data.objects.aggregate(sum=Sum('cost'))['sum']
    total_roaming = Roaming.objects.aggregate(sum=Sum('cost'))['sum']
    data = {
        'total_calls': str(total_calls),
        'total_boosters': str(total_boosters),
        'total_data': str(total_data),
        'total_roaming': str(total_roaming)
    }
    return HttpResponse(json.dumps(data),  content_type='application/json')


# def call_analysis(request):
#     # To improve performance w/ annotate/aggregate (annotate(count=Count(type=Call.OUTGOING_LOCAL_SAME_NETWORK_MOBILE)))
#     total_calls = Call.objects.all().count()
#     outgoing_local_same_network = Call.objects.filter(type=Call.OUTGOING_LOCAL_SAME_NETWORK_MOBILE).count()
#     outgoing_local_other_network = Call.objects.filter(type=Call.OUTGOING_LOCAL_OTHER_NETWORK_MOBILE).count()
#     outgoing_local_fixed_landline = Call.objects.filter(type=Call.OUTGOING_LOCAL_FIXED_LANDLINE).count()
#     outgoing_std_same_network = Call.objects.filter(type=Call.OUTGOING_STD_SAME_NETWORK_MOBILE).count()
#     outgoing_std_other_network = Call.objects.filter(type=Call.OUTGOING_STD_OTHER_NETWORK_MOBILE).count()
#     outgoing_std_fixed_landline = Call.objects.filter(type=Call.OUTGOING_STD_FIXED_LANDLINE).count()
#     outgoing_intl = Call.objects.filter(type=Call.OUTGOING_INTL).count()
#     data = {
#         'total_calls': total_calls,
#         'outgoing_local_same_network': outgoing_local_same_network,
#         'outgoing_local_other_network': outgoing_local_other_network,
#         'outgoing_local_fixed_landline': outgoing_local_fixed_landline,
#         'outgoing_std_same_network': outgoing_std_same_network,
#         'outgoing_std_other_network': outgoing_std_other_network,
#         'outgoing_std_fixed_landline': outgoing_std_fixed_landline,
#         'outgoing_intl': outgoing_intl,
#     }
#     return HttpResponse(json.dumps(data), content_type='application/json')


# def booster_analysis(request):
#     # To improve performance w/ annotate/aggregate
#     total_boosters = Booster.objects.all().count()
#     outgoing_local_same_network = Call.objects.filter(type=Call.OUTGOING_LOCAL_SAME_NETWORK_MOBILE).count()
#     outgoing_local_other_network = Call.objects.filter(type=Call.OUTGOING_LOCAL_OTHER_NETWORK_MOBILE).count()
#     outgoing_std_same_network = Call.objects.filter(type=Call.OUTGOING_STD_SAME_NETWORK_MOBILE).count()
#     outgoing_std_other_network = Call.objects.filter(type=Call.OUTGOING_STD_OTHER_NETWORK_MOBILE).count()
#     outgoing_intl = Call.objects.filter(type=Call.OUTGOING_INTL).count()
#     data = {
#         'total_boosters': total_boosters,
#         'outgoing_local_same_network': outgoing_local_same_network,
#         'outgoing_local_other_network': outgoing_local_other_network,
#         'outgoing_std_same_network': outgoing_std_same_network,
#         'outgoing_std_other_network': outgoing_std_other_network,
#         'outgoing_intl': outgoing_intl,
#     }
#     return HttpResponse(json.dumps(data), content_type='application/json')


# def data_analysis(request):
#     pass


# def more_analysis(request):
#     prepaid_plans = Plan.objects.filter(type=Plan.POSTPAID).count()
#     postpaid_plans = Plan.objects.filter(type=Plan.PREPAID).count()
#     postpaid_plans_599 = Plan.objects.filter(name__icontains='599').count()
#     postpaid_plans_799 = Plan.objects.filter(name__icontains='799').count()
#     data = {
#         'prepaid_plans': prepaid_plans,
#         'postpaid_plans': postpaid_plans,
#         'postpaid_plans_599': postpaid_plans_599,
#         'postpaid_plans_799': postpaid_plans_799
#     }
#     return HttpResponse(json.dumps(data), content_type='application/json')