import random
from enum import Enum

class DeviceType(Enum):
    LIGHT = "light"
    THERMOSTAT = "thermostat"
    CAMERA = "camera"
    DOOR = "door"
    WINDOW = "window"
    FAN = "fan"

class DeviceStatus(Enum):
    ON = "ON"
    OFF = "OFF"

class SmartDevice:
    def __init__(self, device_id, device_type, room="Living Room"):
        self.device_id = device_id
        self.status = False
        self.device_type = device_type
        self.room = room
        self.color = "#cccccc"  # Default gray color
        self.status_color = {
            True: "#4CAF50",  # Green for ON
            False: "#F44336"   # Red for OFF
        }

    def toggle_status(self):
        self.status = not self.status
        return self.status
    
    def get_status_color(self):
        return self.status_color[self.status]
    
    def get_status_text(self):
        return "ON" if self.status else "OFF"
    
    def get_details(self):
        return f"{self.device_id} ({self.room}): {self.get_status_text()}"

class SmartLight(SmartDevice):
    def __init__(self, device_id, room="Living Room", color_temp=4000):
        super().__init__(device_id, DeviceType.LIGHT, room)
        self.brightness = 0
        self.color_temp = color_temp  # Color temperature in Kelvin (3000-6000)
        self.light_colors = {
            3000: "#FF9E80",  # Warm
            4000: "#FFECB3",  # Neutral
            5000: "#E3F2FD",  # Cool
            6000: "#E1F5FE"   # Daylight
        }
        self.update_light_color()

    def set_brightness(self, brightness):
        self.brightness = brightness
        if self.brightness > 0:
            self.status = True
        elif self.brightness == 0:
            self.status = False
    
    def set_color_temp(self, temp):
        self.color_temp = max(3000, min(6000, temp))
        self.update_light_color()
    
    def update_light_color(self):
        # Find the closest color temperature in our predefined colors
        closest_temp = min(self.light_colors.keys(), key=lambda x: abs(x - self.color_temp))
        self.color = self.light_colors[closest_temp]
    
    def get_details(self):
        if not self.status:
            return f"{self.device_id} ({self.room}): OFF"
        return f"{self.device_id} ({self.room}): {self.brightness}% - {self.color_temp}K"

class Thermostat(SmartDevice):
    def __init__(self, device_id, room="Living Room"):
        super().__init__(device_id, DeviceType.THERMOSTAT, room)
        self.temperature = 20
        self.target_temp = 20
        self.mode = "heat"  # heat, cool, auto
        self.humidity = 50  # Percentage
        self.temp_colors = {
            "cold": "#81D4FA",  # Light blue
            "cool": "#B3E5FC",  # Very light blue
            "neutral": "#E1F5FE",  # Almost white blue
            "warm": "#FFE0B2",  # Light orange
            "hot": "#FFCCBC"    # Light red
        }
        self.update_temp_color()

    def set_temperature(self, temperature):
        self.target_temp = temperature
        self.status = True
    
    def set_mode(self, mode):
        if mode in ["heat", "cool", "auto"]:
            self.mode = mode
    
    def update_temp_color(self):
        if self.temperature < 16:
            self.color = self.temp_colors["cold"]
        elif self.temperature < 19:
            self.color = self.temp_colors["cool"]
        elif self.temperature < 23:
            self.color = self.temp_colors["neutral"]
        elif self.temperature < 26:
            self.color = self.temp_colors["warm"]
        else:
            self.color = self.temp_colors["hot"]
    
    def update_current_temp(self):
        # Simulate temperature moving toward target
        if self.temperature < self.target_temp:
            self.temperature += 0.5
        elif self.temperature > self.target_temp:
            self.temperature -= 0.5
        self.update_temp_color()
    
    def get_details(self):
        if not self.status:
            return f"{self.device_id} ({self.room}): OFF"
        return f"{self.device_id} ({self.room}): {self.temperature}°C - Mode: {self.mode.capitalize()}"

