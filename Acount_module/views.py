from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from .forms import LoginForm, RegisterForm, UserPanelForm, ChangePassForm
from .models import UserAcount
from django.contrib.auth import login, logout
from order_module.models import Order
from bookModel_module.models import BookModels


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'Acount_module/login-page.html', context={
            'login_form': login_form,
        })

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email_user = login_form.cleaned_data.get('email')
            pass_user = login_form.cleaned_data.get('password')
            user: UserAcount = UserAcount.objects.filter(email__iexact=email_user).first()
            if user is not None:
                current_user_pass = user.check_password(pass_user)
                if current_user_pass:  # if current pass is true
                    login(request, user)
                    return redirect(reverse('index-page'))
                else:
                    login_form.add_error('email', 'Email , Password is not valid!!')
            else:
                login_form.add_error('email', 'A user with the entered profile was not found!!!')
        return render(request, 'Acount_module/login-page.html', context={
            'login_form': login_form,
        })


class ForgotPass(TemplateView):
    template_name = 'Acount_module/forgat-pass-page.html'


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'Acount_module/register-page.html', context={
            'register_form': register_form,
        })

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            new_email = register_form.cleaned_data.get('email')
            new_pass = register_form.cleaned_data.get('password')
            new_repeat_pass = register_form.cleaned_data.get('repeat_password')
            if new_pass == new_repeat_pass:
                user: bool = UserAcount.objects.filter(email__iexact=new_email).exists()
                if user:
                    register_form.add_error('email', 'This email is duplicate')
                else:
                    new_user = UserAcount(
                        email=new_email,
                        email_activate_code=get_random_string(70),
                        is_active=True,
                    )
                    new_user.set_password(new_pass)
                    new_user.save()
                    return redirect(reverse('login-page'))
            else:
                register_form.add_error('password', 'The password is not the same')
        return render(request, 'Acount_module/register-page.html', context={
            'register_form': register_form,
        })


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login/')


@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    def get(self, request):
        current_user = UserAcount.objects.filter(id=request.user.id).first()
        edit_form = UserPanelForm(instance=current_user)
        return render(request, 'Acount_module/Panel/user-panel.html', context={
            'form': edit_form,
            'current_user': current_user
        })

    def post(self, request):
        current_user = UserAcount.objects.filter(id=request.user.id).first()
        edit_form = UserPanelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)

        return render(request, 'Acount_module/Panel/user-panel.html', context={
            'form': edit_form,
            'current_user': current_user})


@method_decorator(login_required, name='dispatch')
class ChangePassView(View):
    def get(self, request):
        form = ChangePassForm()
        return render(request, 'Acount_module/Panel/Change-pass.html', context={
            'form': form,
        })

    def post(self, request):
        form = ChangePassForm(request.POST)
        new_pass = ChangePassForm.cleaned_data.get('new_password')
        repeat_pass = ChangePassForm.cleaned_data.get('new_password_repeat')
        if form.is_valid():
            user: UserAcount = UserAcount.objects.filter(id=request.user.id).first()
            if user.check_password(form.cleaned_data.get('current_password')):
                if new_pass == repeat_pass:
                    user.set_password(form.cleaned_data.get('password'))
                    user.save()
                    logout(request)
                    return redirect('login/')
                else:
                    form.add_error('new_password', 'The password is not the same')
            else:
                form.add_error('current_password', 'Current password is not valid!!!')
        return render(request, 'Acount_module/Panel/Change-pass.html', context={
            'form': form
        })


@login_required
def CartDetailView(request):
    curent_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                            user_id=request.user.id)
    total_amount = 0
    for order_detail in curent_order.orderdetail_set.all():
        if order_detail.product.offer:
            total_amount += order_detail.product.offer_price * order_detail.count
        else:
            total_amount += order_detail.product.price * order_detail.count

    return render(request, 'Acount_module/Panel/cart-detail.html', context={
        'order': curent_order,
        'sum': total_amount,
    })


@login_required
def AddtoFavBookView(request, id):
    book = get_object_or_404(BookModels, id=id)
    if book.favorite.filter(id=request.user.id).exists():
        book.favorite.remove(request.user)
    else:
        book.favorite.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def FavListView(request):

    books = BookModels.objects.filter(favorite=request.user)
    return render(request, 'Acount_module/Panel/fav-book.html', context={
        'books': books,
    })
