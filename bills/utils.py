import slate
__author__ = 'roxnairani'


def parse_data(filename, password):
    with open(filename) as f:
        report = slate.PDF(f, password)
        print report

    # with open('/users/roxnairani/Desktop/MobileBill_1039029248_349197277_9980996446.pdf') as file:
    #     report = slate.PDF(file, 'mjq4')