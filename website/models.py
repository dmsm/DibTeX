from django.db import models
from django.contrib.auth.models import User

CHARFIELD_MAX_LENGTH = 255

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    USER_ROLE = (
    	('P', 'Professor'),
    	('G', 'Grader'),
    	('S', 'Student')
    )

    # The additional attributes we wish to include.
    type = models.CharField(max_length=1, choices=USER_ROLE)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class Problem(models.Model):
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    points = models.IntegerField()
    contents = models.TextField()
    solution = models.TextField()
    graders = models.ManyToManyField(UserProfile)


class Submission(models.Model):
    student = models.ForeignKey(UserProfile)
    problems = models.ManyToManyField(Problem)
    contents = models.TextField()
    score = models.IntegerField(null=True, blank=True)


class Assignment(models.Model):
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    due_date = models.DateTimeField()
    problems = models.ManyToManyField(Problem)