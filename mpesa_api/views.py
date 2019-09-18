import requests
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
# validated_mpesa_access_token = {}


def getAccessToken(request):
    # return HttpResponse("Hello, world")
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
    api_URL = settings.API_URL
    # api2 = 'https://sandbox.safaricom.co.ke/oauth/v1/generate'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)


def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_push_url = settings.API_PUSH_URL
    # headers = {"Authorization": "Bearer %s" % access_token}
    headers = {
        "Content-Type": 'application/json',
        'Authorization': "Bearer {}".format(access_token)
    }
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Ammount": 1,
        "PartyA": 254722867603,
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254722867603,
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Charles",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_push_url, json=request, headers=headers)
    return (response.text)


def lipa_na_paybill(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "http://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "Business_short_code": "",
        "ConfirmationURL": "http://ip_address:port/confirmation",
        "ValidationURL": "http://ip_address:port/validation_url"

    }

    response = requests.post(api_url, json = request, headers = headers)
    return (response.text)


def register_c2b_url():
    """
    Register the c2b_url
    :return:
    """
    url = settings.C2B_REGISTER_URL
    headers = {"Content-Type": 'application/json',
               'Authorization': 'Bearer {}'.format(AuthToken.objects.get_token('c2b'))}
    body = dict(
        ShortCode=settings.C2B_SHORT_CODE,
        ResponseType=settings.C2B_RESPONSE_TYPE,
        ConfirmationURL=settings.C2B_CONFIRMATION_URL,
        ValidationURL=settings.C2B_VALIDATE_URL
    )
    response = post(url=url, headers=headers, data=json.dumps(body))
    return response.json()


def process_online_checkout(msisdn, amount, account_reference, transaction_desc):
    """
    Handle the online checkout
    :param msisdn:
    :param amount:
    :param account_reference:
    :param transaction_desc:
    :return:
    """
    url = settings.C2B_ONLINE_CHECKOUT_URL
    headers = {"Content-Type": 'application/json',
               'Authorization': 'Bearer {}'.format(AuthToken.objects.get_token('c2b'))}
    timestamp = str(datetime.now())[:-7].replace('-', '').replace(' ', '').replace(':', '')
    password = base64.b64encode(bytes('{}{}{}'.format(settings.C2B_ONLINE_SHORT_CODE, settings.C2B_ONLINE_PASSKEY,
                                                      timestamp), 'utf-8')).decode('utf-8')
    body = dict(
        BusinessShortCode=settings.C2B_ONLINE_SHORT_CODE,
        Password=password,
        Timestamp=timestamp,
        TransactionType=settings.C2B_TRANSACTION_TYPE,
        Amount=str(amount),
        PartyA=str(msisdn),
        PartyB=settings.C2B_ONLINE_SHORT_CODE,
        PhoneNumber=str(msisdn),
        CallBackURL=settings.C2B_ONLINE_CHECKOUT_CALLBACK_URL,
        AccountReference=account_reference,
        TransactionDesc=transaction_desc
    )
    response = post(url=url, headers=headers, data=json.dumps(body))
    return response.json()