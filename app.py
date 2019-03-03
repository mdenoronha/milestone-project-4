from flask import Flask, render_template, redirect, request, url_for, send_file, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os
import json
from flask_s3 import FlaskS3
import flask_s3
import boto3
import random
import string

app = Flask(__name__)
# SQL-Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///recipeapp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dsaf0897sfdg45sfdgfdsaqzdf98sdf0a'
# AWS
app.config['FLASKS3_BUCKET_NAME'] = "recipe-db"
app.config['FLASKS3_ACTIVE'] = False

s3 = FlaskS3(app)
db = SQLAlchemy(app)

def create_pagination_num(total_pages, page):
    
    pagination_num = []
    for counter, p in enumerate(range(0,total_pages)):
        if len(pagination_num) > 5:
            break
        if total_pages < 6 or page > total_pages - 3:
            for counter, p in enumerate(range(0,5)):
                if total_pages - counter > 0:
    
                    pagination_num.insert(0, total_pages - counter)
            break
        # Added to ensure active number is in middle of pagination where possible
        else:
            if page + counter - 2 > 0 and page + counter - 2 < total_pages:
                print(total_pages)
                pagination_num.append(int(page + counter - 2))
                
    return pagination_num

def return_search(recipe_type, search_term, page):
    if not recipe_type:
        checkboxes = [None, None, None]
        result = (Recipe.query
        .filter(Recipe.name.contains(search_term))
        .order_by(Recipe.views.desc())
        .paginate(page, 15, False))
    elif "vegan" in recipe_type and "gluten-free" in recipe_type:
        checkboxes = ["vegan", "vegetarian", "gluten_free"]
        result = (Recipe.query
        .filter(Recipe.name.contains(search_term))
        .filter(~Recipe.ingredients.any(Ingredients.is_vegan == False))
        .filter(~Recipe.ingredients.any(Ingredients.is_vegetarian == False))
        .filter(~Recipe.ingredients.any(Ingredients.is_gluten_free == False))
        .order_by(Recipe.views.desc())
        .paginate(page, 15, False))
    elif "vegan" in recipe_type:
        checkboxes = ["vegan", "vegetarian", None]
        result = (Recipe.query
        .filter(Recipe.name.contains(search_term))
        .filter(~Recipe.ingredients.any(Ingredients.is_vegan == False))
        .filter(~Recipe.ingredients.any(Ingredients.is_vegetarian == False))
        .order_by(Recipe.views.desc())
        .paginate(page, 15, False))
    elif "vegetarian" in recipe_type and "gluten-free" in recipe_type:
        checkboxes = [None, "vegetarian", "gluten_free"]
        result = (Recipe.query
        .filter(Recipe.name.contains(search_term))
        .filter(~Recipe.ingredients.any(Ingredients.is_vegetarian == False))
        .filter(~Recipe.ingredients.any(Ingredients.is_gluten_free == False))
        .order_by(Recipe.views.desc())
        .paginate(page, 15, False))
    elif "vegetarian" in recipe_type:
        checkboxes = [None, "vegetarian", None]
        result = (Recipe.query
        .filter(Recipe.name.contains(search_term))
        .filter(~Recipe.ingredients.any(Ingredients.is_vegetarian == False))
        .order_by(Recipe.views.desc())
        .paginate(page, 15, False))
    elif "gluten-free" in recipe_type:
        checkboxes = [None, None, "gluten_free"]
        result = (Recipe.query
        .filter(Recipe.name.contains(search_term))
        .filter(~Recipe.ingredients.any(Ingredients.is_gluten_free == False))
        .order_by(Recipe.views.desc())
        .paginate(page, 15, False))
            
    return result

# Assistance for function provided by CI tutor
def save_profile_picture(form_picture):          
    random_hex = ''.join([random.choice(string.digits) for n in range(8)])    
    _, f_ext = os.path.splitext(form_picture.filename)  
    picture_fn = random_hex + f_ext
    s3 = boto3.resource('s3')
    s3.Bucket('recipe-db').put_object(Key="static/recipe_images/" + picture_fn, Body=form_picture)
    
    return picture_fn 

recipe_ingredients = db.Table('recipe_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('ingredients_id', db.Integer, db.ForeignKey('ingredients.id')),
)

