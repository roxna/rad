import datetime
from django.core.management.base import BaseCommand
import re
import slate
from bills.models import Subscriber, Plan, Bill, Call, Booster, Data, Roaming


class Command(BaseCommand):
    help = 'Help text goes here'

    def handle(self, **options):
        # Roxna! How is all of this one huge function?! You could split this up into a 'pipeline' type of model
        # where you call multiple, smaller functions, one after another.
        # A quick obvious way would be to split it up by the different pages you're parsing.
        
        # Parsing/reading PDF data is not fun though, congrats on getting it all working!
        with open('bills/pdfs/Unencrypted_MobileBill_1039029248_349197277_9980996446.pdf') as f:
            report = slate.PDF(f)

            # Split string at multiple white spaces, rejoin into a list w/ 1 space; each page an element in the list
            report_pages = []
            for index, page in enumerate(report):
                report_pages.append(' '.join(report[index].split()))

            """
            PAGE 1 -- SUBSCRIBER INFORMATION
            """

            ##### SUBSCRIBER MODEL DETAILS #####

            # should make variables called first_page, second_page, etc instead of accessing report_pages[0] over and over
            name_match = re.search(r'121\'M\w+\s+\w+\s+\w+', report_pages[0], re.MULTILINE)
            name = name_match.group()[4:]

            relationship_num_match = re.search(r'number\d+amount', report_pages[0], re.MULTILINE)
            relationship_num = int(relationship_num_match.group()[6:16])

            phone_number_match = re.search(r'airtel number\d+', report_pages[0], re.MULTILINE)
            phone_number = int(phone_number_match.group()[13:])

            # Alternative for phone_number match
            # phone_number_match = re.search(r'no.\d+airtel', report_pg_0, re.MULTILINE)
            # phone_number = phone_number_match.group()[3:13]

            address_match = re.search(r'or=\+\-[\w\s]+', report_pages[0], re.MULTILINE)
            address = address_match.group()[5:len(address_match.group())-21]

            city_zip_state_match = re.search(r'oe\w+amount', report_pages[0], re.MULTILINE)
            city = city_zip_state_match.group()[5:len(city_zip_state_match.group())-12]
            zip = int(city_zip_state_match.group()[-12:-6])
            state = city_zip_state_match.group()[2:5]

            credit_limit_match = re.search(r'[\d,\d.]+credit', report_pages[0], re.MULTILINE)
            credit_limit = int("".join(credit_limit_match.group()[:len(credit_limit_match.group())-9].strip().split(',')))

            security_deposit_match = re.search(r'[\d,\d.]+security', report_pages[0], re.MULTILINE)
            security_deposit = int("".join(security_deposit_match.group()[:len(security_deposit_match.group())-11].strip().split(',')))

            subscriber, subscriber_created = Subscriber.objects.get_or_create(
                phone_number=phone_number,
                defaults={
                    name: name,
                    address: address,
                    city: city,
                    state: state,
                    zip: zip,
                    relationship_num: relationship_num,
                    credit_limit: credit_limit,
                    security_deposit: security_deposit
                }
            )

            """
            PAGE 2 -- PLAN INFORMATION
            """

            plan_match = re.search(r'(my plan \d{3})', report_pages[1], re.MULTILINE)
            plan_name = plan_match.group()

            min_rental_match = re.search(r'(rental` \d+)', report_pages[1], re.MULTILINE)
            min_rental = int(min_rental_match.group()[8:])

            currency = 'INR'

            plan, plan_created = Plan.objects.get_or_create(
                name=plan_name,
                defaults={
                    type: 1,
                    min_rental: min_rental,
                    currency: currency
                }
            )

            # Page 3?
            """
            PAGE 1 -- BILL INFORMATION
            """

            ##### BILL MODEL DETAILS #####

            bill_number_match = re.search(r'bill number\d+', report_pages[0], re.MULTILINE)
            bill_number = int(bill_number_match.group()[11:])

            start_date_match = re.search(r'\d{2}\-\w{3}\-\d{4}to\d+', report_pages[0], re.MULTILINE)
            start_date = datetime.datetime.strptime(start_date_match.group()[:11], '%d-%b-%Y').date()

            end_date_match = re.search(r'charges\d+\-\w+\-\d+airtel', report_pages[0], re.MULTILINE)
            end_date = datetime.datetime.strptime(end_date_match.group()[7:18], '%d-%b-%Y').date()

            bill_date_match = re.search(r'(\d{2}\-\w{3}\-\d{4}\d+\.)', report_pages[0], re.MULTILINE)
            bill_date = datetime.datetime.strptime(bill_date_match.group()[:11], '%d-%b-%Y').date()

            due_date_match = re.search(r'(\d{2}\-\w+\-\d+beforebill number)', report_pages[0], re.MULTILINE)
            due_date = datetime.datetime.strptime(due_date_match.group()[:11], '%d-%b-%Y').date()

            # Some of this looks like it could be abstracted out, it seems like for a lot there's a "string"
            # you're trying to match on following by numbers. Could make a function you could call that
            # you pass a couple of parameters to, to clean the code up.
            total_bill_match = re.search(r'month\'s charges\s+`[\d,\d.]+', report_pages[0], re.MULTILINE)
            total_bill = float(total_bill_match.group()[17:]) if total_bill_match else 0.00

            onetime_charge_match = re.search(r'one time charges\s+[\d,\d.]+', report_pages[0], re.MULTILINE)
            onetime_charge = float(onetime_charge_match.group()[17:]) if onetime_charge_match else 0.00

            monthly_charge_match = re.search(r'monthly charges\s+[\d,\d.]+', report_pages[0], re.MULTILINE)
            monthly_charge = float(monthly_charge_match.group()[16:]) if monthly_charge_match else 0.00

            call_charge_match = re.search(r'call charges\s+[\d,\d.]+', report_pages[0], re.MULTILINE)
            call_charge = float(call_charge_match.group()[13:]) if call_charge_match else 0.00

            booster_charge_match = re.search(r'boosters\s+[\d,\d.]+', report_pages[0], re.MULTILINE)
            booster_charge = float(booster_charge_match.group()[9:]) if booster_charge_match else 0.00

            data_charge_match = re.search(r'(mobile internet usage\s+[\d,\d.]+)', report_pages[0], re.MULTILINE)
            data_charge = float("".join(data_charge_match.group()[22:].strip().split(','))) if data_charge_match else 0.00

            roaming_charge_match = re.search(r'(roaming\s+[\d,\d.]+)', report_pages[0], re.MULTILINE)
            roaming_charge = float(roaming_charge_match.group()[8:]) if roaming_charge_match else 0.00

            discount_match = re.search(r'(discounts\s+-[\d,\d.]+)', report_pages[0], re.MULTILINE)
            discount = float("".join(discount_match.group()[10:].strip().split(','))) if discount_match else 0.00

            late_fee_match = re.search(r'(late fee\s+[\d,\d.]+)', report_pages[0], re.MULTILINE)
            late_fee = float(late_fee_match.group()[9:]) if late_fee_match else 0.00

            tax_match = re.search(r'(taxes\s+[\d,\d.]+)', report_pages[0], re.MULTILINE)
            tax = float(tax_match.group()[6:]) if tax_match else 0.00

            bill, bill_created = Bill.objects.get_or_create(
                number=bill_number,
                subscriber=subscriber,
                plan=plan,
                defaults={
                    start_date: start_date,
                    end_date: end_date,
                    bill_date: bill_date,
                    due_date: due_date,
                    total_bill: total_bill,
                    onetime_charge: onetime_charge,
                    monthly_charge: monthly_charge,
                    call_charge: call_charge,
                    booster_charge: booster_charge,
                    data_charge: data_charge,
                    roaming_charge: roaming_charge,
                    discount: discount,
                    late_fee: late_fee,
                    tax: tax
                }
            )

            """
            PAGE 4+ -- CALL/SMS/DATA/ROAMING DETAILS INFORMATION
            """

            def assign_values(line_to_search, bill_number, key, type):
                date = ""
                time = ""
                recipient_number = 0
                duration = ""
                volume = 0
                cost = 0

                # Cleaning up front of string to avoid complications with rest of regex parsing
                fuzz_check = re.search(r'([\d\s\w\*]+\d{2}\-\w{3}\-\d{4})', line_to_search)
                if fuzz_check:
                    fuzz = fuzz_check.group()[:-11]
                    line_to_search = line_to_search.replace(fuzz, "")

                date_check = re.search(r'(\d{2}\-\w{3}\-\d{4})', line_to_search)
                if date_check:
                    date = date_check.group()
                    line_to_search = line_to_search.replace(date, "")
                    date = datetime.datetime.strptime(date, '%d-%b-%Y').date()

                time_check = re.search(r'(\d{2}\:\d{2}\:\d{2})', line_to_search)
                if time_check:
                    time = time_check.group()
                    line_to_search = line_to_search.replace(time, "")
                    time = datetime.datetime.strptime(time, '%H:%M:%S').time()

                duration_check = re.search(r'(\d{2}\:\d{2})', line_to_search)
                if duration_check:
                    duration = duration_check.group()
                    line_to_search = line_to_search.replace(duration, "")
                    volume = 0

                # Recipient number is 11 digits to a landline, 403airtelgprs$com for data and 10 digits to a cellphone
                if SUB_CATEGORY_BOOLEANS['calls_local_fixed_landline_boolean'] or SUB_CATEGORY_BOOLEANS['calls_std_fixed_landline_boolean']:
                    recipient_number_check = re.search(r'(\d{11})', line_to_search)
                elif CATEGORY_BOOLEANS['data_boolean']:
                    recipient_number_check = re.search(r'(\d{3}airtelgprs\$com)', line_to_search)
                else:
                    recipient_number_check = re.search(r'(\d{10})', line_to_search)
                if recipient_number_check:
                    recipient_number = recipient_number_check.group()
                    if CATEGORY_BOOLEANS['data_boolean']:
                        # recipient_number = recipient_number.replace('$', '.')  # Receip # is an int field
                        recipient_number = recipient_number_check.group()[:3]
                    line_to_search = line_to_search.replace(recipient_number, "")
                    recipient_number = int(recipient_number.strip())

                cost_vol_check = re.search(r'(\d+)', line_to_search)
                if cost_vol_check:
                    if duration_check:
                        cost = float(cost_vol_check.group().strip())  # Need to refine to get paise from next line
                    else:
                        duration = '00:00'
                        if CATEGORY_BOOLEANS['data_boolean']:
                            # For corner cases/specific lines where the algorithm doesn't hold
                            try:
                                cost = float(cost_vol_check.group().strip()[-1])
                                volume = int(cost_vol_check.group().strip()[:-1])
                            except ValueError:
                                pass
                        else:
                            # For corner cases/specific lines where the algorithm doesn't hold
                            try:
                                volume = int(cost_vol_check.group().strip()[0])
                                cost = float(cost_vol_check.group().strip()[1:])
                            except ValueError:
                                pass

                # Currently doesn't get paise from next line so rounding up
                cost = 0.50 if cost == 0 else cost

                # You can abstract out all of the 'creates' below since they all seem to take the same information.
                # You could have a variable that you save to represnet Call, Booster, etc then call create on that dynamically.
                # Will clean up a lot of this part.
                if date == "" or time == "" or recipient_number == 0:
                    pass
                # Use elif key in ['call_local_same_network', 'call_local_other_network', etc]:
                elif key == 'call_local_same_network' or key == 'call_local_other_network' or key == 'call_local_fixed_landline' \
                        or key == 'call_std_same_network' or key == 'call_std_other_network' or key == 'call_std_fixed_landline' \
                        or key == 'call_intl':
                    Call.objects.create(
                        date=date,
                        time=time,
                        recipient_number=recipient_number,
                        duration=duration,
                        volume=volume,
                        cost=cost,
                        bill=Bill.objects.get(number=bill_number),
                        type=type,
                    )
                elif key == 'sms_local_same_network' or key == 'sms_local_other_network' or key == 'sms_std_same_network' \
                        or key == 'sms_std_other_network' or key == 'sms_intl':
                    Booster.objects.create(
                        date=date,
                        time=time,
                        recipient_number=recipient_number,
                        duration=duration,
                        volume=volume,
                        cost=cost,
                        bill=Bill.objects.get(number=bill_number),
                        type=type,
                    )
                elif key == 'data_2g' or key == 'data_3g' or key == 'data_4g':
                    Data.objects.create(
                        date=date,
                        time=time,
                        recipient_number=recipient_number,
                        duration=duration,
                        volume=volume,
                        cost=cost,
                        bill=Bill.objects.get(number=bill_number),
                        type=type,
                    )
                elif key == 'roaming_incoming_call' or key == 'roaming_outgoing_call' or key == 'roaming_incoming_sms' \
                        or key == 'roaming_outgoing_sms':
                    Roaming.objects.create(
                        date=date,
                        time=time,
                        recipient_number=recipient_number,
                        duration=duration,
                        volume=volume,
                        cost=cost,
                        bill=Bill.objects.get(number=bill_number),
                        type=type,
                    )

            # Checkout defaultdicts documentation for cleaning these variables up
            # Booleans for main categories (calls/sms/data/roaming)
            CATEGORY_BOOLEANS = {
                'calls_local_boolean': False,
                'calls_std_boolean': False,
                'calls_intl_boolean': False,
                'sms_local_boolean': False,
                'sms_std_boolean': False,
                'sms_intl_boolean': False,
                'data_boolean': False,
                'roaming_boolean': False,
            }

            # Booleans for sub-categories (same network/other network/landline etc)
            SUB_CATEGORY_BOOLEANS = {
                'calls_local_same_network_boolean': False,
                'calls_local_other_network_boolean': False,
                'calls_local_fixed_landline_boolean': False,
                'calls_std_same_network_boolean': False,
                'calls_std_other_network_boolean': False,
                'calls_std_fixed_landline_boolean': False,

                'sms_local_same_network_boolean': False,
                'sms_local_other_network_boolean': False,
                'sms_std_same_network_boolean': False,
                'sms_std_other_network_boolean': False,

                'data_2g_boolean': False,
                'data_3g_boolean': False,
                'data_4g_boolean': False,

                'roaming_incoming_calls_boolean': False,
                'roaming_outgoing_calls_boolean': False,
                'roaming_sms_boolean': False,
            }

            def turn_off_booleans(boolean_dictionary):
                for key, value in boolean_dictionary.iteritems():
                    boolean_dictionary[key] = False
                    

            # PARSING ITEMIZED CALL INFORMATION, STARTS AT PAGE 3
            for page in report_pages[3:]:

                # To avoid issue with splitting at '.' below
                page = page.replace('airtelgprs.com', 'airtelgprs$com')

                # This part of the code could also definitely be abstracted out. Lots of this looks a bit repeated.
                # Usually by using an object-oriented approach with classes or breaking this into multiple functions
                # it could be a lot more readable/maintainable 
                for line in page.split("."):
                    # Turn on and off category booleans
                    calls_local_object = re.search(r'(voice calls - outgoing local)', line)
                    if calls_local_object:
                        turn_off_booleans(CATEGORY_BOOLEANS)
                        CATEGORY_BOOLEANS['calls_local_boolean'] = True
                    calls_std_object = re.search(r'(voice calls - outgoing std)', line)
                    if calls_std_object:
                        turn_off_booleans(CATEGORY_BOOLEANS)
                        CATEGORY_BOOLEANS['calls_std_boolean'] = True
                    sms_local_object = re.search(r'(sms - local)', line)
                    if sms_local_object:
                        turn_off_booleans(CATEGORY_BOOLEANS)
                        CATEGORY_BOOLEANS['sms_local_boolean'] = True
                    sms_std_object = re.search(r'(sms - national)', line)
                    if sms_std_object:
                        turn_off_booleans(CATEGORY_BOOLEANS)
                        CATEGORY_BOOLEANS['sms_std_boolean'] = True
                    data_object = re.search(r'(mobile internet - volume)', line)
                    if data_object:
                        turn_off_booleans(CATEGORY_BOOLEANS)
                        CATEGORY_BOOLEANS['data_boolean'] = True
                    roaming_object = re.search(r'(national roaming)', line)
                    if roaming_object:
                        turn_off_booleans(CATEGORY_BOOLEANS)
                        CATEGORY_BOOLEANS['roaming_boolean'] = True

                    # Turn on and off sub-category booleans based on if category boolean is True or not
                    if CATEGORY_BOOLEANS['calls_local_boolean']:
                        calls_local_same_network = re.search(r'(to airtel mobile)', line)
                        if calls_local_same_network:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['calls_local_same_network_boolean'] = True
                        calls_local_other_network = re.search(r'(to other mobiles)', line)
                        if calls_local_other_network:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['calls_local_other_network_boolean'] = True
                        calls_local_fixed_landline = re.search(r'(to fixed landline)', line)
                        if calls_local_fixed_landline:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['calls_local_fixed_landline_boolean'] = True

                        if SUB_CATEGORY_BOOLEANS['calls_local_same_network_boolean']:
                            assign_values(line, bill_number, key='call_local_same_network', type=1)
                        elif SUB_CATEGORY_BOOLEANS['calls_local_other_network_boolean']:
                            assign_values(line, bill_number, key='call_local_other_network', type=2)
                        elif SUB_CATEGORY_BOOLEANS['calls_local_fixed_landline_boolean']:
                            assign_values(line, bill_number, key='call_local_fixed_landline', type=3)

                    elif CATEGORY_BOOLEANS['calls_std_boolean']:
                        calls_std_same_network = re.search(r'(to airtel mobile)', line)
                        if calls_std_same_network:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['calls_std_same_network_boolean'] = True
                        calls_std_other_network = re.search(r'(to other mobiles)', line)
                        if calls_std_other_network:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['calls_std_other_network_boolean'] = True
                        calls_std_fixed_landline = re.search(r'(to fixed landline)', line)
                        if calls_std_fixed_landline:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['calls_std_fixed_landline_boolean'] = True

                        if SUB_CATEGORY_BOOLEANS['calls_std_same_network_boolean']:
                            assign_values(line, bill_number, key='call_std_same_network', type=4)
                        elif SUB_CATEGORY_BOOLEANS['calls_std_other_network_boolean']:
                            assign_values(line, bill_number, key='call_std_other_network', type=5)
                        elif SUB_CATEGORY_BOOLEANS['calls_std_fixed_landline_boolean']:
                            assign_values(line, bill_number, key='call_std_fixed_landline', type=6)

                    elif CATEGORY_BOOLEANS['sms_local_boolean']:
                        sms_local_same_network = re.search(r'(to airtel mobile)', line)
                        if sms_local_same_network:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['sms_local_same_network_boolean'] = True
                        sms_local_other_network = re.search(r'(to other mobiles)', line)
                        if sms_local_other_network:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['sms_local_other_network_boolean'] = True

                        if SUB_CATEGORY_BOOLEANS['sms_local_same_network_boolean']:
                            assign_values(line, bill_number, key='sms_local_same_network', type=1)
                        elif SUB_CATEGORY_BOOLEANS['sms_local_other_network_boolean']:
                            assign_values(line, bill_number, key='sms_local_other_network', type=2)

                    elif CATEGORY_BOOLEANS['sms_std_boolean']:
                        sms_std_same_network = re.search(r'(to airtel mobile)', line)
                        if sms_std_same_network:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['sms_std_same_network_boolean'] = True
                        sms_std_other_network = re.search(r'(to other mobiles)', line)
                        if sms_std_other_network:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['sms_std_other_network_boolean'] = True

                        if SUB_CATEGORY_BOOLEANS['sms_std_same_network_boolean']:
                            assign_values(line, bill_number, key='sms_std_same_network', type=4)
                        elif SUB_CATEGORY_BOOLEANS['sms_std_other_network_boolean']:
                            assign_values(line, bill_number, key='sms_std_other_network', type=5)

                    elif CATEGORY_BOOLEANS['data_boolean']:
                        data_2g = re.search(r'(mobile internet 2g)', line)
                        if data_2g:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['data_2g_boolean'] = True
                        data_3g = re.search(r'(mobile internet 3g)', line)
                        if data_3g:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['data_3g_boolean'] = True
                        data_4g = re.search(r'(mobile internet 4g)', line)
                        if data_4g:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['data_4g_boolean'] = True

                        if SUB_CATEGORY_BOOLEANS['data_2g_boolean']:
                            assign_values(line, bill_number, key='data_2g', type=1)
                        elif SUB_CATEGORY_BOOLEANS['data_3g_boolean']:
                            assign_values(line, bill_number, key='data_3g', type=2)
                        elif SUB_CATEGORY_BOOLEANS['data_4g_boolean']:
                            assign_values(line, bill_number, key='data_4g', type=3)

                    elif CATEGORY_BOOLEANS['roaming_boolean']:
                        roaming_incoming_calls = re.search(r'(incoming calls - voice)', line)
                        if roaming_incoming_calls:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['roaming_incoming_calls_boolean'] = True
                        roaming_outgoing_calls = re.search(r'(outgoing calls - voice)', line)
                        if roaming_outgoing_calls:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['roaming_outgoing_calls_boolean'] = True
                        roaming_sms = re.search(r'(sms)', line)
                        if roaming_sms:
                            turn_off_booleans(SUB_CATEGORY_BOOLEANS)
                            SUB_CATEGORY_BOOLEANS['roaming_sms_boolean'] = True

                        if SUB_CATEGORY_BOOLEANS['roaming_incoming_calls_boolean']:
                            assign_values(line, bill_number, key='roaming_incoming_call', type=1)
                        elif SUB_CATEGORY_BOOLEANS['roaming_outgoing_calls_boolean']:
                            assign_values(line, bill_number, key='roaming_outgoing_call', type=2)
                        elif SUB_CATEGORY_BOOLEANS['roaming_sms_boolean']:
                            assign_values(line, bill_number, key='roaming_incoming_sms', type=3)
