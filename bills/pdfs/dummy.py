__author__ = 'roxnairani'

import slate
import re

__author__ = 'roxnairani'

# USING STRING SPLITS TO PARSE DATA

with open('Unencrypted_MobileBill_1039029248_378881141_9980996446.pdf') as f:
# with open('Unencrypted_MobileBill_1039029248_349197277_9980996446.pdf') as f:
    report = slate.PDF(f)

    # Split  string at multiple white spaces, rejoin into a list w/ single space & then split each word at that space
    report_pg_1 = ' '.join(report[0].split())
    report_pg_4 = ' '.join(report[3].split())
    print report_pg_4

    # Convert the string into a list split at spaces
    wordList_pg_0 = []
    for word in report_pg_1.split(" "):
        wordList_pg_0.append(word)

    for word in wordList_pg_0:
        print word

    # Declare some variables upfront so loops work
    relationship_num = 0
    address = ""
    address_index = 0

    # PARSING BASIC INFORMATION
    for index, word in enumerate(wordList_pg_0):

        # BILL model details (number, start_date, end_date, bill_date, due_date, total_bill, onetime_charge,
        # monthly_charge, call_charge, booster_charge, data_charge, roaming_charge, discount, late_fee, tax
        if word[0:3] == "no." and word[-6:] == "airtel":
            last_letter = len(word) - 9
            bill_number = word[3:][:last_letter]
            print bill_number
        # start date, bill date, due date
        elif word[0:7] == "charges" and word[-6:] == "airtel":
            last_letter = len(word) - len('airtel')
            end_date = word[7:last_letter]
            # Dates depends on r'ship_num so needs to be called after for loop to ensure a value for r'ship num exists
        elif word == 'charges':
            if wordList_pg_0[index-1] == "month\'s":
                bill_amount = wordList_pg_0[index+1]
                last_letter = len(bill_amount) - len('service')
                total_bill = bill_amount[1:last_letter]
                print total_bill
            elif wordList_pg_0[index-1] == "time":
                onetime_charge = wordList_pg_0[index+1]
                print onetime_charge
            elif wordList_pg_0[index-1] == "monthly":
                monthly_charge = wordList_pg_0[index+1]
                print monthly_charge
            elif wordList_pg_0[index-1] == "call":
                call_charge = wordList_pg_0[index+1]
                print call_charge
        elif word == 'boosters':
            booster_charge = wordList_pg_0[index+1]
        elif word == 'internet' and wordList_pg_0[index+1] == 'usage':
            data_charge = wordList_pg_0[index+2]
        elif word == 'roaming':
            roaming_charge = wordList_pg_0[index+1]
        elif word == 'discounts':
            discount = wordList_pg_0[index+1]
        elif word == 'late' and wordList_pg_0[index+1] == 'fee':
            late_fee = wordList_pg_0[index+2]
        elif word == 'taxes':
            last_letter = len(word) - len('this')
            taxes = wordList_pg_0[index+1][:last_letter]

        # SUBSCRIBER model details (name, address, city, zip, (state), relationship_num, credit_limit)
        elif '121\'M' in word:
            name = wordList_pg_0[index+1] + " " + wordList_pg_0 [index+2]
            print name, word, wordList_pg_0[index+1]
        elif 'or=+-' in word:
            count = 1
            address = word[5:]
            address_index = index
            # Address depends on r'ship_num so needs to be called after for loop to ensure a value for r'ship num exists
        elif word[0:2] == "oe" and word[-6:] == "amount":
            last_letter = len(word) - 12
            city = word[5:last_letter]
            zipcode = word[-12:-6]
            state = word[2:5]   # Not in the model
            print city, zip, state
        elif word[0:6] == "number" and word[-6:] == "amount" and not ' ' in word:  # Eliminates words like 'amount numberamount'
            relationship_num = word[6:][:10]
            print relationship_num, word  ##### works
        elif word[-6:] == "credit" and word[-9] == ".":  # Eliminates words like 'cash/cheque/credit'
            last_letter = len(word) - len('credit')
            credit_limit = word[:last_letter]
            print credit_limit, word
        elif word[-8:] == "security" and word[-11] == ".":  # Eliminates words like 'limitsecurity'
            last_letter = len(word) - len('security')
            security_deposit = word[:last_letter]  # Not in the model
            print security_deposit, word

    # To get the SUBSCRIBER address
    address_count = 1
    while address_count < 8 and relationship_num not in wordList_pg_0 :  # Est. address is less than 8 indices in the list
        address += wordList_pg_0 [address_index + address_count]
        address_count += 1
    print address


    relationship_num_match = re.search(r'number\d+amount', report_pg_0, re.MULTILINE)
    relationship_num = relationship_num_match[7:17]
    monthly_charge_match = re.search(r'monthly charges\s+\d+\.\d+', report_pg_0, re.MULTILINE)
    print monthly_charge_match.group()



