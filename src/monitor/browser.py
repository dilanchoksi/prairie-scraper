from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import ttk
import threading
import time
import os
import platform
import logging
from datetime import datetime
from src.gui.theme import ModernTheme
from src.gui.preferences import ExamPreferences, PreferencesDialog

class PrairieTestMonitor:
    def __init__(self):
        self.setup_logging()
        logging.info("Initializing PrairieTest Monitor...")
        
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        
        # Initialize monitoring variables
        self.driver = None
        self.monitoring = False
        self.monitor_thread = None
        self.last_check_time = None
        self.notification_sound = None
        self.preferences = ExamPreferences()
        
        # Configuration
        self.refresh_interval = 10  # seconds
        self.setup_notification_sound()
        
        logging.info("Application initialization complete")

    def setup_logging(self):
        """Configure logging with timestamps and levels"""
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(f'logs/monitor_{datetime.now().strftime("%Y%m%d")}.log'),
                logging.StreamHandler()
            ]
        )

    def setup_window(self):
        """Configure the main window properties"""
        self.root.title("PrairieTest Availability Monitor")
        self.root.geometry("500x400")
        self.root.configure(bg=ModernTheme.BG_COLOR)
        
        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 400) // 2
        self.root.geometry(f"500x400+{x}+{y}")
        
        # Make window resizable
        self.root.minsize(400, 300)

    def setup_styles(self):
        """Configure custom styles for widgets"""
        ModernTheme.configure_styles()

    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.root, style='Custom.TFrame')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Status frame
        status_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        status_frame.pack(fill='x', pady=(0, 20))
        
        # Status label
        self.status_label = ttk.Label(
            status_frame,
            text="Ready to start monitoring",
            style='Status.TLabel',
            wraplength=460,
            justify='center'
        )
        self.status_label.pack(pady=10)
        
        # Last check time label
        self.last_check_label = ttk.Label(
            status_frame,
            text="Last check: Never",
            style='Status.TLabel'
        )
        self.last_check_label.pack(pady=5)
        
        # Button frame
        button_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        button_frame.pack(pady=10)
        
        # Start button
        self.start_button = ttk.Button(
            button_frame,
            text="Start Monitoring",
            command=self.start_monitoring,
            style='Primary.TButton',
            width=20
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        # Stop button
        self.stop_button = ttk.Button(
            button_frame,
            text="Stop",
            command=self.stop_monitoring,
            style='Stop.TButton',
            width=20,
            state="disabled"
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        # Preferences button
        self.preferences_button = ttk.Button(
            button_frame,
            text="Set Preferences",
            command=self.show_preferences,
            style='Primary.TButton',
            width=20
        )
        self.preferences_button.pack(side=tk.LEFT, padx=10)

    def show_preferences(self):
        """Show the preferences dialog"""
        PreferencesDialog(self.root, self.preferences)

    def setup_chrome_driver(self):
        """Set up and configure Chrome WebDriver with improved error handling"""
        logging.info("Setting up Chrome WebDriver...")
        chrome_options = Options()
        
        # Set up profile directory
        home_dir = os.path.expanduser('~')
        profile_dir = os.path.join(
            home_dir,
            'Library/Application Support/ChromeSelenium' if platform.system() == 'Darwin'
            else 'AppData/Local/ChromeSelenium' if platform.system() == 'Windows'
            else '.config/chrome-selenium'
        )
        
        os.makedirs(profile_dir, exist_ok=True)
        logging.info(f"Using Chrome profile directory: {profile_dir}")
        
        # Configure Chrome options
        chrome_options.add_argument(f'--user-data-dir={profile_dir}')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--start-maximized')
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e:
            logging.error(f"Failed to initialize Chrome WebDriver: {str(e)}")
            self.update_status(f"Error: Failed to start browser. {str(e)}", error=True)
            raise

    def is_exam_page(self):
        """Check if current page is a PrairieTest exam page"""
        try:
            current_url = self.driver.current_url
            is_exam = (
                current_url.startswith("https://us.prairietest.com/pt/student/exam") and
                "prairietest.com" in current_url
            )
            logging.info(f"Current URL: {current_url}, Is exam page: {is_exam}")
            return is_exam
        except Exception as e:
            logging.error(f"Error checking exam page: {str(e)}")
            return False

    def parse_session_info(self, session_element):
        """Parse session information from the session element"""
        try:
            # Extract session details (implement based on actual page structure)
            text = session_element.text
            # This is a simplified example - adjust based on actual page structure
            session_info = {
                'day': 'Monday',  # Extract from text
                'time_slot': 'Morning',  # Extract from text
                'duration': '2 hours',  # Extract from text
                'element': session_element  # Store reference to element
            }
            return session_info
        except Exception as e:
            logging.error(f"Error parsing session info: {str(e)}")
            return None

    def check_availability(self):
        """Check for available exam sessions matching preferences"""
        logging.info("Checking for available sessions...")
        try:
            wait = WebDriverWait(self.driver, 5)
            session_elements = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[contains(text(),"Available")]')
                )
            )
            
            matching_sessions = []
            for element in session_elements:
                session_info = self.parse_session_info(element)
                if session_info and self.preferences.matches_preferences(session_info):
                    matching_sessions.append(session_info)
            
            if matching_sessions:
                sessions_text = "\n".join(
                    f"Session: {session['day']} {session['time_slot']} ({session['duration']})"
                    for session in matching_sessions
                )
                self.update_status(
                    f"Matching sessions found:\n{sessions_text}",
                    success=True
                )
                self.play_notification()
                return True
            
            logging.info("No matching sessions found")
            self.update_status("No matching sessions available")
            return False
            
        except Exception as e:
            logging.warning(f"Error checking availability: {str(e)}")
            self.update_status("Error checking availability", error=True)
            return False

    def update_status(self, message, error=False, success=False):
        """Update status label with color coding based on message type"""
        logging.info(f"Status update: {message}")
        
        def update():
            self.status_label.configure(text=message)
            # Update last check time
            current_time = datetime.now().strftime("%H:%M:%S")
            self.last_check_label.configure(
                text=f"Last check: {current_time}"
            )
            
            # Color coding based on message type
            if error:
                self.status_label.configure(foreground=ModernTheme.ERROR_COLOR)
            elif success:
                self.status_label.configure(foreground=ModernTheme.SUCCESS_COLOR)
            else:
                self.status_label.configure(foreground="#202124")
        
        self.root.after(0, update)

    def monitor_loop(self):
        """Main monitoring loop with improved error handling and recovery"""
        try:
            logging.info("Starting monitor loop...")
            self.driver = self.setup_chrome_driver()
            self.driver.get("https://us.prairietest.com/pt")
            
            while self.monitoring:
                try:
                    if self.is_exam_page():
                        self.update_status("Checking for available sessions...")
                        self.check_availability()
                        time.sleep(self.refresh_interval)
                        self.driver.refresh()
                    else:
                        self.update_status(
                            "Please navigate to a valid exam page...",
                            warning=True
                        )
                        time.sleep(2)
                except Exception as e:
                    logging.error(f"Error in monitor loop: {str(e)}")
                    self.update_status(f"Error: {str(e)}", error=True)
                    time.sleep(self.refresh_interval)
                    
        except Exception as e:
            logging.error(f"Critical error in monitor loop: {str(e)}")
            self.update_status(f"Critical error: {str(e)}", error=True)
        finally:
            if self.monitoring:
                self.stop_monitoring()

    def start_monitoring(self):
        """Start the monitoring process"""
        logging.info("Starting monitoring...")
        self.monitoring = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.monitor_thread = threading.Thread(target=self.monitor_loop)
        self.monitor_thread.daemon = True  # Make thread daemon so it stops with main thread
        self.monitor_thread.start()

    def stop_monitoring(self):
        """Stop the monitoring process"""
        logging.info("Stopping monitoring...")
        self.monitoring = False
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logging.error(f"Error closing browser: {str(e)}")
            finally:
                self.driver = None
        
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.update_status("Monitoring stopped")

    def setup_notification_sound(self):
        """Set up system notification sound"""
        try:
            import winsound
            self.notification_sound = lambda: winsound.MessageBeep()
        except ImportError:
            # Fallback for non-Windows systems
            self.notification_sound = lambda: print("\a")

    def play_notification(self):
        """Play notification sound when session is available"""
        if self.notification_sound:
            self.notification_sound()

    def on_closing(self):
        """Handle application closing"""
        logging.info("Application closing...")
        self.stop_monitoring()
        self.root.destroy()

    def run(self):
        """Start the application"""
        logging.info("Starting main application loop...")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()