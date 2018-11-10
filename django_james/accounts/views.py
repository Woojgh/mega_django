import os
import requests
from .models import UserProfile
from django.shortcuts import render
from django.views import View
from discord.http import HTTPClient
from discord.client import Client
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.db.models import Q
from allauth.account.views import ConfirmEmailView
from django_filters import rest_framework as filters
from django.http import Http404
from django.shortcuts import render_to_response
from rest_framework.response import Response
from django.views.generic.base import TemplateResponseMixin, View
from django.middleware.csrf import get_token
from rest_auth.registration.views import SocialLoginView
from rest_framework import permissions, generics, viewsets, schemas, views
from datetime import datetime
from discord_bind.models import DiscordUser 
from allauth.utils import build_absolute_uri
from requests_oauthlib import OAuth2Session
import uuid
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from django_registration.exceptions import ActivationError
from django_registration.forms import RegistrationForm, UserCreationForm

def oauth_session(request, state=None, token=None):
  """ Constructs the OAuth2 session object. """
  if os.environ.get('DISCORD_REDIRECT_URI') is not None:
      redirect_uri = os.environ.get('DISCORD_REDIRECT_URI')
  else:
      redirect_uri = request.build_absolute_uri(
          'https://localhost:8000')
  scope = (['identify', 'email', 'guilds', 'guilds.join'] if os.environ.get('DISCORD_EMAIL_SCOPE')
           else ['identity', 'guilds.join'])
  return OAuth2Session(os.environ.get('DISCORD_CLIENT_ID'),
                       redirect_uri=redirect_uri,
                       scope=scope,
                       token=token,
                       state=state)


class registration_view(FormView):
    """
    Base class for user registration views.

    """
    disallowed_url = reverse_lazy('django_registration_disallowed')
    form_class = RegistrationForm
    success_url = 'https://localhost:8000/profile'
    template_name = 'registration/registration_form.html'

    def dispatch(self, *args, **kwargs):
        """
        Check that user signup is allowed before even bothering to
        dispatch or do other processing.

        """
        if not self.registration_allowed():
            return HttpResponseRedirect(force_text(self.disallowed_url))
        return super(registration_view, self).dispatch(*args, **kwargs)

    def get_success_url(self, user=None):
        """
        Return the URL to redirect to after successful redirection.

        """
        # This is overridden solely to allow django-registration to
        # support passing the user account as an argument; otherwise,
        # the base FormMixin implementation, which accepts no
        # arguments, could be called and end up raising a TypeError.
        return super(registration_view, self).get_success_url()

    def form_valid(self, form):
        return HttpResponseRedirect(
            self.get_success_url(self.register(form))
        )

    def registration_allowed(self):
        """
        Override this to enable/disable user registration, either
        globally or on a per-request basis.

        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def register(self, form):
        """
        Implement user-registration logic here. Access to both the
        request and the registration form is available here.

        """
        if self.request.method == 'POST':
          form = UserCreationForm(self.request.POST)
          if form.is_valid():
            new_user = form.save()
            messages.info(self.request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(self.request, new_user)
        return HttpResponseRedirect("/profile/")


class profile_view(View):
  """Home view callable, for the home page."""

  state = uuid.uuid4()

  def get(self, request, *args, **kwargs):
    """Gets home view."""

    kwargs = self.request.GET
    if request.user.is_active:
      profile = UserProfile.objects.get(user=request.user)
      if 'code' in request.session:
        token_dict = exchange_code(request.session['code']['code'])
        redirect_uri = request.build_absolute_uri('https://localhost:8000')
        response = request.build_absolute_uri()
        scope = (['identify', 'email', 'connections', 'guilds', 'guilds.join'])
        state = OAuth2Session.new_state(self)
        oauth = oauth_session(request, state=state)
        user_url = "https://discordapp.com/api/v6/users/@me"
        querystring = {"":""}
        payload = ""
        headers = {
            'cookie': "__cfduid" + request.COOKIES['csrftoken'],
            'content-type': "application/json",
            'authorization': "Bearer " + token_dict['access_token'],
          }
        discord_user = requests.request("GET", user_url, data=payload, headers=headers, params=querystring).json()
        data = decompose_data(discord_user, token_dict)
        bind_user(request, data)
        self.session = OAuth2Session(os.environ.get('DISCORD_CLIENT_ID'),
                        redirect_uri=redirect_uri,
                        scope=scope,
                        token=token_dict['access_token'],
                        state=state)
        request.session['is_logged_in'] = True
        request.user.discord_active = True
        request.user.save()
        request.session.save()
        import pdb; pdb.set_trace()
        discord_profile = DiscordUser.objects.filter(user=request.user)[0]
        context = {'discord_user': discord_user, 'discord_profile': discord_profile, 'profile': profile}
      else:
        context = {'profile': profile}
    else:
      context = {}
    return render(request, 'profile.html', context=context)

API_ENDPOINT = 'https://discordapp.com/api/v6'
REDIRECT_URI = 'http://localhost:8000'


def exchange_code(code):
  data = {
    'client_id': os.environ.get('DISCORD_CLIENT_ID'),
    'client_secret': os.environ.get('DISCORD_CLIENT_SECRET'),
    'grant_type': 'client_credentials',
    'code': code,
    'redirect_uri': REDIRECT_URI,
    'scope': 'identify email connections'
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  rb = requests.post('%s/oauth2/token' % API_ENDPOINT, data, headers)
  rb.raise_for_status()
  return rb.json()


def decompose_data(user, token_dict):
  """ Extract the important details """
  data = {
      'uid': user['id'],
      'username': user['username'],
      'discriminator': user['discriminator'],
      'email': user.get('email', ''),
      'avatar': user.get('avatar', ''),
      'access_token': token_dict.get('access_token', ''),
      'refresh_token': token_dict.get('refresh_token', ''),
      'scope': ' '.join(token_dict.get('scope', '')),
  }
  for k in data:
      if data[k] is None:
          data[k] = ''
  try:
      expiry = datetime.utcfromtimestamp(float(token_dict['expires_at']))
      if os.environ.get('USE_TZ'):
          expiry = make_aware(expiry)
      data['expiry'] = expiry
  except KeyError:
      pass
  return data


def bind_user(request, data):
  """ Create or update a DiscordUser instance """
  uid = data.pop('uid')
  count = DiscordUser.objects.filter(uid=uid).update(user=request.user, **data)
  if count == 0:
    # import pdb; pdb.set_trace()
    DiscordUser.objects.create(uid=uid, user=request.user, **data)