__author__ = 'roxnairani'
import re

# CHANGE BILL NUMBER TO FROM SLATETEST.PY
bill_number = 0

##### PAGE 4+ -- CALL/SMS/DATA/ROAMING DETAILS INFORMATION


def find_calls_info(line_to_search):
    calls_same_network_index = re.search(r'(to airtel mobile)', line_to_search)
    print "find calls function"
    print calls_same_network_index
    calls_other_network_index = re.search(r'(to other mobiles)', line_to_search)
    print calls_other_network_index
    calls_fixed_landline_index = re.search(r'(to fixed landline)', line_to_search)
    return calls_same_network_index, calls_other_network_index, calls_fixed_landline_index

def find_sms_info(line_to_search):
    sms_same_network_index = re.search(r'(to airtel mobile)', line_to_search)
    sms_other_network_index = re.search(r'(to other mobiles)', line_to_search)
    return sms_same_network_index, sms_other_network_index

def assign_values(line_to_search, bill_number, key, type):
    date = ""
    time = ""
    recipient_number = 0
    duration = ""
    volume = 0
    cost = 0

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

    recipient_number_cost_check = re.search(r'(\d+)', line_to_search)
    if recipient_number_cost_check:
        recipient_number = recipient_number_cost_check.group()[1:12]
        cost = recipient_number_cost_check.group()[-1]
        line_to_search = line_to_search.replace(recipient_number, "")

    volume_check = re.search(r'(\d)', line_to_search)
    if volume_check:
        volume = volume_check.group()

    if duration_check and volume_check:
        return "ERROR - CAN'T HAVE BOTH DURATION AND VOLUME"
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

# PARSING ITEMIZED CALL INFORMATION
# for line in report_pg_itemized_data.split("."):

report_test = 'e1.voice calls - outgoing localhh:mm:ss1.1 to airtel mobile105-Feb-201414:12:21963282983703:232.00**205-Feb-201416:44:31963282983700:340.50*'
for line in report_test.split("."):
    print line
    calls_local_index = re.search(r'(voice calls - outgoing local)', line)
    print calls_local_index
    calls_std_index = re.search(r'(voice calls - outgoing std)', line)
    print calls_std_index
    sms_local_index = re.search(r'(sms - local)', line)
    print sms_local_index
    sms_std_index = re.search(r'(sms - std)', line)
    print sms_std_index
    data_index = re.search(r'(mobile internet - volume)', line)
    print data_index
    roaming_index = re.search(r'(national roaming)', line)
    print roaming_index

    # If calls_std_index, sms_local/std_index, data_index, roaming_index are not defined,
    # itemized details are of 'voice calls - outgoing local' (similar logic continued for all other elif statements)
    if calls_local_index and not calls_std_index and not sms_local_index and not sms_std_index and not data_index and not roaming_index:
        calls_local_same_network_index, calls_local_other_network_index, calls_local_fixed_landline_index = find_calls_info(line)
        print "in sub function"
        print calls_local_same_network_index, calls_local_other_network_index, calls_local_fixed_landline_index
        if calls_local_same_network_index and not calls_local_other_network_index and not calls_local_fixed_landline_index:
            print 'calls_local_same_network'
            assign_values(line, bill_number, key='call_local_same_network', type=1)
        elif calls_local_other_network_index and not calls_local_fixed_landline_index:
            print 'calls_local_other_network'
            assign_values(line, bill_number, key='call_local_other_network', type=2)
        else:
            assign_values(line, bill_number, key='call_local_fixed_landline', type=2)
    elif calls_std_index and not sms_local_index and not sms_std_index and not data_index and not roaming_index:
        calls_std_same_network_index, calls_std_other_network_index, calls_std_fixed_landline_index = find_calls_info(line)
        if calls_std_same_network_index and not calls_std_other_network_index and not calls_std_fixed_landline_index:
            assign_values(line, bill_number, key='call_std_same_network', type=4)
        elif calls_std_other_network_index and not calls_std_fixed_landline_index:
            assign_values(line, bill_number, key='call_std_other_network', type=5)
        else:
            assign_values(line, bill_number, key='call_std_fixed_landline', type=6)
    elif sms_local_index and not sms_std_index and not data_index and not roaming_index:
        sms_local_same_network_index, sms_local_other_network_index = find_sms_info(line)
        if sms_local_same_network_index and not sms_local_other_network_index:
            assign_values(line, bill_number, key='sms_local_same_network', type=1)
        else:
            assign_values(line, bill_number, key='sms_local_other_network', type=2)
    elif sms_std_index and not data_index and not roaming_index:
        sms_std_same_network_index, sms_std_other_network_index = find_sms_info(line)
        if sms_std_same_network_index and not sms_std_other_network_index:
            assign_values(line, bill_number, key='sms_std_same_network', type=4)
        else:
            assign_values(line, bill_number, key='sms_std_other_network', type=5)
    elif data_index and not roaming_index:
        data_2g_index = re.search(r'(mobile internet 2g)', line)
        data_3g_index = re.search(r'(mobile internet 3g)', line)
        data_4g_index = re.search(r'(mobile internet 4g)', line)
        if data_2g_index and not data_3g_index and not data_4g_index:
            assign_values(line, bill_number, key='data_2g', type=1)
        elif data_3g_index and not data_4g_index:
            assign_values(line, bill_number, key='data_2g', type=2)
        else:
            assign_values(line, bill_number, key='data_4g', type=3)
    elif roaming_index:
        roaming_incoming_calls_index = re.search(r'(incoming calls - voice)', line)
        roaming_outgoing_calls_index = re.search(r'(outgoing calls - voice)', line)
        roaming_sms_index = re.search(r'(sms)', line)
        if roaming_incoming_calls_index and not roaming_outgoing_calls_index and not roaming_sms_index:
            assign_values(line, bill_number, key='roaming_incoming_call', type=1)
        elif roaming_outgoing_calls_index and not roaming_sms_index:
            assign_values(line, bill_number, key='roaming_outgoing_call', type=2)
        else:
            assign_values(line, bill_number, key='roaming_incoming_sms', type=3)

print USAGE_DETAILS_LOG['call_local_same_network']


        # Create bill object
        # Get_or_create subscriber object
        # Get_or_create plan object
        # Create all usage objects