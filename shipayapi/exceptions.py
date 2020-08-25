from rest_framework.exceptions import APIException


class MissingRequiredFields(APIException):
    status_code = 400
    default_detail = "Missing required field. " \
                     "Please send all the necessary fields, including 'establecimento'," \
                     " 'descricao', 'valor' and 'cliente'."
    default_code = "missing_required_field"


class InvalidFieldValue(APIException):
    status_code = 400
    default_detail = "Invalid or incorrect type of one of the fields in the request."
    default_code = "incorrect_field_type"


class InvalidCpfNumber(APIException):
    status_code = 400
    default_detail = "Invalid or incorrect CPF number in the request."
    default_code = "incorrect_cpf"


class InvalidCnpjNumber(APIException):
    status_code = 400
    default_detail = "Invalid or incorrect CNPJ number in the request."
    default_code = "incorrect_cnpj"
