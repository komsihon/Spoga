import json

from django.contrib import messages
from django.shortcuts import render

# Create your views here.

# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from threading import Thread

import requests
from currencies.context_processors import currencies
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _, activate
from django.views.generic import TemplateView

from ikwen.accesscontrol.backends import UMBRELLA
from ikwen.accesscontrol.models import SUDO, Member
from ikwen.core.models import Service, Application
from ikwen.core.utils import get_service_instance, add_event, add_database, set_counters, increment_history_field, \
    get_mail_content, XEmailMessage
from ikwen.rewarding.models import Reward
from ikwen.rewarding.utils import reward_member

from ikwen_kakocase.kako.utils import mark_duplicates
from ikwen_kakocase.kakocase.models import OperatorProfile, SOLD_OUT_EVENT, NEW_ORDER_EVENT
from ikwen_kakocase.kako.models import Product
from ikwen_kakocase.shopping.utils import parse_order_info, send_order_confirmation_sms
from ikwen_kakocase.shopping.models import Customer
from ikwen_kakocase.shopping.views import Cart
from ikwen_kakocase.trade.models import Order
from ikwen_kakocase.trade.utils import generate_tx_code

from daraja.models import Dara


from daraja.models import DARAJA, REFEREE_JOINED_EVENT

logger = logging.getLogger('ikwen')


def set_ticket_payment_checkout(request, payment_mean, *args, **kwargs):
    """
    This function has no URL associated with it.
    It serves as ikwen setting "MOMO_BEFORE_CHECKOUT"
    """
    service = get_service_instance()
    config = service.config
    request.session['amount'] = request.POST['amount']


def confirm_ticket_payment(request, *args, **kwargs):
    messages.success(request, "Ticket purchased")
    return HttpResponse("Notification received")


class Home(TemplateView):
    template_name = 'easygame/home.html'


class Dashboard(TemplateView):
    template_name = 'easygame/dashboard.html'
