# from .serializers import ImageSerializer, RecognitionResultsSerializer
# from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Images, RecognitionResults, User
from .forms import ImageForm, RegisterForm, LoginForm, PasswordChangeForm1
from .utils import get_latex_from_image

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView,PasswordChangeView
from django.views.generic.edit import FormView
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
# Create your views here.
    
class AuthView(View):
    template_name = 'base.html'
    register_form_class = RegisterForm
    login_form_class = LoginForm
    register_success_url = reverse_lazy('auth')
    login_success_url = reverse_lazy('index')

    def get(self, request):
        register_form = self.register_form_class()
        login_form = self.login_form_class()
        return render(request, self.template_name, {
            'form_signup': register_form,
            'form_login': login_form,
            'view_type': 'login'
        })

    def post(self, request):
        register_form = self.register_form_class()
        login_form = self.login_form_class()
        if 'register' in request.POST:
            register_form = self.register_form_class(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.raw_password = register_form.cleaned_data['password']
                user.password = make_password(register_form.cleaned_data['password'])
                user.save()
                messages.success(request, f'Account created for {user.username}')
                return redirect(self.register_success_url)
            
        elif 'login' in request.POST:
            login_form = self.login_form_class(request, data=request.POST)
            if login_form.is_valid():
                login(request, login_form.get_user())
                if not login_form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(0)
                return redirect(self.login_success_url)
            
        return render(request, self.template_name, {
            'form_signup': register_form,
            'form_login': login_form,
            'view_type': 'login'
        })
    
    
class LogoutView(FormView):
    def get(self, request, *args, **kwargs):
        if 'is_logged_in' in request.session:
            del request.session['is_logged_in']
        logout(request)
        return redirect('auth')

class ImageView(LoginRequiredMixin, View):
    template_name = 'index.html'
    image_form_class = ImageForm
    password_form_class = PasswordChangeForm1

    def get(self, request, pk=None):
        image_form = self.image_form_class()
        password_form = self.password_form_class(user=request.user)
        images = Images.objects.filter(user=request.user)
        context = {
            'form': image_form,
            'password_form': password_form,
            'images': images
        }

        if pk:
            image = get_object_or_404(Images, pk=pk)
            results = RecognitionResults.objects.filter(imageID=image)
            context.update({'image': image, 'results': results})

        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        image_form = self.image_form_class(request.POST, request.FILES)
        password_form = self.password_form_class(user=request.user, data=request.POST)
        images = Images.objects.filter(user=request.user)

        if 'change_password' in request.POST:
            if password_form.is_valid():
                password_form.user.raw_password = password_form.cleaned_data['new_password1']
                password_form.save()
                messages.success(request, 'Your password was successfully updated!')
                context = {
                    'form': image_form,
                    'password_form': password_form,
                    'images': images,
                }
                return redirect('auth')
        elif 'submit' in request.POST:
            if image_form.is_valid():
                image = image_form.save(commit=False)
                image.user = request.user
                image.save()
                result = get_latex_from_image(image.image)
                RecognitionResults.objects.create(imageID=image, result=result)
                results = RecognitionResults.objects.filter(imageID=image)
                context = {
                    'form': image_form,
                    'password_form': password_form,
                    'images': images,
                    'image': image,
                    'results': results
                }
                return render(request, self.template_name, context)
        elif 'reload' in request.POST:
            image = get_object_or_404(Images, pk=pk)
            result = get_latex_from_image(image.image)
            RecognitionResults.objects.create(imageID=image, result=result)
            results = RecognitionResults.objects.filter(imageID=image)
            context = {
                'form': image_form,
                'password_form': password_form,
                'images': images,
                'image': image,
                'results': results
            }
            return render(request, self.template_name, context)
        elif 'delete' in request.POST:
            image = get_object_or_404(Images, pk=request.POST['image_id'])
            image.delete()
            images = Images.objects.filter(user=request.user)
            context = {
                'form': image_form,
                'password_form': password_form,
                'images': images
            }
            return render(request, self.template_name, context)

        context = {
            'form': image_form,
            'password_form': password_form,
            'images': images
        }
        return render(request, self.template_name, context)
        


