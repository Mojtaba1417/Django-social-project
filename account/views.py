from django.shortcuts import render, redirect
from django.views import View
from . forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from . models import Relation


class UserRegisterView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        print('aaaa')
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                cd['username'],
                cd['email'],
                cd['password']
            )
            messages.success(request, 'you registered successfully', 'success')
            return redirect('home:home_page')
        return render(request, 'account/register.html', {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home_page')
            messages.error(request, 'your username or password are wrong', 'danger')
        return render(request, 'account/login.html', {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('home:home_page')


class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        posts = user.posts.all()
        return render(request, 'account/profile.html', {'posts': posts, 'user':user})


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, 'you already follow this user', 'danger')
        else:
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, 'you followed successfully', 'success')
        return redirect('account:user_profile', user.id)


