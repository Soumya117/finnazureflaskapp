# finnazureflaskapp

The python project will parse finn.no and present the results.
The parsing includes:
1. Scanning for new ads of realstates.
2. Scanning each realstate ad and parsing the price.
3. Scanning for sold houses.
4. Listing all the visnings.

The ads are stored in links.json along with the time stamp. So its possible to find out when the link was first seen on finn. The prices are stored in pris.json with the links and timestamp. So if 1 ad contains two different prices at 2 different timestamps, it is easier to find out the change in price.

It also tells you the SOLD status. Finn.no doesnt display the sold houses in the search. If the link is saved somewhere it is easy to browse it and see the sold houses. The webapp scans links and records the status changes.
Additionaly it also collects all the visnings.

The app is triggered by an azure timer function so it collects data in the background and store the json in the Azure Storage Blob.

DEPLOYMENT:<br />
LOCAL

1. Clone the project.
2. Enter the project directory.
3. Enter following commands: <br />
   python3 -m venv venv <br />
   source venv/bin/activate <br />
   pip install -r requirements.txt <br />
4. Run the project by entering the following command:   
   FLASK_APP=application.py flask run <br />
   This will start the flask and you can browse your app on the localhost.

MICROSOFT AZURE

1. Get a free azure account (or paid if you can).
2. Enter the cloud shell.
3. Clone the project.
4. Enter the project directory and run the following command: 
   az webapp up -n "app-name"
5. Using cloud shell, you can makes changes to the code and then deploy it back with the same command.
6. Since now the /price request takes long time to load, the app timed out. So i changed the startup configuration using        command: az webapp config set --resource-group "resource-group" --name "app-name" --startup-file "gunicorn --bind=0.0.0.0    --timeout 2000 application:app"

GOOGLE CLOUD 

1. For google cloud, i need to create app.yaml and add an entrypoint to main.py or application.py.
2. App is deployed on the cloud locally using :
   gcloud app deploy
3. The flask app is now deployed on the google app engine and the azure timer function sends the request to scan every 3 hours.

****************************************************************************************************************************

UPDATE: I am not running this app as an app service on GCP. I am running it as a daemon inside a GCP vm instance. The reason for this change was it was not really handling the huge requests well. It was getting timedout. 
For running it inside a vm instance as a daemon:
1. Create a VM instance.
2. Git clone this project there.
3. Change the required keys (gmaps and azure blob)
4. Create a conf file inside /etc/supervisor/conf.d/ as finnazureflaskapp.conf. 
5. Write the conf file with following:<br />
   [program:finn-flask-app]<br />
   directory=/home/soumya/python/finnazureflaskapp<br />
   command=python main.py<br />
   autostart=true<br />
   autorestart=true<br />
   stopsignal=INT<br />
   stopasgroup=true<br />
   killasgroup=true<br />
6. Run sudo /usr/bin/supervisord. Make sure no other supervisor processes are running. (sudo ps -ax | grep 'supervisor').
7. Enter sudo supervisorctl and check your app.

After this architectural change, there is a timer daemon running inside the vm that will schedule the scans. 

****************************************************************************************************************************

UPDATE Again: So i changed the arhitecture a little bit. I wanted to run prometheus, grafana and elk service along with my python web app. So i found out that good solution will be to dockarize it. So every thing is now running as dockers.
Changes: 
1. docker-compose.yml contains configuration of the webapp.
2. docker-compose-infra.yml contains configuration of prometheus, grafana, elastic search and kibana.
3. To start the dockers, just navigate to the project folder and run sudo bash start.sh.This script will perform a docker        build and fire up the required containers.
4. After all the dockers are running, run install_filebeat.sh to install and start filebeat service. Change the configuration in /etc/filebeat/filebeat.yml and restart filebeat.

****************************************************************************************************************************

Services and ports<br/ ><br/ >
Prometheus: 9090<br/ >
Grafana: 3000<br/ >
ElasticSearch: 9200<br/ >
Kibana: 5601<br/ >

Since the dockers are running inside the VM, i have to open some ports to access prometheus and grafana. That can be done by enabling some firewalls. For ex: <br />
gcloud compute firewall-rules create allow-http-5000 \
    --allow tcp:5000 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server \
    --description "Allow port 5000 access to http-server" <br />
To tail docker-compose logs: sudo docker-compose logs --tail="all" -f
ARCHITECTURE

![alt text](https://github.com/Soumya117/finnazureflaskapp/blob/master/app/Selection_152.png) <br /><br />
