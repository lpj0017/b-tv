from django.db import models

class Video(models.Model):
    aid = models.IntegerField()
    title = models.CharField(max_length=150)
    pic_url = models.CharField(max_length=2048)
    type = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return self.title

class VideoPart(models.Model):
    cid = models.IntegerField()
    part_name = models.CharField(max_length=150)
    desc = models.TextField(blank=True)
    mp4 = models.FileField(upload_to='video',blank=True,null=True) 
    video= models.ForeignKey(Video)

    def __unicode__(self):
        return self.part_name
# Create your models here.
