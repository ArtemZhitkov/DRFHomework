from rest_framework import serializers


def validate_url(value):
    valid_url = "https://youtube.com/"
    if not value.startswith(valid_url):
        raise serializers.ValidationError(
            "Неверный URL-адрес. Пожалуйста, укажите правильный URL-адрес YouTube."
        )
