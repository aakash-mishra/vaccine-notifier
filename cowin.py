import requests
from email_service import send_email
import datetime


punelist='aakash21696@gmail.com'
kondapurlist=''
BASE_URI = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin'
MESSAGE_TEMPLATE = 'Vaccine slot available on {date} at pincode {pincode}({address}) for age limit {age_limit}+\n'
pincode_dict = {'411057': {'18+only':False, 'subscribers':punelist},
                    '411033': {'18+only':False, 'subscribers':punelist},
                    '411045': {'18+only':False, 'subscribers':punelist},
                    '411067': {'18+only':False, 'subscribers':punelist},
                    '500048': {'18+only':True, 'subscribers':kondapurlist}}

def getTodaysDate():
    datetokens = str(datetime.date.today()).split('-')
    return datetokens[2] + '-' + datetokens[1] + '-' + datetokens[0]

def getTomorrowsDate():
    datetokens = str(datetime.date.today() + datetime.timedelta(days=1)).split('-')
    return datetokens[2] + '-' + datetokens[1] + '-' + datetokens[0]

def main():
    today = getTodaysDate()
    tomorrow = getTomorrowsDate()
    headers={"Accept":"application/json",
    "Accept-Language":"en_US",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    req_params = {}

    for pincode in pincode_dict:
        req_params['pincode'] = pincode
        req_params['date'] = today
        data_today = requests.get(url = BASE_URI, params = req_params, headers = headers).json()
        req_params['date'] = tomorrow
        data_tomorrow = requests.get(url = BASE_URI, params = req_params, headers = headers).json()
        #if equal to 0 then no slots available
        if len(data_today['sessions']) > 0 or len(data_tomorrow['sessions']) > 0 :
            message = ''
            #need to send email only for 18+ category
            if pincode_dict[pincode]['18+only']:
                for center in data_today['sessions']:
                    if center['min_age_limit'] == '18':
                        message += MESSAGE_TEMPLATE.format(date=today, pincode=pincode, address= center['address'], age_limit=center['min_age_limit'])
                for center in data_tomorrow['sessions']:
                    if center['min_age_limit'] == '18':
                        message += MESSAGE_TEMPLATE.format(date=tomorrow, pincode=pincode, address= center['address'], age_limit=center['min_age_limit'])
                
            else:
                for center in data_today['sessions']:
                    message += MESSAGE_TEMPLATE.format(date=today, pincode=pincode, address= center['address'], age_limit=center['min_age_limit'])
                for center in data_tomorrow['sessions']:
                    message += MESSAGE_TEMPLATE.format(date=tomorrow, pincode=pincode, address= center['address'], age_limit=center['min_age_limit'])

            if message:
                send_email(message, pincode_dict[pincode]['subscribers'])

if __name__ == "__main__":
    main()