# from BS4 import BeautifulSoup

    ##### PAGE 4+ -- CALL/SMS/DATA/ROAMING DETAILS INFORMATION

    # Convert the string into a list split at spaces
    report_pg_4_list = []
    for word in report_pg_4.split("."):
        report_pg_4_list.append(word)

    # PARSING BASIC INFORMATION
    for index, word in enumerate(report_pg_4_list):
        # Find index of 'voice calls - outgoing local'
        if word[:28] == 'voice calls - outgoing local':
            if word[index+1][:18] == '1 to airtel mobile':
                calls_local_same_network_index = index + 1
            elif word[index+1][:18] == '2 to other mobiles':
                calls_local_other_network_index = index + 1
            elif word[index+1][:20] == '3 to fixed landline':
                calls_local_fixed_landline_index = index + 1
        if word[:26] == 'voice calls - outgoing std':
            if word[index+1][:18] == '1 to airtel mobile':
                calls_std_same_network_index = index + 1
            elif word[index+1][:18] == '2 to other mobiles':
                calls_std_other_network_index = index + 1
            elif word[index+1][:20] == '3 to fixed landline':
                calls_std_fixed_landline_index = index + 1
        if word[:11] == 'sms - local':
            if word[index+1][:18] == '1 to airtel mobile':
                sms_local_same_network_index = index + 1
            elif word[index+1][:18] == '2 to other mobiles':
                sms_local_other_network_index = index + 1
        if word[:24] == 'mobile internet - volume':
            if word[index+1][:20] == '1 mobile internet 3g':
                data_3g_index = index + 1
            elif word[index+1][:20] == '1 mobile internet 2g':
                data_2g_index = index + 1

        if word[:16] == 'national roaming':
            if word[index+1][:22] == 'incoming calls - voice':
                roaming_calls_incoming_index = index + 1
            elif word[index+1][:22] == 'outgoing calls - voice':
                roaming_calls_outgoing_index = index + 1
            elif word[index+1][:3] == 'sms':
                roaming_sms_index = index + 1



   # # PARSING BASIC INFORMATION
   #  for line in report_pg_4.split("."):
   #      calls_local_index = re.search(r'(voice calls outgoing - outgoing local)', line)
   #
   #      # If calls_std_index etc not defined, details belongs to voice calls - outgoing local (similar logic contd.)
   #      if calls_local_index and not calls_std_index and not sms_local_index and not sms_std_index and not data_index and not roaming_index:
   #          # If calls_std_index etc are not defined yet, the details belongs to voice calls - outgoing local
   #          same_network_index = re.search(r'(1 to airtel mobile)', line)
   #          other_network_index = re.search(r'(2 to other mobiles)', line)
   #          fixed_landline_index = re.search(r'(3 to fixed landline)', line)
   #
   #          date_check = re.search(r'(\d{2}\-\w{3}\-\d{4})', line)
   #          if date_check:
   #              date = date_check.group()
   #              line = line.replace(date, "")
   #
   #          time_check = re.search(r'(\d{2}\:\d{2}\:\d{2})', line)
   #          if time_check:
   #              time = time_check.group()
   #              line = line.replace(time, "")
   #
   #          duration_check = re.search(r'(\d{2}\:\d{2})', line)
   #          if duration_check:
   #              duration = duration_check.group()
   #              line = line.replace(duration, "")
   #
   #          recipient_number = re.search(r'(\d+)', line).group()[1:12]
   #          cost = re.search(r'(\d+)', line).group()[-1]
   #          line = line.replace(recipient_number, "")
   #
   #          volume_check = re.search(r'(\d)', line)
   #          if volume_check:
   #              volume = volume_check.group()
   #              line = line.replace(volume, "")
   #
   #          if duration_check and volume_check:
   #              print "ERROR - CAN'T HAVE BOTH DURATION AND VOLUME"
   #
   #          if calls_local_same_network_index and not calls_local_other_network_index and not calls_local_fixed_landline_index:
   #              key = 'call_local_same_network'
   #              type = 1
   #          elif calls_local_other_network_index and not calls_local_fixed_landline_index:
   #              key = 'call_local_other_network'
   #              type = 2
   #          else:
   #              key = 'call_local_fixed_landline'
   #              type = 3
   #
   #          if duration:
   #              USAGE_DETAILS_LOG[key].push({
   #                  'date': date,
   #                  'time': time,
   #                  'recipient_number': recipient_number,
   #                  'duration': duration,
   #                  'cost': cost,
   #                  'bill': bill_number,
   #                  'type': type
   #              })
   #          elif volume:
   #              USAGE_DETAILS_LOG[key].push({
   #                  'date': date,
   #                  'time': time,
   #                  'recipient_number': recipient_number,
   #                  'volume': volume,
   #                  'cost': cost,
   #                  'bill': bill_number,
   #                  'type': type
   #              })



























