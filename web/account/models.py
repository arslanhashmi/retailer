
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext as _
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        """
        Creates and saves a User with the given parameters.
        """
        user = self.model(email=email)
        user.is_active = True
        user.is_superuser = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a Superuser with the given parameters.
        """
        user = self.model(email=email)
        user.is_active = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model.
    """
    email = models.EmailField(verbose_name='email address', max_length=255, null=True, unique=True)
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(
        verbose_name=_('admin status'),
        default=False,
        help_text=_('Designates whether the user can log into this Django Admin Site.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.email

    @property
    def is_staff(self):
        """
        Is the user a member of staff?
        Simplest possible answer: All admins are staff
        """
        return self.is_superuser


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    This is triggered whenever a new user has been created and saved
    to the database.

    Arguments:
        sender: sender of this signal
        instance: model instance
        created: boolean indicating if db record was created

    Keyword Arguments:
        kwargs: dict containing keyword arguments
    """
    if created:
        Token.objects.create(user=instance)
