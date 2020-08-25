from shipayapi.models import Transaction


def create_transaction(request_body: dict):
    created_model = Transaction.objects.create(
        establishment=request_body.get("estabelecimento"),
        description=request_body.get("descricao"),
        amount=request_body.get("valor"),
        customer=request_body.get("cliente")
    )

    return created_model
