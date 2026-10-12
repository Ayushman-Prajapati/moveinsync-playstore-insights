\
from pipeline.analyze import classify_text

def test_gps_and_eta_detected():
    themes = classify_text("GPS tracking is slow and the arrival time is inaccurate")
    assert "gps_and_eta" in themes

def test_booking_and_no_show_detected():
    themes = classify_text("Booking was made for the wrong date and I was marked no-show")
    assert "booking_and_scheduling" in themes
    assert "transport_operations_and_safety" in themes

def test_ui_regression_detected():
    themes = classify_text("The UI is confusing and booking is now a two step process")
    assert "usability_and_ui" in themes
