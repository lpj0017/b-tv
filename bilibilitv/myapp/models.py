from django.db import models

class Video(models.Model):
    aid = models.IntegerField()
    title = models.CharField(max_length=150)
    pic_url = models.CharField(max_length=2048)
    category = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return self.title

class Part(models.Model):
    cid = models.IntegerField()
    name = models.CharField(max_length=150)
    desc = models.TextField(blank=True)
    mp4 = models.FileField(upload_to='video/%Y-%m-%d/',blank=True,null=True) 
    video= models.ForeignKey(Video)

    def __unicode__(self):
        return str(self.cid)

class Topic(models.Model):
    image_url = models.CharField(max_length=2048)
    link = models.CharField(max_length=2048)
    title = models.CharField(max_length=150)
    desc = models.TextField()
    date = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    clicked = models.CharField(max_length=50)
    comments = models.CharField(max_length=50)

    def __unicode__(self):
        return self.title

class VideoURL(models.Model):
    url=models.CharField(max_length=2048)
    is_saved = models.BooleanField(default=False)

    def __unicode__(self):
        return self.url
# Create your models here.
