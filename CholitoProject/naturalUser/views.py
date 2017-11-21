from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.core import serializers
import json
from django.http import JsonResponse

from CholitoProject.userManager import get_user_index
from complaint.models import AnimalType
from naturalUser.forms import SignUpForm, AvatarForm
from naturalUser.models import NaturalUser, UserFavorite
from animals.models import Animal
from ong.models import ONG


class IndexView(TemplateView):
    context = {}

    def get(self, request, **kwargs):
        c_user = get_user_index(request.user)
        self.context['c_user'] = c_user

        animals = AnimalType.objects.all()

        # Get animals in JSON format
        ong_animals = Animal.objects.exclude(ong__isnull=True)
        ong_animals = serializers.serialize("json",ong_animals)
        #ong_animals = json.dumps(ong_animals)

        # Get all the ONGs
        ongs = ONG.objects.all()

        if request.user.is_authenticated:
            # Get our favorite ids
            if NaturalUser.objects.filter(user_id=request.user.id).exists():
                natural_user = NaturalUser.objects.get(user_id=request.user.id)
                favs = UserFavorite.objects.filter(nat_user_id=natural_user.id)
                favs_id = list()
                for fav in favs:
                    favs_id.append(fav.ong.id)
                self.context['favs'] = favs_id
            else:
                # Wrong user logged in
                pass

        self.context['animals'] = animals
        self.context['ongs'] = ongs
        self.context['ong_animals'] = ong_animals
        if c_user is None:
            return render(request, 'index.html', context=self.context)
        return c_user.get_index(request, context=self.context)


class LogInView(TemplateView):
    template_name = 'login.html'
    animals = AnimalType.objects.all()
    context = {'animals': animals}

    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.context)


class SignUpView(View):
    user_form = SignUpForm(initial={'username': 'dummy'}, prefix='user')
    avatar_form = AvatarForm(prefix='avatar')
    animals = AnimalType.objects.all()
    context = {'user_form': user_form,
               'avatar_form': avatar_form, 'animals': animals}
    template_name = 'sign_up.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.context)

    def post(self, request, **kwargs):
        user_form = SignUpForm(request.POST, prefix='user')
        avatar_form = AvatarForm(request.POST, request.FILES, prefix='avatar')
        if user_form.is_valid() and avatar_form.is_valid():
            user_ = user_form.save()
            user_.refresh_from_db()
            natural_user = NaturalUser.objects.create(
                user=user_, avatar=avatar_form.cleaned_data.get('avatar'))
            username = user_form.cleaned_data.get('email')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        messages.error(request,
                       "Ha ocurrido un error en el registro. Debes ingresar todos los campos para registrarse")
        return render(request, self.template_name, context=self.context)


class UserDetail(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'naturalUser.natural_user_access'

    def post(self, request, **kwargs):
        c_user = get_user_index(request.user)
        c_user.user.first_name = request.POST['f_name']
        c_user.user.last_name = request.POST['l_name']
        if 'avatar' in request.FILES:
            c_user.avatar = request.FILES['avatar']
        c_user.save()
        return redirect('/')


class OngInViewTemplate(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    permission_required = 'naturalUser.natural_user_access'
    template_name = 'usuario-in-ong.html'
    context = {}

    def get(self, request, **kwargs):
        c_user = get_user_index(request.user)
        self.context['c_user'] = c_user
        animals = AnimalType.objects.all()
        self.context['animals'] = animals
        return render(request, self.template_name, context=self.context)


class OngOutViewTemplate(TemplateView):
    template_name = 'usuario-out-ong.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name)


def putFavorite(request):
    if request.method == 'GET':
        userid = int(request.GET.get('user'))
        ongid = int(request.GET.get('ong'))

        if userid==None or ongid==None:
            data = {
                'sucess': 'error'
            }
            return JsonResponse(data)

        if NaturalUser.objects.filter(user_id=request.user.id).exists():
            nat_id = NaturalUser.objects.get(user_id=userid)
            uf = UserFavorite.objects.filter(nat_user_id=nat_id.id,ong_id=ongid)

            if uf.exists():
                uf.delete()
                data = {
                    'sucess': 'deleted'
                }
                return JsonResponse(data)
            else:
                new_user_fav = UserFavorite()
                new_user_fav.nat_user_id = NaturalUser.objects.get(id=nat_id).id
                new_user_fav.ong_id = ONG.objects.get(id=ongid).id
                new_user_fav.save()
                data = {
                    'sucess': 'created'
                }
                return JsonResponse(data)
            
        else:
            data = {
                'sucess': 'error'
            }
            return JsonResponse(data)

