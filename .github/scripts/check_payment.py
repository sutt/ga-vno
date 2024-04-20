import time

def check_payment(attempts: int = 10, delay_seconds: int = 10) -> None:
    for _ in range(attempts):
        print("Attempting...")
        time.sleep(delay_seconds)
        