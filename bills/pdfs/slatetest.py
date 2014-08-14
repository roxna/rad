import slate
import re

__author__ = 'roxnairani'

with open('Unencrypted_MobileBill_1039029248_378881141_9980996446.pdf') as f:
# with open('Unencrypted_MobileBill_1039029248_349197277_9980996446.pdf') as f:
    report = slate.PDF(f)

    strList = []
    strlist_with_charges = []
    credit_limit = 0
    security_deposit = 0

    # Split  string at multiple white spaces, rejoin into a list w/ single space & then split each word at that space
    report_pg_0 = ' '.join(report[0].split())
    for word in report_pg_0.split(" "):
        strList.append(word)

    for word in strList:
        print word

    # Declare some variables upfront so loops work
    relationship_num = ""
    address = ""
    address_index = 0

    # Parsing basic information
    for index, word in enumerate(strList):
        # if word == 'charges':
        #     strlist_with_charges.append(strList[index+1])

        # BILL model details (number, start_date, end_date, bill_date, due_date, total_bill, onetime_charge,
        # monthly_charge, call_charge, booster_charge, data_charge, roaming_charge, discount, late_fee, tax
        if word[0:3] == "no." and word[-6:] == "airtel":
            last_letter = len(word) - 9
            bill_number = word[3:][:last_letter]
            print bill_number

        # SUBSCRIBER model details (name, address, city, zip, relationship_num, credit_limit)
        elif '121\'M' in word:
            name = strList[index+1] + " " + strList[index+2]
            print name, word, strList[index+1]
        elif 'or=+-' in word:
            count = 1
            address = word[5:]
            address_index = index
            # Address depends on r'ship_num so needs to be called after for loop to ensure a value for r'ship num exists
        elif word[0:2] == "oe" and word[-6:] == "amount":
            city = 0
            zip = 
            state = word[2:5]   # Not in the model
        elif word[0:6] == "number" and word[-6:] == "amount" and not ' ' in word:  # Eliminates words like 'amount numberamount'
            relationship_num = word[6:][:10]
            print relationship_num, word  ##### works
        elif word[-6:] == "credit" and word[-9] == ".":  # Eliminates words like 'cash/cheque/credit'
            last_letter = len(word) - 6
            credit_limit = word[:last_letter]
            print credit_limit, word  ##### works
        elif word[-8:] == "security" and word[-11] == ".":  # Eliminates words like 'limitsecurity'
            last_letter = len(word) - 8
            security_deposit = word[:last_letter]  # Not in the model
            print security_deposit, word  ##### works

    # To get the address
    address_count = 1
    while address_count < 8 and relationship_num not in strList:  # Est. address is less than 8 indices in the list
        address += strList[address_index + address_count]
        address_count += 1
    print address


    # Find monthly charges
    match = re.search(r'^monthly charges\d+', report[0], re.VERBOSE)
    # print match.group()



# from BS4 import BeautifulSoup