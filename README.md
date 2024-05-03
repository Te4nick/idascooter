# Scooter Control System
## Development
- Clone repo:
  ```bash
  git clone <link>
  ```
- cd to cloned project:
  ```bash
  cd idascooter
  ```
- Set up virtual environment:
  ```bash
  python -m venv .venv
  ```
- Activate virtual environment:
  
  Unix:
  ```bash
  ./.venv/Scripts/activate
  ```
  Windows:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- Install project:
  ```bash
  pip install .
  ```
- Run django development server:
  ```bash
  python manage.py runserver
  ```
- Run all tests:
  ```bash
  python manage.py test
  ```
- Run unit tests:
  ```bash
  python manage.py test scooter_control/tests/unit_tests
  ```
- Run component tests:
  ```bash
  python manage.py test scooter_control/tests/component_tests
  ```
