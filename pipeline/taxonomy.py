\
"""Transparent keyword-based theme taxonomy; treat labels as suggestions requiring review."""
THEMES = {
    "booking_and_scheduling": [
        "booking", "booked", "book", "schedule", "date", "shuttle", "cancel",
        "no show", "no-show", "waitlist", "waitlisted", "trip created"
    ],
    "gps_and_eta": [
        "gps", "tracking", "location", "eta", "arrival time", "pickup time",
        "drop timing", "live location", "driver location"
    ],
    "notifications_and_checkin": [
        "notification", "notifications", "check in", "check-in", "checkin",
        "remind", "alert", "not received", "delayed"
    ],
    "login_and_stability": [
        "login", "log in", "otp", "crash", "crashes", "freeze", "freezes",
        "loading", "doesn't open", "cannot open", "can't open"
    ],
    "usability_and_ui": [
        "ui", "user interface", "confusing", "difficult to use", "two step",
        "2 step", "one step", "2-step", "redesign", "layout", "unnecessary steps"
    ],
    "transport_operations_and_safety": [
        "late cab", "cab late", "driver", "route", "safety", "no show",
        "no-show", "missed cab", "missed pickup", "salary", "transport desk"
    ],
    "support_and_communication": [
        "support", "helpdesk", "help desk", "response", "complaint", "ticket"
    ],
}

OWNER_MAP = {
    "booking_and_scheduling": "Product + Booking Backend",
    "gps_and_eta": "Mobile + Location/Dispatch Backend",
    "notifications_and_checkin": "Mobile + Notifications Backend",
    "login_and_stability": "Mobile + Identity/Platform",
    "usability_and_ui": "Product + Mobile + QA",
    "transport_operations_and_safety": "Transport Operations + Customer Support",
    "support_and_communication": "Customer Support + Operations",
}

SEVERITY_MAP = {
    "booking_and_scheduling": 5,
    "gps_and_eta": 4,
    "notifications_and_checkin": 4,
    "login_and_stability": 4,
    "usability_and_ui": 3,
    "transport_operations_and_safety": 5,
    "support_and_communication": 2,
}
