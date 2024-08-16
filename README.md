# FTSE Feeling

FTSE Feeling is a web application that provides real-time financial data and sentiment analysis for FTSE 100 companies. It offers stock predictions, company recommendations, and news sentiment analysis to help users make informed decisions.

## Features

- Real-time financial data for FTSE 100 companies
- Stock price prediction using machine learning
- News sentiment analysis
- Company recommendations based on user interests
- User authentication and profile management

## Prerequisites

Before running the application, ensure you have the following installed:
- Python 3.x
- Node.js and npm
- PostgreSQL (CockroachDB is used in this project)

## Installation

1. Clone the repository:
git clone https://github.com/Pushkal2407/ftse-feeling.git
cd ftse-feeling
Copy
2. Install Python dependencies:
pip install -r requirements.txt
Copy
3. Install Node.js dependencies:
cd frontend
npm install
npm install @mui/material
npm install chart.js
Copy
4. Set up the database certificate:

For Windows:
mkdir -p $env:appdata\postgresql; Invoke-WebRequest -Uri https://cockroachlabs.cloud/clusters/70f872cc-8221-4609-b2f5-decb5a7f4efa/cert -OutFile $env:appdata\postgresql\root.crt
Copy
For Linux/MacOS:
curl --create-dirs -o $HOME/.postgresql/root.crt 'https://cockroachlabs.cloud/clusters/70f872cc-8221-4609-b2f5-decb5a7f4efa/cert'
Copy
## Running the Application

1. Start the backend:

For Windows:
flask --app webapp run --debug
Copy
For Linux/MacOS:
python3 -m flask --app webapp run --debug
Copy
2. Start the frontend:
cd frontend
npm start
Copy
The application should now be running on `http://localhost:3000`.

## Testing

Detailed information about the testing process can be found in the project report.

## Future Work

- Expand the dataset to include more companies and stock exchanges
- Implement user-tailored approaches for content filtering and sorting
- Add peer networking features
- Improve graph visualizations and data precision

## Contributors

[List the team members here]


