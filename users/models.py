from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='/static/img/user.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 220 or img.width > 322500:
            img = Image.open('image.jpg')
            new_img = img.resize((220, 225))
            new_img.save('new_image.jpg')

# Create your models here.
