# finnazureflaskapp

The python project will parse finn.no and present the results.
The parsing includes:
1. Scanning for new ads of realstates.
2. Scanning each realstate ad and parsing the price.
3. Scanning for sold houses.

The ads are stored in links.json along with the time stamp. So its possible to find out when the link was first seen on finn. The prices are stored in pris.json with the links and timestamp. So if 1 ad contains two different prices at 2 different timestamps, it is easier to find out the change in price.

It also tells you the SOLD status. Finn.no doesnt display the sold houses in the search. If the link is saved somewhere it is easy to browse it and see the sold houses. The webapp scans links and records the status changes.
The app is triggered by an azure timer function so it collects data in the background and store the json in the Azure Storage Blob.

LOCAL

DEPLOYMENT:<br />
App can be deployed locally using flask. 
1. Clone the project.
2. Enter the project directory.
3. Enter following commands: <br />
   python3 -m venv venv <br />
   source venv/bin/activate <br />
   pip install -r requirements.txt <br />
4. Run the project by entering the following command:   
   FLASK_APP=application.py flask run <br />
   This will start the flask and you can browse your app on the localhost.

CLOUD (MICROSOFT AZURE)

DEPLOYMENT:<br />
I have deployed this app on my azure account. 
1. Get a free azure account (or paid if you can).
2. Enter the cloud shell.
3. Clone the project.
4. Enter the project directory and run the following command: 
   az webapp up -n "app-name"
5. Using cloud shell, you can makes changes to the code and then deploy it back with the same command.
6. Since now the /price request takes long time to load, the app timed out. So i changed the startup configuration using        command: az webapp config set --resource-group "resource-group" --name "app-name" --startup-file "gunicorn --bind=0.0.0.0    --timeout 2000 application:app"
7. I have a timer-function created on azure that requests the scan every n hours.
