from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff set to True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser set to True")

        return self._create(email, password, **extra_fields)


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        RATHER_NOT_SAY = "RATHER_NOT_SAY", "Rather not say"

    username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    email = models.EmailField("Email address", unique=True)
    profile = models.ImageField(upload_to="profiles", default="default.jpg", blank=True)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=20, choices=Gender.choices, default=Gender.RATHER_NOT_SAY)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
