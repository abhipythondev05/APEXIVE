import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Base class to include common fields
class BaseModel(models.Model):
    """
    Abstract base class for models with common fields.

    Fields:
        user_id (IntegerField): ID of the user who created or modified the record.
        guid (UUIDField): Unique identifier for the record.
        platform (IntegerField): Platform ID associated with the record.
        _modified (IntegerField): Timestamp or integer representing the last modification.
    """
    user_id = models.IntegerField()
    guid = models.UUIDField(unique=True)
    platform = models.IntegerField()
    _modified = models.IntegerField()

    class Meta:
        abstract = True

# Aircraft Model
class Aircraft(BaseModel):
    """
    The Aircraft model stores information about different aircraft.

    Fields:
        make (CharField): Manufacturer of the aircraft.
        model (CharField): Model of the aircraft.
        category (IntegerField): Category of the aircraft.
        aircraft_class (IntegerField): Class of the aircraft.
        power (IntegerField): Power of the aircraft's engine.
        seats (IntegerField): Number of seats in the aircraft.
        active (BooleanField): Indicates if the aircraft is active.
        reference (CharField): Reference identifier for the aircraft.
        tailwheel (BooleanField): Indicates if the aircraft has a tailwheel.
        engyype (IntegerField): Engine type of the aircraft.
        complex (BooleanField): Indicates if the aircraft is complex.
        high_perf (BooleanField): Indicates if the aircraft is high performance.
        aerobatic (BooleanField): Indicates if the aircraft is aerobatic.
        fnpt (IntegerField): FNPT (Flight Navigation Procedures Trainer) rating.
        kg5700 (BooleanField): Indicates if the aircraft is KG5700 compliant.
        rating (CharField): Rating of the aircraft.
        company (CharField): Company associated with the aircraft.
        cond_log (IntegerField): Condition log identifier.
        fav_list (BooleanField): Indicates if the aircraft is in the favorite list.
        sub_model (CharField): Sub-model of the aircraft.
        record_modified (IntegerField): Timestamp or integer representing the last modification.
    """
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    category = models.IntegerField()
    aircraft_class = models.IntegerField()
    power = models.IntegerField()
    seats = models.IntegerField()
    active = models.BooleanField()
    reference = models.CharField(max_length=100)
    tailwheel = models.BooleanField()
    engyype = models.IntegerField(default=0)
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

# Flight Model
class Flight(BaseModel):
    """
    The Flight model stores detailed information about flights.

    Fields:
        aircraft_id (ForeignKey): Reference to the Aircraft model.
        date (DateField): Date of the flight.
        from_airport (CharField): Departure airport.
        to_airport (CharField): Arrival airport.
        route (TextField): Flight route description.
        time_out (TimeField): Time of departure.
        time_off (TimeField): Time of takeoff.
        time_on (TimeField): Time of landing.
        time_in (TimeField): Time of arrival.
        on_duty (TimeField): Duty start time.
        off_duty (TimeField): Duty end time.
        total_time (DecimalField): Total flight time.
        pic (DecimalField): Pilot-in-command time.
        sic (DecimalField): Second-in-command time.
        night (DecimalField): Night flying time.
        solo (DecimalField): Solo flying time.
        cross_country (DecimalField): Cross-country flying time.
        nvg (DecimalField): NVG (Night Vision Goggles) time.
        nvg_ops (DecimalField): NVG operations time.
        distance (DecimalField): Flight distance.
        day_takeoffs (IntegerField): Number of daytime takeoffs.
        day_landings_full_stop (IntegerField): Number of daytime full-stop landings.
        night_takeoffs (IntegerField): Number of nighttime takeoffs.
        night_landings_full_stop (IntegerField): Number of nighttime full-stop landings.
        all_landings (IntegerField): Total number of landings.
        actual_instrument (DecimalField): Actual instrument time.
        simulated_instrument (DecimalField): Simulated instrument time.
        hobbs_start (DecimalField): Hobbs meter start time.
        hobbs_end (DecimalField): Hobbs meter end time.
        tach_start (DecimalField): Tachometer start time.
        tach_end (DecimalField): Tachometer end time.
        holds (IntegerField): Number of holds.
        approach (CharField): Approach type.
        dual_given (DecimalField): Dual instruction given time.
        simulated_flight (DecimalField): Simulated flight time.
        ground_training (DecimalField): Ground training time.
        instructor_name (CharField): Name of the instructor.
        instructor_comments (TextField): Comments from the instructor.
        pilot_comments (TextField): Comments from the pilot.
        flight_review (BooleanField): Indicates if the flight is reviewed.
        checkride (BooleanField): Indicates if the flight was a checkride.
        ipc (BooleanField): Indicates if the flight was for IPC (Instrument Proficiency Check).
        nvg_proficiency (BooleanField): Indicates NVG proficiency.
    """
    aircraft_id = models.ForeignKey(Aircraft, on_delete=models.CASCADE, default=1)
    date = models.DateField(null=True)
    from_airport = models.CharField(max_length=100)
    to_airport = models.CharField(max_length=100)
    route = models.TextField(blank=True)
    time_out = models.TimeField(null=True)
    time_off = models.TimeField(null=True)
    time_on = models.TimeField(null=True)
    time_in = models.TimeField(null=True)
    on_duty = models.TimeField(null=True)
    off_duty = models.TimeField(null=True)
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
    approach = models.CharField(max_length=100, blank=True)

    dual_given = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
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



