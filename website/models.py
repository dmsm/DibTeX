from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    USER_ROLE = (
    	('P', 'Professer'),
    	('G', 'Grader'),
    	('S', 'Student')
    )

    # The additional attributes we wish to include.
    type = models.CharField(max_length=1, choices=USER_ROLE)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
