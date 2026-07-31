from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

class Organization(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    slug = models.SlugField(unique = True)
    logo = models.ImageField(upload_to="org_logos/", blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "owned_organizations"
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through = 'Membership',
        related_name = "organization"
    )
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def is_owner(self, user):
        if user == self.owner:
            return True
        return False

    def is_member(self,user):
        return self.members.filter(id=user.id).exists()

    def __str__(self):
        return self.name


#     utility functions
    def add_member(self, user , role):
        membership , created = Membership.objects.update_or_create(
            user=user,
            organizations=self,
            defaults={'role' : role}
        )
        return membership

    def delete_member(self, user):
        if self.owner==user:
            raise ValidationError("the owner of the organization cannot be removed")
        deleted_count, _=Membership.objects.filter(
            user=user,
            organizations=self
        ).delete()
        return deleted_count>0



class Membership(models.Model):
    CHOICE=[
        ("admin","ADMIN"),
        ("manager","MANAGER"),
        ("member","MEMBER")
    ]
    role = models.CharField(choices=CHOICE, default="member")
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "memberships"
    )
    organizations = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    # constraints
    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=['user', 'organizations'],
                name = "Unique_User_Organization_Membership"
            )
        ]

    @property
    def is_admin(self):
        return self.role == 1

    def __str__(self):
        return f"{self.user} - {self.organizations.name} ({self.get_role_display()})"
