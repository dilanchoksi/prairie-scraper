# src/gui/theme.py
from tkinter import ttk

class ModernTheme:
    """Theme constants for the application"""
    BG_COLOR = "#f0f2f5"
    PRIMARY_COLOR = "#1a73e8"
    SUCCESS_COLOR = "#34a853"
    ERROR_COLOR = "#ea4335"
    WARNING_COLOR = "#fbbc04"
    FONT_FAMILY = "Helvetica"
    
    @classmethod
    def configure_styles(cls):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure frame style
        style.configure(
            'Custom.TFrame',
            background=cls.BG_COLOR
        )
        
        # Configure button styles
        style.configure(
            'Primary.TButton',
            padding=10,
            font=(cls.FONT_FAMILY, 10, 'bold'),
            background=cls.PRIMARY_COLOR,
            foreground='white'
        )
        
        style.configure(
            'Stop.TButton',
            padding=10,
            font=(cls.FONT_FAMILY, 10, 'bold'),
            background=cls.ERROR_COLOR,
            foreground='white'
        )
        
        # Configure label style
        style.configure(
            'Status.TLabel',
            font=(cls.FONT_FAMILY, 11),
            background=cls.BG_COLOR,
            foreground='#202124'
        )