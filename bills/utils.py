from distutils.spawn import find_executable
import re
import slate
import subprocess

__author__ = 'roxnairani'


def parse_data(file, password):
    subprocess.check_call('qpdf --password=' + password + ' --decrypt', file, 'Unencrypted_'+file)
    print 'Unencrypted_'+filename

    with open('Unencrypted_'+filename) as f:
    # with open('Unencrypted_MobileBill_1039029248_349197277_9980996446.pdf') as f:
        report = slate.PDF(f)

        # Split string at multiple white spaces, rejoin into a list w/ 1 space; each page an element in the list
        report_pages = []
        for index, page in enumerate(report):
            report_pages.append(' '.join(report[index].split()))

        """
        PAGE 1 -- BASIC INFORMATION
        """

        ##### SUBSCRIBER MODEL DETAILS
        name_match = re.search(r'121\'M\w+\s+\w+\s+\w+', report_pages[0], re.MULTILINE)
        name = name_match.group()[4:]

        relationship_num_match = re.search(r'number\d+amount', report_pages[0], re.MULTILINE)
        relationship_num = relationship_num_match.group()[6:16]

        phone_number_match = re.search(r'airtel number\d+', report_pages[0], re.MULTILINE)
        phone_number = phone_number_match.group()[13:]

        # Alternative for phone_number match
        # phone_number_match = re.search(r'no.\d+airtel', report_pg_0, re.MULTILINE)
        # phone_number = phone_number_match.group()[3:13]

        address_match = re.search(r'or=\+\-[\w\s]+', report_pages[0], re.MULTILINE)
        address = address_match.group()[5:len(address_match.group())-21]

        city_zip_state_match = re.search(r'oe\w+amount', report_pages[0], re.MULTILINE)
        city = city_zip_state_match.group()[5:len(city_zip_state_match.group())-12]
        zip = city_zip_state_match.group()[-12:-6]
        state = city_zip_state_match.group()[2:5]

        credit_limit_match = re.search(r'[\d,\d.]+credit', report_pages[0], re.MULTILINE)
        credit_limit = credit_limit_match.group()[:len(credit_limit_match.group())-6]

        security_deposit_match = re.search(r'[\d,\d.]+security', report_pages[0], re.MULTILINE)
        security_deposit = security_deposit_match.group()[:len(security_deposit_match.group())-8]


        ##### BILL MODEL DETAILS
        bill_number_match = re.search(r'bill number\d+', report_pages[0], re.MULTILINE)
        bill_number = bill_number_match.group()[11:]

        start_date_match = re.search(r'\d{2}\-\w{3}\-\d{4}to\d+', report_pages[0], re.MULTILINE)
        start_date = start_date_match.group()[:11]

        end_date_match = re.search(r'charges\d+\-\w+\-\d+airtel', report_pages[0], re.MULTILINE)
        end_date = end_date_match.group()[7:18]

        bill_date_match = re.search(r'(\d{2}\-\w{3}\-\d{4}\d+\.)', report_pages[0], re.MULTILINE)
        bill_date = bill_date_match.group()[:11]

        due_date_match = re.search(r'(\d{2}\-\w+\-\d+beforebill number)', report_pages[0], re.MULTILINE)
        due_date = due_date_match.group()[:11]

        total_bill_match = re.search(r'month\'s charges\s+`[\d,\d.]+', report_pages[0], re.MULTILINE)
        total_bill = total_bill_match.group()[17:]

        onetime_charge_match = re.search(r'one time charges\s+[\d,\d.]+', report_pages[0], re.MULTILINE)
        onetime_charge = onetime_charge_match.group()[17:]

        monthly_charge_match = re.search(r'monthly charges\s+[\d,\d.]+', report_pages[0], re.MULTILINE)
        monthly_charge = monthly_charge_match.group()[16:]

        call_charge_match = re.search(r'call charges\s+[\d,\d.]+', report_pages[0], re.MULTILINE)
        call_charge = call_charge_match.group()[13:]

        booster_charge_match = re.search(r'boosters\s+[\d,\d.]+', report_pages[0], re.MULTILINE)
        booster_charge = booster_charge_match.group()[9:]

        data_charge_match = re.search(r'(mobile internet usage\s+[\d,\d.]+)', report_pages[0], re.MULTILINE)
        data_charge = data_charge_match.group()[22:]

        roaming_charge_match = re.search(r'(roaming\s+[\d,\d.]+)', report_pages[0], re.MULTILINE)
        roaming_charge = roaming_charge_match.group()[8:]

        discount_match = re.search(r'(discounts\s+-[\d,\d.]+)', report_pages[0], re.MULTILINE)
        discount = discount_match.group()[10:]

        late_fee_match = re.search(r'(late fee\s+[\d,\d.]+)', report_pages[0], re.MULTILINE)
        late_fee = late_fee_match.group()[9:]

        tax_match = re.search(r'(taxes\s+[\d,\d.]+)', report_pages[0], re.MULTILINE)
        tax = tax_match.group()[6:]

        # print relationship_num, name, phone_number, address, city, zip, state, credit_limit, security_deposit, \
        #     bill_number, start_date, end_date, bill_date, due_date, total_bill, onetime_charge, monthly_charge, \
        #     call_charge, booster_charge, data_charge, roaming_charge, discount, late_fee, tax

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
            volume_check = False

            # Cleaning up front of string to avoid complications with rest of regex parsing
            fuzz_check = re.search(r'([\d\s\w\*]+\d{2}\-\w{3}\-\d{4})', line_to_search)
            if fuzz_check:
                fuzz = fuzz_check.group()[:-11]
                line_to_search = line_to_search.replace(fuzz, "")

            date_check = re.search(r'(\d{2}\-\w{3}\-\d{4})', line_to_search)
            if date_check:
                date = date_check.group()
                line_to_search = line_to_search.replace(date, "")

            time_check = re.search(r'(\d{2}\:\d{2}\:\d{2})', line_to_search)
            if time_check:
                time = time_check.group()
                line_to_search = line_to_search.replace(time, "")

            duration_check = re.search(r'(\d{2}\:\d{2})', line_to_search)
            if duration_check:
                duration = duration_check.group()
                line_to_search = line_to_search.replace(duration, "")

            # Recipient number is 11 digits to a landline, 403airtelgprs$com for data and 10 digits to a cellphone
            if SUB_CATEGORY_BOOLEANS['calls_local_fixed_landline_boolean'] or SUB_CATEGORY_BOOLEANS['calls_std_fixed_landline_boolean']:
                recipient_number_check = re.search(r'(\d{11})', line_to_search)
            elif CATEGORY_BOOLEANS['data_boolean']:
                recipient_number_check = re.search(r'(\d{3}airtelgprs\$com)', line_to_search)
            else:
                recipient_number_check = re.search(r'(\d{10})', line_to_search)
            if recipient_number_check:
                recipient_number = recipient_number_check.group()
                line_to_search = line_to_search.replace(recipient_number, "")
                if CATEGORY_BOOLEANS['data_boolean']:
                    recipient_number = recipient_number.replace('$', '.')

            cost_vol_check = re.search(r'(\d+)', line_to_search)
            if cost_vol_check:
                if duration_check:
                    cost = cost_vol_check.group()  # Need to refine to get paise from next line
                else:
                    if CATEGORY_BOOLEANS['data_boolean']:
                        cost = cost_vol_check.group()[-1]
                        volume = cost_vol_check.group()[:-1]
                        volume_check = True
                    else:
                        volume = cost_vol_check.group()[0]
                        volume_check = True
                        cost = cost_vol_check.group()[1:]

            if date == "" or time == "" or recipient_number == 0:
                pass
            elif duration_check:
                USAGE_DETAILS_LOG[key].append({
                    'date': date,
                    'time': time,
                    'recipient_number': recipient_number,
                    'duration': duration,
                    'cost': cost,
                    'bill': bill_number,
                    'type': type
                })
            elif volume_check:
                USAGE_DETAILS_LOG[key].append({
                    'date': date,
                    'time': time,
                    'recipient_number': recipient_number,
                    'volume': volume,
                    'cost': cost,
                    'bill': bill_number,
                    'type': type
                })

                # Create bill object
                # Get_or_create subscriber object
                # Get_or_create plan object
                # Create all usage objects

        USAGE_DETAILS_LOG = {
            'call_local_same_network': [],
            'call_local_other_network': [],
            'call_local_fixed_landline': [],
            'call_std_same_network': [],
            'call_std_other_network': [],
            'call_std_fixed_landline': [],
            'call_intl': [],
            'sms_local_same_network': [],
            'sms_local_other_network': [],
            'sms_std_same_network': [],
            'sms_std_other_network': [],
            'sms_intl': [],
            'data_2g': [],
            'data_3g': [],
            'data_4g': [],
            'roaming_incoming_call': [],
            'roaming_outgoing_call': [],
            'roaming_incoming_sms': [],
            'roaming_outgoing_sms': [],
        }

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

        def turn_off_category_booleans():
            for key, value in CATEGORY_BOOLEANS.iteritems():
                CATEGORY_BOOLEANS[key] = False

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

        def turn_off_sub_category_booleans():
            for key, value in SUB_CATEGORY_BOOLEANS.iteritems():
                SUB_CATEGORY_BOOLEANS[key] = False

        # PARSING ITEMIZED CALL INFORMATION, STARTS AT PAGE 3
        for page in report_pages[3:]:

            # To avoid issue with splitting at '.' below
            page = page.replace('airtelgprs.com', 'airtelgprs$com')

            for line in page.split("."):
                # Turn on and off category booleans
                calls_local_object = re.search(r'(voice calls - outgoing local)', line)
                if calls_local_object:
                    turn_off_category_booleans()
                    CATEGORY_BOOLEANS['calls_local_boolean'] = True
                calls_std_object = re.search(r'(voice calls - outgoing std)', line)
                if calls_std_object:
                    turn_off_category_booleans()
                    CATEGORY_BOOLEANS['calls_std_boolean'] = True
                sms_local_object = re.search(r'(sms - local)', line)
                if sms_local_object:
                    turn_off_category_booleans()
                    CATEGORY_BOOLEANS['sms_local_boolean'] = True
                sms_std_object = re.search(r'(sms - national)', line)
                if sms_std_object:
                    turn_off_category_booleans()
                    CATEGORY_BOOLEANS['sms_std_boolean'] = True
                data_object = re.search(r'(mobile internet - volume)', line)
                if data_object:
                    turn_off_category_booleans()
                    CATEGORY_BOOLEANS['data_boolean'] = True
                roaming_object = re.search(r'(national roaming)', line)
                if roaming_object:
                    turn_off_category_booleans()
                    CATEGORY_BOOLEANS['roaming_boolean'] = True

                # Turn on and off sub-category booleans based on if category boolean is True or not
                if CATEGORY_BOOLEANS['calls_local_boolean']:
                    calls_local_same_network = re.search(r'(to airtel mobile)', line)
                    if calls_local_same_network:
                        turn_off_sub_category_booleans()
                        SUB_CATEGORY_BOOLEANS['calls_local_same_network_boolean'] = True
                    calls_local_other_network = re.search(r'(to other mobiles)', line)
                    if calls_local_other_network:
                        turn_off_sub_category_booleans()
                        SUB_CATEGORY_BOOLEANS['calls_local_other_network_boolean'] = True
                    calls_local_fixed_landline = re.search(r'(to fixed landline)', line)
                    if calls_local_fixed_landline:
                        turn_off_sub_category_booleans()
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
                        turn_off_sub_category_booleans()
                        SUB_CATEGORY_BOOLEANS['calls_std_same_network_boolean'] = True
                    calls_std_other_network = re.search(r'(to other mobiles)', line)
                    if calls_std_other_network:
                        turn_off_sub_category_booleans()
                        SUB_CATEGORY_BOOLEANS['calls_std_other_network_boolean'] = True
                    calls_std_fixed_landline = re.search(r'(to fixed landline)', line)
                    if calls_std_fixed_landline:
                        turn_off_sub_category_booleans()
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
                        turn_off_sub_category_booleans()
                        SUB_CATEGORY_BOOLEANS['sms_local_same_network_boolean'] = True
                    sms_local_other_network = re.search(r'(to other mobiles)', line)
                    if sms_local_other_network:
                        turn_off_sub_category_booleans()
                        SUB_CATEGORY_BOOLEANS['sms_local_other_network_boolean'] = True

                    if SUB_CATEGORY_BOOLEANS['sms_local_same_network_boolean']:
                        assign_values(line, bill_number, key='sms_local_same_network', type=1)
                    elif SUB_CATEGORY_BOOLEANS['sms_local_other_network_boolean']:
                        assign_values(line, bill_number, key='sms_local_other_network', type=2)

                elif CATEGORY_BOOLEANS['sms_std_boolean']:
                    sms_std_same_network = re.search(r'(to airtel mobile)', line)
                    if sms_std_same_network:
                        turn_off_sub_category_booleans()
                        SUB_CATEGORY_BOOLEANS['sms_std_same_network_boolean'] = True
                    sms_std_other_network = re.search(r'(to other mobiles)', line)
                    if sms_std_other_network:
                        turn_off_sub_category_booleans()
                        SUB_CATEGORY_BOOLEANS['sms_std_other_network_boolean'] = True

                    if SUB_CATEGORY_BOOLEANS['sms_std_same_network_boolean']:
                        assign_values(line, bill_number, key='sms_std_same_network', type=4)
                    elif SUB_CATEGORY_BOOLEANS['sms_std_other_network_boolean']:
                        assign_values(line, bill_number, key='sms_std_other_network', type=5)

                elif CATEGORY_BOOLEANS['data_boolean']:
                    data_2g = re.search(r'(mobile internet 2g)', line)
                    if data_2g:
                        turn_off_sub_category_booleans()
                        SUB_CATEGORY_BOOLEANS['data_2g_boolean'] = True
                    data_3g = re.search(r'(mobile internet 3g)', line)
                    if data_3g:
                        turn_off_sub_category_booleans()
                        SUB_CATEGORY_BOOLEANS['data_3g_boolean'] = True
                    data_4g = re.search(r'(mobile internet 4g)', line)
                    if data_4g:
                        turn_off_sub_category_booleans()
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
                        turn_off_sub_category_booleans()
                        SUB_CATEGORY_BOOLEANS['roaming_incoming_calls_boolean'] = True
                    roaming_outgoing_calls = re.search(r'(outgoing calls - voice)', line)
                    if roaming_outgoing_calls:
                        turn_off_sub_category_booleans()
                        SUB_CATEGORY_BOOLEANS['roaming_outgoing_calls_boolean'] = True
                    roaming_sms = re.search(r'(sms)', line)
                    if roaming_sms:
                        turn_off_sub_category_booleans()
                        SUB_CATEGORY_BOOLEANS['roaming_sms_boolean'] = True

                    if SUB_CATEGORY_BOOLEANS['roaming_incoming_calls_boolean']:
                        assign_values(line, bill_number, key='roaming_incoming_call', type=1)
                    elif SUB_CATEGORY_BOOLEANS['roaming_outgoing_calls_boolean']:
                        assign_values(line, bill_number, key='roaming_outgoing_call', type=2)
                    elif SUB_CATEGORY_BOOLEANS['roaming_sms_boolean']:
                        assign_values(line, bill_number, key='roaming_incoming_sms', type=3)