class SecurityCamera(SmartDevice):
    def __init__(self, device_id, room="Front Door"):
        super().__init__(device_id, DeviceType.CAMERA, room)
        self.motion_detected = False
        self.recording = False
        self.battery_level = 100  # Percentage
        self.status_color = {
            True: "#4CAF50",  # Green for ON
            False: "#F44336"   # Red for OFF
        }
        self.motion_color = {
            True: "#FFC107",   # Amber for motion detected
            False: "#9E9E9E"   # Gray for no motion
        }

    def detect_motion(self, force_state=None):
        if force_state is not None:
            self.motion_detected = force_state
        else:
            self.motion_detected = random.choice([True, False])
        return self.motion_detected
    
    def start_recording(self):
        if self.status:
            self.recording = True
    
    def stop_recording(self):
        self.recording = False
    
    def get_motion_color(self):
        return self.motion_color[self.motion_detected]
    
    def get_details(self):
        if not self.status:
            return f"{self.device_id} ({self.room}): OFF"
        motion_status = "Motion Detected!" if self.motion_detected else "No Motion"
        recording_status = "Recording" if self.recording else "Standby"
        return f"{self.device_id} ({self.room}): {motion_status} - {recording_status} - Battery: {self.battery_level}%"

class SmartDoor(SmartDevice):
    def __init__(self, device_id, room="Front Door"):
        super().__init__(device_id, DeviceType.DOOR, room)
        self.locked = True
        self.door_open = False
        self.lock_color = {
            True: "#4CAF50",   # Green for locked
            False: "#F44336"   # Red for unlocked
        }
    
    def toggle_lock(self):
        self.locked = not self.locked
        return self.locked
    
    def open_door(self):
        if not self.locked:
            self.door_open = True
            return True
        return False
    
    def close_door(self):
        self.door_open = False
        return True
    
    def get_lock_color(self):
        return self.lock_color[self.locked]
    
    def get_details(self):
        if not self.status:
            return f"{self.device_id} ({self.room}): OFF"
        lock_status = "Locked" if self.locked else "Unlocked"
        door_status = "Open" if self.door_open else "Closed"
        return f"{self.device_id} ({self.room}): {door_status} - {lock_status}"

class SmartWindow(SmartDevice):
    def __init__(self, device_id, room="Living Room"):
        super().__init__(device_id, DeviceType.WINDOW, room)
        self.open_percentage = 0
        self.blinds_percentage = 0
        self.light_level = 50  # Percentage of outside light
    
    def set_open_percentage(self, percentage):
        self.open_percentage = max(0, min(100, percentage))
        if self.open_percentage > 0:
            self.status = True
        else:
            self.status = False
    
    def set_blinds_percentage(self, percentage):
        self.blinds_percentage = max(0, min(100, percentage))
        self.calculate_light_level()
    
    def calculate_light_level(self):
        # Light level is affected by both window opening and blinds
        self.light_level = (self.open_percentage * (100 - self.blinds_percentage)) / 100
    
    def get_details(self):
        if not self.status:
            return f"{self.device_id} ({self.room}): CLOSED"
        return f"{self.device_id} ({self.room}): {self.open_percentage}% Open - Blinds: {self.blinds_percentage}% - Light: {self.light_level}%"

class SmartFan(SmartDevice):
    def __init__(self, device_id, room="Living Room"):
        super().__init__(device_id, DeviceType.FAN, room)
        self.speed = 0  # 0-3 (0=off, 3=high)
        self.oscillating = False
        self.timer = 0  # Minutes until auto-off (0 = no timer)
    
    def set_speed(self, speed):
        self.speed = max(0, min(3, speed))
        if self.speed > 0:
            self.status = True
        else:
            self.status = False
    
    def toggle_oscillation(self):
        if self.status:
            self.oscillating = not self.oscillating
        return self.oscillating
    
    def set_timer(self, minutes):
        self.timer = max(0, minutes)
    
    def get_details(self):
        if not self.status or self.speed == 0:
            return f"{self.device_id} ({self.room}): OFF"
        
        speed_labels = {1: "Low", 2: "Medium", 3: "High"}
        osc_status = "Oscillating" if self.oscillating else "Fixed"
        timer_status = f"Timer: {self.timer}min" if self.timer > 0 else "No Timer"
        
        return f"{self.device_id} ({self.room}): {speed_labels[self.speed]} - {osc_status} - {timer_status}" 