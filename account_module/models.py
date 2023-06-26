from django.db import models
from django.db.models import Manager
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin , AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .user_manager import UserManager
from django.core.validators import RegexValidator
from base_module.models.mixin import RescaleImageMixin






class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = 'auth_user'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(
        verbose_name=_("email address"), unique=True,
        error_messages={
            'unique': _(
                "A user is already registered with this email address"),
        },
        db_index=True,
    )

    is_staff = models.BooleanField(
        verbose_name=_("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        verbose_name=_("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_banned = models.BooleanField(
        verbose_name=_("ban"),
        default=False
    )
    date_joined = models.DateTimeField(
        verbose_name=_("date joined"), default=timezone.now,
    )
    activation_code = models.CharField(
        verbose_name=_("activation code"),
        max_length= 200 , null=True
    )
    activation_code_created_date = models.DateTimeField(
        verbose_name=_("activation code sent date"),
        null=True
    )

    objects = UserManager()

    def __str__(self):
        return self.email

ascii_validator = RegexValidator(
    regex=r"^[a-zA-Z]+$",
    message="Only ASCII letters (both lowercase and uppercase) are allowed."
)

from django.contrib.sessions.backends.db import SessionStore
class AnonymousUser (models.Model):
    ip_address = models.CharField(max_length=45 , db_index=True)
    session_key = models.CharField(max_length=40, blank=True)
    is_banned = models.BooleanField(blank=True , null=True)

class UserExtraInformations(RescaleImageMixin , models.Model):

    class Gender(models.TextChoices):
        GENDER_MALE = 'M' , _("Male")
        GENDER_FEMALE = 'F' , _("Female")

    user = models.OneToOneField(to=User,on_delete=models.CASCADE , db_index=True)


    first_name = models.CharField(
        max_length=30, verbose_name=_("first name"),
        blank=True, null=True, validators=[ascii_validator],
    )
    last_name = models.CharField(
        max_length=30, verbose_name=_("last name"),
        blank=True, null=True, validators=[ascii_validator]
    )
    gender = models.CharField(
        max_length=1, blank=True, null=True,
        choices=Gender.choices,
        verbose_name=_("gender"),
    )
    birthdate = models.DateField(blank=True , null=True)

    avatar = models.ImageField(upload_to='images/user_profiles/',
                               blank=True, null=True,
                               verbose_name=_("more informations"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_field_name = 'avatar'
        self.max_size = 200000
        self.max_width = 800

    @property
    def get_fullname(self):
        " returns firstname and/or lastname with space between else 'No Name' "

        first_name = self.first_name if self.first_name else ''
        last_name = self.last_name if self.last_name else ''
        if self.last_name or self.first_name:
            return (first_name+ ' ' + last_name).strip()
        return 'No Name'


    def save(self, *args, **kwargs):
        if self.first_name:
            self.first_name = self.first_name.title()
        if self.last_name:
            self.last_name = self.last_name.title()
        super().save(*args, **kwargs)



    def __str__(self):
        return self.get_fullname



@receiver(post_save,sender=User)
def user_extra(sender , instance , created , **kwargs ):
    '''
    if a new user creates, it will create new object for UserExtraInformations
    '''
    if created:
        UserExtraInformations.objects.create(user= instance)