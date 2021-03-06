Recipe Site
=============
A milestone project displaying capabilities in HTML, CSS, Javascript, Python, the Flask framework and SQLAlchemy and Flask-SQLAlchemy toolkits.
The project is a site containing food recipes, which users register accounts, add their own recipes, search through other recipes, etc.
The project makes use of the MaterializeCSS framework for front end styling and functionality.

The project can be found [here](http://recipe-app-m4.herokuapp.com)

UX
---------------
The intended users are as follow:
* Users interested in sharing their recipes with others
    * Users are able to create an account and upload their recipes (method, ingredients, image, etc.) which are publicly viewable
* Users looking to heavily promote their recipes to others
    * The site makes use of a view counter feature, which increments when a registered user views a recipe. For users looking to promote their recipe, being viewed by a large number of people, they can make use of this view counter and become a 'popular recipe' (which is featured more prominently on the site). 
* Users who wish to store their recipes online for future reading
    * By creating an account and uploading their recipes, users are able to view their recipe from anywhere at a later date 
* Users looking for information on particular recipes
    * The sute makes use of search feature, allowing users to search for recipe names. Using this feature, users can locate a recipe and see information they want to view (e.g. ingredients, method, etc.) 
* Users who want to find allergy/dietary information for particular dishes
    * Every ingredient added to the site is marked with relevant allergy/dietary requirement information (vegan, vegetarian or gluten free). Using the search feature, users can find particular recipes and see the allergy/dietary information of the dishes
    * *As a learning project, the dietary/allergy information of the ingredients may not be accurate. It instead is used to display the possible functionality.*
* Users interested in finding dishes similar to those they have a preference for
    * The site makes use of a related recipes feature, displaying similar recipes to the one the user is currently viewing. This feature can be used to find similar recipes to those the user has a preference for already
* Users looking for recipes based on particular criteria:
* Dietary/allergy information
    * For users wishing to find recipes based on dietary/allergy information, the site makes use of vegan, vegetarian and gluten free search filters 
* Ingredients they have available
    * For users wishing to find recipes based on particular ingredients they have, the site makes use an ingredients search filter
* The number of people they are required to serves
    * For users looking to find recipes based on how many it serves, the site makes use of a 'serves amount' search filter 
* The amount of time they have available to cook
    * For users looking to find recipes based on how long it takes to cook, the sites makes use of a 'time takes to cook' search filter 
* The difficulty of the recipe
    * For users looking for a challenging recipe or something simple, the site makes use of a difficulty search filter 

Wireframes can be found [here](https://github.com/mdenoronha/milestone-project-4/tree/master/static/imgs/wireframes)

The following alterations were made after the mock-up phase:
* Change of colours used on recipe page for recipe information and view counter
* Input fields on register page being fill width
* Menu options in header

Features
---------------
### Existing Features ###
*Creating a user*
* Users are able to enter their name, and a username and password, to the register form to create an account which is added to the database
* Other users are not able to register the same username, giving a unique account for users to make use of
* Usernames are saved to a user's session, allowing them leave the site and return logged in (within limitations of session cookie)
* Users are able to log out of their account by clicking the log out icon
* Users are able to log in at anytime using the login button

*Updating user information*
* Users are able to change all information on their account in their account section
* Security checks only allow users who are aware of an account's password to make changes

*Adding a recipe*
* Users are able to add a recipe using the add recipe link. Users are able to add:
    * Recipe name
    * The number of people the recipe serves
    * The amount of time it takes to cook the recipe
    * The difficulty of the recipe
    * The ingredients used and the amount of each ingredient
    * The dietary information of each ingredient
    * The method of cooking the recipe
    * An image for the recipe
* A 3 step adding recipe process is utilised to make adding a recipe simple, allowing users to navigate back and forth steps
* A final preview is offered allowing users to see how it will appear before the final submission

*Updating a recipe*
* Once a recipe is added, users are able to make edits at anytime by clicking the update button on the recipe page
* All information is pre-entered, making it easy to keep many changes of the recipe
* Only logged in users who own the recipe can submit an update

*Deleting a recipe*
* Once a recipe is added, users are able to delete the recipe at anytime by clicking the delete button on the recipe page
* Only logged in users who own the recipe can successfully delete it

*Searching through recipes*
* Users are able to search through all recipes from the search bar on the homepage and the search page.
* Filters can be applied, allowing users to filter recipes based on allergy/dietary information, difficulty, ingredients used, etc. 

*Other features*
* Message popups are used throughout (e.g. logging out, creating a recipe) to inform users of a successful/unsuccessful action

### Features Left to Implement ###
* The related recipes feature makes use of basic recommendation functionality, filter recipes depending on whether they use the same keywords. As the related recipes list is completed once 3 recipes are found, related recipes based on keywords later in their title may be overlooked. Similarly, _more relevant_ recipes may be ignored. A more advanced recommendation feature can be implemented to overcome this.
* The site does not make use of secure authentication, with passwords being saved unencrypted. Secure authentication would be a beneficial feature to add.

Technologies Used
---------------
* Python was used extensively in the creation of the app
* A number of modules were used within the app:
    * Flask framework necessary for building web application
    * flask-sqlalchemy, an extension of toolkit sqlalchemy, used to interact with the database
    * flask_s3 and boto3 used to connect to and write to S3 bucket
    * random module used to create random string
* Heroku Postgres was used as the SQL database management system
* AWS S3 was used for data storage of recipe image files
* Javascript was used to aid front end functionality
* The MaterializeCSS framework was used for front end functionality, specific HTML componenents and CSS styling
* The wNumb.js library was used to aid MaterializeCSS's slider feature
* noUiSlider was used to aid MaterializeCSS's slider feature
* jQuery library was used to aid the creation of front end functionality
* unittest was used to build the testing framework
* flask_testing was used to aid testing framework and its connection to Flask app and database connection

Testing
---------------
Python testing document can be found [here](https://github.com/mdenoronha/milestone-project-4/blob/master/app_test.py)
The file is run by using 'python app_test.py' command
The testing file uses these records and should be present in the database when testing:
Users
* username = "testing-account-viewed-recipe"
* username = "mstonieri"
* username = "testing-account-not-viewed-recipe"

Recipes
* name = "star-pizzas" user_id = 19

viewed_recipe
* user = "testing-account-viewed-recipe" recipe = "star-pizzas"

The following records must not exists:
viewed_recipes
* user = "testing-account-not-viewed-recipe" recipe = "star-pizzas"

### Testing through app_test.py ###
Test  | Status
------------- | -------------
Testing 200 Responses |
Visiting homepage returns a 200 response | Successful
Visiting search returns a 200 response | Successful
Visiting recipe page returns a 200 response | Successful
Visiting register page returns a 200 response | Successful
Visiting login page returns a 200 response | Successful
Visiting add recipe info returns a 200 response when the appropriate attributes are met | Successful
Visiting add recipe ingredients returns a 200 response when the appropriate attributes are met | Successful
Visiting add recipe submit returns a 200 response when the appropriate attributes are met | Successful
Visiting update recipe info returns a 200 response when the appropriate attributes are met | Successful
Visiting update recipe ingredients returns a 200 response when the appropriate attributes are met | Successful
Visiting update recipe submit returns a 200 response when the appropriate attributes are met | Successful
View Count |
View counts increases by one when a recipe is visited by a registered user for the first time | Successful
View counts doesn't increase by one when a recipe is visited by a registered user but not for the first time | Successful
Database Connection |
Post to add recipe submit adds session data as database record | Successful
Post to update recipe submit updates a database record to session data | Successful
Visiting delete removes a database record when the appropriate attributes are met | Successful


### Manual Testing ###
Test  | Status
------------- | -------------
Homepage |
The autocomplete search bar on the homepage displays suggestions based on user input | Successful
Selecting an autocomplete option takes user to the relevant recipe page | Successful
The Special Diets section becomes a slider on mobile and can be utilised | Successful
Search |
The MaterializeCSS chips functionality on the ingredients input can be utilised as intended | Successful
The MaterializeCSS serves slider works as intended | Successful
The MaterializeCSS time slider works as intended | Successful
Changing the MaterializeCSS chips updates a hidden input | Successful
Changing the MaterializeCSS serves slider updates a hidden input | Successful
Changing the MaterializeCSS ingredients updates a hidden input | Successful
Selecting the vegan option in recipe type also selects vegetarian | Successful
Selecting the vegetarian option when the vegan option is selected removes the vegan option | Successful
The filters section becomes a collapsible section on mobile | Successful
The reset filters option becomes selectable when any of the filters are not at the default position | Successful
Selecting the reset filters resets all filters to their default position | Successful
The pagination distributes the recipes across the necessary number of pages | Successful
The pagination can be navigated as intended | Successful
Recipe Page |
The serves result matches the recipe's record | Successful
The difficulty result matches the recipe's record | Successful
The time result matches the recipe's record | Successful
The views result matches the recipe's record | Successful
If all ingredients are marked vegetarian, vegetarian result is active | Successful
If all ingredients are marked vegan, vegan result is active | Successful
If all ingredients are marked gluten free, gluten free result is active | Successful
The method result matches the recipe's record | Successful
The amount and ingredient results match the recipe_ingredients table | Successful
If available, 2-3 recipes with matching keywords are visible in the related recipes section with a 'Related Recipes' title | Successful
If not available, the top 3 most viewed recipes are visible with a 'Popular Recipes' title | Successful
If the recipe belongs to the user, the edit and delete option is available | Successful
Selecting the update recipe option takes the user to update-recipe of the relevant recipe | Successful
Selecting delete recipe and confirming removes the recipe and ingredients from the database | Successful
Register |
Entering user details and submitting creates a relevant record in the database | Successful
Login |
Entering invalid username fails login and flashes message | Successful
Entering incorrect password fails login and flashes message | Successful
Entering correct login information adds username to session | Successful
Add Recipe - Info |
Uploading an incorrect file type fails upload and flashes message | Successful
Uploading a file over 500kb fails upload and flashes message | Successful
Adding details and submitting adds information to session | Successful
Navigating away from the page and returning keeps information in inputs (exc. image) | Successful
Add Recipe - Ingredients |
Selecting vegan also select vegetarian of the relevant ingredient | Successful
Clicking plus adds a new ingredient option | Successful
Clicking delete removes the ingredient option | Successful
After 21 ingredients, the add ingredient option is no longer selectable | Successful
Adding details and submitting adds information to session | Successful
Navigating away from the page and returning keeps information in inputs | Successful
Add Recipe - Submit |
The serves result matches the added recipe's record | Successful
The difficulty result matches the added recipe's record | Successful
The time result matches the added recipe's record | Successful
The views result matches the added recipe's record | Successful
If all added ingredients are marked vegetarian, vegetarian result is active | Successful
If all added ingredients are marked vegan, vegan result is active | Successful
If all added ingredients are marked gluten free, gluten free result is active | Successful
The method result matches the added recipe's record | Successful
The amount and ingredient results match the added recipe_ingredients records | Successful
Clicking submit adds information to database | Successful
Update Recipe - Info |
Inputs are prefilled with relevant recipe information | Successful
Clicking Change Image shows input | Successful
Clicking cancel hides input and shows original image | Successful
Uploading an incorrect file type fails upload and flashes message | Successful
Uploading a file over 500kb fails upload and flashes message | Successful
Adding details and submitting adds information to session | Successful
Update Recipe - Ingredients |
Inputs are prefilled with relevant recipe information | Successful
Selecting vegan also select vegetarian of the relevant ingredient | Successful
Clicking plus adds a new ingredient option | Successful
Clicking delete removes the ingredient option | Successful
After 21 ingredients, the add ingredient option is no longer selectable | Successful
Adding details and submitting adds information to session | Successful
Add Recipe - Submit |
The serves result matches the updated recipe's record | Successful
The difficulty result matches the updated recipe's record | Successful
The time result matches the updated recipe's record | Successful
The views result matches the updated recipe's record | Successful
If all updated ingredients are marked vegetarian, vegetarian result is active | Successful
If all updated ingredients are marked vegan, vegan result is active | Successful
If all updated ingredients are marked gluten free, gluten free result is active | Successful
The method result matches the updated recipe's record | Successful
The amount and ingredient results match the updated recipe_ingredients records | Successful
Clicking submit updates record in the database | Successful
My Account | 
Clicking Add New takes user to add recipe - info page | Successful
My Recipe dropdown shows all recipes belonging to user | Successful
Account Details show user account information | Successful
Selecting edit option makes input editable | Successful
Entering incorrect password fails account update and flashes message | Successful
Entering correct password updates user information and flashes message | Successful

Deployment
---------------
Project has been deployed to Heroku and is accessible [here](http://recipe-app-m4.herokuapp.com/).
The process for deployment was as follows:
* Clicked New and and Create New app on Heroku
* Add an app name, location and click Add App
* Log into Heroku via the terminal using $ heroku login
* All instances of '= 0' in SQL statements need to be changed to '= false' for Heroku
* Create a new git repository using $ git init
* Connect to Heroku app using $ heroku git:remote -a recipe_app
* Within the terminal created requirements.txt file with dependencies
* Create Procfile to inform app.py is to be run
* Update app's PORT and IP to correspond with Heroku
* Add files to git using $ git add .
* Commit files to git using $ git commit -m "Initial commit"
* Push to Heroku using $ git push heroku master

Credits
---------------
* Assistance from [here](https://stackoverflow.com/questions/13620051/heroku-push-of-django-app-gets-no-module-named-psycopg2-extensions) for psycopg2-binary in requirements.txt
* Assistance from [Flask documentation](http://flask.pocoo.org/docs/1.0/patterns/fileuploads/) for file upload verification
* Assistance from [here](https://kite.com/python/docs/sqlalchemy.engine.result.ResultProxy) on working with ResultProxy 
* Assistance from [here](https://stackoverflow.com/questions/19884900/how-to-pass-dictionary-from-jinja2-using-python-to-javascript) on passing dict from Python to JS
* Assistance from CI tutor on save_profile_picture function to add image to S3 bucket
* Homepage background photo provided by Canva
* Social icons provided by Canva
* Vegetarian Photo by Anh Nguyen on Unsplash
* Vegan Photo by Anna Pelzer on Unsplash
* Gluten free Photo by Wesual Click on Unsplash
* Added recipe images and information provided by [Tesco Recipes](https://realfood.tesco.com/recipes.html)