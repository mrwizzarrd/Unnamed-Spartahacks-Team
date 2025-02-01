import cv2
import ocr
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.graphics.texture import Texture
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from datetime import datetime
import json

# Example of a simple JSON file for events
json_file = "events.json"

# Load JSON from file
def load_json():
    try:
        with open(json_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"events": []}

# Save JSON to file
def save_json(data):
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Background color
        with layout.canvas.before:
            Color(0.2, 0.4, 0.8, 1)  # Background color (light blue)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

        # Label with default text
        self.label = Label(text="Welcome to My Kivy App", font_size=30, color=(1, 1, 1, 1),
                           size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5})
        layout.add_widget(self.label)

        # Button that changes the label text when pressed
        button = Button(text="Click Me!", size_hint=(None, None), size=(200, 50),
                        pos_hint={'center_x': 0.5})
        button.bind(on_press=self.change_text)
        layout.add_widget(button)

        # Navigation buttons
        button_camera = Button(text="Go to Camera", size_hint=(None, None), size=(200, 50),
                                 pos_hint={'center_x': 0.5})
        button_camera.bind(on_press=self.change_screen_camera)
        layout.add_widget(button_camera)

        button_calendar = Button(text="Go to Calendar", size_hint=(None, None), size=(200, 50),
                                   pos_hint={'center_x': 0.5})
        button_calendar.bind(on_press=self.change_screen_calendar)
        layout.add_widget(button_calendar)

        button_upload = Button(text="Upload Photo", size_hint=(None, None), size=(200, 50),
                               pos_hint={'center_x': 0.5})
        button_upload.bind(on_press=self.upload_photo)
        layout.add_widget(button_upload)

        self.add_widget(layout)

    def change_text(self, instance):
        self.label.text = "Button Pressed!"

    def change_screen_camera(self, instance):
        self.manager.current = 'camera'  # Accessing ScreenManager via self.manager

    def change_screen_calendar(self, instance):
        self.manager.current = 'calendar'  # Accessing ScreenManager via self.manager

    def upload_photo(self, instance):
        # Create a file chooser to select a file
        filechooser = FileChooserIconView()
        filechooser.bind(on_selection=self.on_file_select)

        # Create and show a popup with the file chooser
        popup = Popup(title="Select an Image", content=filechooser, size_hint=(0.8, 0.8))
        popup.open()

    def on_file_select(self, instance, value):
        if value:
            filepath = value[0]
            print(f"File selected: {filepath}")
            ocr.ocr(filepath)  # Process the selected image with OCR

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout for the camera screen
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Create an Image widget to display the camera feed
        self.img = Image(size_hint=(1, 1), allow_stretch=True)
        layout.add_widget(self.img)

        # Button to take picture
        button_take_picture = Button(text="Take Picture", size_hint=(None, None), size=(200, 50),
                                       pos_hint={'center_x': 0.5})
        button_take_picture.bind(on_press=self.take_picture)
        layout.add_widget(button_take_picture)

        # Button to go back to the main screen
        button_back = Button(text="Back to Main", size_hint=(None, None), size=(200, 50),
                             pos_hint={'center_x': 0.5})
        button_back.bind(on_press=self.go_back_to_main)
        layout.add_widget(button_back)

        self.add_widget(layout)

        # Start OpenCV camera capture
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            print("Error: Could not open video capture.")
            return

        # Set up a clock to update the camera feed
        self.event = Clock.schedule_interval(self.update_frame, 1.0 / 30.0)  # 30 FPS

    def update_frame(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Convert the frame to texture for Kivy
            frame = cv2.flip(frame, 0)  # Flip the frame vertically
            buf = frame.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            # Update the image widget with the new frame
            self.img.texture = texture

    def take_picture(self, instance):
        ret, frame = self.capture.read()
        if ret:
            # Save the current frame as an image
            current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f"photo_{current_time}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Picture saved as {filename}")
            ocr.ocr(filename)

    def go_back_to_main(self, instance):
        self.manager.current = 'main'  # Go back to the main screen

    def on_stop(self):
        # Release the camera capture when the app is stopped
        if self.capture.isOpened():
            self.capture.release()
        super().on_stop()


class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout for the calendar screen
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Get current date and display it
        current_date = datetime.now().strftime('%Y-%m-%d')
        label = Label(text=f"Calendar Screen\nToday is: {current_date}", font_size=30,
                      color=(1, 1, 1, 1), size_hint=(None, None), size=(300, 50),
                      pos_hint={'center_x': 0.5})
        layout.add_widget(label)

        # Create and store the ScrollView in an instance variable
        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        self.scroll_view.add_widget(self.create_event_grid())
        layout.add_widget(self.scroll_view)

        # Button to go back to the main screen
        button_back = Button(text="Back to Main", size_hint=(None, None), size=(200, 50),
                             pos_hint={'center_x': 0.5})
        button_back.bind(on_press=self.go_back_to_main)
        layout.add_widget(button_back)

        self.add_widget(layout)

    def create_event_grid(self):
        """Create a grid with events from the JSON."""
        data = load_json()
        events = data.get("events", [])

        # Adjusting grid layout with more spacing and padding
        grid = GridLayout(cols=1, size_hint_y=None, padding=15, spacing=15)
        grid.bind(minimum_height=grid.setter('height'))

        # Create a section for each event
        for event in events:
            # Event name with more spacing
            event_label = Label(text=event["event"], size_hint_y=None, height=50, font_size=18)
            grid.add_widget(event_label)

            # Date(s) with more spacing
            date_label = Label(text=f"Date: {event.get('date', '')} - {event.get('end_date', '')}",
                               size_hint_y=None, height=50, font_size=16)
            grid.add_widget(date_label)

            # Time and location (if provided)
            time_label = Label(text=f"Time: {event.get('time', 'N/A')}", size_hint_y=None, height=50, font_size=16)
            grid.add_widget(time_label)

            location_label = Label(text=f"Location: {event.get('location', 'N/A')}",
                                   size_hint_y=None, height=50, font_size=16)
            grid.add_widget(location_label)

            # Notes with more spacing
            notes_label = Label(text=f"Notes: {event.get('notes', 'None')}",
                                size_hint_y=None, height=50, font_size=14)
            grid.add_widget(notes_label)

            # Trash can button for deleting event
            trash_button = Button(size_hint_y=None, height=60, width=60)
            trash_button.text = "Delete"  # Optionally, set an icon or different style
            # Use a lambda to pass the current event to delete_event
            trash_button.bind(on_press=lambda instance, ev=event: self.delete_event(ev))
            grid.add_widget(trash_button)

        return grid

    def delete_event(self, event):
        """Delete an event from the JSON and update the display."""
        data = load_json()
        # Remove the event from the list
        data["events"] = [e for e in data["events"] if e != event]
        # Save the updated data to JSON
        save_json(data)
        # Refresh the calendar display
        self.refresh_calendar()

    def refresh_calendar(self):
        """Refresh the calendar view."""
        self.scroll_view.clear_widgets()
        self.scroll_view.add_widget(self.create_event_grid())

    def go_back_to_main(self, instance):
        self.manager.current = 'main'  # Go back to the main screen


class MyApp(App):
    def build(self):
        # Set window size
        Window.size = (400, 600)

        # Screen manager to handle multiple screens
        sm = ScreenManager()

        # Add the screens
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CameraScreen(name='camera'))
        sm.add_widget(CalendarScreen(name='calendar'))

        return sm


if __name__ == '__main__':
    MyApp().run()
