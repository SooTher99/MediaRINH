from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.account.serializers import PersonalAreaSerializer
from apps.account.models import User


class PersonalAreaView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PersonalAreaSerializer
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        """Изменение данных в личном кабинете"""
        queryset = self.get_queryset().filter(pk=request.user.pk).first()
        serializer = self.get_serializer(queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        """Вывод информации из личного кабинета"""
        queryset = self.get_queryset().filter(pk=request.user.pk).first()
        serializer = self.get_serializer(queryset)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
