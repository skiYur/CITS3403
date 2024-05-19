# CITS3403 Group Project - Mix'd Opinion

# Purpose of the application
Mix'd Opinions is a platform designed for enthusiasts of both alcoholic and non-alcoholic beverages. It allows users to explore, share, and discuss detailed reviews of various drinks of their likings. The site aims to create a community where users can learn about new beverages, understand different taste profiles, and explore drinks from different continents. The application features a user-friendly interface that categorizes drinks into alcoholic and non-alcoholic sections. The alchohl category offers further sub-categories like Vodka, Gin, Whiskey, etc., for alcoholic beverages and similar classifications for non-alcoholic options. Users can contribute by posting their drink recipe, drink review, rating drinks, and engaging with community discussions through commenting system.

# Architecture of the our application.

Presentation Layer: Handled through HTML, CSS, and JavaScript, ensuring a responsive user interface. Bootstrap was used to maintain visual consistency and responsiveness across various devices.

Business Logic Layer: Flask was used whihc is a Python web framework. It handled request processing, authentication, database operations, and serves as the middleware between the user interface and the database.

Data Access Layer: Utilizes a relational database management system (such as PostgreSQL or MySQL) to manage all data related to users, drink reviews, and community interactions. SQLAlchemy is employed for ORM capabilities to interact with the database through Python.

# How to use, run and test the application. 

Firstly, run pip install -r requirements.txt
After, you can run the application by - flask run or run the 'python3 Project.py' command, this will start a development server
Open it in web browser and the loading/homepage should display. You can signup and use the application. 

Testing the Application:
Ensure your tests are in a directory (e.g., `/tests`). You can run them using: python -m unittest discover -s tests
You can perform functional testing by interacting with the application through the browser or using tools like Selenium to automate the browser or loading testing and see
how it behaves under stress. 

# Members 

| UWA Student Number | Name | Github User Name |
| :---:              |     :---:      |     :---:       |
| 23482415           | Shashwat Abrol    | skiYur       |
| 23416986           | Ben Samson Daniel | Lockdauun, Lockdxwn|
| 23335344           | Matei Hepcal      | mateihepcal24|
| 23348892           | Dilan Anand       | 23348892     |

Referencing free images: 
https://www.pexels.com/search/drink/
https://www.pexels.com/photo/assorted-wine-bottles-1283219/

