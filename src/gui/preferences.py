import tkinter as tk
from tkinter import ttk

class ExamPreferences:
    """Stores and validates user preferences for exam monitoring"""
    def __init__(self):
        self.preferred_days = []  # e.g., ["Monday", "Wednesday"]
        self.preferred_times = []  # e.g., ["Morning", "Afternoon"]
        self.preferred_duration = None  # e.g., "2 hours"
        self.notify_only = True  # Default to notification-only mode

    def matches_preferences(self, session_info):
        """Check if a session matches user preferences"""
        if not (self.preferred_days or self.preferred_times or self.preferred_duration):
            return True  # If no preferences set, accept any session
            
        # Parse session_info and check against preferences
        matches_day = not self.preferred_days or session_info['day'] in self.preferred_days
        matches_time = not self.preferred_times or session_info['time_slot'] in self.preferred_times
        matches_duration = not self.preferred_duration or session_info['duration'] == self.preferred_duration
        
        return matches_day and matches_time and matches_duration

class PreferencesDialog:
    """Dialog for setting exam preferences"""
    def __init__(self, parent, preferences):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Exam Preferences")
        self.dialog.geometry("400x500")
        self.preferences = preferences
        self.setup_dialog()

    def setup_dialog(self):
        # Days Frame
        days_frame = ttk.LabelFrame(self.dialog, text="Preferred Days", padding=10)
        days_frame.pack(fill="x", padx=10, pady=5)
        
        self.day_vars = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for day in days:
            var = tk.BooleanVar(value=day in self.preferences.preferred_days)
            self.day_vars[day] = var
            ttk.Checkbutton(days_frame, text=day, variable=var).pack(anchor="w")

        # Times Frame
        times_frame = ttk.LabelFrame(self.dialog, text="Preferred Times", padding=10)
        times_frame.pack(fill="x", padx=10, pady=5)
        
        self.time_vars = {}
        times = ["Morning", "Afternoon", "Evening"]
        for time in times:
            var = tk.BooleanVar(value=time in self.preferences.preferred_times)
            self.time_vars[time] = var
            ttk.Checkbutton(times_frame, text=time, variable=var).pack(anchor="w")

        # Duration Frame
        duration_frame = ttk.LabelFrame(self.dialog, text="Exam Duration", padding=10)
        duration_frame.pack(fill="x", padx=10, pady=5)
        
        self.duration_var = tk.StringVar(value=self.preferences.preferred_duration or "Any")
        durations = ["Any", "1 hour", "2 hours", "3 hours"]
        ttk.Combobox(duration_frame, textvariable=self.duration_var, values=durations).pack(fill="x")

        # Mode Frame
        mode_frame = ttk.LabelFrame(self.dialog, text="Monitoring Mode", padding=10)
        mode_frame.pack(fill="x", padx=10, pady=5)
        
        self.notify_only_var = tk.BooleanVar(value=self.preferences.notify_only)
        ttk.Radiobutton(mode_frame, text="Notify Only", variable=self.notify_only_var, value=True).pack(anchor="w")
        ttk.Radiobutton(mode_frame, text="Notify and Show Available Sessions", variable=self.notify_only_var, value=False).pack(anchor="w")

        # Save Button
        ttk.Button(self.dialog, text="Save Preferences", command=self.save_preferences).pack(pady=10)

    def save_preferences(self):
        self.preferences.preferred_days = [day for day, var in self.day_vars.items() if var.get()]
        self.preferences.preferred_times = [time for time, var in self.time_vars.items() if var.get()]
        self.preferences.preferred_duration = None if self.duration_var.get() == "Any" else self.duration_var.get()
        self.preferences.notify_only = self.notify_only_var.get()
        self.dialog.destroy()