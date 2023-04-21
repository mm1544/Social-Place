from django.db import models
# Importing default User model
from django.contrib.auth.models import User


# Topic can have multiple rooms, but one Room can have one Topic
class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

# Room is a Child of a Topic
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # 'on_delete=models.SET_NULL' --> If related 'Topic' obj. is deleted, then Room will not be deleted
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) #OneToMany
    name = models.CharField(max_length=200)
    # blank=True --> for when we run save() a Room instance, 'description' field can be empty
    # null=True --> for the database, allows empty field
    description = models.TextField(null=True, blank=True)
    # Many2Many field
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    # 'auto_now_add' adds time stamp only when we crete the instance
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # To specify ordering where first are the most recently updated and created
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

# Message is a Child of a Room
class Message(models.Model):
    # Django's default User model
    user = models.ForeignKey(User, on_delete=models.CASCADE) #OneToMany
    # 'on_delete=models.CASCADE' --> If Room is deleted, then all related messages will be deleted.
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #OneToMany
    body = models.TextField() # --> by default this field is REQUIRED
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50] # First 50 characters
