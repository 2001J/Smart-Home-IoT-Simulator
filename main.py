#!/usr/bin/env python3
"""
Smart Home IoT Simulator
A Python-based application that simulates a smart home environment with various IoT devices,
automation rules, and a graphical user interface.
"""

import tkinter as tk
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Try to import PIL, but continue if not available
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.info("PIL not available. Some image features may not work.")

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from devices.smart_devices import (
    SmartLight, Thermostat, SecurityCamera, 
    SmartDoor, SmartWindow, SmartFan
)
from utils.automation import (
    AutomationSystem, create_motion_lighting_rule,
    create_temperature_control_rule, create_security_rule,
    create_energy_saving_rule, create_morning_routine_rule,
    create_evening_routine_rule
)
from ui.dashboard import Dashboard

def create_devices():
    """Create and return a list of smart devices for the simulation"""
    devices = [
        # Living Room
        SmartLight("Living Room Light", "Living Room", 4000),
        SmartLight("Living Room Lamp", "Living Room", 3000),
        Thermostat("Living Room Thermostat", "Living Room"),
        SmartWindow("Living Room Window", "Living Room"),
        SmartFan("Living Room Fan", "Living Room"),
        
        # Kitchen
        SmartLight("Kitchen Light", "Kitchen", 5000),
        SmartLight("Kitchen Counter Light", "Kitchen", 4500),
        Thermostat("Kitchen Thermostat", "Kitchen"),
        SmartWindow("Kitchen Window", "Kitchen"),
        
        # Bedroom
        SmartLight("Bedroom Light", "Bedroom", 3000),
        SmartLight("Bedroom Lamp", "Bedroom", 2700),
        Thermostat("Bedroom Thermostat", "Bedroom"),
        SmartWindow("Bedroom Window", "Bedroom"),
        SmartFan("Bedroom Fan", "Bedroom"),
        
        # Bathroom
        SmartLight("Bathroom Light", "Bathroom", 4000),
        SmartWindow("Bathroom Window", "Bathroom"),
        
        # Entrance
        SmartLight("Entrance Light", "Entrance", 4000),
        SecurityCamera("Front Door Camera", "Entrance"),
        SmartDoor("Front Door", "Entrance")
    ]
    
    return devices

def create_automation_system(devices):
    """Create and configure the automation system with devices and rules"""
    system = AutomationSystem()
    
    # Add all devices
    for device in devices:
        system.add_device(device)
    
    # Add automation rules
    system.add_rule(create_motion_lighting_rule())
    system.add_rule(create_temperature_control_rule(22))
    system.add_rule(create_security_rule())
    system.add_rule(create_energy_saving_rule())
    system.add_rule(create_morning_routine_rule(7))
    system.add_rule(create_evening_routine_rule(19))
    
    return system

def main():
    """Main function to run the Smart Home IoT Simulator"""
    # Create devices
    devices = create_devices()
    
    # Create automation system
    automation_system = create_automation_system(devices)
    
    # Create GUI
    root = tk.Tk()
    dashboard = Dashboard(root, automation_system)
    
    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main() 