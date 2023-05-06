<p align="center">
  <img src="https://github.com/sacramento-state-biology-collections/bre-react-app/blob/main/public/manifest-icon-512.maskable.png?raw=true" style="width: 70%; height: auto">
</p>

&nbsp;

# Biology Research Engine (BRE)

## About

The California State University of Sacramento's Biology Department has ~7000 collections and they wanted a way to manage them digitally. They asked us to create an easily accessible and reliable database software that would allow both faculty members and students of the school to edit or review the university's data collections, laboratories, and museums. We created an app where users can search through the databases and the faculty can sign in and modify the collection data.

## Features

The application communicates with the provided specific collections of the department, giving visiting users read access. The ability to edit or delete is only provided to those who are faculty of the department, as they are the people who can alter the database accurately according to the collections of the department.

## Purpose

The application was created in order to provide the Biology Department with a cleaner, user-friendly, and straightforward database that they can manage and uphold to provide necessary information about the collections of species that the department obtains. Originally, the collections were held under an excel file which had a long list of entries, thus adding, removing, or managing the file was an inconvenience they had to deal with on a daily basis. Our application gives them the ability to use excel sheets combined with a user-friendly application which can communicate with the database and help them manage it much more easily.

## App Screenshots

<p align="center"><br>
  <strong>Home Page</strong>
  <img src="https://github.com/sacramento-state-biology-collections/sacramento-state-biology-collections.github.io/blob/main/static/img/readme/Home.png?raw=true" style="width: 100%; height: auto"><br><br>
  
</p>

This is the home page where the user can either go to the BRE search engine to search through the collecions, or go to the admin login screen.

<p align="center"><br>
  <strong>PWA (Progressive Web Application)</strong>
  <img src="https://github.com/sacramento-state-biology-collections/sacramento-state-biology-collections.github.io/blob/main/static/img/readme/PWA.png?raw=true" style="width: 100%; height: auto"><br><br>
  
</p>

This is an option for the user to download the app off of the browser to user locally.

---

## Search Engine

<p align="center"><br>
  <strong>Quick Search</strong>
  <img src="https://github.com/sacramento-state-biology-collections/sacramento-state-biology-collections.github.io/blob/main/static/img/readme/QuickSearch.png?raw=true" style="width: 100%; height: auto"><br><br>
  
</p>

This is the quick search page where the user can click on a collection to view all of the specimens or search for a specific one using the search bar.

<p align="center"><br>
  <strong>Search List View</strong>
  <img src="https://github.com/sacramento-state-biology-collections/sacramento-state-biology-collections.github.io/blob/main/static/img/readme/Search.png?raw=true" style="width: 100%; height: auto"><br><br>
  
</p>

This is the page that shows a list of all the results of what you searched, or all the specimens of the collections you chose to quick search for. There is also an option to change between this list view and a card view to change how the search results are presented.

<p align="center"><br>
  <strong>Search Card View</strong>
  <img src="https://github.com/sacramento-state-biology-collections/sacramento-state-biology-collections.github.io/blob/main/static/img/readme/CardView.png?raw=true" style="width: 100%; height: auto"><br><br>
  
</p>

This is an alternate search view that allows you to see all the results in a more visual manner by showing the image of the specimen if there is one in the database, or a filler image if not.

<p align="center"><br>
  <strong>Info Card</strong>
  <img src="https://github.com/sacramento-state-biology-collections/sacramento-state-biology-collections.github.io/blob/main/static/img/readme/Card.png?raw=true" style="width: 100%; height: auto"><br><br>
  
</p>

This is a pop-up view of the specimen you click on that shows you the picture and all the information the list view provides. There is an option to view all the information for that specimen.

<p align="center"><br>
  <strong>Full Data View</strong>
  <img src="https://github.com/sacramento-state-biology-collections/sacramento-state-biology-collections.github.io/blob/main/static/img/readme/Full.png?raw=true" style="width: 100%; height: auto"><br><br>
  
</p>

This is the page that shows all the details of the specimen that is stored in the database.

---

## Admin

<p align="center"><br>
  <strong>Login</strong>
  <img src="https://github.com/sacramento-state-biology-collections/sacramento-state-biology-collections.github.io/blob/main/static/img/readme/Login.png?raw=true" style="width: 100%; height: auto"><br><br>
  
