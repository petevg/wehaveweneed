from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Q, signals
from wehaveweneed.accounts.listeners import send_activation_email

POSTCHOICE = (
  ('have', 'Have'),
  ('need', 'Need'),
)
PRIORITYCHOICE = (
  ('short', 'Immediate / Life-Saving'),
  ('mid', 'Mid-Term / Life-Sustaining'),
  ('long', 'Long-Term / Life-Enhancing'),
)

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child')
    
    class Meta:
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user  = models.ForeignKey(User, unique=True)
    phone = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=200)

    def __unicode__(self):
        return 'profile of %s' % self.user.username

signals.post_save.connect(send_activation_email, sender=User)

UNITS = (
    ('units', 'generic units'),
    ('people', 'people'),
    ('lbs', 'lbs'),
    ('kg', 'kg'),
    ('gallons', 'gallons'),
    ('liters', 'liters'),
    ('feed', 'feet'),
    ('yards', 'yards'),
    ('meters', 'meters'),
    )

class PostManager(models.Manager):
    def open(self):
        """
        Return posts that are not fulfilled, current time is
        greater than start time, and end time does not exist
        or current time is less than end time.
        """
        now = datetime.utcnow()
        return Post.objects.filter(
            fulfilled=False, time_start__lte=now).filter(
                Q(time_end__gte=now) | Q(time_end__isnull=True))

class Post(models.Model):
    objects     = PostManager()
    created_at  = models.DateTimeField(default=datetime.utcnow)
    title       = models.CharField(max_length=200)
    type        = models.CharField(max_length=10, choices=POSTCHOICE,
                                   default='need')
    priority    = models.CharField(max_length=10, choices=PRIORITYCHOICE,
                                   default='mid')
    location    = models.CharField(max_length=100)
    geostamp    = models.CharField(max_length=100, blank=True)
    time_start  = models.DateTimeField(default=datetime.utcnow, blank=True)
    time_end    = models.DateTimeField(blank=True, null=True)
    category    = models.ForeignKey(Category)
    contact     = models.ForeignKey(User, blank=True, null=True)
    content     = models.TextField()
    responses   = models.IntegerField(default=0)
    fulfilled   = models.BooleanField(default=False)

    object = models.CharField(max_length=100, default='', blank=True)
    number = models.PositiveIntegerField(default=0, blank=True)
    unit = models.CharField(max_length=100, choices=UNITS,
                            default='', blank=True)

    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('view_post', (), {'id': self.id})

    @property
    def priority_full(self):
        return {'short': 'Immediate / Life-Saving',
                'mid': 'Mid-Term / Life-Sustaining',
                'long': 'Long-Term / Life-Enhancing'}[self.priority]


class Reply(models.Model):
    post = models.ForeignKey(Post, related_name='replies')
    created_at = models.DateTimeField(default=datetime.utcnow)
    sender = models.ForeignKey(User, related_name='replies')
    content = models.TextField()

    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return "reply from %s to '%s'" % (self.sender.username,
                                          self.post.title)
