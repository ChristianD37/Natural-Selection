import time

class FPS():
    def __init__(self):
        self.previous_time = time.time()
        self.times_taken = []
        self.fps = 0

    def elapsed_time(self):
        now = time.time()
        elapsed_time = now - self.previous_time
        self.previous_time = now
        self.times_taken.append(elapsed_time)
        return elapsed_time

    def get_fps(self):
        self.times_taken = self.times_taken[-500:]
        fps = len(self.times_taken) / sum(self.times_taken)
        return fps

    def get_delta_time(self, target_fps):
        elapsed_time  = self.elapsed_time()
        if elapsed_time == 0: elapsed_time = 1
        return  elapsed_time* target_fps

    def cap_fps(self, cap,elapsed_time):
        delay = max(1.0 / cap - elapsed_time, 0)
        self.fps = 1 / (elapsed_time + delay)
        time.sleep(delay)
