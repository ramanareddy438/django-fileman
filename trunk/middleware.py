# -*- coding: utf-8 -*-

from fileman.settings import ANONYMOUSES
from django.contrib.auth.models import User

class Anonymous_fileman_Setting(object):
    def process_request(self, request):
        if ANONYMOUSES and not request.user.is_authenticated():
            try:
                user = User.objects.get(username="Anonymous")
                request.user = user
            except:
                pass
