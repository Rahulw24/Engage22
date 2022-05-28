from django.db import models



types = [('employee','employee'),('manager','manager')]
class Profile(models.Model):
    # Required fields for a Profile
    first_name = models.CharField(max_length=70)  # so as to uniquely map image name and first_name 
    last_name = models.CharField(max_length=70)
    date = models.DateField()
    phone = models.BigIntegerField()
    email = models.EmailField()
    ranking = models.IntegerField()
    profession = models.CharField(max_length=200)
    role= models.CharField(choices=types,max_length=20,null=True,blank=False,default='employee')
    present = models.BooleanField(default=False)
    image = models.ImageField()
    updated = models.DateTimeField(auto_now=True)
    shift = models.TimeField()
    days_present=models.IntegerField(default=0)
    def __str__(self):
        return self.first_name+' '+self.last_name


class LastFace(models.Model):
    last_face = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.last_face

class FilterDate(models.Model):
    req_date=models.DateField();

class LoginDetails(models.Model):
    last_face = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.last_face