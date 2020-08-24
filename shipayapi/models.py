from django.db import models


class Establishment(models.Model):

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

    class Meta:
        db_table = 'transaction'

    establishment = models.CharField(max_length=60)
    description = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    customer = models.CharField(max_length=60)

