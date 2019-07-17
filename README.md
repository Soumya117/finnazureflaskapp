# finnazureflaskapp

The python project will parse finn.no and present the results.
The parsing includes:
1. Scanning for new ads of realstates.
2. Scanning each realstate ad and parsing the price.

The app will return the recorded change in price. The ads are stored in links.json along with the time stamp. So its possible to find out when the link was first seen on finn. The prices are stored in pris.json with the links and timestamp. 
So if 1 ad contains two different prices at 2 different timestamps, it is easier to find out the change in price.


Project uses json2html to convert json format to an html table representation. 

LOCAL

DEPLOYMENT:
App can be deployed locally using flask. 
1. Clone the project.
2. Enter the project directory.
3. Enter following commands:
   python3 -m venv venv
   source venv/bin/activ
   pip install -r requirements.txt
4. Run the project by entering the following command:   
   FLASK_APP=application.py flask run
   This will start the flask and you can browse your app on the localhost.

BROWSE:
1. To retrieve the list of realstate ads on finn. Type:
    http://localhost:5000/links
2. To retrieve the links of prices per ad. Type:
    http://localhost:5000/price
    
    
CLOUD (MICROSOFT AZURE)

DEPLOYMENT:
I have deployed this app on my azure account. 
1. Get a free azure account (or paid if you can).
2. Enter the cloud shell.
3. Clone the project.
4. Enter the project directory and run the following command: 
   az webapp up -n <app-name>
5. Using cloud shell, you can makes changes to the code and then deploy it back with the same command.
  
BROWSE:
You can see the app link on your azure account under app services. And after shell deployment the link will be displayed on your screen as well.
1. To retrieve the list of realstate ads on finn. Type:
    http://app-name.azurewebsites.net/links
2. To retrieve the links of prices per ad. Type:
    http://app-name.azurewebsites.net/price
