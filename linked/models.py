from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import F

import datetime


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    display_name = models.CharField(max_length=15)

    bio = models.CharField(max_length=500)
    terms_and_conditions = models.BooleanField(default=False)
    joined_on = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        # return self.display_name if (self.display_name != "") else self.user.username
        return self.user.username

    def addPoints(self, earned_points: int) -> int:
        UserProfile.objects.filter(pk=self.pk).update(points=F('points') + earned_points)


class Category(models.Model):
    name = models.CharField(max_length=20)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Link(models.Model):
    by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    domain = models.CharField(max_length=30)
    url = models.CharField(max_length=120)
    description = models.CharField(max_length=350)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def user_already_has_review(self, user: User) -> bool:
        print("hehehehe")
        return Review.objects.filter(link=self, by=user.pk).count() > 0

    def get_user_review(self, user: User):
        return Review.objects.get(link=self, by=user.pk)


class Review(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(max_length=350)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review

