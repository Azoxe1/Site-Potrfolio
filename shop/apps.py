from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'shop'
    verbose_name = 'Магазин'

    def ready(self):
        """
        импортируем сигналы
        """