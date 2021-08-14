from django.db import models


class Province(models.Model):
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class Region(models.Model):
    Name = models.CharField(max_length=20)
    Province = models.ForeignKey(
        Province, on_delete=models.CASCADE, related_name="regions")

    def __str__(self):
        return self.Name


class Car(models.Model):
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class Ads(models.Model):
    Driver = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='ads')
    From = models.ForeignKey(
        Region, related_name="From", on_delete=models.CASCADE)
    To = models.ForeignKey(Region, related_name="To", on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    scheduled_date = models.DateField(auto_now_add=False)
    has_mail = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.Driver.Name}, {self.From.Name} - {self.To.Name}, {self.scheduled_date.strftime('%Y/%m/%d')}"


class User(models.Model):
    Telegram_id = models.IntegerField(unique=True)
    Name = models.CharField(max_length=20, null=False)
    Username = models.CharField(max_length=20, blank=True, null=True)
    Phone_number = models.CharField(max_length=20, blank=True)
    Age = models.IntegerField(blank=True, null=True)
    Is_registered = models.BooleanField(default=False)
    Is_Driver = models.BooleanField(default=False)
    Car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    Saved_Ads = models.ManyToManyField(Ads)
    Joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Name
