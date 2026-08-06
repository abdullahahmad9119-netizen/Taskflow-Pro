from django.contrib.auth.base_user import BaseUserManager

class CreateUserManager(BaseUserManager):
    def create_user(self, email, password, **otherfields):
        if not email:
            raise ValueError("email not provided")
        email=self.normalize_email(email)
        user=self.model(email=email, **otherfields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email , password=None, **otherfields):
        otherfields.setdefault('is_staff', True)
        otherfields.setdefault('is_superuser', True)
        otherfields.setdefault('is_active', True)

        if otherfields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if otherfields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.CreateUser(email, password , **otherfields)