from rest_framework import serializers
from payments.models import *


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class PaymentSerializer(serializers.ModelSerializer):
    status = ChoiceField(choices=Payment.STATUS)

    class Meta:
        model = Payment
        fields = (
            'id',
            'status',
            'company_id'
        )

# class CompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company
#         fields = ('id',)
