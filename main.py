# Reference for writing and reading text files: https://www.geeksforgeeks.org/reading-writing-text-files-python/
# Reference for strip() and split() : https://www.w3schools.com/python/python_ref_string.asp

import datetime # Reference: https://www.w3schools.com/python/python_datetime.asp

import getpass # Reference:https://www.geeksforgeeks.org/getpass-and-getuser-in-python-password-without-echo/

import os  # Import the os module to check whether a file exists  
# Reference: https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions

tickets_list = []  # Created an empty list to store the ticket data

# Function to read tickets from the "TicketsList.txt" file
def ReadTextfile(tickets_list):
  if os.path.exists("TicketsList.txt"):  # Checking whether the file exists  
    file = open("TicketsList.txt", "r")
    for line in file:
        ticket_data = line.strip().split(", ")
        ticket = {
            'ticketID': ticket_data[0],
            'eventID': ticket_data[1],
            'username': ticket_data[2],
            'date': ticket_data[3],
            'priority': int(ticket_data[4])
        }
        tickets_list.append(ticket)
  else:
    print("No tickets data found.")


# Function to upload tickets to the "TicketsList.txt" file
def uploadTickets(tickets_list):
    file = open("TicketsList.txt", "w")
    for ticket in tickets_list:
            file.write(
                f"{ticket['ticketID']}, {ticket['eventID']}, {ticket['username']}, {ticket['date']}, {ticket['priority']}\n"
            )

# Display Statistics choice
def Display_Statistics(tickets_list):
  event_tickets = {}
  for ticket in tickets_list:
    event_id = ticket['eventID']
    event_tickets[event_id] = event_tickets.get(event_id, 0) + 1

  if event_tickets:
    max_event_id = max(event_tickets, key=lambda k: event_tickets[k])
    max_tickets = event_tickets[max_event_id]
    print(
        f"The event ID with the highest number of tickets : {max_event_id} , which has {max_tickets} tickets."
    )


# Book a ticket choice for Admin 
def book_ticket(tickets_list):
  ticket_id = f"tick{len(tickets_list) + 1:03}"
  event_id = input("Enter event ID: ")
  username = input("Enter username: ")
  
  date = input("Enter event's date (YYYYMMDD): ")
  priority = int(input("Enter priority: "))

  ticket = {
      'ticketID': ticket_id,
      'eventID': event_id,
      'username': username,
      'date': date,
      'priority': priority
  }
  tickets_list.append(ticket)

  print("The ticket booked successfully!")

  # Add the new tickets to the "TicketsList.txt" fle 
  uploadTickets(tickets_list)


# Display all Tickets (ordered by event's date and event ID,old tickets should not be shown.)
def Display_all_Tickets(tickets_list):
  today = datetime.datetime.now().strftime("%Y%m%d")

  print("Today's and future's events:")
  for ticket in sorted(tickets_list, key=lambda x: (x['date'], x['eventID'])):
    if ticket['date'] >= today:
      print(
          f"Ticket ID: {ticket['ticketID']}, Event ID: {ticket['eventID']}, Username: {ticket['username']}, Date: {ticket['date']}, Priority {ticket['priority']}"
      )

# Change the priority of a ticket 
def Change_Ticket_Priority(tickets_list):
    ticket_id = input("Enter the ticket ID : ")
    for ticket in tickets_list:
        if ticket['ticketID'] == ticket_id:
            new_priority = int(input("Enter the new priority: "))
            ticket['priority'] = new_priority
            print(f"The new priority for {ticket_id} is : {new_priority}.")
            uploadTickets(tickets_list)  
    else:
        print(f"Ticket {ticket_id} not found.")


# Remove a ticket from the system by providing the ticket ID
def Disable_Ticket(tickets_list):
    ticket_id = input("Enter the ticket ID : ")
    for ticket in tickets_list:
        if ticket['ticketID'] == ticket_id:
            tickets_list.remove(ticket)
            print(f"Ticket {ticket_id} is disabled.")
            uploadTickets(tickets_list) 
            break
    else:
        print(f"Ticket {ticket_id} not found.")


# Display today's events found in the list, Sorted by priority
def Run_Events(tickets_list):
    today = datetime.datetime.now().strftime("%Y%m%d")
    today_events = [ticket for ticket in tickets_list if ticket['date'] == today]
    today_events.sort(key=lambda x: x['priority'], reverse=True)

    if today_events:
        print("Today's events:")
        for event in today_events:
          print( f"Event ID: {event['eventID']}, Ticket ID: {event['ticketID']}, Username: {event['username']}, Priority: {event['priority']}")

        # Remove today's events from the tickets list
        tickets_list[:] = [ticket for ticket in tickets_list if ticket not in today_events]
        uploadTickets(tickets_list)
    else:
        print("No events today.")


# Book a ticket for normal users
def Book_Ticket_for_Users(tickets_list, username):
    ticket_id = f"tick{len(tickets_list) + 1:03}"
    event_id = input("Enter the event ID: ")
    date = input("Enter the event date (YYYYMMDD): ")

    ticket = {
        'ticketID': ticket_id,
        'eventID': event_id,
        'username': username,
        'date': date,
        'priority': 0
    }
    tickets_list.append(ticket) 

    print("The ticket booked successfully!")

# Display the normal users menu
def NormalUsers_Menu(tickets_list, username):
    while True:
        print("\nUser Menu:")
        print("1. Book a Ticket")
        print("2. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            Book_Ticket_for_Users(tickets_list, username)
        elif choice == "2":
            uploadTickets(tickets_list)
            print("Tickets saved. Program exit.")
            break
        else:
            print("Invalid choice.")


# Display the admin menu
def Admin_Menu(tickets_list):
  while True:
    print("\nAdmin Menu:")
    print("1. Display Statistics")
    print("2. Book a Ticket")
    print("3. Display all Tickets")
    print("4. Change Ticket's Priority")
    print("5. Disable Ticket")
    print("6. Run Events")
    print("7. Exit")

    choice = input("Enter your choice: ").strip()
    if choice == "1":
      Display_Statistics(tickets_list)
    elif choice == "2":
      book_ticket(tickets_list)
    elif choice == "3":
      Display_all_Tickets(tickets_list)
    elif choice == "4":
      Change_Ticket_Priority(tickets_list)
    elif choice == "5":
      Disable_Ticket(tickets_list)
    elif choice == "6":
      Run_Events(tickets_list)
    elif choice == "7":
      print("Tickets saved and program exit.")
      break
    else:
      print("Invalid choice.")


# User and admin login 
def main():
   ReadTextfile(tickets_list)
   for _ in range(5):
    username = input("Username: ").strip().lower()
    password = getpass.getpass(prompt="Password: ")

    if username == "users" and password == "":
      NormalUsers_Menu(tickets_list, username)  
      break
    elif username == "admin" and password == "admin123123":
      Admin_Menu(tickets_list) 
      break
    else:
      print("Incorrect Username and/or Password")
   else:
    print("Try again after 5 minutes")


# Display the main menu 
def main_menu():
  while True:
    print("\nMain Menu:")
    print("1. Start")
    print("2. Turn Off")
    choice = input("Enter your choice: ").strip()
    if choice == "1":
      main()
    elif choice == "2":
      print("Exit.")
      break
    else:
      print("Invalid choice.")

# Call the main menu 
main_menu()
