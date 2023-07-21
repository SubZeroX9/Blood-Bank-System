# Blood Bank System

The Blood Bank System is a desktop application that helps manage blood donations, donors, and withdrawals. The application uses Firebase for authentication and database management.

## Authors

- Rafael Azriaiev 309044071
- Tal Shaked 312208523

## Features

- User authentication (signup(future), login, and logout)
- Dashboard to view blood bank information (number of donations, donors, and withdrawals)
- Record blood withdrawals and donations, logs of activity
- Generate PDF reports of Records and Inventory
- Added HIPAA requirements for user access - App Ver3
- Added registered donators contacts with donation history - App Ver4
- Added guest donators contacts with donation history - App Ver4
- Added feature to send thank you mail after donation - App Ver4
- Added questionnaire to filter out bad donation - App Ver4
- Added feedback questionnaire to allow clinic improvement - App Ver4
- Added alert messages to notify when specific blood type is running low - App Ver4
- Added Profile Page for donors - App Ver5
- Added Loyalty System (upon reaching multipliers of 5 donations) recieve Coupons by email -App Ver5

## Installation

To install the Blood Bank System, follow these steps:

1. Download the latest release from the GitHub repository(https://github.com/SubZeroX9/Blood-Bank-System).
2. Extract the zip file to a directory on your computer.
3. Run the Blood Bank Manager.exe file to start the application.

## User Types

To access the system using different accounts:

1. Admin account (email: admin@admin.com pass: 123456).
2. Technician account (email: tech@tech.com pass: 123456)
3. Research Student account (email: stud@stud.com pass: 123456)
4. Donor account (email: donor@donor.com pass: 123456)

## Usage

To use the Blood Bank System, follow these steps:

1. Open the Blood Bank Manager.exe file.
2. Create a new account (future) or login with an existing account.
3. Navigate to the appropriate page to manage donations, blood bank inventory or Records (Only accessable to account with sufficient permissions (admin)).
4. Use the appropriate buttons to add a donation or withdrawals and emergency withdrawals (Only accessable to account with sufficient permissions (admin, technician)).
5. Use the dashboard to view the current status of the blood bank (Only accessable to account with sufficient permissions (admin, technician)).
6. Use the report feature to generate PDF reports of all the records and inventory (Only accessable to account with sufficient permissions (admin, research student)).
7. Use the feedback feature to enter a website with a questionnaire (Only accessable to account with sufficient permissions (admin, donor)).
8. Use the donation questionnaire to see if the blood donor needs to be rejected (Only accessable to account with sufficient permissions (admin, tech)).

## Contributing

To contribute to the Blood Bank System, follow these steps:

1. Fork this repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Create a pull request.

## License

The Blood Bank System is licensed under the MIT License.
