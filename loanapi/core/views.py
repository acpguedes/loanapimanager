from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import LoanForm, PaymentForm
from .models import Loan, Payment
from .serializers import LoanSerializer, PaymentSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })


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


def home(res):
    permission_classes = (IsAuthenticated,)
    return render(res, "home.html", {})


def login(res):
    return render(res, "login.html", {})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:homepage")


@csrf_exempt
def create_loan(request):
    permission_classes = (IsAuthenticated,)
    context = {}
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            client_ip = request.META['REMOTE_ADDR']
            loan = form.save(commit=False)
            loan.ClientIDRef = request.user
            loan.ipAddress = client_ip
            loan.save()
            return render(request, "home.html")
        else:
            return HttpResponse('Something went wrong')
    else:
        form = LoanForm()
        context = {
            'form': form,
        }
        return render(request, 'create.html', context)


def load_loans(request):
    user = request.user
    loans = Loan.objects.filter(ClientIDRef=user)
    return render(request, 'hr/loans_dropdown.html', {'Loans': loans})


@csrf_exempt
def create_payment(request):
    permission_classes = (IsAuthenticated,)
    context = {}
    if request.method == 'POST':
        form = PaymentForm(request.user, request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.ClientIDRef = request.user
            payment.save()
            return render(request, "home.html")
        else:
            return HttpResponse('Something went wrong')
    else:
        form = PaymentForm(request.user)
        context = {
            'form': form,
        }
        return render(request, 'create.html', context)
