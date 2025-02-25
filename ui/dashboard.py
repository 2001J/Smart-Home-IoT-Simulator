import tkinter as tk
from tkinter import ttk, font, messagebox
import time
from threading import Thread
import random
import os
import sys
import logging

# Try to import PIL, but continue if not available
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.info("PIL not available. Some image features may not work.")

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from devices.smart_devices import (
    SmartDevice, SmartLight, Thermostat, SecurityCamera, 
    SmartDoor, SmartWindow, SmartFan, DeviceType
)
from utils.automation import AutomationSystem

class ModernUI:
    """Class containing modern UI elements and styles"""
    
    # Color scheme
    COLORS = {
        "primary": "#2196F3",  # Blue
        "secondary": "#FF9800",  # Orange
        "success": "#4CAF50",  # Green
        "danger": "#F44336",  # Red
        "warning": "#FFC107",  # Amber
        "info": "#00BCD4",  # Cyan
        "light": "#F5F5F5",  # Light Gray
        "dark": "#212121",  # Dark Gray
        "white": "#FFFFFF",  # White
        "black": "#000000",  # Black
        "background": "#ECEFF1",  # Light Blue Gray
        "card": "#FFFFFF",  # White
        "text": "#212121",  # Darker text color for better contrast
        "sidebar_text": "#FFFFFF",  # White text for sidebar
        "border": "#CFD8DC",  # Light Blue Gray
    }
    
    # Font styles
    FONTS = {
        "title": ("Helvetica", 18, "bold"),
        "subtitle": ("Helvetica", 14, "bold"),
        "body": ("Helvetica", 12),
        "small": ("Helvetica", 10),
        "button": ("Helvetica", 12, "bold"),
    }
    
    @staticmethod
    def setup_styles():
        """Configure ttk styles for the application"""
        style = ttk.Style()
        
        # Configure the main window style
        style.configure("TFrame", background=ModernUI.COLORS["background"])
        style.configure("TLabel", background=ModernUI.COLORS["background"], foreground=ModernUI.COLORS["text"])
        style.configure("TButton", font=ModernUI.FONTS["button"])
        
        # Device card style - darker background for better contrast
        style.configure("Card.TFrame", background=ModernUI.COLORS["dark"], relief="raised", borderwidth=1)
        style.configure("Card.TLabel", background=ModernUI.COLORS["dark"], foreground=ModernUI.COLORS["white"])
        
        # Device list frame style
        style.configure("DeviceList.TFrame", background=ModernUI.COLORS["light"])
        style.configure("DeviceList.TLabel", background=ModernUI.COLORS["light"], foreground=ModernUI.COLORS["text"])
        
        # Device card content styles
        style.configure("CardContent.TFrame", background=ModernUI.COLORS["dark"])
        style.configure("CardContent.TLabel", background=ModernUI.COLORS["dark"], foreground=ModernUI.COLORS["white"])
        
        # Header style
        style.configure("Header.TFrame", background=ModernUI.COLORS["primary"])
        style.configure("Header.TLabel", background=ModernUI.COLORS["primary"], foreground=ModernUI.COLORS["white"], font=ModernUI.FONTS["title"])
        
        # Status indicators
        style.configure("Success.TLabel", foreground=ModernUI.COLORS["success"])
        style.configure("Danger.TLabel", foreground=ModernUI.COLORS["danger"])
        style.configure("Warning.TLabel", foreground=ModernUI.COLORS["warning"])
        style.configure("Info.TLabel", foreground=ModernUI.COLORS["info"])
        
        # Button styles
        style.configure("Primary.TButton", background=ModernUI.COLORS["primary"], foreground=ModernUI.COLORS["white"])
        style.configure("Success.TButton", background=ModernUI.COLORS["success"], foreground=ModernUI.COLORS["white"])
        style.configure("Danger.TButton", background=ModernUI.COLORS["danger"], foreground=ModernUI.COLORS["white"])
        
        # System status panel style
        style.configure("SystemStatus.TFrame", background=ModernUI.COLORS["dark"])
        style.configure("SystemStatus.TLabel", background=ModernUI.COLORS["dark"], foreground=ModernUI.COLORS["sidebar_text"], font=ModernUI.FONTS["body"])
        
        return style

