from django.db import models

# Base class to include common fields
class BaseModel(models.Model):
    user_id = models.IntegerField()
    guid = models.UUIDField(unique=True)
    platform = models.IntegerField()
    _modified = models.IntegerField()

    class Meta:
        abstract = True

# Aircraft Model
class Aircraft(BaseModel):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    category = models.IntegerField()
    aircraft_class = models.IntegerField()
    power = models.IntegerField()
    seats = models.IntegerField()
    active = models.BooleanField()
    reference = models.CharField(max_length=100)
    tailwheel = models.BooleanField()
    complex = models.BooleanField()
    high_perf = models.BooleanField()
    aerobatic = models.BooleanField()
    fnpt = models.IntegerField()
    kg5700 = models.BooleanField()
    rating = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100)
    cond_log = models.IntegerField()
    fav_list = models.BooleanField()
    sub_model = models.CharField(max_length=100, blank=True)
    record_modified = models.IntegerField()

    def __str__(self):
        return f"{self.make} {self.model} ({self.reference})"

# Flights Model
class Flight(BaseModel):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    date = models.DateField()
    from_airport = models.CharField(max_length=100)
    to_airport = models.CharField(max_length=100)
    route = models.TextField(blank=True)
    time_out = models.TimeField()
    time_off = models.TimeField()
    time_on = models.TimeField()
    time_in = models.TimeField()
    on_duty = models.TimeField()
    off_duty = models.TimeField()
    total_time = models.DecimalField(max_digits=5, decimal_places=2)
    pic = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sic = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    night = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    solo = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cross_country = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    nvg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    nvg_ops = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    day_takeoffs = models.IntegerField(blank=True, null=True)
    day_landings_full_stop = models.IntegerField(blank=True, null=True)
    night_takeoffs = models.IntegerField(blank=True, null=True)
    night_landings_full_stop = models.IntegerField(blank=True, null=True)
    all_landings = models.IntegerField(blank=True, null=True)
    actual_instrument = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    simulated_instrument = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hobbs_start = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hobbs_end = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tach_start = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tach_end = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    holds = models.IntegerField(blank=True, null=True)
    approach1 = models.CharField(max_length=100, blank=True)
    approach2 = models.CharField(max_length=100, blank=True)
    approach3 = models.CharField(max_length=100, blank=True)
    approach4 = models.CharField(max_length=100, blank=True)
    approach5 = models.CharField(max_length=100, blank=True)
    approach6 = models.CharField(max_length=100, blank=True)
    dual_given = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dual_received = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    simulated_flight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ground_training = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    instructor_name = models.CharField(max_length=100, blank=True)
    instructor_comments = models.TextField(blank=True)
    pilot_comments = models.TextField(blank=True)
    flight_review = models.BooleanField(default=False)
    checkride = models.BooleanField(default=False)
    ipc = models.BooleanField(default=False)
    nvg_proficiency = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Flight on {self.date} from {self.from_airport} to {self.to_airport}"

# Add more models as needed for other `table` values like `Pilot`, `Logbook`, etc.
