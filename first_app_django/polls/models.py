from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin

"""
Three-step guide to making model changes:
1. Change your models (in models.py).
2. Run python manage.py makemigrations to create migrations for those changes
3. Run python manage.py migrate to apply those changes to the database.
"""

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text
    
    # adding support for output from was_published_recently() method
    # add sorting feature and proper type representation
    @admin.display(
            boolean=True,
            ordering="pub_date",
            description="Published recently?",
    )
    
    def was_published_recently(self):
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        # fix the bug
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default = 0)

    def __str__(self):
        return self.choice_text