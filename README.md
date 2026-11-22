\# CyberShield X – API Threat Detection and Incident Response Lab



CyberShield X is an educational cybersecurity project built using Python and FastAPI. It demonstrates API login monitoring, security event logging, repeated failed-login detection, and security alert generation through a dashboard.



\## Features



\- Demo login API

\- Successful and failed login event monitoring

\- Repeated failed-login detection

\- High-severity security alert generation

\- SQLite database integration

\- Security events and alerts APIs

\- Web-based security dashboard

\- API health-check endpoint



\## Technologies Used



\- Python

\- FastAPI

\- SQLite

\- Pydantic

\- HTML, CSS and JavaScript

\- Uvicorn



\## Project Structure



```text

CyberShield-X/

│

├── frontend/

│   └── index.html

│

├── main.py

├── database.py

├── requirements.txt

├── .gitignore

└── README.md

```



\## Installation and Setup



1\. Clone the repository:



```bash

git clone https://github.com/YOUR-USERNAME/CyberShield-X.git

cd CyberShield-X

```



2\. Create a virtual environment:



```bash

python -m venv .venv

```



3\. Activate the environment on Windows:



```bash

.venv\\Scripts\\activate

```



4\. Install dependencies:



```bash

pip install -r requirements.txt

```



5\. Start the application:



```bash

python -m uvicorn main:app --reload

```



6\. Open the application:



\- Dashboard: http://127.0.0.1:8000/

\- API Documentation: http://127.0.0.1:8000/docs

\- Health Check: http://127.0.0.1:8000/health



\## Demo Login



This project uses demo-only login credentials for educational testing.



\- Username: `student`

\- Password: `CyberShieldDemo123!`



Do not use these demo credentials for real accounts or production systems.



\## Disclaimer



CyberShield X is developed for educational and cybersecurity learning purposes. It is a local demonstration lab, not a production-ready security platform.



\## Author



CyberShield X – Cybersecurity Project
