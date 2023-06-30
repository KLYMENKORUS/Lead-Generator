from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, UpdateView
from .forms import LoginForm, UserSignUpForm, UserUpdateForm
from django.contrib.auth import get_user_model


User = get_user_model()


__all__ = (
    'UserLoginView',
    'UserLogoutView',
    'UserSignUpView',
    "UserUpdateView"
)


class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data.get('password'))
        new_user.save()
        messages.success(self.request, 'User is created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'User is created failed')
        return super().form_invalid(form)


class UserLoginView(FormView):
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('lead_generator:lead_generator')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(self.request,
                         f'Hi {username}')

        return super().form_valid(form)


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'users/login.html'

    def get_success_url(self):
        messages.success(self.request, 'You have successfully logged out')
        return reverse_lazy('users:login')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'lead_generator/lead_generator.html'
    form_class = UserUpdateForm

    def form_valid(self, form):
        update_form = self.form_class(
            self.request.POST, instance=self.object
        )
        if update_form.is_valid():
            update_form.save()
            messages.success(self.request, 'User is updated successfully')
            return super().form_valid(form)

        messages.error(self.request, 'User is not updated successfully')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('lead_generator:lead_generator')