class DeviceCard(ttk.Frame):
    """A card widget to display a single device"""
    
    def __init__(self, parent, device, dashboard, **kwargs):
        super().__init__(parent, style="Card.TFrame", padding=10, **kwargs)
        self.device = device
        self.dashboard = dashboard
        self.status_var = tk.StringVar(value="OFF")
        self.details_var = tk.StringVar(value="")
        
        # Card header with device name and type
        header_frame = ttk.Frame(self, style="CardContent.TFrame")
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Device icon (placeholder for now)
        self.icon_label = ttk.Label(header_frame, text="📱", font=("Helvetica", 16), style="CardContent.TLabel")
        self.icon_label.pack(side="left")
        
        # Device name and type
        name_frame = ttk.Frame(header_frame, style="CardContent.TFrame")
        name_frame.pack(side="left", padx=10, fill="x", expand=True)
        
        ttk.Label(name_frame, text=device.device_id, font=ModernUI.FONTS["subtitle"], style="CardContent.TLabel").pack(anchor="w")
        ttk.Label(name_frame, text=f"Room: {device.room}", font=ModernUI.FONTS["small"], style="CardContent.TLabel").pack(anchor="w")
        
        # Status indicator
        self.status_frame = ttk.Frame(self, style="CardContent.TFrame")
        self.status_frame.pack(fill="x", pady=5)
        
        # Use a custom style for the status label that inherits from CardContent.TLabel
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var, font=ModernUI.FONTS["body"], style="CardContent.TLabel")
        self.status_label.pack(side="left")
        
        self.details_label = ttk.Label(self.status_frame, textvariable=self.details_var, font=ModernUI.FONTS["small"], style="CardContent.TLabel")
        self.details_label.pack(side="right")
        
        # Controls frame
        self.controls_frame = ttk.Frame(self, style="CardContent.TFrame")
        self.controls_frame.pack(fill="x", pady=5)
        
        # Toggle button
        self.toggle_btn = ttk.Button(self.controls_frame, text="Turn ON", command=self.toggle_device)
        self.toggle_btn.pack(side="left", padx=5)
        
        # Create device-specific controls
        self.create_device_controls()
        
        # Initial update
        self.update_display()
    
    def create_device_controls(self):
        """Create controls specific to the device type"""
        if isinstance(self.device, SmartLight):
            self.create_light_controls()
            self.icon_label.configure(text="💡")
        elif isinstance(self.device, Thermostat):
            self.create_thermostat_controls()
            self.icon_label.configure(text="🌡️")
        elif isinstance(self.device, SecurityCamera):
            self.create_camera_controls()
            self.icon_label.configure(text="📹")
        elif isinstance(self.device, SmartDoor):
            self.create_door_controls()
            self.icon_label.configure(text="🚪")
        elif isinstance(self.device, SmartWindow):
            self.create_window_controls()
            self.icon_label.configure(text="🪟")
        elif isinstance(self.device, SmartFan):
            self.create_fan_controls()
            self.icon_label.configure(text="💨")
    
    def create_light_controls(self):
        """Create controls for a smart light"""
        # Brightness slider
        brightness_frame = ttk.Frame(self, style="CardContent.TFrame")
        brightness_frame.pack(fill="x", pady=5)
        
        ttk.Label(brightness_frame, text="Brightness:", style="CardContent.TLabel").pack(side="left")
        
        brightness_slider = ttk.Scale(
            brightness_frame, 
            from_=0, 
            to=100, 
            orient="horizontal",
            command=lambda v: self.device.set_brightness(int(float(v)))
        )
        brightness_slider.set(self.device.brightness)
        brightness_slider.pack(side="right", fill="x", expand=True, padx=5)
        
        # Color temperature slider
        color_temp_frame = ttk.Frame(self, style="CardContent.TFrame")
        color_temp_frame.pack(fill="x", pady=5)
        
        ttk.Label(color_temp_frame, text="Color:", style="CardContent.TLabel").pack(side="left")
        
        color_temp_slider = ttk.Scale(
            color_temp_frame, 
            from_=3000, 
            to=6000, 
            orient="horizontal",
            command=lambda v: self.device.set_color_temp(int(float(v)))
        )
        color_temp_slider.set(self.device.color_temp)
        color_temp_slider.pack(side="right", fill="x", expand=True, padx=5)
    
    def create_thermostat_controls(self):
        """Create controls for a thermostat"""
        # Temperature slider
        temp_frame = ttk.Frame(self, style="CardContent.TFrame")
        temp_frame.pack(fill="x", pady=5)
        
        ttk.Label(temp_frame, text="Temperature:", style="CardContent.TLabel").pack(side="left")
        
        temp_slider = ttk.Scale(
            temp_frame, 
            from_=10, 
            to=30, 
            orient="horizontal",
            command=lambda v: self.device.set_temperature(int(float(v)))
        )
        temp_slider.set(self.device.target_temp)
        temp_slider.pack(side="right", fill="x", expand=True, padx=5)
        
        # Mode selection
        mode_frame = ttk.Frame(self, style="CardContent.TFrame")
        mode_frame.pack(fill="x", pady=5)
        
        ttk.Label(mode_frame, text="Mode:", style="CardContent.TLabel").pack(side="left")
        
        mode_var = tk.StringVar(value=self.device.mode)
        
        def set_mode(mode):
            self.device.set_mode(mode)
            mode_var.set(mode)
        
        heat_btn = ttk.Button(mode_frame, text="Heat", command=lambda: set_mode("heat"))
        cool_btn = ttk.Button(mode_frame, text="Cool", command=lambda: set_mode("cool"))
        auto_btn = ttk.Button(mode_frame, text="Auto", command=lambda: set_mode("auto"))
        
        heat_btn.pack(side="left", padx=2)
        cool_btn.pack(side="left", padx=2)
        auto_btn.pack(side="left", padx=2)
    
    def create_camera_controls(self):
        """Create controls for a security camera"""
        # Motion detection
        motion_frame = ttk.Frame(self, style="CardContent.TFrame")
        motion_frame.pack(fill="x", pady=5)
        
        self.motion_var = tk.StringVar(value="No Motion")
        motion_label = ttk.Label(motion_frame, textvariable=self.motion_var, style="CardContent.TLabel")
        motion_label.pack(side="left")
        
        # Simulate motion button
        simulate_btn = ttk.Button(
            motion_frame, 
            text="Simulate Motion", 
            command=lambda: self.simulate_motion()
        )
        simulate_btn.pack(side="right")
        
        # Recording controls
        recording_frame = ttk.Frame(self, style="CardContent.TFrame")
        recording_frame.pack(fill="x", pady=5)
        
        self.recording_var = tk.StringVar(value="Not Recording")
        recording_label = ttk.Label(recording_frame, textvariable=self.recording_var, style="CardContent.TLabel")
        recording_label.pack(side="left")
        
        # Record button
        self.record_btn = ttk.Button(
            recording_frame, 
            text="Start Recording", 
            command=self.toggle_recording
        )
        self.record_btn.pack(side="right")
    
    def create_door_controls(self):
        """Create controls for a smart door"""
        # Lock controls
        lock_frame = ttk.Frame(self, style="CardContent.TFrame")
        lock_frame.pack(fill="x", pady=5)
        
        self.lock_var = tk.StringVar(value="Locked" if self.device.locked else "Unlocked")
        lock_label = ttk.Label(lock_frame, textvariable=self.lock_var, style="CardContent.TLabel")
        lock_label.pack(side="left")
        
        # Lock/unlock button
        self.lock_btn = ttk.Button(
            lock_frame, 
            text="Toggle Lock", 
            command=self.toggle_lock
        )
        self.lock_btn.pack(side="right")
        
        # Door open/close controls
        door_frame = ttk.Frame(self, style="CardContent.TFrame")
        door_frame.pack(fill="x", pady=5)
        
        self.door_var = tk.StringVar(value="Closed" if not self.device.door_open else "Open")
        door_label = ttk.Label(door_frame, textvariable=self.door_var, style="CardContent.TLabel")
        door_label.pack(side="left")
        
        # Open/close button
        self.door_btn = ttk.Button(
            door_frame, 
            text="Open Door" if not self.device.door_open else "Close Door", 
            command=self.toggle_door
        )
        self.door_btn.pack(side="right")
    
    def create_window_controls(self):
        """Create controls for a smart window"""
        # Window open percentage
        open_frame = ttk.Frame(self, style="CardContent.TFrame")
        open_frame.pack(fill="x", pady=5)
        
        ttk.Label(open_frame, text="Open:", style="CardContent.TLabel").pack(side="left")
        
        open_slider = ttk.Scale(
            open_frame, 
            from_=0, 
            to=100, 
            orient="horizontal",
            command=lambda v: self.device.set_open_percentage(int(float(v)))
        )
        open_slider.set(self.device.open_percentage)
        open_slider.pack(side="right", fill="x", expand=True, padx=5)
        
        # Blinds percentage
        blinds_frame = ttk.Frame(self, style="CardContent.TFrame")
        blinds_frame.pack(fill="x", pady=5)
        
        ttk.Label(blinds_frame, text="Blinds:", style="CardContent.TLabel").pack(side="left")
        
        blinds_slider = ttk.Scale(
            blinds_frame, 
            from_=0, 
            to=100, 
            orient="horizontal",
            command=lambda v: self.device.set_blinds_percentage(int(float(v)))
        )
        blinds_slider.set(self.device.blinds_percentage)
        blinds_slider.pack(side="right", fill="x", expand=True, padx=5)
    
    def create_fan_controls(self):
        """Create controls for a smart fan"""
        # Fan speed
        speed_frame = ttk.Frame(self, style="CardContent.TFrame")
        speed_frame.pack(fill="x", pady=5)
        
        ttk.Label(speed_frame, text="Speed:", style="CardContent.TLabel").pack(side="left")
        
        speed_var = tk.IntVar(value=self.device.speed)
        
        def set_speed(speed):
            self.device.set_speed(speed)
            speed_var.set(speed)
        
        speed_0 = ttk.Radiobutton(speed_frame, text="Off", variable=speed_var, value=0, command=lambda: set_speed(0))
        speed_1 = ttk.Radiobutton(speed_frame, text="Low", variable=speed_var, value=1, command=lambda: set_speed(1))
        speed_2 = ttk.Radiobutton(speed_frame, text="Med", variable=speed_var, value=2, command=lambda: set_speed(2))
        speed_3 = ttk.Radiobutton(speed_frame, text="High", variable=speed_var, value=3, command=lambda: set_speed(3))
        
        speed_0.pack(side="left")
        speed_1.pack(side="left")
        speed_2.pack(side="left")
        speed_3.pack(side="left")
        
        # Oscillation toggle
        osc_frame = ttk.Frame(self, style="CardContent.TFrame")
        osc_frame.pack(fill="x", pady=5)
        
        self.osc_var = tk.StringVar(value="Oscillating" if self.device.oscillating else "Fixed")
        osc_label = ttk.Label(osc_frame, textvariable=self.osc_var, style="CardContent.TLabel")
        osc_label.pack(side="left")
        
        # Oscillation button
        self.osc_btn = ttk.Button(
            osc_frame, 
            text="Toggle Oscillation", 
            command=self.toggle_oscillation
        )
        self.osc_btn.pack(side="right")
    
    def toggle_device(self):
        """Toggle the device on/off"""
        self.device.toggle_status()
        self.update_display()
    
    def simulate_motion(self):
        """Simulate motion detection for a camera"""
        if isinstance(self.device, SecurityCamera):
            self.device.detect_motion(True)
            self.update_display()
            
            # Schedule motion to turn off after 5 seconds
            self.after(5000, lambda: self.device.detect_motion(False))
            self.after(5000, self.update_display)
    
    def toggle_recording(self):
        """Toggle recording for a camera"""
        if isinstance(self.device, SecurityCamera):
            if self.device.recording:
                self.device.stop_recording()
                self.record_btn.configure(text="Start Recording")
            else:
                self.device.start_recording()
                self.record_btn.configure(text="Stop Recording")
            self.update_display()
    
    def toggle_lock(self):
        """Toggle lock for a door"""
        if isinstance(self.device, SmartDoor):
            self.device.toggle_lock()
            self.update_display()
    
    def toggle_door(self):
        """Toggle door open/closed"""
        if isinstance(self.device, SmartDoor):
            if self.device.door_open:
                self.device.close_door()
                self.door_btn.configure(text="Open Door")
            else:
                success = self.device.open_door()
                if not success:
                    messagebox.showwarning("Door Locked", "Cannot open door while it is locked.")
                else:
                    self.door_btn.configure(text="Close Door")
            self.update_display()
    
    def toggle_oscillation(self):
        """Toggle oscillation for a fan"""
        if isinstance(self.device, SmartFan):
            self.device.toggle_oscillation()
            self.update_display()
    
    def update_display(self):
        """Update the display with current device state"""
        # Update status
        status_text = "ON" if self.device.status else "OFF"
        self.status_var.set(f"Status: {status_text}")
        
        # Update toggle button text
        self.toggle_btn.configure(text=f"Turn {'OFF' if self.device.status else 'ON'}")
        
        # Update status label style - use foreground color directly instead of style
        if self.device.status:
            self.status_label.configure(foreground=ModernUI.COLORS["success"])
        else:
            self.status_label.configure(foreground=ModernUI.COLORS["danger"])
        
        # Update details
        self.details_var.set(self.device.get_details())
        
        # Device-specific updates
        if isinstance(self.device, SecurityCamera):
            motion_text = "Motion Detected!" if self.device.motion_detected else "No Motion"
            self.motion_var.set(motion_text)
            
            recording_text = "Recording" if self.device.recording else "Not Recording"
            self.recording_var.set(recording_text)
        
        elif isinstance(self.device, SmartDoor):
            lock_text = "Locked" if self.device.locked else "Unlocked"
            self.lock_var.set(lock_text)
            
            door_text = "Open" if self.device.door_open else "Closed"
            self.door_var.set(door_text)
        
        elif isinstance(self.device, SmartFan):
            osc_text = "Oscillating" if self.device.oscillating else "Fixed"
            self.osc_var.set(osc_text)

