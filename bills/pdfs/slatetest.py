import slate
import re

__author__ = 'roxnairani'

# with open('Unencrypted_MobileBill_1039029248_378881141_9980996446.pdf') as f:
with open('Unencrypted_MobileBill_1039029248_349197277_9980996446.pdf') as f:
    report = slate.PDF(f)

    # Split  string at multiple white spaces, rejoin into a list w/ single space & then split each word at that space
    report_pg_1 = ' '.join(report[0].split())
    report_pg_itemized_data = ' '.join(report[1].split())

    ##### PAGE 1 -- BASIC INFORMATION

    # R'ship number set up first for use in other regex
    relationship_num_match = re.search(r'number\d+amount', report_pg_1, re.MULTILINE)
    relationship_num = relationship_num_match.group()[6:16]


    ##### SUBSCRIBER MODEL DETAILS
    name_match = re.search(r'121\'M\w+\s+\w+\s+\w+', report_pg_1, re.MULTILINE)
    name = name_match.group()[7:]

    phone_number_match = re.search(r'airtel number\d+', report_pg_1, re.MULTILINE)
    phone_number = phone_number_match.group()[13:]
    # phone_number_match = re.search(r'no.\d+airtel', report_pg_0, re.MULTILINE)
    # phone_number = phone_number_match.group()[3:13]

# Make address regex end with relationship number ------ TO DOOOOOOOO
#     address_regex = r'or=\+\-\w+' + re.escape(relationship_num)
#     address_match = re.search(address_regex, report_pg_0, re.MULTILINE)
#     address = address_match.group()

    city_zip_state_match = re.search(r'oe\w+amount', report_pg_1, re.MULTILINE)
    city = city_zip_state_match.group()[5:len(city_zip_state_match.group())-12]
    zip = city_zip_state_match.group()[-12:-6]
    state = city_zip_state_match.group()[2:5]

    credit_limit_match = re.search(r'[\d,\d.]+credit', report_pg_1, re.MULTILINE)
    credit_limit = credit_limit_match.group()[:len(credit_limit_match.group())-6]

    security_deposit_match = re.search(r'[\d,\d.]+security', report_pg_1, re.MULTILINE)
    security_deposit = security_deposit_match.group()[:len(security_deposit_match.group())-8]


    ##### BILL MODEL DETAILS
    bill_number_match = re.search(r'bill number\d+', report_pg_1, re.MULTILINE)
    bill_number = bill_number_match.group()[11:]

# start date

    end_date_match = re.search(r'charges\d+\-\w+\-\d+airtel', report_pg_1, re.MULTILINE)
    end_date = end_date_match.group()[7:18]

# bill date,
    due_date_match = re.search(r'(\d{2}\-\w+\-\d+beforebill number)', report_pg_1, re.MULTILINE)
    due_date = due_date_match.group()[:11]

    total_bill_match = re.search(r'month\'s charges\s+`[\d,\d.]+', report_pg_1, re.MULTILINE)
    total_bill = total_bill_match.group()[17:]

    onetime_charge_match = re.search(r'one time charges\s+[\d,\d.]+', report_pg_1, re.MULTILINE)
    onetime_charge = onetime_charge_match.group()[17:]

    monthly_charge_match = re.search(r'monthly charges\s+[\d,\d.]+', report_pg_1, re.MULTILINE)
    monthly_charge = monthly_charge_match.group()[16:]

    call_charge_match = re.search(r'call charges\s+[\d,\d.]+', report_pg_1, re.MULTILINE)
    call_charge = call_charge_match.group()[13:]

    booster_charge_match = re.search(r'boosters\s+[\d,\d.]+', report_pg_1, re.MULTILINE)
    booster_charge = booster_charge_match.group()[9:]

    data_charge_match = re.search(r'(mobile internet usage\s+[\d,\d.]+)', report_pg_1, re.MULTILINE)
    data_charge = data_charge_match.group()[22:]

    roaming_charge_match = re.search(r'(roaming\s+[\d,\d.]+)', report_pg_1, re.MULTILINE)
    roaming_charge = roaming_charge_match.group()[8:]

    discount_match = re.search(r'(discounts\s+-[\d,\d.]+)', report_pg_1, re.MULTILINE)
    discount = discount_match.group()[10:]

    late_fee_match = re.search(r'(late fee\s+[\d,\d.]+)', report_pg_1, re.MULTILINE)
    late_fee = late_fee_match.group()[9:]

    tax_match = re.search(r'(taxes\s+[\d,\d.]+)', report_pg_1, re.MULTILINE)
    tax = tax_match.group()[6:]

    # print relationship_num, name, phone_number, city, zip, state, credit_limit, security_deposit, \
    #     bill_number, end_date, due_date, total_bill, onetime_charge, monthly_charge, call_charge, booster_charge, \
    #     data_charge, roaming_charge, discount, late_fee, tax

