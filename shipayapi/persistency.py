from shipaypdv.shipayapi.models import Transaction


def create_transaction(request_body: dict):
    created_model = Transaction.objects.create(
        establishment=request_body.get("establishment"),
        description=request_body.get("description"),
        amount=request_body.get("amount"),
        customer=request_body.get("customer")
    )

    return created_model
