# __author__ = 'roxnairani'
import slate
import re

with open('Unencrypted_MobileBill_1039029248_349197277_9980996446.pdf') as f:
    report = slate.PDF(f)

    # Split string at multiple white spaces, rejoin into a list w/ 1 space; each page an element in the list
    report_pages = []
    for index, page in enumerate(report):
        report_pages.append(' '.join(report[index].split()))

    print report_pages[1]

#
# # CHANGE BILL NUMBER TO FROM SLATETEST.PY
# bill_number = 0
#
# ##### PAGE 4+ -- CALL/SMS/DATA/ROAMING DETAILS INFORMATION
#
#
# def assign_values(line_to_search, bill_number, key, type):
#     date = ""
#     time = ""
#     recipient_number = 0
#     duration = ""
#     volume = 0
#     cost = 0
#     volume_check = False
#
#     print line_to_search
#     date_check = re.search(r'(\d{2}\-\w{3}\-\d{4})', line_to_search)
#     if date_check:
#         date = date_check.group()
#         print date
#         line_to_search = line_to_search.replace(date, "")
#         print line_to_search
#
#     time_check = re.search(r'(\d{2}\:\d{2}\:\d{2})', line_to_search)
#     if time_check:
#         time = time_check.group()
#         print time
#         line_to_search = line_to_search.replace(time, "")
#
#     duration_check = re.search(r'(\d{2}\:\d{2})', line_to_search)
#     if duration_check:
#         duration = duration_check.group()
#         print 'dur', duration
#         line_to_search = line_to_search.replace(duration, "")
#
#     recipient_number_cost_check = re.search(r'(\d{12,13})', line_to_search)
#     if recipient_number_cost_check:
#         recipient_number = recipient_number_cost_check.group()[1:11]
#         cost = recipient_number_cost_check.group()[-1]  # Need to refine to get paise from next line
#         print recipient_number, cost
#         line_to_search = line_to_search.replace(recipient_number, "")
#         print line_to_search
#
#     if not duration_check:
#         volume_check = re.search(r'(\d)', line_to_search)
#         volume = volume_check.group()
#         print 'vol', volume_check
#
#     if date == "" and time == "":
#         pass
#     elif duration_check and volume_check:
#         return "ERROR - CAN'T HAVE BOTH DURATION AND VOLUME"
#     elif duration_check:
#         USAGE_DETAILS_LOG[key].append({
#             'date': date,
#             'time': time,
#             'recipient_number': recipient_number,
#             'duration': duration,
#             'cost': cost,
#             'bill': bill_number,
#             'type': type
#         })
#     elif volume_check:
#         USAGE_DETAILS_LOG[key].append({
#             'date': date,
#             'time': time,
#             'recipient_number': recipient_number,
#             'volume': volume,
#             'cost': cost,
#             'bill': bill_number,
#             'type': type
#         })
#
# USAGE_DETAILS_LOG = {
#     'call_local_same_network': [],
#     'call_local_other_network': [],
#     'call_local_fixed_landline': [],
#     'call_std_same_network': [],
#     'call_std_other_network': [],
#     'call_std_fixed_landline': [],
#     'call_intl': [],
#     'sms_local_same_network': [],
#     'sms_local_other_network': [],
#     'sms_std_same_network': [],
#     'sms_std_other_network': [],
#     'sms_intl': [],
#     'data_2g': [],
#     'data_3g': [],
#     'data_4g': [],
#     'roaming_incoming_call': [],
#     'roaming_outgoing_call': [],
#     'roaming_incoming_sms': [],
#     'roaming_outgoing_sms': [],
# }
#
# # Pre-defined variables
# calls_local_boolean = True
# calls_std_boolean = False
# sms_local_boolean = False
# sms_std_boolean = False
# data_boolean = False
# roaming_boolean = False
#
# calls_local_same_network_boolean = False
# calls_local_other_network_boolean = False
# calls_local_fixed_landline_boolean = False
# calls_std_same_network_boolean = False
# calls_std_other_network_boolean = False
# calls_std_fixed_landline_boolean = False
#
# sms_local_same_network_boolean = False
# sms_local_other_network_boolean = False
# sms_std_same_network_boolean = False
# sms_std_other_network_boolean = False
#
# data_2g_boolean = False
# data_3g_boolean = False
# data_4g_boolean = False
#
# roaming_incoming_calls_boolean = False
# roaming_outgoing_calls_boolean = False
# roaming_sms_boolean = False
#
#
# # PARSING ITEMIZED CALL INFORMATION
# # for line in report_pg_itemized_data.split("."):
#
# report_test = 'e1.voice calls - outgoing localhh:mm:ss1.1 to airtel mobile105-Feb-201414:12:21963282983703:232.00**205-Feb-201416:44:31963282983700:340.50*'
# for line in report_test.split("."):
#     calls_local_object = re.search(r'(voice calls - outgoing local)', line)
#     calls_std_object = re.search(r'(voice calls - outgoing std)', line)
#     if calls_std_object:
#         calls_local_boolean = False
#         calls_std_boolean = True
#     sms_local_object = re.search(r'(sms - local)', line)
#     if sms_local_object:
#         calls_std_boolean = False
#         sms_local_boolean = True
#     sms_std_object = re.search(r'(sms - std)', line)
#     if sms_std_object:
#         sms_local_boolean = False
#         sms_std_boolean = True
#     data_object = re.search(r'(mobile internet - volume)', line)
#     if data_object:
#         sms_std_boolean = False
#         data_boolean = True
#     roaming_object = re.search(r'(national roaming)', line)
#     if roaming_object:
#         data_boolean = False
#         roaming_boolean = True
#
#     # If calls_std_index, sms_local/std_index, data_index, roaming_index are not defined,
#     # itemized details are of 'voice calls - outgoing local' (similar logic continued for all other elif statements)
#     # if calls_local_boolean and not calls_std_boolean and not sms_local_boolean and not sms_std_boolean and not data_boolean and not roaming_boolean:
#     if calls_local_boolean:
#         calls_local_same_network_index = re.search(r'(to airtel mobile)', line)
#         if calls_local_same_network_index:
#             calls_local_same_network_boolean = True
#         calls_local_other_network_index = re.search(r'(to other mobiles)', line)
#         if calls_local_other_network_index:
#             calls_local_same_network_boolean = False
#             calls_local_other_network_boolean = True
#         calls_local_fixed_landline_index = re.search(r'(to fixed landline)', line)
#         if calls_local_fixed_landline_index:
#             calls_local_other_network_boolean = False
#             calls_local_fixed_landline_boolean = True
#
#         if calls_local_same_network_boolean:
#             print 'calls_local_same_network'
#             assign_values(line, bill_number, key='call_local_same_network', type=1)
#         elif calls_local_other_network_boolean:
#             print 'calls_local_other_network'
#             assign_values(line, bill_number, key='call_local_other_network', type=2)
#         elif calls_local_fixed_landline_boolean:
#             assign_values(line, bill_number, key='call_local_fixed_landline', type=2)
#
#     elif calls_std_boolean:
#         calls_std_same_network_index = re.search(r'(to airtel mobile)', line)
#         if calls_std_same_network_index:
#             calls_std_same_network_boolean = True
#         calls_std_other_network_index = re.search(r'(to other mobiles)', line)
#         if calls_std_other_network_index:
#             calls_std_same_network_boolean = False
#             calls_std_other_network_boolean = True
#         calls_std_fixed_landline_index = re.search(r'(to fixed landline)', line)
#         if calls_std_fixed_landline_index:
#             calls_std_other_network_boolean = False
#             calls_std_fixed_landline_boolean = True
#
#         if calls_std_same_network_boolean:
#             assign_values(line, bill_number, key='call_std_same_network', type=4)
#         elif calls_std_other_network_boolean:
#             assign_values(line, bill_number, key='call_std_other_network', type=5)
#         elif calls_std_fixed_landline_boolean:
#             assign_values(line, bill_number, key='call_std_fixed_landline', type=6)
#
#     elif sms_local_boolean:
#     # elif sms_local_boolean and not sms_std_boolean and not data_boolean and not roaming_boolean:
#         sms_local_same_network_index = re.search(r'(to airtel mobile)', line)
#         if sms_local_same_network_index:
#             sms_local_same_network_boolean = True
#         sms_local_other_network_index = re.search(r'(to other mobiles)', line)
#         if sms_local_other_network_index:
#             sms_local_other_network_boolean = True
#
#         if sms_local_same_network_boolean:
#             assign_values(line, bill_number, key='sms_local_same_network', type=1)
#         elif sms_local_other_network_boolean:
#             assign_values(line, bill_number, key='sms_local_other_network', type=2)
#
#     elif sms_std_boolean:
#     # elif sms_std_boolean and not data_boolean and not roaming_boolean:
#         sms_std_same_network_index = re.search(r'(to airtel mobile)', line)
#         if sms_std_same_network_index:
#             sms_std_same_network_boolean = True
#         sms_std_other_network_index = re.search(r'(to other mobiles)', line)
#         if sms_std_other_network_index:
#             sms_std_other_network_boolean = True
#
#         if sms_std_same_network_boolean:
#             assign_values(line, bill_number, key='sms_std_same_network', type=4)
#         elif sms_std_other_network_boolean:
#             assign_values(line, bill_number, key='sms_std_other_network', type=5)
#
#     elif data_boolean:
#     # elif data_boolean and not roaming_boolean:
#         data_2g_index = re.search(r'(mobile internet 2g)', line)
#         if data_2g_index:
#             data_2g_boolean = True
#         data_3g_index = re.search(r'(mobile internet 3g)', line)
#         if data_3g_index:
#             data_3g_boolean = True
#         data_4g_index = re.search(r'(mobile internet 4g)', line)
#         if data_4g_index:
#             data_4g_boolean = True
#
#         if data_2g_boolean:
#             assign_values(line, bill_number, key='data_2g', type=1)
#         elif data_3g_boolean:
#             assign_values(line, bill_number, key='data_2g', type=2)
#         elif data_4g_boolean:
#             assign_values(line, bill_number, key='data_4g', type=3)
#
#     elif roaming_boolean:
#         roaming_incoming_calls_index = re.search(r'(incoming calls - voice)', line)
#         if roaming_incoming_calls_index:
#             roaming_incoming_calls_boolean = True
#         roaming_outgoing_calls_index = re.search(r'(outgoing calls - voice)', line)
#         if roaming_outgoing_calls_index:
#             roaming_outgoing_calls_boolean = True
#         roaming_sms_index = re.search(r'(sms)', line)
#         if roaming_sms_index:
#             roaming_sms_boolean = True
#
#         if roaming_incoming_calls_boolean:
#             assign_values(line, bill_number, key='roaming_incoming_call', type=1)
#         elif roaming_outgoing_calls_boolean:
#             assign_values(line, bill_number, key='roaming_outgoing_call', type=2)
#         elif roaming_sms_boolean:
#             assign_values(line, bill_number, key='roaming_incoming_sms', type=3)
#
# print USAGE_DETAILS_LOG
#
#
#         # Create bill object
#         # Get_or_create subscriber object
#         # Get_or_create plan object
#         # Create all usage objects
#
#
# # Mon afternoon
#
# import slate
# import re
#
# __author__ = 'roxnairani'
#
# with open('Unencrypted_MobileBill_1039029248_378881141_9980996446.pdf') as f:
# # with open('Unencrypted_MobileBill_1039029248_349197277_9980996446.pdf') as f:
#     report = slate.PDF(f)
#
#     # Split  string at multiple white spaces, rejoin into a list w/ single space; each page an element in the list
#     report_pages = []
#     for index, page in enumerate(report):
#         report_pages.append(' '.join(report[index].split()))
#
#     """
#     PAGE 1 -- BASIC INFORMATION
#     """
#
#     ##### SUBSCRIBER MODEL DETAILS
#     name_match = re.search(r'121\'M\w+\s+\w+\s+\w+', report_pages[0], re.MULTILINE)
#     name = name_match.group()[4:]
#
#     relationship_num_match = re.search(r'number\d+amount', report_pages[0], re.MULTILINE)
#     relationship_num = relationship_num_match.group()[6:16]
#
#     phone_number_match = re.search(r'airtel number\d+', report_pages[0], re.MULTILINE)
#     phone_number = phone_number_match.group()[13:]
#     # phone_number_match = re.search(r'no.\d+airtel', report_pg_0, re.MULTILINE)
#     # phone_number = phone_number_match.group()[3:13]
#
#     address_regex = re.compile('or=\+\-[\w\s]+{}'.format(relationship_num))
#     address_match = re.search(r'or=\+\-[\w\s]+', report_pages[0], re.MULTILINE)
#     address = address_match.group()[5:len(address_match.group())-21]
#
#     city_zip_state_match = re.search(r'oe\w+amount', report_pages[0], re.MULTILINE)
#     city = city_zip_state_match.group()[5:len(city_zip_state_match.group())-12]
#     zip = city_zip_state_match.group()[-12:-6]
#     state = city_zip_state_match.group()[2:5]
#
#     credit_limit_match = re.search(r'[\d,\d.]+credit', report_pages[0], re.MULTILINE)
#     credit_limit = credit_limit_match.group()[:len(credit_limit_match.group())-6]
#
#     security_deposit_match = re.search(r'[\d,\d.]+security', report_pages[0], re.MULTILINE)
#     security_deposit = security_deposit_match.group()[:len(security_deposit_match.group())-8]
#
#
#     ##### BILL MODEL DETAILS
#     bill_number_match = re.search(r'bill number\d+', report_pages[0], re.MULTILINE)
#     bill_number = bill_number_match.group()[11:]
#
#     start_date_match = re.search(r'\d{2}\-\w{3}\-\d{4}to\d+', report_pages[0], re.MULTILINE)
#     start_date = start_date_match.group()[:11]
#
#     end_date_match = re.search(r'charges\d+\-\w+\-\d+airtel', report_pages[0], re.MULTILINE)
#     end_date = end_date_match.group()[7:18]
#
#     bill_date_match = re.search(r'(\d{2}\-\w{3}\-\d{4}\d+\.)', report_pages[0], re.MULTILINE)
#     bill_date = bill_date_match.group()[:11]
#
#     due_date_match = re.search(r'(\d{2}\-\w+\-\d+beforebill number)', report_pages[0], re.MULTILINE)
#     due_date = due_date_match.group()[:11]
#
#     total_bill_match = re.search(r'month\'s charges\s+`[\d,\d.]+', report_pages[0], re.MULTILINE)
#     total_bill = total_bill_match.group()[17:]
#
#     onetime_charge_match = re.search(r'one time charges\s+[\d,\d.]+', report_pages[0], re.MULTILINE)
#     onetime_charge = onetime_charge_match.group()[17:]
#
#     monthly_charge_match = re.search(r'monthly charges\s+[\d,\d.]+', report_pages[0], re.MULTILINE)
#     monthly_charge = monthly_charge_match.group()[16:]
#
#     call_charge_match = re.search(r'call charges\s+[\d,\d.]+', report_pages[0], re.MULTILINE)
#     call_charge = call_charge_match.group()[13:]
#
#     booster_charge_match = re.search(r'boosters\s+[\d,\d.]+', report_pages[0], re.MULTILINE)
#     booster_charge = booster_charge_match.group()[9:]
#
#     data_charge_match = re.search(r'(mobile internet usage\s+[\d,\d.]+)', report_pages[0], re.MULTILINE)
#     data_charge = data_charge_match.group()[22:]
#
#     roaming_charge_match = re.search(r'(roaming\s+[\d,\d.]+)', report_pages[0], re.MULTILINE)
#     roaming_charge = roaming_charge_match.group()[8:]
#
#     discount_match = re.search(r'(discounts\s+-[\d,\d.]+)', report_pages[0], re.MULTILINE)
#     discount = discount_match.group()[10:]
#
#     late_fee_match = re.search(r'(late fee\s+[\d,\d.]+)', report_pages[0], re.MULTILINE)
#     late_fee = late_fee_match.group()[9:]
#
#     tax_match = re.search(r'(taxes\s+[\d,\d.]+)', report_pages[0], re.MULTILINE)
#     tax = tax_match.group()[6:]
#
#     # print relationship_num, name, phone_number, address, city, zip, state, credit_limit, security_deposit, \
#     #     bill_number, start_date, end_date, bill_date, due_date, total_bill, onetime_charge, monthly_charge, \
#     #     call_charge, booster_charge, data_charge, roaming_charge, discount, late_fee, tax
#
#     """
#     PAGE 4+ -- CALL/SMS/DATA/ROAMING DETAILS INFORMATION
#     """
#
#     def assign_values(line_to_search, bill_number, key, type):
#         date = ""
#         time = ""
#         recipient_number = 0
#         duration = ""
#         volume = 0
#         cost = 0
#         volume_check = False
#
#         # Cleaning up front of string to avoid complications with rest of regex parsing
#         fuzz_check = re.search(r'([\d\s\w\*]+\d{2}\-\w{3}\-\d{4})', line_to_search)
#         if fuzz_check:
#             fuzz = fuzz_check.group()[:-11]
#             line_to_search = line_to_search.replace(fuzz, "")
#
#             # If no 'fuzz', don't need to go through the rest of this
#             date_check = re.search(r'(\d{2}\-\w{3}\-\d{4})', line_to_search)
#             if date_check:
#                 date = date_check.group()
#                 line_to_search = line_to_search.replace(date, "")
#
#             time_check = re.search(r'(\d{2}\:\d{2}\:\d{2})', line_to_search)
#             if time_check:
#                 time = time_check.group()
#                 line_to_search = line_to_search.replace(time, "")
#
#             duration_check = re.search(r'(\d{2}\:\d{2})', line_to_search)
#             if duration_check:
#                 duration = duration_check.group()
#                 line_to_search = line_to_search.replace(duration, "")
#
#             # Recipient number is 11 digits to a landline, 403airtelgprs$com for data and 10 digits to a cellphone
#             if calls_local_fixed_landline_boolean or calls_std_fixed_landline_boolean:
#                 recipient_number_check = re.search(r'(\d{11})', line_to_search)
#             elif data_2g_boolean or data_3g_boolean or data_4g_boolean:
#                 recipient_number_check = re.search(r'(\d{3}airtelgprs$com)', line_to_search)
#             else:
#                 recipient_number_check = re.search(r'(\d{10})', line_to_search)
#             if recipient_number_check:
#                 recipient_number = recipient_number_check.group()
#                 line_to_search = line_to_search.replace(recipient_number, "")
#
#             cost_vol_check = re.search(r'(\d+)', line_to_search)
#             if cost_vol_check:
#                 if duration_check:
#                     cost = cost_vol_check.group()  # Need to refine to get paise from next line
#                 else:
#                     volume = cost_vol_check.group()[0]
#                     volume_check = True
#                     cost = cost_vol_check.group()[1:]
#
#             if date == "" or time == "" or recipient_number == 0:
#                 pass
#             elif duration_check:
#                 USAGE_DETAILS_LOG[key].append({
#                     'date': date,
#                     'time': time,
#                     'recipient_number': recipient_number,
#                     'duration': duration,
#                     'cost': cost,
#                     'bill': bill_number,
#                     'type': type
#                 })
#             elif volume_check:
#                 USAGE_DETAILS_LOG[key].append({
#                     'date': date,
#                     'time': time,
#                     'recipient_number': recipient_number,
#                     'volume': volume,
#                     'cost': cost,
#                     'bill': bill_number,
#                     'type': type
#                 })
#
#         else:
#             pass
#
#             # Create bill object
#             # Get_or_create subscriber object
#             # Get_or_create plan object
#             # Create all usage objects
#
#     USAGE_DETAILS_LOG = {
#         'call_local_same_network': [],
#         'call_local_other_network': [],
#         'call_local_fixed_landline': [],
#         'call_std_same_network': [],
#         'call_std_other_network': [],
#         'call_std_fixed_landline': [],
#         'call_intl': [],
#         'sms_local_same_network': [],
#         'sms_local_other_network': [],
#         'sms_std_same_network': [],
#         'sms_std_other_network': [],
#         'sms_intl': [],
#         'data_2g': [],
#         'data_3g': [],
#         'data_4g': [],
#         'roaming_incoming_call': [],
#         'roaming_outgoing_call': [],
#         'roaming_incoming_sms': [],
#         'roaming_outgoing_sms': [],
#     }
#
#     # Pre-defined variables
#     calls_local_boolean = False
#     calls_std_boolean = False
#     calls_intl_boolean = False
#     sms_local_boolean = False
#     sms_std_boolean = False
#     sms_intl_boolean = False
#     data_boolean = False
#     roaming_boolean = False
#
#
#     # Booleans for sub-categories
#     SUB_CATEGORY_BOOLEANS = {
#         'calls_local_same_network_boolean': False,
#         'calls_local_other_network_boolean': False,
#         'calls_local_fixed_landline_boolean': False,
#         'calls_std_same_network_boolean': False,
#         'calls_std_other_network_boolean': False,
#         'calls_std_fixed_landline_boolean': False,
#
#         'sms_local_same_network_boolean': False,
#         'sms_local_other_network_boolean': False,
#         'sms_std_same_network_boolean': False,
#         'sms_std_other_network_boolean': False,
#
#         'data_2g_boolean': False,
#         'data_3g_boolean': False,
#         'data_4g_boolean': False,
#
#         'roaming_incoming_calls_boolean': False,
#         'roaming_outgoing_calls_boolean': False,
#         'roaming_sms_boolean': False,
#     }
#
#     def turn_off_sub_category_booleans():
#         for key, value in SUB_CATEGORY_BOOLEANS.iteritems():
#             SUB_CATEGORY_BOOLEANS[key] = False
#
#     # calls_local_same_network_boolean = False
#     # calls_local_other_network_boolean = False
#     # calls_local_fixed_landline_boolean = False
#     # calls_std_same_network_boolean = False
#     # calls_std_other_network_boolean = False
#     # calls_std_fixed_landline_boolean = False
#     #
#     # sms_local_same_network_boolean = False
#     # sms_local_other_network_boolean = False
#     # sms_std_same_network_boolean = False
#     # sms_std_other_network_boolean = False
#     #
#     # data_2g_boolean = False
#     # data_3g_boolean = False
#     # data_4g_boolean = False
#     #
#     # roaming_incoming_calls_boolean = False
#     # roaming_outgoing_calls_boolean = False
#     # roaming_sms_boolean = False
#
#     # PARSING ITEMIZED CALL INFORMATION, STARTS AT PAGE 3
#     for page in report_pages[3:]:
#
#         # To avoid issue with splitting at '.' below
#         page.replace('airtelgprs.com', 'airtelgprs$com')
#
#         for line in page.split("."):
#             calls_local_object = re.search(r'(voice calls - outgoing local)', line)
#             if calls_local_object:
#                 turn_off_sub_category_booleans()
#                 calls_local_boolean = True
#             calls_std_object = re.search(r'(voice calls - outgoing std)', line)
#             if calls_std_object:
#                 turn_off_sub_category_booleans()
#                 calls_std_boolean = True
#             sms_local_object = re.search(r'(sms - local)', line)
#             if sms_local_object:
#                 turn_off_sub_category_booleans()
#                 sms_local_boolean = True
#             sms_std_object = re.search(r'(sms - national)', line)
#             if sms_std_object:
#                 turn_off_sub_category_booleans()
#                 sms_std_boolean = True
#             data_object = re.search(r'(mobile internet - volume)', line)
#             if data_object:
#                 turn_off_sub_category_booleans()
#                 data_boolean = True
#             roaming_object = re.search(r'(national roaming)', line)
#             if roaming_object:
#                 turn_off_sub_category_booleans()
#                 roaming_boolean = True
#
#             # Turn on and off booleans based on if the container has been found
#             if calls_local_boolean:
#                 calls_local_same_network = re.search(r'(to airtel mobile)', line)
#                 if calls_local_same_network:
#                     turn_off_sub_category_booleans()
#                     calls_local_same_network_boolean = True
#                 calls_local_other_network = re.search(r'(to other mobiles)', line)
#                 if calls_local_other_network:
#                     turn_off_sub_category_booleans()
#                     calls_local_other_network_boolean = True
#                 calls_local_fixed_landline = re.search(r'(to fixed landline)', line)
#                 if calls_local_fixed_landline:
#                     turn_off_sub_category_booleans()
#                     calls_local_fixed_landline_boolean = True
#
#                 if calls_local_same_network_boolean:
#                     assign_values(line, bill_number, key='call_local_same_network', type=1)
#                 elif calls_local_other_network_boolean:
#                     assign_values(line, bill_number, key='call_local_other_network', type=2)
#                 elif calls_local_fixed_landline_boolean:
#                     assign_values(line, bill_number, key='call_local_fixed_landline', type=3)
#
#             elif calls_std_boolean:
#                 calls_std_same_network = re.search(r'(to airtel mobile)', line)
#                 if calls_std_same_network:
#                     turn_off_sub_category_booleans()
#                     calls_std_same_network_boolean = True
#                 calls_std_other_network = re.search(r'(to other mobiles)', line)
#                 if calls_std_other_network:
#                     turn_off_sub_category_booleans()
#                     calls_std_other_network_boolean = True
#                 calls_std_fixed_landline = re.search(r'(to fixed landline)', line)
#                 if calls_std_fixed_landline:
#                     turn_off_sub_category_booleans()
#                     calls_std_fixed_landline_boolean = True
#
#                 if calls_std_same_network_boolean:
#                     assign_values(line, bill_number, key='call_std_same_network', type=4)
#                 elif calls_std_other_network_boolean:
#                     assign_values(line, bill_number, key='call_std_other_network', type=5)
#                 elif calls_std_fixed_landline_boolean:
#                     assign_values(line, bill_number, key='call_std_fixed_landline', type=6)
#
#             elif sms_local_boolean:
#                 sms_local_same_network = re.search(r'(to airtel mobile)', line)
#                 if sms_local_same_network:
#                     calls_std_fixed_landline_boolean = False
#                     sms_local_same_network_boolean = True
#                 sms_local_other_network = re.search(r'(to other mobiles)', line)
#                 if sms_local_other_network:
#                     sms_local_same_network_boolean = False
#                     sms_local_other_network_boolean = True
#
#                 if sms_local_same_network_boolean:
#                     assign_values(line, bill_number, key='sms_local_same_network', type=1)
#                 elif sms_local_other_network_boolean:
#                     assign_values(line, bill_number, key='sms_local_other_network', type=2)
#
#             elif sms_std_boolean:
#                 sms_std_same_network = re.search(r'(to airtel mobile)', line)
#                 if sms_std_same_network:
#                     sms_local_other_network_boolean = False
#                     sms_std_same_network_boolean = True
#                 sms_std_other_network = re.search(r'(to other mobiles)', line)
#                 if sms_std_other_network:
#                     sms_std_same_network_boolean = False
#                     sms_std_other_network_boolean = True
#
#                 if sms_std_same_network_boolean:
#                     assign_values(line, bill_number, key='sms_std_same_network', type=4)
#                 elif sms_std_other_network_boolean:
#                     assign_values(line, bill_number, key='sms_std_other_network', type=5)
#
#             elif data_boolean:
#                 data_2g = re.search(r'(mobile internet 2g)', line)
#                 if data_2g:
#                     sms_std_other_network_boolean = False
#                     data_2g_boolean = True
#                 data_3g = re.search(r'(mobile internet 3g)', line)
#                 if data_3g:
#                     data_2g_boolean = False
#                     data_3g_boolean = True
#                 data_4g = re.search(r'(mobile internet 4g)', line)
#                 if data_4g:
#                     data_3g_boolean = False
#                     data_4g_boolean = True
#
#                 if data_2g_boolean:
#                     assign_values(line, bill_number, key='data_2g', type=1)
#                 elif data_3g_boolean:
#                     assign_values(line, bill_number, key='data_2g', type=2)
#                 elif data_4g_boolean:
#                     assign_values(line, bill_number, key='data_4g', type=3)
#
#             elif roaming_boolean:
#                 roaming_incoming_calls = re.search(r'(incoming calls - voice)', line)
#                 if roaming_incoming_calls:
#                     data_4g_boolean = False
#                     roaming_incoming_calls_boolean = True
#                 roaming_outgoing_calls = re.search(r'(outgoing calls - voice)', line)
#                 if roaming_outgoing_calls:
#                     roaming_incoming_calls_boolean = False
#                     roaming_outgoing_calls_boolean = True
#                 roaming_sms = re.search(r'(sms)', line)
#                 if roaming_sms:
#                     roaming_outgoing_calls_boolean = False
#                     roaming_sms_boolean = True
#
#                 if roaming_incoming_calls_boolean:
#                     assign_values(line, bill_number, key='roaming_incoming_call', type=1)
#                 elif roaming_outgoing_calls_boolean:
#                     assign_values(line, bill_number, key='roaming_outgoing_call', type=2)
#                 elif roaming_sms_boolean:
#                     assign_values(line, bill_number, key='roaming_incoming_sms', type=3)
#
#     print 'local calls same', USAGE_DETAILS_LOG['call_local_same_network'][110:112]
#     print 'local calls other', USAGE_DETAILS_LOG['call_local_other_network'][10:12]
#     print 'local calls fixed', USAGE_DETAILS_LOG['call_local_fixed_landline'][10:12]
#     print 'std calls same', USAGE_DETAILS_LOG['call_std_same_network'][10:12]
#     print 'std calls other', USAGE_DETAILS_LOG['call_std_other_network'][10:12]
#     print 'std calls fixed', USAGE_DETAILS_LOG['call_std_fixed_landline'][:2]
#     print 'calls intl', USAGE_DETAILS_LOG['call_intl']  # to refine
#     print 'local sms same', USAGE_DETAILS_LOG['sms_local_same_network'][10:12]
#     print 'local sms other', USAGE_DETAILS_LOG['sms_local_other_network'][5:7]
#     print 'std sms same', USAGE_DETAILS_LOG['sms_std_same_network'][10:12]
#     print 'std sms other', USAGE_DETAILS_LOG['sms_std_other_network'][10:12]
#     print 'sms intl', USAGE_DETAILS_LOG['sms_intl']  # to refine
#     print 'data 2g', USAGE_DETAILS_LOG['data_2g']
#     print 'data 3g', USAGE_DETAILS_LOG['data_3g'][10:12]
#     print 'data 4g', USAGE_DETAILS_LOG['data_2g']
#     print 'roaming incoming call', USAGE_DETAILS_LOG['roaming_incoming_call'][10:12]
#     print 'roaming outgoing call', USAGE_DETAILS_LOG['roaming_outgoing_call'][10:12]
#     print 'roaming incoming sms', USAGE_DETAILS_LOG['roaming_incoming_sms'][10:12]
#     print 'roaming outgoing sms', USAGE_DETAILS_LOG['roaming_outgoing_sms']




            # print relationship_num, name, phone_number, address, city, zip, state, credit_limit, security_deposit, \
            #     bill_number, start_date, end_date, bill_date, due_date, total_bill, onetime_charge, monthly_charge, \
            #     call_charge, booster_charge, data_charge, roaming_charge, discount, late_fee, tax