# complex method using a custom Manager or QuerySet to filter or aggregate data.

class ImagePicQuerySet(models.QuerySet):
    def uploaded_and_downloaded(self):
        return self.filter(img_upload=True, img_download=True)

    def recently_modified(self, days):
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        return self.filter(record_modified__gte=int(cutoff_date.timestamp()))
    
    def uploaded_images_by_extension(self, extension, days=30):
        """
        Get images that are uploaded and match the specified file extension,
        modified within the last 'days' days.
        """
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        return self.filter(
            img_upload=True,
            file_ext=extension,
            record_modified__gte=int(cutoff_date.timestamp())
        )

class ImagePicManager(models.Manager):
    def get_queryset(self):
        return ImagePicQuerySet(self.model, using=self._db)

    def uploaded_and_downloaded_images(self):
        return self.get_queryset().uploaded_and_downloaded()

    def images_modified_recently(self, days=30):
        return self.get_queryset().recently_modified(days)

# ImagePic Model
class ImagePic(BaseModel):
    """
    The ImagePic model stores information about images related to records.

    Fields:
        file_ext (CharField): File extension of the image.
        img_code (UUIDField): Unique code for the image.
        file_name (CharField): Name of the image file.
        link_code (UUIDField): Code for linking related records.
        img_upload (BooleanField): Indicates if the image is uploaded.
        img_download (BooleanField): Indicates if the image is available for download.
        record_modified (IntegerField): Timestamp or integer representing the last modification.
    """
    objects = ImagePicManager()  
    file_ext = models.CharField(max_length=10)
    img_code = models.UUIDField(unique=True)
    file_name = models.CharField(max_length=255)
    link_code = models.UUIDField()
    img_upload = models.BooleanField(default=False)
    img_download = models.BooleanField(default=False)
    record_modified = models.IntegerField()

    def __str__(self):
        return f"ImagePic {self.file_name} ({self.img_code})"

# LimitRules Model
class LimitRules(BaseModel):
    """
    The LimitRules model stores information about various limit rules.

    Fields:
        limit_code (UUIDField): Unique code for the limit rule.
        l_from (DateField): Start date of the limit rule.
        l_to (DateField): End date of the limit rule.
        l_type (IntegerField): Type of the limit rule.
        l_zone (IntegerField): Zone associated with the limit rule.
        l_minutes (IntegerField): Number of minutes associated with the limit rule.
        l_period_code (IntegerField): Period code for the limit rule.
        record_modified (IntegerField): Timestamp or integer representing the last modification.
    """
    limit_code = models.UUIDField(unique=True)
    l_from = models.DateField(null=True)
    l_to = models.DateField(null=True)
    l_type = models.IntegerField()
    l_zone = models.IntegerField()
    l_minutes = models.IntegerField()
    l_period_code = models.IntegerField()
    record_modified = models.IntegerField()

    def __str__(self):
        return f"LimitRule {self.limit_code}"

