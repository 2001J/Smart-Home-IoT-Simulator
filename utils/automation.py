import time
from threading import Timer
from devices.smart_devices import SmartLight, SecurityCamera, Thermostat, SmartDoor, SmartWindow, SmartFan

class AutomationRule:
    def __init__(self, name, condition, action, enabled=True):
        self.name = name
        self.condition = condition
        self.action = action
        self.enabled = enabled
        self.last_triggered = None
    
    def apply(self, devices):
        if not self.enabled:
            return False
        
        if self.condition(devices):
            self.action(devices)
            self.last_triggered = time.time()
            return True
        return False
    
    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

class AutomationSystem:
    def __init__(self):
        self.devices = []
        self.rules = []
        self.enabled = True
        self.last_execution = time.time()
        self.motion_timer = None
    
    def add_device(self, device):
        self.devices.append(device)
    
    def remove_device(self, device_id):
        self.devices = [d for d in self.devices if d.device_id != device_id]
    
    def add_rule(self, rule):
        self.rules.append(rule)
    
    def remove_rule(self, rule_name):
        self.rules = [r for r in self.rules if r.name != rule_name]
    
    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled
    
    def execute_rules(self):
        if not self.enabled:
            return
        
        self.last_execution = time.time()
        for rule in self.rules:
            if rule.enabled:
                rule.apply(self.devices)
    
    def get_device_by_id(self, device_id):
        for device in self.devices:
            if device.device_id == device_id:
                return device
        return None
    
    def get_devices_by_type(self, device_type):
        return [d for d in self.devices if d.device_type == device_type]
    
    def get_devices_by_room(self, room):
        return [d for d in self.devices if d.room == room]

# Predefined automation rules
def create_motion_lighting_rule():
    """Create a rule that turns on lights when motion is detected"""
    def condition(devices):
        return any(isinstance(d, SecurityCamera) and d.status and d.motion_detected for d in devices)
    
    def action(devices):
        for device in devices:
            if isinstance(device, SmartLight):
                device.status = True
                device.set_brightness(100)
    
    return AutomationRule("Motion Lighting", condition, action)

def create_temperature_control_rule(target_temp=22):
    """Create a rule that adjusts thermostat based on target temperature"""
    def condition(devices):
        return any(isinstance(d, Thermostat) and d.status and abs(d.temperature - target_temp) > 1 for d in devices)
    
    def action(devices):
        for device in devices:
            if isinstance(device, Thermostat) and device.status:
                device.set_temperature(target_temp)
    
    return AutomationRule("Temperature Control", condition, action)

def create_security_rule():
    """Create a rule that locks doors when no motion is detected for a period"""
    def condition(devices):
        cameras = [d for d in devices if isinstance(d, SecurityCamera) and d.status]
        if not cameras:
            return False
        
        # Check if no motion detected on any camera
        return all(not camera.motion_detected for camera in cameras)
    
    def action(devices):
        for device in devices:
            if isinstance(device, SmartDoor) and device.status:
                device.locked = True
    
    return AutomationRule("Auto Lock", condition, action)

def create_energy_saving_rule():
    """Create a rule that turns off devices when not needed"""
    def condition(devices):
        # Check if no motion detected for a while
        cameras = [d for d in devices if isinstance(d, SecurityCamera) and d.status]
        if not cameras:
            return False
        
        no_motion = all(not camera.motion_detected for camera in cameras)
        return no_motion
    
    def action(devices):
        for device in devices:
            if isinstance(device, SmartLight) and device.status:
                device.set_brightness(0)
            elif isinstance(device, SmartFan) and device.status:
                device.set_speed(0)
    
    return AutomationRule("Energy Saving", condition, action)

def create_morning_routine_rule(morning_hour=7):
    """Create a rule that sets up the home in the morning"""
    def condition(devices):
        current_hour = time.localtime().tm_hour
        return current_hour == morning_hour
    
    def action(devices):
        for device in devices:
            if isinstance(device, SmartLight):
                device.status = True
                device.set_brightness(70)
                device.set_color_temp(5000)  # Daylight color temperature
            elif isinstance(device, Thermostat):
                device.status = True
                device.set_temperature(22)
            elif isinstance(device, SmartWindow):
                device.set_blinds_percentage(30)  # Open blinds partially
    
    return AutomationRule("Morning Routine", condition, action)

def create_evening_routine_rule(evening_hour=19):
    """Create a rule that sets up the home in the evening"""
    def condition(devices):
        current_hour = time.localtime().tm_hour
        return current_hour == evening_hour
    
    def action(devices):
        for device in devices:
            if isinstance(device, SmartLight):
                device.status = True
                device.set_brightness(50)
                device.set_color_temp(3000)  # Warm color temperature
            elif isinstance(device, Thermostat):
                device.status = True
                device.set_temperature(21)
            elif isinstance(device, SmartWindow):
                device.set_blinds_percentage(100)  # Close blinds completely
    
    return AutomationRule("Evening Routine", condition, action) 