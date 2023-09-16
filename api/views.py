from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from api.paginations import DefaultPaginations
from .models import Account, Entry, Transfer
from .serializers import AccountSerializer, EntrySerializer, TransferSerializer, TurnOverSerializer


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    pagination_class = DefaultPaginations
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def me(self, request):
        try:
            account = Account.objects.get(owner_id=request.user.id)
            serializer = AccountSerializer(account)
            return Response(serializer.data)

        except Account.DoesNotExist:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            


    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TurnOverSerializer
        return AccountSerializer
    
    


class TransferViewSet(ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    pagination_class = DefaultPaginations
    permission_classes = [IsAuthenticated]


class EntryViewSet(ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    pagination_class = DefaultPaginations
    permission_classes = [IsAdminUser]

    