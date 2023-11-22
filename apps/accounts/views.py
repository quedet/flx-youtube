import http

from django.contrib.auth import authenticate, login
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.accounts.models import User
from apps.accounts.forms import UserCreationForm, AuthenticationCompleteForm, AuthenticationIdentifierForm, UserCreationNameForm, \
    UserCreationBasicInfoForm, UserCreationEmailForm


# Create your views here.
class LoginIdentifierView(FormView):
    template_name = 'pages/registration/login/identifier.html'
    form_class = AuthenticationIdentifierForm

    def get(self, request, *args, **kwargs):
        email = request.session.get('user_email')
        initial = {
            'email': email
        }
        form = self.form_class(initial=initial)

        if request.user.is_authenticated:
            return redirect('index')

        return self.render_to_response({
            'form': form
        })

    def form_valid(self, form):
        self.request.session['user_email'] = form.cleaned_data.get('email')
        return redirect('accounts:login-complete')

    def form_invalid(self, form):
        response: object = super().form_invalid(form)
        response.status_code = http.HTTPStatus.UNPROCESSABLE_ENTITY
        return response


class LoginCompleteView(FormView):
    template_name = 'pages/registration/login/password.html'
    form_class = AuthenticationCompleteForm
    success_url = reverse_lazy('assets:index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):
        if request.session.get('user_email') is None:
            return redirect('accounts:login-identifier')

        if request.user.is_authenticated:
            return redirect('index')

        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        response: object = super().form_invalid(form)
        response.status_code = http.HTTPStatus.UNPROCESSABLE_ENTITY
        return response


class SignupNameView(FormView):
    template_name = 'pages/registration/signup/name.html'
    form_class = UserCreationNameForm
    success_url = reverse_lazy('accounts:signup-info')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):
        user = request.session.get('user')

        if request.user.is_authenticated:
            return redirect('index')

        if user is not None:
            initial = {
                **user
            }
        else:
            initial = None

        form = self.form_class(initial=initial)

        return self.render_to_response({
            'form': form
        })

    def form_invalid(self, form):
        response: object = super().form_invalid(form)
        response.status_code = http.HTTPStatus.UNPROCESSABLE_ENTITY
        return response


class SignupBasicInformationView(FormView):
    template_name = 'pages/registration/signup/basic_information.html'
    form_class = UserCreationBasicInfoForm
    success_url = reverse_lazy('accounts:signup-email')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):
        user = request.session.get('user')

        if request.user.is_authenticated:
            return redirect('index')

        initial = {
            **user
        }
        print(user)
        form = self.form_class(initial=initial)

        return self.render_to_response({
            'form': form
        })

    def form_invalid(self, form):
        response: object = super().form_invalid(form)
        response.status_code = http.HTTPStatus.UNPROCESSABLE_ENTITY
        return response


class SignupEmailView(FormView):
    template_name = 'pages/registration/signup/email.html'
    form_class = UserCreationEmailForm
    success_url = reverse_lazy('accounts:signup')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):
        user = request.session.get('user')

        if request.user.is_authenticated:
            return redirect('core:index')

        initial = {
            **user
        }

        print(user)
        form = self.form_class(initial=initial)

        return self.render_to_response({
            'form': form
        })

    def form_invalid(self, form):
        response: object = super().form_invalid(form)
        response.status_code = http.HTTPStatus.UNPROCESSABLE_ENTITY
        return response


class SignupView(FormView):
    template_name = "pages/registration/signup/name.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:skip-or-create-channel')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:index')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        session_user = self.request.session['user']
        raw_password = form.cleaned_data.get('password1')

        if session_user is None:
            return redirect('accounts:signup-name')

        User.objects.create_user(**session_user, password=raw_password)

        email = session_user.get('email')

        user = authenticate(email=email, password=raw_password)
        login(self.request, user, 'apps.accounts.backends.EmailAuthentication')

        return redirect('accounts:skip-or-create-channel')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = http.HTTPStatus.UNPROCESSABLE_ENTITY
        return response


class SignupSkipChannelCreationView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/registration/signup/skip_or_create_channel.html'

