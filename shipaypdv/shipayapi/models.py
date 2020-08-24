from django.db import models


class User(models.Model):

    class Meta:

        db_table = 'user'

    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    user_token = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    password = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.name} {self.last_name}'


class Transaction(models.Model):

    class Meta:
        db_table = 'transaction'

    establishment = models.CharField(max_length=60)
    description = models.CharField(max_length=120)
    amount = models.DecimalField
    customer = models.CharField(max_length=60)

