from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext as _

from account.manager import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_verified = models.BooleanField(default=False, help_text=_('Designates whether the user\'s email is verified.'),)
    created = models.DateTimeField(_('date joined'), auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = UserManager()
    
    pfp = models.ImageField(upload_to ='static/pfp', blank=True) 
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    FIELDS_TO_UPDATE = ("first_name", "last_name", "phone_number")