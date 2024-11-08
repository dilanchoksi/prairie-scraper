# PrairieTest Availability Monitor

A Python-based monitoring system that helps students track exam slot availability on PrairieTest. This tool provides real-time notifications when exam slots matching your preferences become available.

## Features

- 🔍 Real-time monitoring of exam slot availability
- ⚡ Automated refresh every 10 seconds
- 🎯 Custom preference filters for:
  - Days of the week
  - Time slots (Morning/Afternoon/Evening)
  - Exam duration
- 🔔 Desktop notifications when matching slots are found
- 💻 Modern, user-friendly GUI
- 📝 Comprehensive logging system

## Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/prairietest-monitor.git
cd prairietest-monitor
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# MacOS/Linux
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python src/main.py
```

2. Configure your preferences using the "Set Preferences" button:
   - Select preferred days
   - Choose time slots
   - Set exam duration preference
   - Choose notification mode

3. Click "Start Monitoring"

4. Log in to PrairieTest in the opened browser window

5. Navigate to your exam page

6. The application will monitor for available slots matching your preferences

## Project Structure
```
src/
├── gui/
│   ├── theme.py       # GUI styling and theme
│   └── preferences.py # User preferences management
├── monitor/
│   └── browser.py     # Browser automation and monitoring
└── utils/
    └── logger.py      # Logging configuration
```

## Known Issues

- The first-time Chrome setup might take a few seconds
- On macOS, system notifications might require additional permissions
- Chrome updates may temporarily affect WebDriver functionality

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is designed for educational purposes and personal use only. Please ensure compliance with your institution's policies regarding exam registration.

## Acknowledgments

- Built using Selenium WebDriver for browser automation
- GUI implemented with Python's tkinter library
- Special thanks to the PrairieLearn team for their educational platform