from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid, string
import random


class UserManager(BaseUserManager):
    def create_user(self, email, firstName, lastName, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not firstName:
            raise ValueError('Users must have a first name')
        if not lastName:
            raise ValueError('Users must have a last name')

        user = self.model(
            email=self.normalize_email(email),
            firstName=firstName,
            lastName=lastName,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, firstName, lastName, password=None):
        user = self.create_user(
            email,
            firstName=firstName,
            lastName=lastName,
        )
        
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    userId = models.CharField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def save(self, *args, **kwargs):
        if not self.userId:
            self.generate_unique_field()
        # self.set_password(self.password)
        super(User, self).save(*args, **kwargs)


    def generate_unique_field(self):
        while True:
            # Generate 9 uppercase letters
            letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(9))
            
            # Generate 3 random numbers
            numbers = ''.join(random.choice(string.digits) for _ in range(3))
            
            # Combine letters and numbers
            unique_value = letters + numbers

            # Shuffle the unique_value to ensure numbers are not in the first position
            unique_value_list = list(unique_value)
            random.shuffle(unique_value_list)
            self.userId = ''.join(unique_value_list)

            # Check if the value is unique
            if not User.objects.filter(userId=self.userId).exists():
                break



class Organisation(models.Model):
    org_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User, related_name='organisations')

    def __str__(self):
        return self.name