class AutomationPanel(ttk.Frame):
    """Panel to display and control automation rules"""
    
    def __init__(self, parent, automation_system, **kwargs):
        super().__init__(parent, style="SystemStatus.TFrame", padding=10, **kwargs)
        self.system = automation_system
        
        # Header
        ttk.Label(self, text="Automation Rules", font=ModernUI.FONTS["subtitle"], style="SystemStatus.TLabel").pack(anchor="w", pady=(0, 10))
        
        # Automation toggle
        self.automation_var = tk.StringVar(value=f"Automation: {'ON' if self.system.enabled else 'OFF'}")
        
        toggle_frame = ttk.Frame(self, style="SystemStatus.TFrame")
        toggle_frame.pack(fill="x", pady=5)
        
        ttk.Label(toggle_frame, textvariable=self.automation_var, font=ModernUI.FONTS["body"], style="SystemStatus.TLabel").pack(side="left")
        
        self.toggle_btn = ttk.Button(
            toggle_frame, 
            text="Disable" if self.system.enabled else "Enable",
            command=self.toggle_automation
        )
        self.toggle_btn.pack(side="right")
        
        # Rules list
        self.rules_frame = ttk.Frame(self, style="SystemStatus.TFrame")
        self.rules_frame.pack(fill="both", expand=True, pady=10)
        
        # Initial update
        self.update_rules()
    
    def toggle_automation(self):
        """Toggle the automation system on/off"""
        enabled = self.system.toggle()
        self.automation_var.set(f"Automation: {'ON' if enabled else 'OFF'}")
        self.toggle_btn.configure(text="Disable" if enabled else "Enable")
    
    def toggle_rule(self, rule):
        """Toggle a specific rule on/off"""
        rule.toggle()
        self.update_rules()
    
    def update_rules(self):
        """Update the rules display"""
        # Clear existing rules
        for widget in self.rules_frame.winfo_children():
            widget.destroy()
        
        # Add each rule
        for rule in self.system.rules:
            rule_frame = ttk.Frame(self.rules_frame, style="SystemStatus.TFrame")
            rule_frame.pack(fill="x", pady=2)
            
            # Rule status indicator
            status_color = ModernUI.COLORS["success"] if rule.enabled else ModernUI.COLORS["danger"]
            status_indicator = tk.Frame(rule_frame, width=10, height=10, bg=status_color)
            status_indicator.pack(side="left", padx=(0, 5))
            
            # Rule name - limit width to ensure buttons have enough space
            name_frame = ttk.Frame(rule_frame, style="SystemStatus.TFrame")
            name_frame.pack(side="left", fill="x", expand=True, padx=5)
            
            ttk.Label(name_frame, text=rule.name, font=ModernUI.FONTS["body"], style="SystemStatus.TLabel").pack(side="left")
            
            # Last triggered time
            if rule.last_triggered:
                time_diff = time.time() - rule.last_triggered
                if time_diff < 60:
                    time_text = "just now"
                elif time_diff < 3600:
                    time_text = f"{int(time_diff / 60)}m ago"
                else:
                    time_text = f"{int(time_diff / 3600)}h ago"
                
                ttk.Label(name_frame, text=f"Last: {time_text}", font=ModernUI.FONTS["small"], style="SystemStatus.TLabel").pack(side="left", padx=5)
            
            # Toggle button - fixed width to ensure consistent display
            toggle_btn = ttk.Button(
                rule_frame, 
                text="Disable" if rule.enabled else "Enable",
                command=lambda r=rule: self.toggle_rule(r),
                width=8  # Fixed width to ensure full text is visible
            )
            toggle_btn.pack(side="right", padx=(5, 0))