# Query Model
class Query(BaseModel):
    """
    The Query model stores information about predefined queries.

    Fields:
        name (CharField): Name of the query.
        mQCode (CharField): Query code.
        quick_view (BooleanField): Indicates if the query is for quick view.
        short_name (CharField): Short name for the query.
        record_modified (IntegerField): Timestamp or integer representing the last modification.
    """
    name = models.CharField(max_length=255)
    mQCode = models.CharField(max_length=255)
    quick_view = models.BooleanField(default=False)
    short_name = models.CharField(max_length=255, blank=True)
    record_modified = models.IntegerField()

    def __str__(self):
        return self.name

# MyQueryBuild Model
class MyQueryBuild(BaseModel):
    """
    The MyQueryBuild model stores custom query build information.

    Fields:
        build1 (TextField): Custom field for query build 1.
        build2 (IntegerField): Custom field for query build 2.
        build3 (IntegerField): Custom field for query build 3.
        build4 (CharField): Custom field for query build 4.
        mQCode (UUIDField): Query code associated with the build.
        mQBCode (UUIDField): Build code associated with the query.
        record_modified (IntegerField): Timestamp or integer representing the last modification.
    """
    build1 = models.TextField()
    build2 = models.IntegerField()
    build3 = models.IntegerField()
    build4 = models.CharField(max_length=255)
    mQCode = models.UUIDField()
    mQBCode = models.UUIDField()
    record_modified = models.IntegerField()

    def __str__(self):
        return f"Build for {self.mQCode}"

# Pilot Model
class Pilot(BaseModel):
    """
    The Pilot model stores information about pilots.

    Fields:
        notes (TextField): Additional notes about the pilot.
        active (BooleanField): Indicates if the pilot is active.
        company (CharField): Company associated with the pilot.
        fav_list (BooleanField): Indicates if the pilot is in the favorite list.
        user_api (CharField): API key for the user.
        facebook (CharField): Facebook profile link.
        linkedin (CharField): LinkedIn profile link.
        pilot_ref (CharField): Reference identifier for the pilot.
        pilot_code (UUIDField): Unique code for the pilot.
        pilot_name (CharField): Name of the pilot.
        pilot_email (EmailField): Email address of the pilot.
        pilot_phone (CharField): Phone number of the pilot.
        certificate (CharField): Certificate associated with the pilot.
        phone_search (CharField): Phone search identifier.
        pilot_search (CharField): Pilot search identifier.
        roster_alias (CharField): Roster alias for the pilot.
        record_modified (IntegerField): Timestamp or integer representing the last modification.
    """
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    company = models.CharField(max_length=255, blank=True)
    fav_list = models.BooleanField(default=False)
    user_api = models.CharField(max_length=255, blank=True)
    facebook = models.CharField(max_length=255, blank=True)
    linkedin = models.CharField(max_length=255, blank=True)
    pilot_ref = models.CharField(max_length=255, blank=True)
    pilot_code = models.UUIDField(unique=True)
    pilot_name = models.CharField(max_length=255)
    pilot_email = models.EmailField(blank=True)
    pilot_phone = models.CharField(max_length=50, blank=True)
    certificate = models.CharField(max_length=255, blank=True)
    phone_search = models.CharField(max_length=255, blank=True)
    pilot_search = models.CharField(max_length=255, blank=True)
    roster_alias = models.CharField(max_length=255, blank=True)
    record_modified = models.IntegerField()

    def __str__(self):
        return f"Pilot {self.pilot_name} ({self.pilot_code})"

