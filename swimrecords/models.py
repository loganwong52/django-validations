from django.db import models
from django.core.exceptions import ValidationError # import ValidationError from Django
from django.utils.translation import gettext_lazy as text # import gettext_lazy
from django.core.validators import *            # import built-in Django Validators
from django.utils import timezone

# Helper function to validate input for stroke
def validate_stroke_type(stroke_type):
    valid_stroke_types = ['front crawl', 'butterfly', 'breast', 'back', 'freestyle']
    if stroke_type not in valid_stroke_types:
        raise ValidationError(text(f"{stroke_type} is not a valid stroke"))

# Helper function to validate input for record_date and record_broken_date
def validate_record_date(date_input):
    # print(date_input)
    if date_input > timezone.now():
        raise ValidationError(text("Can't set record in the future."))


class SwimRecord(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    relay = models.BooleanField()
    stroke = models.CharField(max_length=11, validators=[validate_stroke_type])     # validate it's one of 'front crawl', 'butterfly', 'breast', 'back', or 'freestyle'
    distance = models.IntegerField(validators=[MinValueValidator(50)])
    record_date = models.DateTimeField(validators=[validate_record_date])   

    record_broken_date = models.DateTimeField()

    def clean(self):
        super().clean()     # base do what you want

        if self.record_broken_date is not None:
            if self.record_broken_date < self.record_date:
                raise ValidationError ({"record_broken_date": "Can't break record before record was set."})
    