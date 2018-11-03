from django.shortcuts import render_to_response, render
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.db.models.signals import post_save
from rest_framework.response import Response
from django.dispatch import receiver
from rest_framework import status


# @login_required
class DiscordDashboard(TemplateView):

    success_url = None
    template_name = 'disc_chat/disc-chat.html'

    def get(self, *args, **kwargs):
        """Gets discord dashboard view."""
        
        # import pdb; pdb.set_trace()
        # self.context = {'stuff': 'print things'}
        return super(DiscordDashboard, self).get(*args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     self.request = request
        
    #     return self.get_response()

