from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
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


def home(res):
    permission_classes = (IsAuthenticated,)
    return render(res, "home.html", {})


def login(res):
    return render(res, "login.html", {})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:homepage")


def create_loan(request):
    permission_classes = (IsAuthenticated,)
    if request.method == 'POST':
        form = LoanForm(request.POST)
        import pdb;
        pdb.set_trace()

        #        form = form.cleaned_data
        # form['ClientIDRef'] = request.user.username
        form_new = form.save(commit=False)
        user = request.user
        form_new.ClientIDRef = user
        import pdb;
        pdb.set_trace()
        form = LoanForm(form_new)
        import pdb;
        pdb.set_trace()

        if form.is_valid():
            loan = form.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            form = LoanForm()
    else:
        form = LoanForm()
    return render(request, 'create.html', {
        'form': form,
    })


def create_payment(request):
    permission_classes = (IsAuthenticated,)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            pay = form.save(commit=False)
            pay.user = request.user
            pay.save()
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'create.html', {
        'form': PaymentForm,
    })
