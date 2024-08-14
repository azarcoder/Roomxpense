# Roomxpense

#### Video Demo:  https://youtu.be/CN_nGb0nV0c?si=2rCqmRCeiz3CFSca

## Description:
Roomxpense is a Django-based application developed to simplify the management and calculation of shared expenses within a group, such as roommates sharing rent, utilities, groceries, or other communal costs. The core functionality revolves around distributing any payments made by a member evenly across all members, ensuring that at the end of the billing cycle, the application can accurately determine who owes whom and how much.

Whether you are living with roommates, splitting costs with friends, or managing expenses in any other group scenario, Roomxpense aims to remove the complexities of keeping track of payments and settling up at the end of the month.

## Features:
- **Room Management**: Users can create and manage rooms, which represent a group of people who share expenses. Each room can have multiple members.
- **Expense Tracking**: When a member of a room makes a payment, the expense is recorded and automatically split among all members of the room.
- **Balance Calculation**: The application calculates the balance for each member, showing how much they have paid, how much they have been charged, and their current balance.
- **Settlement Feature**: At the end of the month or billing period, the application generates a settlement report showing who needs to pay whom and how much.
- **User Authentication**: Secure login and registration for users, ensuring that only authenticated users can manage rooms and expenses.

## File Structure and Design:
### 1. `models.py`:
This file contains the data models that define the structure of the application's database.

- **Room**: Represents a group of people who share expenses. It contains fields for the room name, creation date, and the user who created the room.
- **Person**: Represents an individual in a room. Each person has a name, email, contact number, and financial fields (balance, paid, charged). The person is linked to a specific room.
- **Transaction**: Represents a financial transaction made by a member. It includes details about the product/service, the date of the transaction, and the members involved.
- **TransactionDetail**: Represents the details of each transaction, including the amount paid by a member and the amount charged to others. This model links transactions to the people involved and tracks how much each person owes.

### 2. `views.py`:
This file contains the logic that handles HTTP requests and responses, linking the models to the templates.

- **index**: Displays the rooms created by the logged-in user. If the user is not authenticated, they are redirected to the login page.
- **login_view**: Manages user authentication. It validates login credentials and redirects users to their dashboard if successful.
- **custom_logout_view**: Handles user logout and redirects them to the homepage with a success message.
- **sign_up**: Manages user registration. New users can create an account, and once registered, they are automatically logged in and redirected to the dashboard.
- **newroom**: Allows users to create a new room. The room is linked to the user who created it.
- **add_person**: Enables users to add members to a room. Each person is linked to a room, and their financial balance is initialized.
- **view_members**: Displays the members of a room. It provides an overview of who is in the room and their contact details.
- **transactions**: Handles the creation of new transactions. It calculates how much each person should be charged and updates their financial balances.
- **settle**: Generates a settlement report, indicating who needs to pay whom and how much to balance out the expenses.

### Design Choices:
- **Database Structure**: The use of separate models for `Room`, `Person`, `Transaction`, and `TransactionDetail` ensures that the data is well-organized and scalable. Each model has a clear responsibility, which makes the code easier to maintain and extend.
- **Transaction Handling**: Transactions are split between members, with the person who paid having a positive balance and others having a negative balance. This approach simplifies the process of settling up at the end of the month.
- **User Interface**: The views are designed to be simple and intuitive, making it easy for users to manage rooms, add members, and track expenses without needing extensive instructions.

## Dependencies:
- `Django`: The primary web framework used to build the application.
- `Python`: The programming language used for development.

## Installation:
1. Clone the repository using:
    ```bash
    git clone <repository-url>
    ```
2. Navigate to the project directory:
    ```bash
    cd Roomxpense
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Apply the migrations to set up the database:
    ```bash
    python manage.py migrate
    ```
5. Create a superuser to manage the application:
    ```bash
    python manage.py createsuperuser
    ```
6. Run the development server:
    ```bash
    python manage.py runserver
    ```
7. Access the application in your web browser at `http://127.0.0.1:8000`.

## Usage:
1. Log in or create an account.
2. Create a room and add members to it.
3. Record transactions as members pay for shared expenses.
4. At the end of the billing period, view the settlement report to see who owes whom.

## Testing:
- The project includes test cases to ensure that all functionalities work as expected.
- To run the tests, use:
    ```bash
    python manage.py test
    ```
- The tests cover scenarios such as adding rooms, members, transactions, and generating settlement reports.

## Future Enhancements:
- **Notification System**: Adding email or SMS notifications to remind members about pending payments.
- **Expense Categories**: Introducing categories for expenses to better organize and analyze spending.
- **Integration with Payment Gateways**: Allowing members to settle up directly through the app using online payment methods.
