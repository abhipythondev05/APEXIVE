import json
import os
import uuid
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.conf import settings
from django.core.management.base import BaseCommand
from pilotlog.models import *

class Command(BaseCommand):
    """
    A Django management command to import data from a JSON file into the database.
    The command handles multiple types of records, including Aircraft, Flight, ImagePic,
    LimitRules, MyQuery, and more, by mapping each record type to its corresponding
    import method.
    """

    help = "Import data from JSON file into the database"

    Table_Mapping = {
        'aircraft': "import_aircraft", 
        'flight': "import_flights",
        'imagepic': "import_imagepic",
        'limitrules': "import_limitrules",
        'myquery': "import_myquery",
        'myquerybuild': "import_myquerybuild",
        'pilot': "import_pilot",
        'qualification': "import_qualification",
        'settingconfig': "import_settingconfig",
        'airfield': "import_airfield"
    }

    def handle(self, *args, **kwargs):
        """
        Entry point for the command. This method reads the JSON file, parses the data,
        and directs each record to the appropriate import method based on the table name.
        """
        # Path to the JSON file (modify as needed)
        json_file_path = os.path.join(
            settings.BASE_DIR, 'pilotlog', 'required_resource', 'import - pilotlog_mcc.json'
        )
        self.stdout.write(self.style.SUCCESS("Successfully opened JSON file"))
        self.stdout.write(f"JSON file path: {json_file_path}")
        
        # Open and load the JSON data
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        # Iterate over each record in the JSON data
        for record in data:
            table_name = record['table'].lower()  # Convert table name to lowercase
            
            # Find and call the appropriate import method
            method_name = self.Table_Mapping.get(table_name)
            if method_name:
                method_to_call = getattr(self, method_name)
                method_to_call(record)
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {table_name} record: {record["guid"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'No import method for table: {table_name}'))

    def get_valid_date(self, value):
        """
        Convert date strings to date objects.
        
        Parameters:
            value (str): The date string to convert.
        
        Returns:
            date: The converted date object, or None if invalid.
        """
        if isinstance(value, str) and value:
            try:
                return datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(self.style.WARNING(f"Invalid date format for value: {value}. Skipping."))
        elif value is None or value == '':
            return None
        else:
            self.stdout.write(self.style.WARNING(f"Unexpected value type for date conversion: {type(value)}. Skipping."))
        return None

    def get_valid_decimal(self, value, default=0):
        """
        Convert value to Decimal if valid, otherwise return the default.
        
        Parameters:
            value (str): The value to convert to Decimal.
            default (Decimal): The default value to return if conversion fails.
        
        Returns:
            Decimal: The converted Decimal object, or the default value.
        """
        if value:
            try:
                return Decimal(value)
            except (InvalidOperation, ValueError) as e:
                self.stdout.write(self.style.WARNING(f"Invalid decimal value for {value}: {e}.  Using default value {default}."))
        return Decimal(default)

    def get_valid_integer(self, value):
        """
        Convert value to Integer if valid, otherwise return None.
        
        Parameters:
            value (str): The value to convert to Integer.
        
        Returns:
            int: The converted Integer object, or None if conversion fails.
        """
        if value:
            try:
                return int(value)
            except (ValueError, TypeError) as e:
                self.stdout.write(self.style.WARNING(f"Invalid integer value for {value}: {e}. Skipping."))
        return None

    def get_valid_time(self, value):
        """
        Convert time strings to integers.
        
        Parameters:
            value (str): The time string to convert.
        
        Returns:
            int: The converted integer time value, or None if invalid.
        """
        if isinstance(value, str) and value:
            try:
                return int(value)
            except ValueError:
                self.stdout.write(self.style.WARNING(f"Invalid time format for value: {value}. Skipping."))
        return None

    def validate_guid(self, guid):
        """
        Validate a GUID string to ensure it meets the expected format.
        
        Parameters:
            guid (str): The GUID string to validate.
        
        Returns:
            bool: True if the GUID is valid, False otherwise.
        """
        if guid and isinstance(guid, str) and len(guid) == 36:  # Example validation
            return True
        return False

    def import_aircraft(self, record):
        """
        Import Aircraft data from the provided record.
        
        Parameters:
            record (dict): A dictionary representing the Aircraft record to import.
        
        Returns:
            None
        """
        meta = record['meta']

        # Create or update the Aircraft record
        aircraft, created = Aircraft.objects.update_or_create(
            guid=uuid.UUID(record['guid']),
            defaults={
                'user_id': record['user_id'],
                'platform': record['platform'],
                '_modified': record['_modified'],
                'make': meta.get('Make', ''),
                'model': meta.get('Model', ''),
                'category': meta.get('Category', 0),
                'aircraft_class': meta.get('Class', 0),
                'power': meta.get('Power', 0),
                'seats': meta.get('Seats', 0),
                'active': meta.get('Active', False),
                'reference': meta.get('Reference', ''),
                'tailwheel': meta.get('Tailwheel', False),
                'complex': meta.get('Complex', False),
                'high_perf': meta.get('HighPerf', False),
                'aerobatic': meta.get('Aerobatic', False),
                'fnpt': meta.get('FNPT', 0),
                'kg5700': meta.get('Kg5700', False),
                'rating': meta.get('Rating', ''),
                'company': meta.get('Company', ''),
                'cond_log': meta.get('CondLog', 0),
                'fav_list': meta.get('FavList', False),
                'sub_model': meta.get('SubModel', ''),
                'record_modified': meta.get('Record_Modified', 0),
                'engyype' : meta.get('EngType', 0)
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created new Aircraft: {aircraft.reference}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated Aircraft: {aircraft.reference}'))

        # Assign the Aircraft to a Flight if a Flight record exists
        try:
            flight_instance = Flight.objects.get(guid=uuid.UUID(record['guid']))
            flight_instance.aircraft = aircraft
            flight_instance.save()
            self.stdout.write(self.style.SUCCESS(f'Assigned Aircraft to Flight: {flight_instance.guid}'))
        except Flight.DoesNotExist:
            self.stdout.write(self.style.WARNING(f'No Flight found with guid: {record.get("FlightGuid", "")}'))
            
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created new Aircraft: {aircraft.reference}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated Aircraft: {aircraft.reference}'))
            
    def import_flights(self, record):
        """
        Import Flight data from the provided record.
        
        Parameters:
            record (dict): A dictionary representing the Flight record to import.
        
        Returns:
            None
        """
        guid = record.get('guid')
        if not self.validate_guid(guid):
            self.stdout.write(self.style.ERROR(f'Invalid or missing GUID: {guid}'))
            return

        meta = record['meta']

        # Create or update the Flight record
        flight, created = Flight.objects.update_or_create(
            guid=uuid.UUID(guid),
            defaults={
                'user_id': record.get('user_id', 0),
                'platform': record.get('platform', 0),
                '_modified': record.get('_modified', 0),
                # 'aircraft_id': meta.get('AircraftCode', ''),
                'from_airport': meta.get('ArrCode', ''),  # Assuming 'ArrCode' as 'from_airport'
                'to_airport': meta.get('DepCode', ''),    # Assuming 'DepCode' as 'to_airport'
                'route': meta.get('Route', ''),
                'date': self.get_valid_date(meta.get('DateUTC', '')),
                'time_out': self.get_valid_time(meta.get('ArrTimeUTC', '')),
                'time_off': self.get_valid_time(meta.get('DepTimeUTC', '')),
                'time_on': self.get_valid_time(meta.get('LdgTimeUTC', '')),
                'time_in': self.get_valid_time(meta.get('ArrTimeUTC', '')),  # Consider replacing if another field is more appropriate
                'on_duty': self.get_valid_time(meta.get('ArrOffset', '')),
                'off_duty': self.get_valid_time(meta.get('DepOffset', '')),
                'total_time': self.get_valid_decimal(meta.get('minTOTAL', 0)),  # Based on available fields, `minTOTAL` seems closest
                'pic': self.get_valid_decimal(meta.get('minPIC', 0)),
                'sic': self.get_valid_decimal(meta.get('minCOP', 0)),  # Assuming 'minCOP' as 'SIC'
                'night': self.get_valid_decimal(meta.get('minNIGHT', 0)),
                'solo': self.get_valid_decimal(meta.get('minSFR', 0)),
                'cross_country': self.get_valid_decimal(meta.get('minXC', 0)),
                'nvg': self.get_valid_decimal(meta.get('minNIGHT', 0)),  # Assuming 'minNIGHT' for NVG, adjust if necessary
                'nvg_ops': self.get_valid_decimal(meta.get('minAIR', 0)),
                'distance': self.get_valid_decimal(meta.get('FuelUsed', 0)),  # No direct distance field found, 'FuelUsed' may be a placeholder
                'day_takeoffs': self.get_valid_integer(meta.get('ToDay', 0)),  # Assuming 'ToDay' might represent day takeoffs
                'day_landings_full_stop': self.get_valid_integer(meta.get('LdgDay', 0)),  # Assuming 'LdgDay' represents day landings full stop
                'night_takeoffs': self.get_valid_integer(meta.get('ToNight', 0)),  # Assuming 'ToNight' might represent night takeoffs
                'night_landings_full_stop': self.get_valid_integer(meta.get('LdgNight', 0)),
                'all_landings': self.get_valid_integer(meta.get('Holding', 0)),  # 'Holding' used as a placeholder, adjust if necessary
                'actual_instrument': self.get_valid_decimal(meta.get('minINSTR', 0)),
                'simulated_instrument': self.get_valid_decimal(meta.get('minIFR', 0)),  # No direct field for simulated instrument found
                'hobbs_start': self.get_valid_decimal(meta.get('HobbsIn', 0)),
                'hobbs_end': self.get_valid_decimal(meta.get('HobbsOut', 0)),
                'tach_start': self.get_valid_decimal(meta.get('ArrTimeSCHED', 0)),  # Placeholder for tach start
                'tach_end': self.get_valid_decimal(meta.get('DepTimeSCHED', 0)),    # Placeholder for tach end
                'holds': self.get_valid_integer(meta.get('Holding', 0)),
                'approach': meta.get('TagApproach', ''),
                'dual_given': self.get_valid_decimal(meta.get('minDUAL', 0)),
                'simulated_flight': self.get_valid_decimal(meta.get('minEXAM', 0)),  # Placeholder for simulated flight
                'ground_training': self.get_valid_decimal(meta.get('Training', 0)),
                'instructor_comments': meta.get('Remarks', ''),
                'pilot_comments': meta.get('Remarks', ''),
                'flight_review': meta.get('ToEdit', False),  # Using 'ToEdit' as a placeholder
                'checkride': meta.get('NextPage', False),
                'ipc': meta.get('UserBool', False),  # Assuming 'UserBool' for IPC status
                'nvg_proficiency': meta.get('PF', False)  # Assuming 'PF' represents NVG proficiency
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created new Flight: {flight.guid}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated Flight: {flight.guid}'))
            
    def import_imagepic(self, record):
        """Import ImagePic data."""
        guid = record.get('guid')
        if not self.validate_guid(guid):
            self.stdout.write(self.style.ERROR(f'Invalid or missing GUID: {guid}'))
            return
        meta = record['meta']
        
        # Create or update the ImagePic record
        imagepic, created = ImagePic.objects.update_or_create(
            guid=uuid.UUID(guid),
            img_code=meta['ImgCode'],
            defaults={
                'user_id': record['user_id'],
                'platform': record['platform'],
                '_modified': record['_modified'],
                'file_ext': meta.get('FileExt', ''),
                'file_name': meta.get('FileName', ''),
                'link_code': meta.get('LinkCode', ''),
                'img_upload': meta.get('Img_Upload', ''),
                'img_download': meta.get('Img_Download', ''),
                'record_modified': meta.get('Record_Modified', 0),
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created new ImagePic: {imagepic.img_code}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated ImagePic: {imagepic.img_code}'))

    def import_limitrules(self, record):
        """Import LimitRules data."""
        guid = record.get('guid')
        if not self.validate_guid(guid):
            self.stdout.write(self.style.ERROR(f'Invalid or missing GUID: {guid}'))
            return

        meta = record['meta']

        # Create or update the LimitRules record
        limitrules, created = LimitRules.objects.update_or_create(
            user_id=record.get('user_id', 0),
            limit_code=uuid.UUID(meta.get('LimitCode', '')),
            platform=record.get('platform', 0),
            defaults={
                'guid': uuid.UUID(guid),  
                '_modified': record.get('_modified', 0),
                'l_from': self.get_valid_date(meta.get('LFrom', '')),
                'l_to': self.get_valid_date(meta.get('LTo', '')),
                'l_type': meta.get('LType', 0),
                'l_zone': meta.get('LZone', 0),
                'l_minutes': meta.get('LMinutes', 0),
                'l_period_code': meta.get('LPeriodCode', 0),
                'record_modified': meta.get('Record_Modified', 0),
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created new LimitRules: {limitrules.limit_code}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated LimitRules: {limitrules.limit_code}'))

    def import_myquery(self, record):
        """Import MyQuery data."""
        guid = record.get('guid')
        if not self.validate_guid(guid):
            self.stdout.write(self.style.ERROR(f'Invalid or missing GUID: {guid}'))
            return

        meta = record['meta']

        # Create or update the Query record
        query, created = Query.objects.update_or_create(
            guid=uuid.UUID(guid),
            defaults={
                'name': meta.get('Name', ''),
                'mQCode': meta.get('mQCode', ''),
                'quick_view': meta.get('QuickView', False),
                'short_name': meta.get('ShortName', ''),
                'record_modified': meta.get('Record_Modified', 0),
                'user_id': record.get('user_id', 0),
                'platform': record.get('platform', 0),
                '_modified': record.get('_modified', 0),
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created new Query: {query.name}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated Query: {query.name}'))


    def import_myquerybuild(self, record):
        """Import MyQueryBuild data."""
        guid = record.get('guid')
        if not self.validate_guid(guid):
            self.stdout.write(self.style.ERROR(f'Invalid or missing GUID: {guid}'))
            return

        meta = record['meta']
        
        # Create or update the MyQueryBuild record
        myquerybuild, created = MyQueryBuild.objects.update_or_create(
            guid=uuid.UUID(guid),
            defaults={
                'user_id': record.get('user_id', 0),
                'platform': record.get('platform', 0),
                '_modified': record.get('_modified', 0),
                'build1': meta.get('Build1', ''),
                'build2': meta.get('Build2', 0),
                'build3': meta.get('Build3', 0),
                'build4': meta.get('Build4', ''),
                'mQCode': meta.get('mQCode', ''),
                'mQBCode': meta.get('mQBCode', ''),
                'record_modified': meta.get('Record_Modified', 0),
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created new MyQueryBuild: {myquerybuild.guid}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated MyQueryBuild: {myquerybuild.guid}'))

    def import_pilot(self, record):
        """Import Pilot data."""
        guid = record.get('guid')
        if not self.validate_guid(guid):
            self.stdout.write(self.style.ERROR(f'Invalid or missing GUID: {guid}'))
            return

        meta = record['meta']
        
        # Create or update the Pilot record
        pilot, created = Pilot.objects.update_or_create(
            guid=uuid.UUID(guid),
            defaults={
                'user_id': record.get('user_id', 0),
                'platform': record.get('platform', 0),
                '_modified': record.get('_modified', 0),
                'notes': meta.get('Notes', ''),
                'active': meta.get('Active', False),
                'company': meta.get('Company', ''),
                'fav_list': meta.get('FavList', False),
                'user_api': meta.get('UserAPI', ''),
                'facebook': meta.get('Facebook', ''),
                'linkedin': meta.get('LinkedIn', ''),
                'pilot_ref': meta.get('PilotRef', ''),
                'pilot_code': meta.get('PilotCode', ''),
                'pilot_name': meta.get('PilotName', ''),
                'pilot_email': meta.get('PilotEMail', ''),
                'pilot_phone': meta.get('PilotPhone', ''),
                'certificate': meta.get('Certificate', ''),
                'phone_search': meta.get('PhoneSearch', ''),
                'pilot_search': meta.get('PilotSearch', ''),
                'roster_alias': meta.get('RosterAlias', ''),
                'record_modified': meta.get('Record_Modified', 0),
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created new Pilot: {pilot.pilot_name.encode("ascii", "ignore").decode("ascii")}'))
            # self.stdout.write(self.style.SUCCESS(f'Created new Pilot: {pilot.pilot_name}'))
            # print(f'Created new Pilot: {pilot.pilot_name}')

        else:
            self.stdout.write(self.style.SUCCESS(f'Updated Pilot: {pilot.pilot_name.encode("ascii", "ignore").decode("ascii")}'))
            # self.stdout.write(self.style.SUCCESS(f'Updated Pilot: {pilot.pilot_name}'))
            # print(f'Updated Pilot: {pilot.pilot_name}')


    def import_qualification(self, record):
        """Import Qualification data."""
        guid = record.get('guid')
        if not self.validate_guid(guid):
            self.stdout.write(self.style.ERROR(f'Invalid or missing GUID: {guid}'))
            return

        meta = record['meta']
    
        # Create or update the Qualification record
        qualification, created = Qualification.objects.update_or_create(
            guid=uuid.UUID(guid),
            defaults={
                'user_id': record.get('user_id', 0),
                'platform': record.get('platform', 0),
                '_modified': record.get('_modified', 0),
                'q_code': uuid.UUID(meta.get('QCode')),
                'ref_extra': meta.get('RefExtra', 0),
                'ref_model': meta.get('RefModel', ''),
                'validity': meta.get('Validity', 0),
                'date_valid': self.get_valid_date(meta.get('DateValid', '')),
                'q_type_code': meta.get('QTypeCode', 0),
                'date_issued': self.get_valid_date(meta.get('DateIssued', '')),
                'minimum_qty': meta.get('MinimumQty', 0),
                'notify_days': meta.get('NotifyDays', 0),
                'ref_airfield': meta.get('RefAirfield', uuid.uuid4()),  # Default UUID if missing
                'minimum_period': meta.get('MinimumPeriod', 0),
                'notify_comment': meta.get('NotifyComment', ''),
                'record_modified': meta.get('Record_Modified', 0),
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created new Qualification: {qualification.guid}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated Qualification: {qualification.guid}'))


    def import_settingconfig(self, record):
        """Import SettingConfig data."""
        guid = record.get('guid')
        if isinstance(guid, str):
            if not self.validate_guid(guid):
                self.stdout.write(self.style.ERROR(f'Invalid or missing GUID: {guid}'))
                # If the guid is not a valid UUID, convert numeric string to UUID
                if guid.isdigit():
                    # Generate a UUID with the numeric value appended
                    base_uuid = uuid.UUID('00000000-0000-0000-0000-000000000000')
                    # Create UUID based on the numeric value
                    new_uuid = uuid.UUID(int=(base_uuid.int + int(guid)))
                    guid = str(new_uuid)
                    print(f"Created guid is : {guid}")
                else:
                    raise ValueError("Invalid GUID format")
        else:
            raise ValueError("GUID must be a string")

        meta = record['meta']

        # Create or update the SettingConfig record
        setting_config, created = SettingConfig.objects.update_or_create(
            guid=uuid.UUID(guid),
            defaults={
                'user_id': record.get('user_id', 0),
                'platform': record.get('platform', 0),
                'config_code': meta.get('ConfigCode', 0),
                '_modified': record.get('_modified', 0),
                'name': meta.get('Name', ''),
                'group': meta.get('Group', ''),
                'data': meta.get('Data', ''),
                'record_modified': meta.get('Record_Modified', 0),
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created new SettingConfig: {setting_config.guid}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated SettingConfig: {setting_config.guid}'))


    def import_airfield(self, record):
        """Import Airfield data."""
        try:
            guid = record.get('guid')
            if not self.validate_guid(guid):
                self.stdout.write(self.style.ERROR(f'Invalid or missing GUID: {guid}'))
                return
        except TypeError as e:
            print("Error occurred:", e)
        meta = record['meta']

        # Create or update the Airfield record
        airfield, created = Airfield.objects.update_or_create(
            guid=uuid.UUID(guid),
            defaults={
                'user_id': record.get('user_id', 0),
                'platform': record.get('platform', 0),
                '_modified': record.get('_modified', 0),
                'af_code': meta.get('AFCode', ''),
                'af_iata': meta.get('AFIATA', ''),
                'af_icao': meta.get('AFICAO', ''),
                'af_name': meta.get('AFName', ''),
                'city': meta.get('City', ''),
                'af_cat': meta.get('AFCat', 0),
                'tz_code': meta.get('TZCode', 0),
                'latitude': meta.get('Latitude', 0),
                'longitude': meta.get('Longitude', 0),
                'show_list': meta.get('ShowList', False),
                'user_edit': meta.get('UserEdit', False),
                'af_country': meta.get('AFCountry', 0),
                'notes': meta.get('Notes', ''),
                'notes_user': meta.get('NotesUser', ''),
                'region_user': meta.get('RegionUser', 0),
                'elevation_ft': meta.get('ElevationFT', 0),
                'record_modified': meta.get('Record_Modified', 0),
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created new Airfield: {airfield.guid}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated Airfield: {airfield.guid}'))
