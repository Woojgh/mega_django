import os
import requests
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


def oauth_session(request, state=None, token=None):
  """ Constructs the OAuth2 session object. """
  if os.environ.get('DISCORD_REDIRECT_URI') is not None:
      redirect_uri = os.environ.get('DISCORD_REDIRECT_URI')
  else:
      redirect_uri = request.build_absolute_uri(
          'https://localhost:8000')
  scope = (['identify', 'email', 'guilds.join'] if os.environ.get('DISCORD_EMAIL_SCOPE')
           else ['identity', 'guilds.join'])
  return OAuth2Session(os.environ.get('DISCORD_CLIENT_ID'),
                       redirect_uri=redirect_uri,
                       scope=scope,
                       token=token,
                       state=state)


class home_view(View):
  """Home view callable, for the home page."""

  # state = uuid.uuid4()

  def get(self, request, *args, **kwargs):
    """Gets home view."""
    kwargs = self.request.GET
    import pdb; pdb.set_trace()
    if 'code' in self.request.GET:
      request.session['code'] = self.request.GET
      request.session['is_logged_in'] = True
      request.session.save()
      temp = DiscordUser.objects.filter(user=request.user)[0]
      discord_profile = dict({i:k for (i,k) in temp.__dict__.items()})
      context = {'discord_profile': discord_profile}
    context = {}
    return render(request, 'home.html', context=context)


   
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