class Dashboard:
    """Main dashboard for the Smart Home IoT Simulator"""
    
    def __init__(self, root, system):
        self.root = root
        self.system = system
        self.setup_ui()
        
        # Start update thread
        self.update_thread = Thread(target=self.simulation_loop)
        self.update_thread.daemon = True
        self.update_thread.start()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Configure the window
        self.root.title("Smart Home IoT Simulator")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Set up styles
        self.style = ModernUI.setup_styles()
        
        # Main content frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = ttk.Frame(content_frame, style="Header.TFrame", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)  # Prevent shrinking
        
        ttk.Label(header_frame, text="Smart Home IoT Simulator", style="Header.TLabel").pack(side="left", padx=20, pady=10)
        
        # Devices section
        devices_frame = ttk.Frame(content_frame)
        devices_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Devices header with dark background for better visibility
        devices_header = ttk.Frame(devices_frame, style="SystemStatus.TFrame", height=40)
        devices_header.pack(fill="x", pady=(0, 10))
        devices_header.pack_propagate(False)  # Prevent shrinking
        
        ttk.Label(devices_header, text="Devices", style="SystemStatus.TLabel", font=ModernUI.FONTS["subtitle"]).pack(side="left", padx=20, pady=5)
        
        # Device cards container with scrolling
        devices_scroll_frame = ttk.Frame(devices_frame)
        devices_scroll_frame.pack(fill="both", expand=True)
        
        # Create a canvas with a light background color
        self.devices_canvas = tk.Canvas(
            devices_scroll_frame, 
            bg=ModernUI.COLORS["light"],  # Light background
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(devices_scroll_frame, orient="vertical", command=self.devices_canvas.yview)
        
        # Create a frame inside the canvas with the same background color
        self.devices_frame = ttk.Frame(self.devices_canvas)
        self.style.configure("DeviceList.TFrame", background=ModernUI.COLORS["light"])
        self.devices_frame.configure(style="DeviceList.TFrame")
        
        self.devices_frame.bind(
            "<Configure>",
            lambda e: self.devices_canvas.configure(scrollregion=self.devices_canvas.bbox("all"))
        )
        
        # Create the window in the canvas
        self.canvas_window = self.devices_canvas.create_window(
            (0, 0), 
            window=self.devices_frame, 
            anchor="nw", 
            width=devices_scroll_frame.winfo_width()
        )
        self.devices_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.devices_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Make sure the canvas resizes with the window
        self.root.bind("<Configure>", self.on_window_resize)
        
        # Create device cards
        self.create_device_cards()
        
        # Right sidebar with automation and status - increase width for better button display
        sidebar_frame = ttk.Frame(content_frame, width=350)
        sidebar_frame.pack(side="right", fill="y", padx=(10, 0))
        sidebar_frame.pack_propagate(False)  # Prevent shrinking
        
        # Automation panel
        self.automation_panel = AutomationPanel(sidebar_frame, self.system)
        self.automation_panel.pack(fill="x", pady=(0, 10))
        
        # Status panel
        status_frame = ttk.Frame(sidebar_frame, style="SystemStatus.TFrame", padding=10)
        status_frame.pack(fill="x")
        
        ttk.Label(status_frame, text="System Status", font=ModernUI.FONTS["subtitle"], style="SystemStatus.TLabel").pack(anchor="w", pady=(0, 10))
        
        # Status indicators
        self.status_vars = {
            "devices": tk.StringVar(value=f"Devices: {len(self.system.devices)}"),
            "active": tk.StringVar(value=f"Active: {sum(1 for d in self.system.devices if d.status)}"),
            "rules": tk.StringVar(value=f"Rules: {len(self.system.rules)}"),
            "last_update": tk.StringVar(value="Last update: Just now")
        }
        
        for key, var in self.status_vars.items():
            ttk.Label(status_frame, textvariable=var, font=ModernUI.FONTS["body"], style="SystemStatus.TLabel").pack(anchor="w", pady=2)
    
    def create_device_cards(self):
        """Create cards for each device"""
        # Clear existing cards
        for widget in self.devices_frame.winfo_children():
            widget.destroy()
        
        # Group devices by room
        rooms = {}
        for device in self.system.devices:
            if device.room not in rooms:
                rooms[device.room] = []
            rooms[device.room].append(device)
        
        # Create a section for each room
        for room, devices in rooms.items():
            # Room header with background
            room_frame = ttk.Frame(self.devices_frame, style="Card.TFrame")
            room_frame.pack(fill="x", pady=10, padx=10)
            
            ttk.Label(room_frame, text=room, font=ModernUI.FONTS["subtitle"], style="Card.TLabel").pack(anchor="w", padx=10, pady=5)
            
            # Container for device cards in this room
            for device in devices:
                # Create a card with padding and margin
                card_container = ttk.Frame(self.devices_frame, style="DeviceList.TFrame")
                card_container.pack(fill="x", pady=5, padx=10)
                
                card = DeviceCard(card_container, device, self)
                card.pack(fill="x", expand=True)
    
    def simulation_loop(self):
        """Background thread for simulation updates"""
        while True:
            if self.system.enabled:
                self.system.execute_rules()
                
                # Update thermostat temperatures
                for device in self.system.devices:
                    if isinstance(device, Thermostat) and device.status:
                        device.update_current_temp()
            
            # Update UI
            self.root.after(0, self.update_ui)
            
            # Update last update time
            self.root.after(0, lambda: self.status_vars["last_update"].set(f"Last update: Just now"))
            
            # Sleep for update interval
            time.sleep(2)
    
    def update_ui(self):
        """Update the UI with current device states"""
        # Update status indicators
        self.status_vars["active"].set(f"Active: {sum(1 for d in self.system.devices if d.status)}")
        
        # Update device cards
        for widget in self.devices_frame.winfo_children():
            if isinstance(widget, DeviceCard):
                widget.update_display()
        
        # Update automation panel
        self.automation_panel.update_rules()
    
    def on_window_resize(self, event):
        """Handle window resize events to adjust the canvas width"""
        # Only process events from the root window
        if event.widget == self.root:
            # Update the canvas width to match the frame
            canvas_width = self.devices_canvas.winfo_width()
            self.devices_canvas.itemconfig(self.canvas_window, width=canvas_width)