viewed_recipes = db.Table('viewed_recipes',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
    # Change to user_id when database is updated
    db.Column('user_ud', db.Integer, db.ForeignKey('user.id')),
)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    serves = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(6), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, nullable=False, default='0')
    method = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.Text, nullable=False)
    ingredients = db.relationship('Ingredients', secondary=recipe_ingredients, lazy='dynamic',
        backref=db.backref('ingredients', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)    

    def __repr__(self):
        return '<Recipe %r>' % (self.id)
        
class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Removed unique, still need to db.create_all()
    name = db.Column(db.String(80), nullable=False)
    unit = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    is_vegetarian = db.Column(db.Boolean, nullable=False)
    is_vegan = db.Column(db.Boolean, nullable=False)
    is_gluten_free = db.Column(db.Boolean, nullable=False)
    
    def __repr__(self):
        return '<Ingredients %r>' % self.name
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    recipe = db.relationship('Recipe', backref="author", lazy=True)
    viewed_recipe = db.relationship('Recipe', secondary=viewed_recipes, lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username
    
@app.route('/')
def index():
    # Dealing with ResultProxy help https://kite.com/python/docs/sqlalchemy.engine.result.ResultProxy
    # Average view count
    total_views = db.engine.execute('SELECT SUM(views), COUNT(views) FROM Recipe WHERE views > 0;')
    view_data = total_views.fetchone()
    average_views = view_data[0] / view_data[1]

    recipe_names = Recipe.query.filter(Recipe.views > average_views).all()
    recipe_dict = {}
    for recipe in recipe_names:
        # recipe_dict.update({recipe.name:recipe.id})
        recipe_dict.update({recipe.name:recipe.id})
    # https://stackoverflow.com/questions/19884900/how-to-pass-dictionary-from-jinja2-using-python-to-javascript
    recipe_object = (json.dumps(recipe_dict)
    .replace(u'<', u'\\u003c')
    .replace(u'>', u'\\u003e')
    .replace(u'&', u'\\u0026')
    .replace(u"'", u'\\u0027'))
    
    # Altering the homepage 
    allergies = ['is_gluten_free','is_vegan','is_vegetarian']
    featured_recipes_ids = [5, 6, 9, 10]
    vegan_recipes_ids = [4,5, 6, 7]
    featured_recipes = []
    vegan_recipes = []
    allergy_info = {}

    
    for recipe in featured_recipes_ids:
        temp_recipe = Recipe.query.filter_by(id=recipe).first()
        featured_recipes.append(temp_recipe)
        temp_allergy = {}
        for allergy in allergies:
            allergy_res = db.engine.execute('SELECT (NOT EXISTS (SELECT * FROM ingredients INNER JOIN recipe_ingredients on ingredients.id = recipe_ingredients.ingredients_id WHERE recipe_ingredients.recipe_id = %s AND ingredients.%s = 0))' % (recipe, allergy)).fetchall()
            temp_allergy[allergy] = allergy_res[0][0]
        allergy_info[recipe] = temp_allergy

    for recipe in vegan_recipes_ids:
        temp_recipe = Recipe.query.filter_by(id=recipe).first()
        vegan_recipes.append(temp_recipe)
        
    print(allergy_info)
    
    return render_template('index.html',recipe_object=recipe_object, featured_recipes=featured_recipes, vegan_recipes=vegan_recipes, allergy_info=allergy_info)
    
@app.route('/add-recipe/info', methods=['POST', 'GET'])
def add_recipe_info():
    
    if request.method == 'POST':
        
        # Add check to see if recipe name has been added before
        
        recipe_picture = request.files['inputFile']
        image_file_url = save_profile_picture(recipe_picture)
        
        session["added_recipe"] = {
            'name': request.form['dish_name'],
            'serves': request.form['serves'],
            'difficulty': request.form['difficulty'],
            'time': request.form['time'],
            'method': request.form['method'],
            'image_file_url': image_file_url
        }
        
        return redirect(url_for('add_recipe_ingredients'))
    
    return render_template('upload.html')

@app.route('/update-recipe/info/<recipe_id>', methods=['POST', 'GET'])
def update_recipe_info(recipe_id):
    
    # Add check to see if session has username
    
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    user = User.query.filter_by(username=session["username"]).first()
    
    # Check if user.id is same as recipe
    if recipe.user_id != user.id:
        # Change to account with message
        return redirect(url_for('index'))
        
    if request.method == "POST":
        
        
        try:
            request.files['inputFile']
        except KeyError:
            image_file_url = recipe.image_file
        else:
            recipe_picture = request.files['inputFile']
            image_file_url = save_profile_picture(recipe_picture)
            
        print(image_file_url)
        
        session["update_recipe"] = {
            'name': request.form['dish_name'],
            'serves': request.form['serves'],
            'difficulty': request.form['difficulty'],
            'time': request.form['time'],
            'method': request.form['method'],
            'image_file_url': image_file_url
        }
    
    # If post update values and redirect to ingreds
        
        return redirect(url_for('update_recipe_ingredients', recipe_id=recipe_id))
    
    return render_template('update.html', recipe=recipe)
    
@app.route('/add-recipe/ingredients', methods=['POST', 'GET'])
def add_recipe_ingredients():
    
    # Why is this not working?    
    try:
        session["added_recipe"]
    except KeyError:
        redirect(url_for('add_recipe_info'))
    
    if request.method == "POST":
        
        session["added_recipe_ingredients"] = {}

        for counter, (ingred, amount, unit) in enumerate(zip(request.form.getlist('ingredient'),
                                          request.form.getlist('amount'),
                                          request.form.getlist('unit'))):
                
                is_vegetarian = False
                is_vegan = False
                is_gluten_free = False
                
                if request.form.getlist('vegetarian-' + str(counter)):
                    is_vegetarian = True

                if request.form.getlist('vegan-' + str(counter)):
                    is_vegan = True
                
                if request.form.getlist('gluten-free-' + str(counter)):
                    is_gluten_free = True
            
                temp_ingred = {
                    "ingred": ingred,
                    "amount": amount,
                    "unit": unit,
                    "is_vegetarian" : is_vegetarian,
                    "is_vegan" : is_vegan,
                    "is_gluten_free" : is_gluten_free
                }
                session["added_recipe_ingredients"][counter] = temp_ingred
    
                

        return redirect(url_for('add_recipe_submit'))
    
    # temp_recipe = Recipe(name=name,image_file=image_file_url,serves = serves,difficulty=difficulty,time=time,views = 0,method = method,user_id = 1)
    # db.session.add(temp_recipe)
    # db.session.commit()
    
    return render_template('upload_ingred.html')

@app.route('/update-recipe/ingredients/<recipe_id>', methods=['POST', 'GET'])  
def update_recipe_ingredients(recipe_id):
    
    user = User.query.filter_by(username=session["username"]).first()
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    # Check if user.id is same as recipe
    if recipe.user_id != user.id:
        # Change to account with message
        return redirect(url_for('index'))
    
    search_str = "SELECT * FROM recipe_ingredients WHERE recipe_id = %s ;" % recipe_id
    all_ingreds_id = db.engine.execute(search_str).fetchall()
    
    all_ingreds = {}
    for counter, (k, v) in enumerate(all_ingreds_id):

        all_ingreds[counter] = Ingredients.query.filter_by(id=v).first()
        
        # Why is this not working? 
    # Add check to see update recipe is same as recipe_id
    try:
        session["update_recipe"]
    except KeyError:
        redirect(url_for('update_recipe_info', recipe_id=recipe_id))
    
    if request.method == "POST":
        
        session["update_recipe_ingredients"] = {}

        for counter, (ingred, amount, unit) in enumerate(zip(request.form.getlist('ingredient'),
                                          request.form.getlist('amount'),
                                          request.form.getlist('unit'))):
                
                is_vegetarian = False
                is_vegan = False
                is_gluten_free = False
                
                if request.form.getlist('vegetarian-' + str(counter)):
                    is_vegetarian = True

                if request.form.getlist('vegan-' + str(counter)):
                    is_vegan = True
                
                if request.form.getlist('gluten-free-' + str(counter)):
                    is_gluten_free = True
            
                temp_ingred = {
                    "ingred": ingred,
                    "amount": amount,
                    "unit": unit,
                    "is_vegetarian" : is_vegetarian,
                    "is_vegan" : is_vegan,
                    "is_gluten_free" : is_gluten_free
                }
                session["update_recipe_ingredients"][counter] = temp_ingred
    
        return redirect(url_for('update_recipe_submit', recipe_id=recipe_id))
    
    # temp_recipe = Recipe(name=name,image_file=image_file_url,serves = serves,difficulty=difficulty,time=time,views = 0,method = method,user_id = 1)
    # db.session.add(temp_recipe)
    # db.session.commit()
    
    return render_template('update_ingred.html', all_ingreds=all_ingreds)
    
@app.route('/add-recipe/submit', methods=['POST', 'GET'])
def add_recipe_submit():
    # Why is this not working?    
    try:
        session["added_recipe_ingredients"]
    except KeyError:
        redirect(url_for('add_recipe_info'))
    
    user = User.query.filter_by(username=session["username"]).first()
    added_recipe_ingredients = session["added_recipe_ingredients"]
    added_recipe = session["added_recipe"]
    
    temp_recipe = Recipe(name=session["added_recipe"]["name"],
                        image_file=session["added_recipe"]["image_file_url"],
                        serves = session["added_recipe"]["serves"],
                        difficulty=session["added_recipe"]["difficulty"],
                        time=session["added_recipe"]["time"],
                        views = 0,
                        method = session["added_recipe"]["method"],
                        user_id = user.id)
                        
    db.session.add(temp_recipe)
    
    for counter, (k, v) in enumerate(session["added_recipe_ingredients"].items()):
        
        # Add check to see if ingredient, unit, amount has been added before, if so skip adding it and append from db
        
        ingreds = Ingredients(name=v["ingred"],
                              is_vegetarian = v["is_vegetarian"],
                              is_vegan=v["is_vegan"],
                              is_gluten_free=v["is_gluten_free"],
                              unit=v["unit"],
                              amount=v["amount"])
        
        db.session.add(ingreds)
        temp_recipe.ingredients.append(ingreds)
    
    if request.method == "POST":
        session.pop("added_recipe")
        session.pop("added_recipe_ingredients")
        db.session.commit()
        
        return redirect(url_for('index'))
        
    
    
    return render_template('upload_submit.html', added_recipe=added_recipe, added_recipe_ingredients=added_recipe_ingredients)
    
@app.route('/update_recipe/submit/<recipe_id>', methods=['POST', 'GET'])
def update_recipe_submit(recipe_id):
    
    print(session["update_recipe_ingredients"])
        # Why is this not working?    
    try:
        session["added_recipe_ingredients"]
    except KeyError:
        redirect(url_for('add_recipe_info'))
    
    update_recipe_ingredients = session["update_recipe_ingredients"]
    update_recipe = session["update_recipe"]
                        
    temp_recipe = Recipe.query.filter_by(id=recipe_id).first()
    temp_recipe.name = session["update_recipe"]["name"]
    temp_recipe.image_file = session["update_recipe"]["image_file_url"]
    temp_recipe.serves = session["update_recipe"]["serves"]
    temp_recipe.difficulty=session["update_recipe"]["difficulty"]
    temp_recipe.time=session["update_recipe"]["time"]
    temp_recipe.method = session["update_recipe"]["method"]
    
    for counter, (k, v) in enumerate(session["update_recipe_ingredients"].items()):
        
        # Add check to see if ingredient, unit, amount has been added before, if so skip adding it and append from db
        
        ingreds = Ingredients(name=v["ingred"],
                              is_vegetarian = v["is_vegetarian"],
                              is_vegan=v["is_vegan"],
                              is_gluten_free=v["is_gluten_free"],
                              unit=v["unit"],
                              amount=v["amount"])
        
        db.session.add(ingreds)
        temp_recipe.ingredients.append(ingreds)
    
    if request.method == "POST":
        
        delete_str = "DELETE FROM recipe_ingredients WHERE recipe_id = %s ;" % recipe_id
        db.engine.execute(delete_str)
        
        session.pop("update_recipe")
        session.pop("update_recipe_ingredients")
        db.session.commit()
        
        return redirect(url_for('index'))
    
    
    return render_template('update_submit.html', update_recipe=update_recipe, update_recipe_ingredients=update_recipe_ingredients)
    
@app.route('/recipe/<recipe_name>/<recipe_id>')
def recipe(recipe_name, recipe_id):
    session["username"] = "mstonieri"
    
    recipe_result = Recipe.query.filter_by(id=recipe_id).first()
    
    # Will need to change to try
    if session["username"]:
        
        user = User.query.filter_by(username=session["username"]).first()
        
        # Change to user_id when database is updated
        search_str = "SELECT * FROM viewed_recipes WHERE user_ud = %s AND recipe_id = %s ;" % (user.id, recipe_id)
        viewed_recipe = db.engine.execute(search_str).fetchall()
        
        if not viewed_recipe:
            user.viewed_recipe.append(recipe_result)
            recipe_result.views = recipe_result.views + 1
            db.session.commit()
            

    
    recipe_result = Recipe.query.filter_by(id=recipe_id).first()
    
    return render_template('recipe.html', recipe_result=recipe_result)
    
@app.route('/search', methods=['POST', 'GET'])
def search():
    
    page = request.args.get('page', 1, type=int)
    
    if "search_term" in session:
        result = return_search(session["recipe_type"], session["search_term"], page)
        search_term = session["search_term"]
        total_pages = result.pages
        pagination_num = create_pagination_num(total_pages, page)
        # Assistance on pagination from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination
        next_url = url_for('search', page=result.next_num) \
        if result.has_next else None
        prev_url = url_for('search', page=result.prev_num) \
        if result.has_prev else None
    else:
        result = None
        search_term = None 
    
    checkboxes = [None, None, None]
    
    if request.method == "POST":
        search_term = request.form["search"] 
        session["search_term"] = search_term
        recipe_type = request.form.getlist('recipe-type')
        session["recipe_type"] = recipe_type
        
        result = return_search(recipe_type, search_term, 1)
        next_url = url_for('search', page=result.next_num) \
        if result.has_next else None
        prev_url = url_for('search', page=result.prev_num) \
        if result.has_prev else None
        
        total_pages = result.pages
        pagination_num = create_pagination_num(total_pages, page)

        # test = Recipe.query.filter(~Recipe.ingredients.any(Ingredients.is_vegan == True))
        # Check to see if returned recipes have nutritional requirements

    
    # checkboxes=checkboxes, make session
    return render_template('search.html', result=result, checkboxes=checkboxes, search_term=search_term, next_url=next_url, prev_url=prev_url, pagination_num=pagination_num, page=page)
    
@app.route('/account/my-recipes', methods=['POST', 'GET'])
def account_my_recipes():

    page = request.args.get('page', 1, type=int)
    
    user = User.query.filter_by(username=session['username']).first()
    
    result = (Recipe.query
        .filter_by(user_id=user.id)
        .order_by(Recipe.views.desc())
        .paginate(page, 15, False))
    total_pages = result.pages

    total_pages = result.pages
    pagination_num = create_pagination_num(total_pages, page)
        # Assistance on pagination from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination
    next_url = url_for('search', page=result.next_num) \
    if result.has_next else None
    prev_url = url_for('search', page=result.prev_num) \
    if result.has_prev else None
    
    print(type(result.items))
    
    return render_template('account_my_recipes.html', result=result, next_url=next_url, prev_url=prev_url, pagination_num=pagination_num, page=page)
    
@app.route('/register', methods=['POST', 'GET'])
def register():
    
    
    return render_template('register.html')
    
@app.route('/register_user', methods=['POST', 'GET'])
def register_user():
    
    first_name = request.form["first_name"].lower()
    last_name = request.form["last_name"].lower() 
    username = request.form["username"].lower()
    password = request.form["password"].lower()
    

    if User.query.filter_by(username=username).count() > 0:
        return redirect(url_for('register'))
    else:
        user = User(first_name=first_name,last_name=last_name, username=username,password = password)
        db.session.add(user)
        db.session.commit()
        
        session["username"] = username
    
        return redirect(url_for('index'))
    return redirect(url_for('register'))
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    
    return render_template('login.html')
    
@app.route('/login_user', methods=['POST', 'GET'])
def login_user():
    
    username = request.form["username"].lower()
    password = request.form["password"]
    
    user = User.query.filter_by(username=username).first()
    
    try:
        user.username
    except AttributeError:
        return redirect(url_for('login'))
    
    if str(user.password) == str(password):
        print("works")
        session["username"] = username
        return redirect(url_for('index'))
    else: 
        print("not works")
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
# add 404 for missing queries http://flask-sqlalchemy.pocoo.org/2.3/queries/#queries-in-views