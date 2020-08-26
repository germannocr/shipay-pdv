from django.apps import AppConfig




class ConaferapiConfig(AppConfig):
    name = 'shipayapi'

    def ready(self):
        from shipayapi.models import Establishment
        from shipayapi.models import Transaction