from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(null=True, blank=True)

    @property
    def full_name(self):
        return super().get_full_name()

    @property
    def events_registered(self):
        return [attendance.event for attendance in self.attendances.all()]

    @property
    def events_attended(self):
        return [attendance.event for attendance in self.attendances.all() if attendance.attended == 'Yes']
    
    @property
    def attendance_rate(self):
        if len(self.events_registered) == 0:
            return 0
        return round((len(self.events_attended) / len(self.events_registered)) * 100, 2)
    
    def __str__(self):
        return f"{self.username}"
    

class Event(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    starttime = models.DateTimeField(null=False, blank=False)
    endtime = models.DateTimeField(null=False, blank=False)
    organizer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name="organized_events")
    price = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
    thumbnail = models.ImageField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    eventtype = models.CharField(max_length=18, choices=[('Public', 'Public'), ('Private', 'Private')], default="Public", null=False, blank=False)
    # category = models.CharField(max_length=255)

    @property
    def isfree(self):
        return self.price == 0
    
    @property
    def rating(self):
        rating = self.ratings.aggregate(avg_rating=Avg("value"))['avg_rating']
        return round(rating, 2) if rating is not None else 0
    
    @property
    def pending_requests(self):
        return [er for er in self.join_requests.all() if er.status == 'Pending']
    
    @property
    def processed_requests(self):
        return [er for er in self.join_requests.all() if er.status != 'Pending']
    
    @property
    def is_notstarted(self):
        return self.starttime > timezone.now()
    
    @property
    def is_ongoing(self):
        return self.starttime <= timezone.now() <= self.endtime
    
    @property
    def is_completed(self):
        return self.endtime < timezone.now()
    
    @property
    def status(self):
        if self.is_notstarted:
            return "Upcoming"
        elif self.is_ongoing:
            return "Live Now"
        elif self.is_completed:
            return "Completed"
        else:
            return None
    
    @property
    def registered_users(self):
        return [attendee.user for attendee in self.attendees.all()]
    
    @property
    def attended_users(self):
        return [attendee.user for attendee in self.attendees.all() if attendee == True]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Attendee.objects.get_or_create(user=self.organizer, event=self)
    
    def __str__(self):
        return self.name


class Attendee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendances")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="attendees")
    attended = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unknown', 'Unknown')], default="Unknown", null=False, blank=False)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"


class EventRating(models.Model):
    event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.CASCADE, related_name="ratings")
    value = models.IntegerField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="ratings")
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.event} | {self.value} | {self.user}"
    

class EventRequest(models.Model):
    requester = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name="event_requests")
    event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.CASCADE, related_name="join_requests")
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined')])

    def __str__(self) -> str:
        return f"{self.requester} | {self.event} | {self.status}"
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    card_details = models.CharField(max_length=16, null=True, blank=True)  # Mock card details
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[('Success', 'Success'), ('Failed', 'Failed')],
        default='Success',
    )

    def __str__(self):
        return f"Payment by {self.user.username} for {self.event.name} - ${self.amount}"
