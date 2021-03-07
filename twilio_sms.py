def twilio_send_sms(code, phone):
    import requests
    from requests.auth import HTTPBasicAuth

    sid = 'ACd8e113fdda12f39251ad8f69d6affce7'
    token = '961c2c37eb841e74c5d13d71ea471a00'
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