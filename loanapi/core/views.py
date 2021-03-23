from django.shortcuts import render
from django.template import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import Loan, Payment
from .serializers import LoanSerializer, PaymentSerializer
from django.http import JsonResponse


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class LoanView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LoanSerializer

    def get(self, request):
        user = self.request.user
        content = Loan.objects.filter(ClientIDRef=user).values()
        content_list = list(content)
        return JsonResponse(content_list, safe=False)


class PaymentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentSerializer

    def get(self, request):
        user = self.request.user
        loans = Loan.objects.filter(ClientIDRef=user)
        content = Payment.objects.filter(LoanIDRef__in=loans).values()
        content_list = list(content)
        return JsonResponse(content_list, safe=False)
