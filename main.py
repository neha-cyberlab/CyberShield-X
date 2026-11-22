from fastapi.responses import FileResponse
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from database import get_connection, init_db


app = FastAPI(
    title="CyberShield X",
    description="Custom API Threat Detection and Incident Response Lab",
    version="1.0.0",
)

# CORS configuration for local frontend testing.
# Use a restricted origin list before production deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

MAX_FAILED_ATTEMPTS = 3


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=100)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "CyberShield X API",
    }


@app.post("/login")
def demo_login(request: LoginRequest):
    username = request.username.strip()

    # Demo credentials for this local educational lab only.
    success = (
        username == "student"
        and request.password == "CyberShieldDemo123!"
    )

    timestamp = datetime.now(timezone.utc).isoformat()
    event_type = "login_success" if success else "login_failure"
    severity = "LOW" if success else "MEDIUM"

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO security_events
                (timestamp, event_type, username, severity)
            VALUES (?, ?, ?, ?)
            """,
            (timestamp, event_type, username, severity),
        )

        event_id = connection.execute(
            "SELECT last_insert_rowid()"
        ).fetchone()[0]

        event = {
            "event_id": event_id,
            "timestamp": timestamp,
            "event_type": event_type,
            "username": username,
            "severity": severity,
        }

        if success:
            return {
                "message": "Demo login successful",
                "success": True,
                "event": event,
            }

        row = connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM security_events
            WHERE username = ?
              AND event_type = 'login_failure'
            """,
            (username,),
        ).fetchone()

        attempts = row["total"]

        if attempts >= MAX_FAILED_ATTEMPTS:
            alert_timestamp = datetime.now(
                timezone.utc
            ).isoformat()

            existing = connection.execute(
                """
                SELECT alert_id
                FROM security_alerts
                WHERE username = ?
                  AND alert_type = 'repeated_failed_logins'
                ORDER BY alert_id DESC
                LIMIT 1
                """,
                (username,),
            ).fetchone()

            if existing is None:
                connection.execute(
                    """
                    INSERT INTO security_alerts
                        (timestamp, alert_type, username, severity,
                         failed_attempts, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        alert_timestamp,
                        "repeated_failed_logins",
                        username,
                        "HIGH",
                        attempts,
                        "Repeated failed demo login attempts detected",
                    ),
                )
            else:
                connection.execute(
                    """
                    UPDATE security_alerts
                    SET timestamp = ?, failed_attempts = ?
                    WHERE alert_id = ?
                    """,
                    (
                        alert_timestamp,
                        attempts,
                        existing["alert_id"],
                    ),
                )

        return {
            "message": "Invalid demo credentials",
            "success": False,
            "failed_attempts": attempts,
            "event": event,
        }


@app.get("/security/events")
def get_security_events():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT event_id, timestamp, event_type, username, severity
            FROM security_events
            ORDER BY event_id
            """
        ).fetchall()

    events = [dict(row) for row in rows]

    return {
        "total": len(events),
        "events": events,
    }


@app.get("/security/alerts")
def get_security_alerts():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT alert_id, timestamp, alert_type, username,
                   severity, failed_attempts, description
            FROM security_alerts
            ORDER BY alert_id
            """
        ).fetchall()

    alerts = [dict(row) for row in rows]

    return {
        "total": len(alerts),
        "alerts": alerts,
    }


@app.get("/security/dashboard")
def get_security_dashboard():
    with get_connection() as connection:
        total_events = connection.execute(
            "SELECT COUNT(*) FROM security_events"
        ).fetchone()[0]

        failed_logins = connection.execute(
            """
            SELECT COUNT(*)
            FROM security_events
            WHERE event_type = 'login_failure'
            """
        ).fetchone()[0]

        successful_logins = connection.execute(
            """
            SELECT COUNT(*)
            FROM security_events
            WHERE event_type = 'login_success'
            """
        ).fetchone()[0]

        high_severity_alerts = connection.execute(
            """
            SELECT COUNT(*)
            FROM security_alerts
            WHERE severity = 'HIGH'
            """
        ).fetchone()[0]

    return {
        "project": "CyberShield X",
        "total_events": total_events,
        "failed_logins": failed_logins,
        "successful_logins": successful_logins,
        "high_severity_alerts": high_severity_alerts,
    }
