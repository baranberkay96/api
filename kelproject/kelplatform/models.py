from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager



class User_Manager(BaseUserManager):
    """Helps Django works with our custom user model"""

    def create_user(self, email, name, password=None):
        """Creates a new user profile object"""

        if not email:
            raise ValueError('Users must have an email address.')

        email = self.normalize_email(email)

        user = self.model(email=email, name=name)

        user.set_password(password)

        user.save(using=self._db)

        return user


    def create_superuser(self, email, name, password):
        """Creates a new super user."""

        user = self.create_user(email, name, password)

        user.is_superuser = True

        user.is_staff = True

        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """User profile"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = User_Manager()
    created_on = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
    confirmation_token = models.CharField(default=True, max_length=255)
    change_password_request_date =  models.DateTimeField(null=True, auto_now_add=True)
    change_password_count = models.IntegerField(default=0,null=False)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Used to get user full name"""
        return self.name

    def get_short_name(self):
        """Used to get user short name"""
        return self.name

    def __str__(self):
        """Used to convert object to string"""
        return self.email
