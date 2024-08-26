import json
import os
from django.core.management.base import BaseCommand
from pilotlog.models import Aircraft, Flight  

class Command(BaseCommand):
    help = "Import data from JSON file into the database"

    def handle(self, *args, **kwargs):
        # Path to the JSON file (modify as needed)
        # json_file_path = os.path.join('required_resource', 'import-pilotlog_mcc.json')
        json_file_path = r'C:\Users\zd\Desktop\assignment\project_APEXIVE\pilotlog_project\required_resource\import - pilotlog_mcc.json'

        # Open and load the JSON data
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        # Iterate over each record in the JSON data
        for record in data:
            table_name = record['table'].lower()  # Convert table name to lowercase
            
            # Handle Aircraft table data
            if table_name == 'aircraft':
                self.import_aircraft(record)
                # Print progress
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {table_name} record: {record["guid"]}'))
                
            # Add other table handling here if necessary
            elif table_name == 'flight':
                self.import_flights(record)
                # Print progress
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {table_name} record: {record["guid"]}'))

    def import_flights(self, record):
        # Extract the meta data
        meta = record['meta']

        # Create or update the Flight record
        try:
            flight, created = Flight.objects.update_or_create(
                guid=record['guid'],
                defaults={
                    'user_id': record['user_id'],
                    'platform': record['platform'],
                    '_modified': record['_modified'],
                    'aircraft_id': meta.get('AircraftID', ''),
                    'from_airport': meta.get('From', ''),
                    'to_airport': meta.get('To', ''),
                    'route': meta.get('Route', ''),
                    'date': self.parse_date(meta.get('Date', None)),
                    'time_out': self.parse_time(meta.get('TimeOut', '')),
                    'time_off': self.parse_time(meta.get('TimeOff', '')),
                    'time_on': self.parse_time(meta.get('TimeOn', '')),
                    'time_in': self.parse_time(meta.get('TimeIn', '')),
                    'on_duty': self.parse_time(meta.get('OnDuty', '')),
                    'off_duty': self.parse_time(meta.get('OffDuty', '')),
                    'total_time': meta.get('TotalTime', 0),
                    'pic': meta.get('PIC', 0),
                    'sic': meta.get('SIC', 0),
                    'night': meta.get('Night', 0),
                    'solo': meta.get('Solo', 0),
                    'cross_country': meta.get('CrossCountry', 0),
                    'nvg': meta.get('NVG', 0),
                    'nvg_ops': meta.get('NVGOps', 0),
                    'distance': meta.get('Distance', 0),
                    'day_takeoffs': meta.get('DayTakeoffs', 0),
                    'day_landings_full_stop': meta.get('DayLandingsFullStop', 0),
                    'night_takeoffs': meta.get('NightTakeoffs', 0),
                    'night_landings_full_stop': meta.get('NightLandingsFullStop', 0),
                    'all_landings': meta.get('AllLandings', 0),
                    'actual_instrument': meta.get('ActualInstrument', 0),
                    'simulated_instrument': meta.get('SimulatedInstrument', 0),
                    'hobbs_start': meta.get('HobbsStart', 0),
                    'hobbs_end': meta.get('HobbsEnd', 0),
                    'tach_start': meta.get('TachStart', 0),
                    'tach_end': meta.get('TachEnd', 0),
                    'holds': meta.get('Holds', 0),
                    'approach1': meta.get('Approach1', ''),
                    'approach2': meta.get('Approach2', ''),
                    'approach3': meta.get('Approach3', ''),
                    'approach4': meta.get('Approach4', ''),
                    'approach5': meta.get('Approach5', ''),
                    'approach6': meta.get('Approach6', ''),
                    'dual_given': meta.get('DualGiven', 0),
                    'dual_received': meta.get('DualReceived', 0),
                    'simulated_flight': meta.get('SimulatedFlight', 0),
                    'ground_training': meta.get('GroundTraining', 0),
                    'instructor_name': meta.get('InstructorName', ''),
                    'instructor_comments': meta.get('InstructorComments', ''),
                    'pilot_comments': meta.get('PilotComments', '')
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created new Flight: {flight.guid}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated Flight: {flight.guid}'))
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(f'Error importing flight: {e}
        