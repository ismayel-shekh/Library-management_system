from django.template.loader import render_to_string 
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import transaction
from .forms import DepositForm
from django.core.mail import EmailMessage, EmailMultiAlternatives
# Create your views here.
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib import messages

# class DepositView(LoginRequiredMixin, CreateView):
#     model = transaction
#     form_class = DepositForm
#     template_name = 'deposit.html'
#     success_url = reverse_lazy('home')

#     def form_valid(self, form):
#         amount = form.cleaned_data.get('amount')
#         account = self.request.user.account
#         account.balance += amount
#         account.save(
#             update_fields=[
#                 'balance'
#             ]
#         )
#         return super().form_valid(form)
def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template,{
        'user': user,
        'amount': amount,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

class DepositView(LoginRequiredMixin, CreateView):
    model = transaction
    form_class = DepositForm
    template_name = 'deposit.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account

        transaction = form.save(commit=False)
        transaction.account = account
        transaction.save()


        account.balance += amount
        account.save(update_fields=['balance'])
        x = self.request.user.email
        print(x)
        send_transaction_email(self.request.user, amount, "Deposite Message", 'deposit_email.html')

        return super().form_valid(form)