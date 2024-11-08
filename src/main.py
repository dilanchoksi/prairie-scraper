from gui.theme import ModernTheme
from gui.preferences import ExamPreferences, PreferencesDialog
from src.monitor.browser import PrairieTestMonitor

def main():
    app = PrairieTestMonitor()
    app.run()

if __name__ == "__main__":
    main()