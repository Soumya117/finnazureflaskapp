# finnazureflaskapp

The python project will parse finn.no and present the results.
The parsing includes:
1. Scanning for new ads of realstates.
2. Scanning each realstate ad and parsing the price.

The app will return the recorded change in price. The ads are stored in links.json along with the time stamp. So its possible to find out when the link was first seen on finn. The prices are stored in pris.json with the links and timestamp. 
So if 1 ad contains two different prices at 2 different timestamps, it is easier to find out the change in price.


Project uses json2html to convert json format to an html table representation. 

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

BROWSE:<br />

Display: <br / >
1. To retrieve the list of realstate ads on finn. Type: <br />
    http://localhost:5000/links <br />
2. To retrieve the links of prices per ad. Type: <br />
    http://localhost:5000/price <br />
3. To retrieve links which are scanned and inserted during particular ammount of time. <br />
   Input format: YYYY-MM-DD (date=YYYY-MM-DD:YYYY-MM-DD) <br />
   Case 1: Links between start time and end time: <br />
           http://127.0.0.1:5000/links?date=2019-07-16:2019-07-18 <br />
           http://127.0.0.1:5000/price?date=2019-07-16:2019-07-17 <br />
   Case 2: Links between start time and now: <br />
           http://127.0.0.1:5000/links?date=2019-07-16:now <br />
           http://127.0.0.1:5000/price?date=2019-07-16:now <br />
   Case 3: Default-All the links <br />
           http://127.0.0.1:5000/links <br />
4. To retrieve links which have multiple prices associated with them.<br />
    http://127.0.0.1:5000/price?multiple=yes <br />
5. To retrieve price info on the basis of finnId. <br />
    http://127.0.0.1:5000/price?finnId=152134929 <br />

SCAN and DISPLAY: <br />
1. To scan finn.no and save the links to links.json <br />
    http://127.0.0.1:5000/links?scan=yes <br />
2. To scan the links.json and parse the price to pris.json <br />
    http://127.0.0.1:5000/price?scan=yes <br />

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
  
BROWSE:<br />
You can see the app link on your azure account under app services. And after shell deployment the link will be displayed on your screen as well.
1. To retrieve the list of realstate ads on finn. Type:
    http://app-name.azurewebsites.net/links
2. To retrieve the links of prices per ad. Type:
    http://app-name.azurewebsites.net/price
3. Same browsing links apply to azure app. Simple replace the hostname.
