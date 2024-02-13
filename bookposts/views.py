
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib import messages
from django.template.loader import render_to_string 
from django.urls import reverse_lazy
from .models import Post
from accounts.models import UserLibraryAccount
from django.core.mail import EmailMessage, EmailMultiAlternatives
from borrowed_book.models import borrowed_history
# Create your views here.
def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template,{
        'user': user,
        'amount': amount,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()
class BookPostView(DetailView):
    model = models.Post
    pk_url_kwarg = 'id'
    template_name = 'details.html'
    context_object_name = 'bookpost_app'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post =self.object
        reviews = post.reviews.all()
        review_form = forms.ReviewForm()

        context['reviews'] = reviews
        context['reviews_form'] = review_form
        return context



@login_required
def borrowed_book(request, id):
    book = Post.objects.get(pk=id)
    user_account = UserLibraryAccount.objects.get(user = request.user)

    if user_account.balance >= book.book_price:
        borrowed = borrowed_history(
        book_name = book.book_name,
        price = book.book_price,
        account = request.user,
        book_id = book.id,
        )

        borrowed.save()
        user_account.balance -= book.book_price
        user_account.save()
        
        messages.success(request, 'Borrowed successfully')
        send_transaction_email(request.user, book.book_price, "Book Borowing Message", 'borowed_email.html')
        return redirect('home')
        # return request(request, 'review.html', {'reviews_form':book})
    else:
        messages.error(request, 'Insufficient balance to borrow the book')
        return redirect('home')

class BookPostReiewView(DetailView):
    model = models.Post
    pk_url_kwarg = 'id'
    template_name = 'review.html'
    success_url = reverse_lazy('review')
    context_object_name = 'bookpost_app'
    def post(self, request, *args, **kwargs):
        review_form = forms.ReviewForm(data = self.request.POST)
        post = self.get_object()
        book_price = post.book_price
        user_account = UserLibraryAccount.objects.get(user=request.user)
        user_account.balance += book_price
        user_account.save()
        borrow_book = borrowed_history.objects.filter(book_name = post.book_name, account =request.user)
        borrow_book.delete()
        
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.post = post
            new_review.save()
            messages.success(request, 'Review submitted successfully, account balance updated, and book removed from history.')
            return redirect('home')
        return self.get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post =self.object
        reviews = post.reviews.all()
        review_form = forms.ReviewForm()

        context['reviews'] = reviews
        context['reviews_form'] = review_form
        return context
   


# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.urls import reverse_lazy
# from django.views.generic import DetailView
# from django.template.loader import render_to_string
# from django.core.mail import EmailMultiAlternatives
# from . import forms
# from . import models
# from accounts.models import UserLibraryAccount
# from borrowed_book.models import borrowed_history

# class BookPostReiewView(DetailView):
#     model = models.Post
#     template_name = 'review.html'
#     success_url = reverse_lazy('home')
#     context_object_name = 'bookpost_app'

#     def get(self, request, *args, **kwargs):
#         post = self.get_object()
#         reviews = post.reviews.all()
#         review_form = forms.ReviewForm()

#         context = {
#             'reviews': reviews,
#             'reviews_form': review_form,
#             'bookpost_app': post,
#         }

#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         post = self.get_object()
#         review_form = forms.ReviewForm(data=self.request.POST)

#         if review_form.is_valid():
#             new_review = review_form.save(commit=False)
#             new_review.post = post
#             new_review.save()

#         # Borrow the book logic
#         user_account = UserLibraryAccount.objects.get(user=request.user)

#         if user_account.balance >= post.book_price:
#             borrowed = borrowed_history(
#                 book_name=post.book_name,
#                 price=post.book_price,
#                 account=request.user,
#             )
#             borrowed.save()
#             user_account.balance -= post.book_price
#             user_account.save()
#             messages.success(request, 'Borrowed successfully')
#             return redirect('home')
#         else:
#             messages.error(request, 'Insufficient balance to borrow the book')
#             return redirect('detail_post', id=post.id)


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.object
#         reviews = post.reviews.all()
#         review_form = forms.ReviewForm()

#         context['reviews'] = reviews
#         context['reviews_form'] = review_form
#         return context
