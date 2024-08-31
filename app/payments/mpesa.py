import base64
import json
import os
from datetime import datetime, timedelta

import requests
from fastapi import HTTPException

ACCESS_TOKEN_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
STK_PUSH_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
STK_QUERY_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'


MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
MPESA_PASS_KEY = os.getenv('MPESA_PASS_KEY')
MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE')
CALLBACK_URL = os.getenv('CALLBACK_URL')


class Mpesa:
    def __init__(self):
        self.consumer_key = MPESA_CONSUMER_KEY
        self.consumer_secret = MPESA_CONSUMER_SECRET
        self.mpesa_shortcode = MPESA_SHORTCODE
        self.mpesa_passkey = MPESA_PASS_KEY
        self.callback_url = CALLBACK_URL
        self.basic_token = None
        self.access_token = None
        self.access_token_expiry = None
        self.access_token_generated_at = None


    # ENCRYPTING THE ACCESS TOKEN
    def get_basic_token(self):
        if self.consumer_secret is None or self.consumer_key is None:
            raise Exception('No consumer_key and consumer_secret found')

        to_encode = f'{self.consumer_key}:{self.consumer_secret}'
        self.basic_token = base64.b64encode(to_encode.encode('utf-8')).decode('utf-8')

        return self.basic_token


    # GETTING ACCESS TOKEN FOR AUTHORIZING STK PUSH REQUEST
    def get_access_token(self):
        basic_token = self.basic_token or self.get_basic_token()
        print('------Generating access token------')
        response = requests.get(ACCESS_TOKEN_URL, headers={'Authorization': f'Basic {basic_token}'})
        print('Token Status Code:', response.status_code)

        if response.status_code != 200:
            print('-----Unable to generate access token-----')
            print('Status Code:', response.status_code)
            raise Exception('Unable to generate access token')
        else:
            token = response.json()
            self.access_token = token['access_token']
            self.access_token_expiry = token['expires_in']
            self.access_token_generated_at = datetime.now()
            return self.access_token


    # VALIDATING THE ACCESS TOKEN IS TRUE AND IS NOT EXPIRED
    def validate_access_token(self):
        if not self.access_token or not self.access_token_expiry:
            return False
        now = datetime.now()
        return self.access_token_generated_at + timedelta(seconds=(self.access_token_expiry - 10)) > now


    # GENERATING PASSWORD AND TIMESTAMP USED IN STK PAYLOAD
    def stk_password_timestamp(self):
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            to_encode = f'{self.mpesa_shortcode}{self.mpesa_passkey}{timestamp}'
            password = base64.b64encode(to_encode.encode('utf-8')).decode('utf-8')
            return password, timestamp


    # STK PUSH PAYLOAD
    def stk_push(self, phone = int, amount = int):
        password, timestamp = self.stk_password_timestamp()

        stk_payload = {
            "BusinessShortCode": self.mpesa_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "Amount": amount,
            "PartyA": phone,
            "PartyB": self.mpesa_shortcode,
            "PhoneNumber": phone,
            "CallBackURL": self.callback_url,
            "TransactionType": "CustomerPayBillOnline",
            "AccountReference": "Medix Solutions",
            "TransactionDesc": "Medix Solutions"
        }

        return stk_payload


    # SENDING STK PUSH TO USER
    def send_stk_push(self, payload):
        print('-----Sending STK Push Request-----')
        access_token = self.access_token if self.validate_access_token() else self.get_access_token()
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(STK_PUSH_URL, data=json.dumps(payload), headers=headers)
        print('Stk status code:', response.status_code)
        print('--------STK PUSH SENT---------')

        return response


    # CHECKING FOR MPESA PAYMENT STATUS WHEN CALLBACK URL IS NOT CALLED AFTER SENDING STK PUSH
    def check_payment_status_timestamp(self):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        to_encode = f'{self.mpesa_shortcode}{self.mpesa_passkey}{timestamp}'
        password = base64.b64encode(to_encode.encode('utf-8')).decode('utf-8')
        return password, timestamp

    # PAYMENT STATUS PAYLOAD
    def payment_status(self, checkout_request_id = str):
        password, timestamp = self.check_payment_status_timestamp()

        payload = {
            'BusinessShortCode': self.mpesa_shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'CheckoutRequestID': checkout_request_id
        }

        return payload

    # STK QUERY TO CHECK IF PAYMENT WAS COMPLETED OR NOT
    def check_payment_status(self, payload):
        print('------Checking payment status------')
        access_token = self.access_token if self.validate_access_token() else self.get_access_token()

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(STK_QUERY_URL, data=json.dumps(payload), headers=headers)
            result = response.json()
            print('Payment result code:', result.get('ResultCode'))
            print('--------Received payment status--------')
            return result
        except requests.RequestException as e:
            print(f"Request failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to check payment status")
