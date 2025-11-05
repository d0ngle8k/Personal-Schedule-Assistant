"""
Application Launcher
Main entry point for the Google Calendar style UI
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import customtkinter as ctk
from app.views.main_window import MainWindow
from app.controllers.main_controller import MainController


def main():
    """Launch the application"""
    print("="*50)
    print("Trợ lý Lịch trình v0.7.0 (Google Calendar UI)")
    print("="*50)
    
    controller = None
    try:
        # Create main window
        print("Initializing UI...")
        app = MainWindow()
        
        # Create controller (connects view to model/database)
        print("Setting up MVC architecture...")
        controller = MainController(app, "database/events.db")
        
        # Bind controller to view
        app.controller = controller
        
        # Register cleanup on window close
        def on_close():
            if controller:
                controller.on_app_close()
            app.destroy()
        
        app.protocol("WM_DELETE_WINDOW", on_close)
        
        print("✅ Application ready!")
        print("="*50)
        
        # Run the app
        app.mainloop()
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user")
        if controller:
            controller.on_app_close()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()
        if controller:
            controller.on_app_close()
        sys.exit(1)


if __name__ == "__main__":
    main()
