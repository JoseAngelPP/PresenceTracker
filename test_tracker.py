import sys

from io import StringIO
from datetime import datetime
from .PresenceTracker import PresenceTracker


class TestPresenceTracker:
    def setup_method(self):
        self.tracker = PresenceTracker()

    def test_process_presence(self):
        self.tracker.process_presence("Marco", "09:00", "10:00")
        assert self.tracker.students["Marco"]["time"].total_seconds() == 3600
        assert self.tracker.students["Marco"]["days"] == 1

    def test_validate_date_format(self):
        assert self.tracker.validate_datetime_format("09:30", "%H:%M") == datetime(
            1900, 1, 1, 9, 30
        )

    def test_calculate_total_minutes(self):
        start_time = self.tracker.validate_datetime_format("01:30", "%H:%M")
        end_time = self.tracker.validate_datetime_format("02:30", "%H:%M")
        duration = end_time - start_time
        total_minutes = self.tracker.calculate_total_minutes(duration)

        assert total_minutes == 60

    def test_get_attendance(self, monkeypatch):
        input_data = "Student Angel\nPresence Angel 1 08:00 12:00\n"

        # Simular la entrada de consola
        monkeypatch.setattr("sys.argv", ["test.py", "test.txt"])
        # Simular la apertura del archivo
        monkeypatch.setattr(
            "builtins.open", lambda *args, **kwargs: StringIO(input_data)
        )
        monkeypatch.setattr("sys.stdout", StringIO())

        self.tracker.get_attendance()

        output = sys.stdout.getvalue()
        expected_output = "Angel: 240 minutes in 1 days\n"
        assert output == expected_output
