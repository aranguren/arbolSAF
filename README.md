# ArbolSAF
Deploying using Docker
In these manual we will explain how to deploy Arbolsaf web application using docker commands for Ubuntu OS.

Step 1: Docker installation (Optional)
These step is only nedded if docker has not been previously installed. First, update your packges list:
sudo apt update

After that,install some nedded packages for using apt through HTTPS:
sudo apt install apt-transport-https ca-certificates curl software-properties-common

Later, is important to add GPG key for accessing Docker official repository:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

You should add Docker repository to the APT sources
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"

Next,update again your packages list to get access docker packages list.
sudo apt update

Before installing docker,be sure you are about to install from the Docker repository instead of the default Ubuntu repository:
apt-cache policy docker-ce

Although the Docker version number may be different, you will see output like the following: Note that docker-ce is not installed, but the most viable option for installation is from the Docker repository for Ubuntu 20.04 (focal).

Finally, install Docker:
sudo apt install docker-ce

With this, Docker will be installed, the daemon will start, and the process will be enabled to run at startup. Check that it works:
sudo systemctl status docker

The output should be similar to the following, showing that the service is up and running: Installing Docker will now provide you with not only the Docker service (daemon) but also the docker command line utility or the Docker client.
Step 2: Get the application code

You should download the application code from github by clonning it like this if github is previously installed or download it from github:
git clone https://github.com/aranguren/platformSAF
or access github to donwload
https://github.com/aranguren/platformSAF
It is very important to modified .env with enviroment variables for accesing the database server.This .env file is located in /core file directory inside the project code.Enviroment variables should see laike this:

    <li>DEBUG=False</li>

    SECRET_KEY=your_super_secret_key
    SERVER=boilerplate-code-django-dashboard.appseed.us
    DATABASE_NAME=your_database_name
    DATABASE_USER=your_database_user
    DATABASE_PASS=your_database_pass
    DATABASE_HOST=your_database_host
    DATABASE_PORT=your_database_port

Step 3: Get the images to use
In this step, the images required to run the system will be downloaded. Docker will only download them if you don't have it locally. Being in the project directory, run the following command:
sudo docker-compose pull
Docker will download and save the obtained images to build the system in the next step.
Step 4: Build the images
Now we will proceed to build the system using the images downloaded in the previous step. Being in the project directory, run the following command:
sudo docker-compose build
Docker will build the system into their respective containers and be ready to mount.
Step 5: Mount system containers
Finally, we will proceed to mount the system containers in docker. Being in the project directory, run the following command:
sudo docker-compose up -d

The -d option will allow the system to run in the background. This command is the one that will be used every time it is necessary to start the system. This will be exposed at
http://localhost:8000
If this is the first time the system has been run, go to step 6

Step 6: Create the Database
The database must be created the first time the application is run. With the system running (Step 5), run the following command:
docker-compose exec db bash
This will allow you to enter database container command line window.

With the above command executed, enter the following:
psql -U docker -p 5432 -h localhost -d postgres
This will allow you to enter postgres command line window.

Now lets create database:
create database saf;
Pressing enter should show that the database has been successfully created. To exit the postgres command window type this command and press enter:
/q
To exit the database command window type this command and press enter:
exit
Step 7: Run migrations and initial system data
To run the system migrations, the database must be created (Step 6). With the system running (Step 5), run the following command:
docker-compose exec web bash
This will allow you to enter the web system command window

With the above command executed, enter the following:
python3 manage.py makemigrations
This will initiate the creation of the necessary migrations for the system.

With the migrations created, run the following command:
python3 manage.py migrate
This command will create the necessary tables for the system in the database.

With the tables created in the database, run the following command:
python3 manage.py loaddata ./fixtures/initial_data.json
This command will populate the tables with the necessary data for the correct execution of the system.
Step 8: Create super user
python3 manage.py createsuperuser

Finally, to exit the web command window, run:
exit
