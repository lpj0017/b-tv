from django.db import models

class MyStorage(models.Model):
    def custom_upload_to(self, filename):
        return 'foo'

    def random_upload_to(self, filename):
        # This returns a different result each time,
        # to make sure it only gets called once.
        import random
        return '%s/%s' % (random.randint(100, 999), filename)

    normal = models.FileField(upload_to='tests')
    custom = models.FileField(upload_to=custom_upload_to)
    random = models.FileField(upload_to=random_upload_to)
    default = models.FileField(upload_to='tests', default='tests/default.txt')

    def __unicode__(self):
        return str(self.id)
    
