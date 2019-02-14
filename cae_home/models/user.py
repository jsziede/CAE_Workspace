"""
Definitions of "User" related Core Models.
"""

import pytz
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import call_command
from django.core.validators import RegexValidator
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


MAX_LENGTH = 255


class User(AbstractUser):
    """
    An extension of Django's default user, allowing for additional functionality.
    Contains user authentication related information.
    """
    @staticmethod
    def get_or_create_superuser(username, email, password):
        """
        Attempts to either get or create user with the given information.
        """
        try:
            new_user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            new_user = User.objects.create_superuser(username, email, password)
        return new_user

    @staticmethod
    def get_or_create_user(username, email, password):
        """
        Attempts to either get or create user with given information.
        """
        new_user, created = User.objects.get_or_create(username=username, email=email)
        if isinstance(new_user, tuple):
            new_user = new_user[0]

        # If user was newly created, set new password.
        if created:
            new_user.set_password(password)
            new_user.save()

        return new_user


class Profile(models.Model):
    """
    A profile for a given user.
    Contains additional user information not regarding authentication.
    """
    # Relationship Keys.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.ForeignKey('PhoneNumber', on_delete=models.CASCADE, blank=True, null=True)
    site_theme = models.ForeignKey('SiteTheme', on_delete=models.CASCADE, blank=True)

    # Model fields.
    user_timezone = models.CharField(
        choices=[(x, x) for x in pytz.common_timezones], default="America/Detroit",
        max_length=255)

    # Self-setting/Non-user-editable fields.
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return '{0}'.format(self.user)

    def save(self, *args, **kwargs):
        """
        Modify model save behavior.
        """
        self.full_clean()
        super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Profile is new instance. Handle for new user being created.
        try:
            # Attempt to get default theme.
            site_theme = SiteTheme.objects.get(name='wmu')
        except ObjectDoesNotExist:
            # Failed to get theme. Likely a unit test. Run site_theme fixtures and attempt again.
            call_command('loaddata', 'full_models/site_themes')
            site_theme = SiteTheme.objects.get(name='wmu')

        # Create new profile object for new user.
        Profile.objects.create(user=instance, site_theme=site_theme)
    else:
        # Just updating an existing profile. Save.
        instance.profile.save()


class Address(models.Model):
    """
    Address for a user.
    """
    # Model fields.
    street = models.CharField(max_length=MAX_LENGTH)
    optional_street = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    city = models.CharField(max_length=MAX_LENGTH)
    state = models.CharField(max_length=MAX_LENGTH, default='MI')
    zip = models.CharField(max_length=MAX_LENGTH)

    # Self-setting/Non-user-editable fields.
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        if self.optional_street is not None:
            return '{0} {1} {2}, {3}, {4}'.format(self.street, self.optional_street, self.city, self.state,
                                                  self.zip)
        else:
            return '{0} {1}, {2}, {3}'.format(self.street, self.city, self.state, self.zip)

    def save(self, *args, **kwargs):
        """
        Modify model save behavior.
        """
        # Save model.
        self.full_clean()
        super(Address, self).save(*args, **kwargs)


class PhoneNumber(models.Model):
    """
    Phone Number for a user.
    """
    # Model validators.
    phone_regex = RegexValidator(
        regex='^\+?1?\d{10,15}',
        message='Phone number must be entered in the format: "+999999999". Between 10 and 15 digits allowed.',
    )

    # Model fields.
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)

    # Self-setting/Non-user-editable fields.
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Phone Number'
        verbose_name_plural = 'Phone Numbers'

    def __str__(self):
        return '{0}'.format(self.phone_number)

    def save(self, *args, **kwargs):
        """
        Modify model save behavior.
        """
        # Save model.
        self.full_clean()
        super(PhoneNumber, self).save(*args, **kwargs)

    def display(self):
        """
        Returns number in read-friendly format.
        Assumes US formatting of numbers.
        """
        if len(str(self.phone_number)) is 10:
            # Standard phone number with area code.
            return '({0}) {1}-{2}'.format(
                self.phone_number[0:3],
                self.phone_number[3:6],
                self.phone_number[6:10]
            )
        else:
            # Other format. Assume US formatting so last 10 digits are what we want.
            return '({0}) {1}-{2}'.format(
                self.phone_number[-10:-7],
                self.phone_number[-7:-4],
                self.phone_number[-4::]
            )

    def display_int(self):
        """
        Returns number in read-friendly format, plus country code.
        Assumes US formatting of numbers.
        """
        if len(str(self.phone_number)) is 10:
            # Standard phone number with area code.
            return '+1-{0}-{1}-{2}'.format(
                self.phone_number[0:3],
                self.phone_number[3:6],
                self.phone_number[6:10]
            )
        else:
            # Other format. Assume US formatting so last 10 digits are what we want.
            return '+1-{0}-{1}-{2}'.format(
                self.phone_number[-10:-7],
                self.phone_number[-7:-4],
                self.phone_number[-4::]
            )


class SiteTheme(models.Model):
    # Model fields.
    name = models.CharField(max_length=MAX_LENGTH)
    gold_logo = models.BooleanField(default=True)

    # Self-setting/Non-user-editable fields.
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Theme'
        verbose_name_plural = 'Site Themes'

    def __str__(self):
        return '{0}'.format(self.name.capitalize())

    def save(self, *args, **kwargs):
        """
        Modify model save behavior.
        """
        # Save model.
        self.full_clean()
        super(SiteTheme, self).save(*args, **kwargs)
