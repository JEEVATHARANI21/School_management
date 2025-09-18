from django.db import models
from django.utils import timezone

class StudentRegistration(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # You should hash passwords in production
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Newregester(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('admin', 'Admin'),
    ]
    user_name = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
 # You should hash passwords in production
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)  # <-- NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user_name} ({self.role})"


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    regnum = models.CharField(max_length=20, unique=True)
    sec = models.CharField(max_length=100)


    def __str__(self):
        return self.name
    
class Class(models.Model):
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    class_teacher = models.CharField(max_length=100)  # or ForeignKey to Teacher
    room_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.section}"
    
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_permissions")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="permission_roles")
    status = models.BooleanField(default=True)

    class Meta:
        unique_together = ('role', 'permission')  # prevent duplicate role-permission assignments

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"
