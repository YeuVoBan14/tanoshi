from django.db import models
import random
import string


# Create your models here.
def generate_order_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

class Order(models.Model):
    created = models.DateField(null=True, blank=True)
    stt = models.CharField(max_length=255, null=True, blank=True)
    employee = models.CharField(max_length=255, null=True, blank=True)
    customer = models.CharField(max_length=255, null=True, blank=True)
    complete_expect = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True)
    color = models.CharField(max_length=10, default='#0D6EFD')
    quantity = models.PositiveIntegerField(null=True, blank=True)
    note_size = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='orders/', null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=10, default=generate_order_code)

    class Meta:
        app_label = "home"
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
