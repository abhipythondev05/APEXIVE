# APEXIVE Project

## Overview

The APEXIVE project automates bulk data insertion into a Django application, managing various aspects like aircraft, flights, images, limits, queries, pilots, qualifications, settings, and airfields. This README provides instructions for setting up the project, running migrations, and importing data.

## Features

- **Bulk Data Insertion**: Efficiently handle large datasets.
- **Comprehensive Models**: Manage data related to aircraft, flights, images, limit rules, queries, pilots, qualifications, settings, and airfields.
- **Custom Import Commands**: Tailored commands for importing data.

## Prerequisites

- Python 3.10 or higher
- Django 5.0 or higher
- PostgreSQL (or compatible database system)
- Docker (for containerized deployment)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Arpit-zec/project_APEXIVE.git
   cd project_APEXIVE/pilotlog_project
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database**

   Update the `DATABASES` setting in `settings.py` with your database configuration.
   # Default it will use sqlite3

5. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

## Running the Application

1. **Start the Development Server**

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://127.0.0.1:8000/`.

## Data Import

1. **Prepare Your Data**

   Ensure data files are in the correct format and located in the `required_resource` directory. Also you need to change file name in file - pilotlog_project\pilotlog\management\commands\import_data.py
   --At line no. 29 (json_file_path = os.path.join(
                        settings.BASE_DIR, 'pilotlog', 'required_resource', 'import - pilotlog_mcc.json'
                    ))
    'import - pilotlog_mcc.json' with your file name
   # for sample it has import - pilotlog_mcc.json file

2. **Run the Import Command**

   ```bash
   python manage.py import_data
   ```

   This command processes data files and updates the database.

## Data Export

1. **Export Data to CSV**

   After importing the data, you can export it to a CSV file. The exported file will be saved in the `project_APEXIVE\pilotlog_project\pilotlog\required_resource\` directory.

   Run the export command:

   ```bash
   python manage.py export_data
   ```

   This command generates a CSV file based on the data in the database.

## Testing

Run tests using the following command:

```bash
python manage.py test
```

## Docker Deployment (Optional)

1. **Build the Docker Image**

   ```bash
   docker build -t apexive .
   ```

2. **Run the Docker Container**

   ```bash
   docker run -d -p 8000:8000 --name apexive apexive
   ```

   Access the application at `http://localhost:8000/`.

## Contributing

Contributions are welcome. Please:

- Fork the repository
- Create a new branch for your changes
- Submit a pull request with a clear description

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, contact arpit.s@zecdata.com.
