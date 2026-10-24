import html
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_RECIPIENT = "placeholder@example.com"
TEMPLATE_PATH = Path(__file__).parent / "email_template.html"


def load_template(path=TEMPLATE_PATH):
    return Path(path).read_text(encoding="utf-8")


def fill_template(template, values):
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", html.escape(str(value)))
    return template


def build_email(event):
    """Turn an event (dict) into {to, subject, html}. Logs ERROR and re-raises on failure."""
    try:
        config = event.get("emailConfig", {})
        recipient = config.get("recipient", DEFAULT_RECIPIENT)
        subject = config.get("subject", "Notification")
        if event.get("priority") in ("high", "critical"):
            subject = "[URGENT] " + subject
        values = {
            "subject": subject,
            "title": event.get("title", "Notification"),
            "message": event.get("message", ""),
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "source": event.get("source", "custom.application"),
        }
        return {"to": recipient, "subject": subject,
                "html": fill_template(load_template(), values),
                "usedDefaultRecipient": "recipient" not in config}
    except Exception as error:
        logging.error("ERROR building email: %s", error)
        raise


if __name__ == "__main__":
    for name in ("normal", "priority", "bad", "daily_report"):
        event = json.loads(Path(__file__).parent.joinpath("sample_events", name + ".json").read_text())
        mail = build_email(event)
        print(name, "->", mail["to"], "|", mail["subject"])