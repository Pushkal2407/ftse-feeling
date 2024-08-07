Hello everyone

To run the webapp locally:

Windows
- Run this command once (downloading DB certificate):
- mkdir -p $env:appdata\postgresql\; Invoke-WebRequest -Uri https://cockroachlabs.cloud/clusters/70f872cc-8221-4609-b2f5-decb5a7f4efa/cert -OutFile $env:appdata\postgresql\root.crt
- Copy and paste " flask --app webapp run --debug " into command prompt


Linux / MacOS
- Run this command once (downloading DB certificate):
- curl --create-dirs -o $HOME/.postgresql/root.crt 'https://cockroachlabs.cloud/clusters/70f872cc-8221-4609-b2f5-decb5a7f4efa/cert'
- Copy and paste " python3 -m flask --app webapp run --debug " into command prompt


Also check that you have all the libraries in the requirements.txt file installed (these can be installed using "pip install libraryName")

also install the needed node modules using the following commands:
npm install @mui/material
npm install chart.js

To run the frontend the command is 'npm start' in the "frontend" directory
