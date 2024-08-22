from django.db import models
from django.contrib.auth.models import  AbstractBaseUser,BaseUserManager

class UsersManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, Password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, Password, **extra_fields)

class Users(AbstractBaseUser):
    uid = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255,default='')
    last_login = models.DateTimeField(null=True, blank=True)  # New field for last login

    objects = UsersManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Add required fields here

    class Meta:
        db_table = 'netflix_users'

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email} {self.password}"


class Language(models.Model):
    LID = models.AutoField(primary_key=True)
    LName = models.CharField(max_length=255)

    def _str_(self):
        return f"{self.LID} {self.LName}"
    

class Profile(models.Model):
    PID = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    PName = models.CharField(max_length=255)

    def _str_(self):
        return self.PName
    
class Genre(models.Model):
    GID = models.AutoField(primary_key=True)
    GName = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.GID} {self.GName}"

class ProfileGenre(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('profile', 'genre')


class MediaType(models.Model):
    MTID = models.AutoField(primary_key=True)
    MTName = models.CharField(max_length=255)

    def __str__(self):
        return self.MTName
    

class Media(models.Model):
    MID = models.AutoField(primary_key=True)
    MName = models.CharField(max_length=255)
    Plot = models.CharField(max_length=255)
    Image = models.ImageField(upload_to='Media/')
    Link = models.CharField(max_length=255)
    Released_on = models.DateField()
    Rating = models.DecimalField(max_digits=3, decimal_places=2)
    Duration = models.IntegerField()
    Year = models.IntegerField()
    MTID = models.ForeignKey(MediaType, on_delete=models.CASCADE)
    LID = models.ForeignKey(Language, on_delete=models.CASCADE)
    def image_url(self):
        return f'/media/{self.MName.replace(" ", "_").lower()}.jpg'

class ProfileWatchlist(models.Model):
    PID = models.ForeignKey(Profile, on_delete=models.CASCADE)
    MID = models.ForeignKey(Media, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('PID', 'MID')

class MediaGenre(models.Model):
    MID = models.ForeignKey(Media, on_delete=models.CASCADE)
    GID = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('MID', 'GID')


class Season(models.Model):
    SID = models.AutoField(primary_key=True)
    SName = models.CharField(max_length=255)
    MID = models.ForeignKey(Media, on_delete=models.CASCADE)
    Number = models.IntegerField()

class Episode(models.Model):
    EID = models.AutoField(primary_key=True)
    EName = models.CharField(max_length=255)
    Plot = models.TextField()
    Number = models.IntegerField()
    SID = models.ForeignKey(Season, on_delete=models.CASCADE)
    LID = models.ForeignKey(Language, on_delete=models.CASCADE)





