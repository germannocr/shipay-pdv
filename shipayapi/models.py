from django.db import models


class Establishment(models.Model):
    """
    This is a class to represent an establishment with CNPJ.

    Attributes:
        id (int): The object unique identifier.
        name (str): The establishment name.
        cnpj (str): The establishment CNPJ unique number.
        owner (str): The establishment owner name.
        phone (str): The establishment phone contact.
    """

    class Meta:

        db_table = 'establishment'

    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=60)
    cnpj = models.CharField(max_length=60)
    owner = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)


    def __str__(self):
        return f'{self.name} / {self.cnpj}'


class Transaction(models.Model):
    """
    This is a class to represent an establishment with CNPJ.

    Attributes:
        establishment (str): The establishment CNPJ unique number.
        description (str): The transaction detailed description.
        amount (Decimal): The transaction amount, with limit of 5 digits.
        customer (str): The transaction customer' CPF unique number.
    """

    class Meta:
        db_table = 'transaction'

    establishment = models.CharField(max_length=60)
    description = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    customer = models.CharField(max_length=60)

