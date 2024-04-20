import os
import time

import dotenv
import requests


class Invoice:
    def __init__(self, hash: str, request: str) -> None:
        self.payment_hash = hash
        self.payment_request = request


class PaymentService:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key

    def create_invoice(
        self,
        amount: int,
        memo: str = ""
    ) -> str:
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }

        data = {
            "out": False,
            "amount": amount,
            "memo": memo,
            "unit": "sat"
        }

        url = f"https://{self.base_url}/api/v1/payments"

        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 201:
            raise RuntimeError("Couldn't create invoice")
        
        response_json = response.json()
        return Invoice(response_json["payment_hash"], response_json["payment_request"])


    def check_payment(
        self, 
        payment_hash: str,
        attempts: int = 10,
        delay_seconds: int = 30
    ) -> bool:
        url = f"https://{self.base_url}/api/v1/payments/{payment_hash}"
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        # TODO: Refactor
        for i in range(attempts):
            print("Attempt", i + 1)
            response = requests.get(url, headers=headers)
            if response.status_code == 200 and response.json["paid"]:
                return True

            time.sleep(delay_seconds)
        
        return False


if __name__ == "__main__":
    dotenv.load_dotenv()

    # TODO: Null check
    BASE_URL: str = os.getenv("WALLET_BASE_URL")
    API_KEY: str = os.getenv("WALLET_API_KEY")
    INVOICE_AMOUNT: int = int(os.getenv("INVOICE_AMOUNT"), 10)
    
    CHECK_PAYMENT_ATTEMPTS: int = int(os.getenv("CHECK_PAYMENT_ATTEMPTS", 10))
    CHECK_PAYMENT_DELAY: int = int(os.getenv("CHECK_PAYMENT_DELAY"), 30)

    try:
        payment_service = PaymentService(BASE_URL, API_KEY)
        invoice: Invoice = payment_service.create_invoice(INVOICE_AMOUNT)

        print("Please pay the invoice:", invoice.payment_request)

        # TODO: Refactor
        is_paid = payment_service.check_payment(
            invoice.payment_hash,
            CHECK_PAYMENT_ATTEMPTS,
            CHECK_PAYMENT_DELAY
        )  # May run long  
        if is_paid:
            print("Success!")
        else:
            print("Fail!")

    except RuntimeError:
        # TODO: Refactor
        print("Couldn't create invoice")
