import re
from datetime import datetime

from django.forms import ValidationError
from rest_framework import serializers


def validate_year_release(value):
    """Год выпуска не может быть больше текущего."""
    if value > datetime.now().year:
        raise ValidationError(
            ('Год выпуска не может быть больше текущего'),
            params={'value': value},
        )


def validate(self, data):
    """Валидация username в API"""
    username = data.get('username')
    if username and not re.match(r'^[\w.@+-]+$', username):
        raise serializers.ValidationError(
            'Поле username не соответствует паттерну',
        )
    if data.get('username') == 'me':
        raise serializers.ValidationError('Использовать имя me запрещено')
    return data
