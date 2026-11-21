PAYMENT_PROCESSING_CODE = """
import os

API_KEY = "my-secret-api-key"

def get_user(users, user_id):
    for user in users:
        if user["id"] == user_id:
            return user

    return None


def process_payment(user, amount):
    balance = user["balance"]

    if amount > balance:
        print("Insufficient funds")

    user["balance"] -= amount
    return True


def main():
    users = [{"id": 1, "balance": 100}]

    user = get_user(users, 1)

    process_payment(user, -50)

    print("Payment processed")


if __name__ == "__main__":
    main()
"""


EXPECTED_FINDINGS = [
    {
        "id": "hardcoded_api_key",
        "description": "API key is hardcoded in source code.",
        "severity": "security",
    },
    {
        "id": "negative_payment",
        "description": "Negative payment amounts are accepted.",
        "severity": "correctness",
    },
    {
        "id": "insufficient_funds",
        "description": (
            "Payment processing continues after insufficient funds "
            "are detected."
        ),
        "severity": "correctness",
    },
    {
        "id": "missing_none_handling",
        "description": (
            "process_payment does not handle a None user."
        ),
        "severity": "correctness",
    },
    {
        "id": "unused_import",
        "description": "The os import is never used.",
        "severity": "maintainability",
    },
]