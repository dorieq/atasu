from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=50)
    x_axis = models.FloatField()
    y_axis = models.FloatField()

    def __str__(self):
        return self.name
    
class Train(models.Model):
    end_location = models.ForeignKey(Station, on_delete=models.CASCADE)
    days_until_destination = models.IntegerField()
    count = models.IntegerField()

    def __str__(self) -> str:
        return str(self.end_location)
    
class Order(models.Model):
    start_location = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='start_location')
    end_location = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='end_location')
    start_date = models.DateField()
    end_date = models.DateField()
    count = models.IntegerField()