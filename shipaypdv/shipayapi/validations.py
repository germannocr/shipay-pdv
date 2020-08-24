import re

from shipaypdv.shipayapi.exceptions import MissingRequiredFields, InvalidFieldType, InvalidCpfNumber, InvalidCnpjNumber


def validate_post_body(request_body: dict):

    required_fields = [
        'estabelecimento',
        'cliente',
        'valor',
        'descricao'
    ]
    request_fields = request_body.keys()

    for current_required_field in required_fields:
        if current_required_field not in request_fields:
            raise MissingRequiredFields()

        if current_required_field == 'valor' and not isinstance(request_body[current_required_field], float):
            raise InvalidFieldType()

        if current_required_field != 'valor' and not isinstance(request_body[current_required_field], str):
            raise InvalidFieldType()

    customer_cpf = request_body.get('cliente')
    validate_cpf_number(cpf_number=customer_cpf)

    customer_cnpj = request_body.get('estabelecimento')
    validate_cnpj_number(cnpj_number=customer_cnpj)


def validate_cpf_number(cpf_number: str):
    if cpf_number:
        translated_cpf = ''.join(re.findall('\d', str(cpf_number)))

        if len(translated_cpf) < 11:
            raise InvalidCpfNumber()

        cpf_to_int = map(int, translated_cpf)
        new_cpf = cpf_to_int[:9]

        while len(new_cpf) < 11:
            cpf_sum = sum([(len(new_cpf) + 1 - i) * v for i, v in enumerate(new_cpf)]) % 11

            if cpf_sum > 1:
                digit = 11 - cpf_sum
            else:
                digit = 0
            new_cpf.append(digit)

        if new_cpf != cpf_to_int:
            raise InvalidCpfNumber()


def validate_cnpj_number(cnpj_number: str):
    if cnpj_number:

        translated_cnpj = ''.join(re.findall('\d', str(cnpj_number)))

        if len(translated_cnpj) < 14:
            raise InvalidCnpjNumber()

        cnpj_to_int = map(int, translated_cnpj)
        new_cnpj = cnpj_to_int[:12]

        validation_sequence = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        while len(new_cnpj) < 14:
            cnpj_sum = sum([x * y for (x, y) in zip(new_cnpj, validation_sequence)]) % 11
            if cnpj_sum > 1:
                digit = 11 - cnpj_sum
            else:
                digit = 0
            new_cnpj.append(digit)
            validation_sequence.insert(0, 6)

        if new_cnpj != cnpj_to_int:
            raise InvalidCnpjNumber()
