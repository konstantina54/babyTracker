#👶 BabyTracker

A full-stack Flask application designed to log, store, and visualize baby activity data such as feeding, sleeping, and diaper changes. The app supports both manual input from caregivers and automated data collection, storing the information in a PostgreSQL database and providing a separate view for visualization and export.
📖 Overview

#BabyTracker allows caregivers to:

    🖐️ Manually log baby activities via a user-friendly interface.

    🗃️ Store activity data in a PostgreSQL database.

    📊 Visualize logged activities to identify patterns over time.

    📤 Export activity data for further analysis.

This project demonstrates end-to-end backend and data engineering skills, including API development, relational data modeling, user input validation, and basic data analytics.
#🧰 Tech Stack

    Language: Python 3.10

    Framework: Flask

    Database: PostgreSQL

    Data Processing: Pandas

    Frontend: HTML, CSS (via Flask templates)

    Others: SQLAlchemy for ORM, dotenv for environment variable management

#📂 Project Structure

babyTracker/
├── app.py                 # Main Flask application
├── functions.py           # Helper functions for data processing
├── postgres_commands.py   # Database interaction functions
├── templates/             # HTML templates for Flask
│   └── ...
├── static/                # Static files (CSS, JS, images)
│   └── ...
├── .gitignore
└── README.md

#⚙️ Setup Instructions

    Clone the Repository:

git clone https://github.com/konstantina54/babyTracker.git
cd babyTracker

#Create a Virtual Environment:

python3 -m venv venv
source venv/bin/activate

#Install Dependencies:

pip install -r requirements.txt

#Configure Environment Variables:

Create a .env file in the root directory and add your PostgreSQL credentials:

DB_HOST=your_host
DB_PORT=your_port
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password

#Run the Application:

    python app.py

    Access the application at http://localhost:5000.

#🛠️ Features

    Manual Data Entry: Log feeding, sleeping, and diaper change activities.

    Data Visualization: View activities in a separate dashboard to identify patterns.

    Data Export: Export activity data to CSV for further analysis.

    Modular Design: Separation of concerns with dedicated scripts for different functionalities.

#🧪 Testing

To test individual components or the entire application, you can run:

python -m unittest discover

Ensure you have test cases defined in a tests/ directory or within your modules.
#📈 Future Enhancements

    User Authentication: Implement user login and registration to manage multiple caregivers.

    API Integration: Develop RESTful APIs for mobile app integration.

    Data Analytics: Incorporate advanced analytics to provide insights on baby activities.

    Responsive Design: Enhance frontend for better mobile device compatibility.

