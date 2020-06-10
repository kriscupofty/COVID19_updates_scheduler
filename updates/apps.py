from django.apps import AppConfig


class UpdatesConfig(AppConfig):
    name = 'updates'

    def ready(self):
        from updater import extract_records, updater

        extract_records.save_past_records()
        updater.start()


