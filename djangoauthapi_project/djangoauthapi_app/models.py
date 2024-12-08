from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, tc, password=None):
        """
        Creates and saves a User with the given email, name, tc, and password.
        """
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc,
        )
        user.set_password(password)  # Set the password using set_password to hash it
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, tc, password=None):
        """
        Creates and saves a superuser with the given email, name, tc, and password.
        """
        user = self.create_user(
            email,
            name=name,
            tc=tc,
            password=password
        )
        user.is_admin = True
        user.is_staff = True  # Ensure the superuser has staff status
        user.is_active = True  # Ensure superuser is active
        user.save(using=self._db)
        return user


# Custom User Model
class User(AbstractBaseUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)  # Unique email
    tc = models.BooleanField()  # Terms and Conditions field
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Staff status
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = UserManager()  # Use the custom manager

    USERNAME_FIELD = 'email'  # The field to use for authentication
    REQUIRED_FIELDS = ['name', 'tc']  # Fields required during creation of superuser

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        return True

    @property
    def is_staff(self):
        """
        Override staff status to return True if the user is an admin.
        """
        return self.is_admin
