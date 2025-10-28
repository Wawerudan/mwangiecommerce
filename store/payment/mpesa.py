import requests
from django.shortcuts import render
from django.http import JsonResponse
from requests.auth import HTTPBasicAuth
import json
from django.http import HttpResponse
import base64
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from store.views import get_cart  # ✅ make sure this returns the current user's cart

CONSUMER_KEY = "crRK8TJbMyKYnRFs6k6qnaxw1MJ9q3T6G4oJ2ho57dEPaAaj"
CONSUMER_SECRET = "oNC9A2WyU7Mf4zkK0o08L5sXOfjUkYGKRc4bPHwOJrvJCa3PAG3caozL2Q8xmKWF"
PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
BUSINESS_SHORT_CODE = "174379"
CALLBACK_URL = "https://unbragging-conchita-superadjacent.ngrok-free.dev/api/callback/"

def generate_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    return response.json().get('access_token')

@csrf_exempt
@login_required(login_url='/login/')
def lipa_na_mpesa_online(request):
    # 🛒 Always load current cart first
    cart = get_cart(request)
    cart_items = cart.items.select_related('variant')
    total = sum(item.variant.price * item.quantity for item in cart_items)

    if request.method == "POST":
        phone_number = request.POST.get("number", "").strip()
        if not phone_number.startswith("254") or not phone_number.isdigit():
            messages.error(request, "⚠️ Enter a valid phone number starting with 254.")
            return render(request, "store/cart.html", {"cart": cart, "total": total})

        if total <= 0:
            messages.error(request, "⚠️ Your cart is empty or invalid.")
            return render(request, "store/cart.html", {"cart": cart, "total": total})

        access_token = generate_access_token()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode((BUSINESS_SHORT_CODE + PASSKEY + timestamp).encode()).decode()

        payload = {
            "BusinessShortCode": BUSINESS_SHORT_CODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(total),
            "PartyA": int(phone_number),
            "PartyB": BUSINESS_SHORT_CODE,
            "PhoneNumber": int(phone_number),
            "CallBackURL": CALLBACK_URL,
            "AccountReference": "Waweru Dan",
            "TransactionDesc": "Payment for order"
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        res = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers=headers
        )
        data = res.json()
        print("STK Response:", data)

        if data.get("ResponseCode") == "0":
            messages.success(request, " STK Push sent! Check your phone to complete payment.")
        else:
            messages.error(request, f" STK Push failed: {data.get('errorMessage', 'Unknown error')}")

        # 👇 Return same page with actual cart data & messages
        return render(request, "store/cart.html", {
            "cart": cart,
            "total": total,
            "cart_items": cart_items
        })

    # 👇 If not POST, just show the current cart normally
    return render(request, "store/cart.html", {
        "cart": cart,
        "total": total,
        "cart_items": cart_items
    })

    
@csrf_exempt
def stk_callback(request):
    data = json.loads(request.body.decode('utf-8'))
    print("Callback Data:", data)

    # You can save the transaction result in your database here
    return HttpResponse("Callback received successfully")

