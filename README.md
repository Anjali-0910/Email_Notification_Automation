# Email Notification Automation (Azure)

Run the UI locally (no Azure needed):

    python server.py        # then open http://localhost:8000

Test the logic only:

    python email_logic.py

Folders: `ui/` the web page, `sample_events/` test events, `email_template.html` the email layout.
Next steps (after Azure access): Azure Function (HTTP + Event Grid + Timer triggers) and Communication Services sending.