# Django Trader Project

This is a Django project designed for traders to manage their trade accounts, enter trade details, and track their activities, losses, profits, and equity. The project provides a user-friendly interface for traders to sign up, log in, and manage their trades effectively. Additionally, the project generates charts based on the entered trades for a selected account, allowing traders to visualize their trading performance.
Installation

To use this project, follow these steps:

1. Install Python 3 on your system.
2. Install the required dependencies by running the following command:

       pip install -r requirements.txt
3. Create the initial database schema by making migrations:

       python manage.py makemigrations
4. Apply the migrations to the database:

       python manage.py migrate
5. Create default objects in the database by running the following custom command:

       python manage.py create_default
Please note that the create_default command has been added to the base_module app specifically for this project to create some necessary default objects in the database.

## Usage

Once you have installed and set up the project, you can start using it to manage your trades. Here are the main features provided by the project:
Account Management

    Sign up for a new trader account.
    Log in using your credentials.
    Create trade accounts associated with your trader account.

## Trade Details

    Enter details of each trade you perform.
    View your trading activities.
    Track your daily losses and profits.
    Monitor your maximum losses and profits.
    Keep an eye on your equity.

## Charts

    Generate a chart based on all the trades you have entered for a selected account.
    Visualize your trading performance for better analysis.

Feel free to explore the project and utilize its features to enhance your trading experience.

## Contributions

Contributions to this project are welcome. If you have any suggestions, improvements, or bug fixes, please feel free to open an issue or submit a pull request.