from datetime import timedelta, datetime as dt
from time import sleep

class StopWatch:
    "A 'stopwatch' to store a time delay"
    def __init__(self, seconds):
        self.delay = seconds
        self.stop_time = self.time_in_n_seconds(seconds)

    @staticmethod
    def time_in_n_seconds(n):
        return dt.now() + timedelta(seconds=n)

    @property
    def time_is_up(self):
        return dt.now() >= self.stop_time

    @property
    def time_remaining(self):
        if self.time_is_up:
            return 0
        t_delta = (self.stop_time - dt.now())
        sec_part = t_delta.seconds
        microsec_part = t_delta.microseconds / 1e6
        return sec_part + microsec_part

    @property
    def stop_time(self):
        return self._stop_time

    @stop_time.setter
    def stop_time(self, val):
        self._stop_time = val

    def wait(self):
        if self.time_is_up:
            return
        else:
            sleep(self.time_remaining)
            return

    def __repr__(self):
        r = f"StopWatch timer for {self.delay} seconds"
        if self.time_is_up:
            r += " (time's up)"
        else:
            r += f" ({self.time_remaining} seconds left)"
        return r
