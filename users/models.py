from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from django.db import models
from cart.models import Cart


class UserManager(BaseUserManager):
    def create_user(self, phone_number, full_name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number field must be set')
        user = self.model(phone_number=phone_number, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        shopping_cart = Cart.objects.create(user=user)
        shopping_cart.save()
        
        return user

    def create_superuser(self, phone_number, full_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, full_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name']
    
    def delete_model(self, *args, **kwargs):
        OutstandingToken.objects.filter(user=self).delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.phone_number
    
    
    
class Adddress(models.Model):
    user = models.ForeignKey(User,related_name="addresses", on_delete=models.CASCADE)
    description = models.CharField(max_length=650)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ("-created_at",)
        db_table = 'user_addresses'
        
    def __str__(self):
        return self.user.full_name
    