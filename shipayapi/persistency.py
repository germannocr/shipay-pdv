from shipayapi.models import Transaction


def create_transaction(request_body: dict):
    """
    Creates an object of type Transaction that represents a new transaction carried out.

    Parameters:
        request_body (dict):The dictionary with the JSON body passed in the request.

    Returns:
        created_model (Transaction):The newly created Transaction object.
    """
    created_model = Transaction.objects.create(
        establishment=request_body.get("estabelecimento"),
        description=request_body.get("descricao"),
        amount=request_body.get("valor"),
        customer=request_body.get("cliente")
    )

    return created_model
