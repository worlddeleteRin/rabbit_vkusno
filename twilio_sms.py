def twilio_send_sms(code, phone):
    import requests
    from requests.auth import HTTPBasicAuth
    from secure.api_credentials import TWILIO_SID, TWILIO_TOKEN

    sid = TWILIO_SID
    token = TWILIO_TOKEN 
    main_url = 'https://api.twilio.com/2010-04-01/'
    method = '/Accounts/{}/Messages.json'.format(sid)
    url = main_url + method
    data = {
        'Body': 'ваш код для входа - {}'.format(code),
        'From': '+17743714137',
        'To': '+' + phone,
    }
    r = requests.post(url, data = data, auth = HTTPBasicAuth(sid, token))
    return r.json()