</p>

This is where someone with an admin account can sign into the app to make changes or view the history of the collections.

<p align="center"><br>
  <strong>Collection Panel</strong>
  <img src="https://github.com/sacramento-state-biology-collections/sacramento-state-biology-collections.github.io/blob/main/static/img/readme/CollectionPanel.png?raw=true" style="width: 100%; height: auto"><br><br>
  
</p>

This displays all the collections that the admin can modify. There is the option to edit the data, download a csv file of all the data of the collection, or upload a csv file to update the collection. There is also the option to view the history of a collection at the top.

<p align="center"><br>
  <strong>History Page</strong>
  <img src="https://github.com/sacramento-state-biology-collections/sacramento-state-biology-collections.github.io/blob/main/static/img/readme/History.png?raw=true" style="width: 100%; height: auto"><br><br>
  
</p>

This is the page that shows all the past versions of the data and allows the user to download a csv file of it to either view what the data was at a point in the past, or to reupload it and revert the collection data to an older version to undo any unwanted changes.

<p align="center"><br>
  <strong>Edit Search</strong>
  <img src="https://github.com/sacramento-state-biology-collections/sacramento-state-biology-collections.github.io/blob/main/static/img/readme/EditSearch.png?raw=true" style="width: 100%; height: auto"><br><br>
  
</p>

This is a very similar search to the search list view shown above, but instead of displaying data, this allows you to choose a specimen that you need to modify data for.

<p align="center"><br>
  <strong>Collection Editor</strong>
  <img src="https://github.com/sacramento-state-biology-collections/sacramento-state-biology-collections.github.io/blob/main/static/img/readme/EditCollection.png?raw=true" style="width: 100%; height: auto"><br><br>
  
</p>

This is where the user can edit the data within the app. It displays all the data of a specific specimen and the user can edit the text box to make any necessary changes. There is also the option to upload a photo for the specimen.

## Deployment

1. Install git, docker, & docker-compose.

2. Clone both `bre-react-app` & `bre-flask-server` into a desired directory.

   ```shell
   git clone https://github.com/sacramento-state-biology-collections/bre-react-app.git
   git clone https://github.com/sacramento-state-biology-collections/bre-flask-server.git
   ```

3. Create a compose file for the software stack called `docker-compose.yml`. (this file should be in the same directory as the cloned repositories)

   ```shell
   touch docker-compose.yml
   ```

4. Fill the compose file with the desired configuration. Example below:

   ```yaml
   version: "3.9"

   services:
     frontend:
       build: bre-react-app
       ports:
         - "80:3000"
       networks:
         bre_network:
           ipv4_address: 10.0.1.2

     backend:
       build: bre-flask-server
       ports:
         - "9001:9001"
       networks:
         bre_network:
           ipv4_address: 10.0.1.3

     database:
       image: postgres:latest
       ports:
         - "5432:5432"
       environment:
         - POSTGRES_USER=postgres
         - POSTGRES_PASSWORD=glueware@grems
         - POSTGRES_DB=biologydb
       volumes:
         - ./bre-flask-server/scripts/create_tables.sql:/docker-entrypoint-initdb.d/create_tables.sql
         - ./bre-flask-server/scripts/insert_data.sql:/docker-entrypoint-initdb.d/insert_data.sql
       networks:
         bre_network:
           ipv4_address: 10.0.1.4

   networks:
     bre_network:
       ipam:
         driver: default
         config:
           - subnet: 10.0.1.0/24
   ```

5. Run the stack by executing the docker compose command.
   ```shell
   docker compose up
   ```

## Testing

1. To run tests, clone `bre-react-app`.

   ```shell
   git clone https://github.com/sacramento-state-biology-collections/bre-react-app.git
   ```

2. Change directory to the `bre-react-app` and install node dependencies.

   ```shell
   cd bre-react-app
   npm install
   ```

3. Run the node command to run test scripts
   ```shell
   npm run test
   ```

## Contributions

<a href="https://github.com/sacramento-state-biology-collections/bre-react-app/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=sacramento-state-biology-collections/bre-react-app" />
</a>

- Brian Almaguer
- Joseph May
- Lauren Prather
- Ivan Yuen
- Kelly Bringino
- Leonardo Anguiano
- Tawheed Bayaz
- Evan Boswell
- Lukas Dolansky
