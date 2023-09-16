
from dataclasses import field, fields
from rest_framework import serializers

from api.models import Account, Entry, Transfer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'owner', 'balance', 'created_at']


class TransferFromSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['from_account_id', 'amount']


class TransferToSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['to_account_id', 'amount']


class TransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transfer
        fields = ['id', 'from_account_id',
                  'to_account_id', 'amount', 'created_at']

    def validate(self, attrs):
        if attrs['from_account_id'].balance < attrs['amount']:
            raise serializers.ValidationError(
                {'from_account': 'balance not enough!'})
        elif attrs['from_account_id'] == attrs['to_account_id']:
            raise serializers.ValidationError(
                {'Error': 'The two accounts are identical!'})
        return super().validate(attrs)

    def save(self, **kwargs):
        from_acc = self.validated_data['from_account_id']
        to_acc = self.validated_data['to_account_id']
        amount = self.validated_data['amount']

        from_acc.balance -= amount
        from_acc.save()

        to_acc.balance += amount
        to_acc.save()
        return super().save(**kwargs)

class SimpleEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ['id', 'amount', 'created_at']


class EntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ['id', 'account_id', 'amount', 'created_at']

    def save(self, **kwargs):

        self.validated_data['account_id'].balance += self.validated_data['amount']
        self.validated_data['account_id'].save()

        return super().save(**kwargs)


class TurnOverSerializer(serializers.ModelSerializer):
    transfer_to = TransferToSerializer(many=True, source='transfers_from')
    transfer_from = TransferFromSerializer(many=True, source='transfers_to')
    enteries = SimpleEntrySerializer(many=True)

    class Meta:
        model = Account
        fields = ['id', 'owner', 'balance', 'enteries', 'transfer_to', 'transfer_from']
