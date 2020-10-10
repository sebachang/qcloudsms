# -*- coding: utf-8 -*-

from rest_framework import serializers

from mt_apps.example.models import ExampleModel


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleModel
        fields = ('id', 'created', 'title', 'content')