# Qualification Model
class Qualification(BaseModel):
    """
    The Qualification model stores information about qualifications.

    Fields:
        q_code (UUIDField): Unique code for the qualification.
        ref_extra (IntegerField): Reference to extra qualification details.
        ref_model (CharField): Reference model for the qualification.
        validity (IntegerField): Validity period of the qualification.
        date_valid (DateField): Expiration date of the qualification.
        q_type_code (IntegerField): Type code for the qualification.
        date_issued (DateField): Date when the qualification was issued.
        minimum_qty (IntegerField): Minimum quantity required for the qualification.
        notify_days (IntegerField): Number of days before notification.
        ref_airfield (UUIDField): Reference to the airfield for the qualification.
        minimum_period (IntegerField): Minimum period required for the qualification.
        notify_comment (TextField): Notification comment.
        record_modified (IntegerField): Timestamp or integer representing the last modification.
    """
    q_code = models.UUIDField(unique=True)
    ref_extra = models.IntegerField(default=0)
    ref_model = models.CharField(max_length=255, blank=True)
    validity = models.IntegerField(default=0)
    date_valid = models.DateField(null=True, blank=True)
    q_type_code = models.IntegerField(default=0)
    date_issued = models.DateField(null=True, blank=True)
    minimum_qty = models.IntegerField(default=0)
    notify_days = models.IntegerField(default=0)
    ref_airfield = models.UUIDField(default=uuid.uuid4)
    minimum_period = models.IntegerField(default=0)
    notify_comment = models.TextField(blank=True)
    record_modified = models.IntegerField()

    def __str__(self):
        return str(self.q_code)

# SettingConfig Model
class SettingConfig(BaseModel):
    """
    The SettingConfig model stores configuration settings.

    Fields:
        config_code (IntegerField): Unique code for the configuration setting.
        name (CharField): Name of the configuration setting.
        group (CharField): Group associated with the configuration setting.
        data (TextField): Data related to the configuration setting.
        record_modified (IntegerField): Timestamp or integer representing the last modification.
    """
    config_code = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    group = models.CharField(max_length=255)
    data = models.TextField(blank=True)
    record_modified = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.config_code})"

# Airfield Model
class Airfield(BaseModel):
    """
    The Airfield model stores information about airfields.

    Fields:
        af_code (CharField): Unique code for the airfield.
        af_iata (CharField): IATA code for the airfield.
        af_icao (CharField): ICAO code for the airfield.
        af_name (CharField): Name of the airfield.
        city (CharField): City where the airfield is located.
        af_cat (IntegerField): Category of the airfield.
        tz_code (IntegerField): Timezone code of the airfield.
        latitude (IntegerField): Latitude coordinate of the airfield.
        longitude (IntegerField): Longitude coordinate of the airfield.
        show_list (BooleanField): Indicates if the airfield should be shown in a list.
        user_edit (BooleanField): Indicates if the airfield details can be edited by users.
        af_country (IntegerField): Country code for the airfield.
        notes (TextField): Additional notes about the airfield.
        notes_user (TextField): User-specific notes about the airfield.
        region_user (IntegerField): Region code associated with the airfield.
        elevation_ft (IntegerField): Elevation of the airfield in feet.
        record_modified (IntegerField): Timestamp or integer representing the last modification.
    """
    af_code = models.CharField(max_length=255, unique=True)
    af_iata = models.CharField(max_length=10, blank=True)
    af_icao = models.CharField(max_length=10, blank=True)
    af_name = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    af_cat = models.IntegerField()
    tz_code = models.IntegerField()
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    show_list = models.BooleanField(default=False)
    user_edit = models.BooleanField(default=False)
    af_country = models.IntegerField()
    notes = models.TextField(blank=True)
    notes_user = models.TextField(blank=True)
    region_user = models.IntegerField()
    elevation_ft = models.IntegerField()
    record_modified = models.IntegerField()

    def __str__(self):
        return f"{self.af_name} ({self.af_code})"
