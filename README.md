<h1>Lead generation app (Django)</h1>
<h2>Descriptions project</h2>
<h4>The goal of the project is to develop a lead generator that will collect information on keywords in given locations and store in the database.
  The source of data is Google Maps. The table must contain the following mandatory fields: object name, full address, phone, website URL, and email.
  The program must issue at least 30 fully filled positions for one keyword. It is assumed that the developer will use selenium to build the scraper,
  but any other libraries are not excluded.</h4>


   <h2>Technologies used in the project</h2>
  <div>
    <img src="https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white&color=9cf" alt="Python Badge"/>
    <img src="https://img.shields.io/badge/Django-green?style=for-the-badge&logo=django&logoColor=white&color=brightgreen" alt="Django Badge"/>
    <img src="https://img.shields.io/badge/Postgres-green?style=for-the-badge&logo=postgresql&logoColor=white&color=informational" alt="Postgresql Badge"/>
    <img src="https://img.shields.io/badge/Docker-blue?style=for-the-badge&logo=docker&logoColor=white&color=blue" alt="Docker Badge"/>
    <img src="https://img.shields.io/badge/Selenium-blue?style=for-the-badge&logo=selenium&logoColor=white&color=informational" alt="Selenium Badge"/>
  </div>
    <h2>Run project</h2>
  <ul>
  <li>Download and install <a href='https://docs.docker.com/get-docker/'>Docker</a></li>
  <li>Clone repository: <code> git clone https://github.com/KLYMENKORUS/Test_API_Deribit</code></li>
  <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
  <li>At the level with the root directory <code>src</code> create a .env file and fill it like .env.example</li>
  <li>Run command <code>docker compose -f docker-compose.yaml up -d</code></li>
  <li>Run migration <code>python manage.py</code> and command <code>python manage.py runserver</code></li>
  <li>Run the command to start the lead generator <code>python lead_generator.py</code></li>
  </ul>
