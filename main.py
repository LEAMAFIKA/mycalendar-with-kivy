from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import calendar


class CalendarMonthApp(App):
    def build(self):
        # Initialize the grid
        self.grid = GridLayout(cols=7, spacing=2)

        # Create a dropdown menu for selecting months
        self.dropdown = DropDown()
        for i in range(1, 13):
            btn = Button(text=calendar.month_name[i], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.on_month_select(btn.text))
            self.dropdown.add_widget(btn)

        # Button to open the dropdown menu
        self.month_selector = Button(text='Select Month', size_hint=(None, None), size=(150, 44))
        self.month_selector.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.month_selector, 'text', x))

        # Initialize events dictionary to store events for each day
        self.events = {}

        # Add the month selector button to the grid
        self.grid.add_widget(self.month_selector)

        # Display the calendar for January 2024 on startup, starting with Monday
        self.update_calendar(2024, 1)
        return self.grid

    def update_calendar(self, year, month):
        # Clear existing widgets in the grid
        self.grid.clear_widgets()

        # Add the days of the week as headers, starting with Monday
        days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for day in days_of_week:
            self.grid.add_widget(Label(text=day))

        # Get the calendar for the selected month
        month_calendar = calendar.monthcalendar(year, month)
        first_day = month_calendar[0][0]

        # Add empty labels for days before the 1st day of the month
        for i in range((first_day - 1) % 7):
            self.grid.add_widget(Label())

        # Add the days of the month
        for week in month_calendar:
            for day in week:
                if day != 0:
                    # Add a button for each day of the month
                    btn_day = Button(text=str(day), on_press=self.show_selected_day)
                    self.grid.add_widget(btn_day)
                else:
                    # Add an empty label for unused days
                    self.grid.add_widget(Label())

    def show_selected_day(self, instance):
        # Display a message when the user presses a day
        selected_day = instance.text
        print(f"Selected day: {selected_day}")

        # Check if an event exists for the selected day
        if selected_day in self.events:
            # Create a popup for editing an existing event
            popup = Popup(title=f"Edit Event on {selected_day}", size_hint=(None, None), size=(400, 200))
            content = BoxLayout(orientation="vertical")
            event_input = TextInput(text=self.events[selected_day], hint_text='Edit event details')
            save_button = Button(text='Save',
                                 on_press=lambda x: self.save_event(selected_day, event_input.text, popup))
            content.add_widget(event_input)
            content.add_widget(save_button)
            popup.content = content
            popup.open()
        else:
            # Create a popup for adding a new event
            popup = Popup(title=f"Add Event on {selected_day}", size_hint=(None, None), size=(400, 200))
            content = BoxLayout(orientation="vertical")
            event_input = TextInput(hint_text='Enter event details')
            save_button = Button(text='Save',
                                 on_press=lambda x: self.save_event(selected_day, event_input.text, popup))
            content.add_widget(event_input)
            content.add_widget(save_button)
            popup.content = content
            popup.open()

    def save_event(self, day, event_details, popup):
        # Save the event details in the events dictionary
        self.events[day] = event_details
        print(f"Event on {day}: {event_details}")

        # Update the text and color of the button with the event details
        for child in self.grid.children:
            if isinstance(child, Button) and child.text == day:
                child.text = f"{day}\n{event_details}"
                child.background_color = (0, 0, 1, 1)  # Set button background color to blue

        popup.dismiss()

    def on_month_select(self, selected_month):
        # Update the calendar when the user selects a month from the dropdown
        month_number = list(calendar.month_name).index(selected_month)
        self.update_calendar(2024, month_number)


# Check if __name__ is '__main__' outside the class
if __name__ == '__main__':
    # Adjust the window size
    Window.size = (400, 300)
    # Set the application title including the initial month and year
    Window.set_title('Calendar - January 2024')
    # Launch the application
    CalendarMonthApp().run()
