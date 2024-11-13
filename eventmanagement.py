class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

class Participant:
    def __init__(self, participant_id, name, email, phone, address, emergency_contact):
        self.participant_id = participant_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.emergency_contact = emergency_contact

    def __str__(self):
        return (f"{self.participant_id}: {self.name} ({self.email}, Phone: {self.phone}, "
                f"Address: {self.address}, Emergency Contact: {self.emergency_contact})")

class Event:
    def __init__(self, name, date, venue):
        self.name = name
        self.date = date
        self.venue = venue
        self.participants = []

    def add_participant(self, participant):
        self.participants.append(participant)

    def __str__(self):
        return f"Event: {self.name} | Date: {self.date} | Venue: {self.venue} | Participants: {len(self.participants)}"

class EventManager:
    def __init__(self):
        self.events = []  
        self.users = []  
        self.admins = []  
        self.logged_in_user = None
        self.logged_in_admin = None
        
        # Add default events
        self.add_default_events()

    def add_default_events(self):
        default_events = [
            Event("Annual Charity Run", "2024-05-10", "City Park"),
            Event("Music Festival", "2024-05-15", "Downtown Square"),
            Event("Tech Conference", "2024-05-20", "Convention Center"),
            Event("Football Match", "2024-05-22", "Etihad Stadium"),
            Event("Cricket Match", "2024-05-24", "Greenfield Stadium"),
        ]
        self.events.extend(default_events)

    def register_user(self, username, password):
        if any(user.username == username for user in self.users):
            return "Username already taken."
        self.users.append(User(username, password))
        return "User registered successfully!"

    def register_admin(self, username, password):
        if any(admin.username == username for admin in self.admins):
            return "Admin username already taken."
        self.admins.append(Admin(username, password))
        return "Admin registered successfully!"

    def login(self, username, password):
        for user in self.users + self.admins:
            if user.username == username and user.password == password:
                if isinstance(user, Admin):
                    self.logged_in_admin = user
                    return f"Welcome, Admin {username}! You are now logged in."
                self.logged_in_user = user
                return f"Welcome, {username}! You are now logged in."
        return "Incorrect username or password."

    def logout(self):
        if self.logged_in_user:
            print(f"Goodbye, {self.logged_in_user.username}!")
            self.logged_in_user = None
        elif self.logged_in_admin:
            print(f"Goodbye, Admin {self.logged_in_admin.username}!")
            self.logged_in_admin = None
        else:
            print("You are not logged in.")

    def register_participant(self, event_name, participant_id, participant_name, participant_email, participant_phone, participant_address, emergency_contact):
        if self.logged_in_user or self.logged_in_admin:
            for event in self.events:
                if event.name == event_name:
                    event.add_participant(Participant(participant_id, participant_name, participant_email, participant_phone, participant_address, emergency_contact))
                    return f"{participant_name} registered for {event_name}."
            return "Event not found."
        return "Please log in to register participants."

    def delete_event(self, event_name):
        if self.logged_in_admin:
            for event in self.events:
                if event.name == event_name:
                    self.events.remove(event)
                    return f"Event {event_name} deleted successfully."
            return "Event not found."
        return "Only admins can delete events."

    def show_users(self):
        if self.logged_in_admin:
            return "\n".join(user.username for user in self.users) or "No users registered."
        return "Only admins can view users."

    def show_events(self):
        return "\n".join(str(event) for event in self.events) or "No events available."

    def event_details(self, event_name):
        for event in self.events:
            if event.name == event_name:
                details = f"Event: {event.name}\nDate: {event.date}\nVenue: {event.venue}\nParticipants:"
                details += ''.join(f"\n- {p}" for p in event.participants)
                return details
        return "Event not found."

def main():
    manager = EventManager()
    manager.register_admin("admin", "adminpass")

    while True:
        print("\nEvent Management System")
        print("1. Register User")
        print("2. User Login")
        print("3. Admin Login")
        print("4. Logout")
        print("5. Register Participant")
        print("6. Show All Events")
        print("7. View Event Details")
        print("8. Admin: Show All Users")
        print("9. Admin: Delete Event")
        print("10. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            print(manager.register_user(username, password))

        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            print(manager.login(username, password))

        elif choice == '3':
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")
            print(manager.login(username, password))

        elif choice == '4':
            manager.logout()

        elif choice == '5':
            if manager.logged_in_user or manager.logged_in_admin:
                event_name = input("Enter event name: ")
                participant_id = input("Enter participant ID: ")
                participant_name = input("Enter participant name: ")
                participant_email = input("Enter participant email: ")
                participant_phone = input("Enter participant phone: ")
                participant_address = input("Enter participant address: ")
                emergency_contact = input("Enter emergency contact: ")
                print(manager.register_participant(event_name, participant_id, participant_name, participant_email, participant_phone, participant_address, emergency_contact))
            else:
                print("Please log in to register participants.")

        elif choice == '6':
            print("All Events:")
            print(manager.show_events())

        elif choice == '7':
            event_name = input("Enter event name to view details: ")
            print(manager.event_details(event_name))

        elif choice == '8':
            print("All Users:")
            print(manager.show_users())

        elif choice == '9':
            if manager.logged_in_admin:
                event_name = input("Enter event name to delete: ")
                print(manager.delete_event(event_name))
            else:
                print("Only admins can delete events.")

        elif choice == '10':
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
