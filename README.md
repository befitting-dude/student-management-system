 Student Management System

A modular Python command-line application for managing student records with file-based storage.

## Features

- Admin login authentication
- Add, update, delete, and search student records
- Store records in both JSON and CSV formats
- Sort students by name or marks
- Generate reports like topper, average marks, pass count, and fail count
- Validate inputs and handle invalid operations with custom exceptions

## Project Structure

```text
.
|-- main.py
|-- sms/
|   |-- app.py
|   |-- auth.py
|   |-- exceptions.py
|   |-- models.py
|   |-- reports.py
|   |-- service.py
|   |-- storage.py
|   `-- utils.py
|-- data/
|   |-- admin.json
|   |-- students.csv
|   `-- students.json
`-- README.md
```

## Requirements

- Python 3.10 or later

## Run

```bash
python main.py
```

## Default Login

- Username: `admin`
- Password: `admin123`

## Modules

- `sms/app.py` manages the CLI flow and menu handling
- `sms/auth.py` handles admin authentication with hashed passwords
- `sms/storage.py` loads and saves records in JSON and CSV
- `sms/service.py` contains add, update, delete, search, and sort logic
- `sms/reports.py` generates student performance summaries
- `sms/utils.py` validates student input values
- `sms/exceptions.py` defines application-specific exceptions