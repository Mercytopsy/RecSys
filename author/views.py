from flask import Blueprint, render_template, redirect, session, url_for, flash, request, jsonify
#from settings import APP_ID, APP_KEY,DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE_NAME
from werkzeug.security import generate_password_hash
from applications import db
import requests
from py_edamam import Edamam
from  werkzeug.debug import get_current_traceback
import traceback
import os
import json 
import pdfkit
import mysql.connector
from flask import Response,send_file
from flask_mail import Mail, Message
from author import tester
from flask_weasyprint import HTML, render_pdf
#from author.models import Food
from author.forms import RegisterForm,LoginForm
#from author import con
from author.models import Author
#with open('config.json') as config_file:
#    config_data = json.load(config_file)
author_app = Blueprint('author_app', __name__)
def return_500_if_errors(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            response = {
                'status_code': 500,
                'status': 'Internal Server Error'
            }
            return flask.jsonify(response), 500
    return wrapper

@author_app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('author/index.html')

@author_app.route('/contactus', methods=('GET', 'POST'))
def contact():
    return render_template('author/contactus.html')


@author_app.route('/contact', methods=('GET', 'POST'))
def retu():
    return render_template('author/return.html')


@author_app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        author = Author(
            form.email.data,
            hashed_password
        )
        db.session.add(author)
        db.session.commit()
        #flash("You are now registered, please login")
        return redirect(url_for('author_app.login'))
    return render_template('author/register.html')
   # , form=form
@author_app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        author = Author.query.filter_by(email=form.email.data).first()
        session['id'] = author.id
        if 'next' in session:
            next = session.get('next')
            session.pop('next')
            return redirect(next)
        else:        
            return redirect(url_for('author_app.index'))
    return render_template('author/login.html', form=form, error=error)

@author_app.route('/logout')
def logout():
    session.pop('id')
    #flash("User logged out")
    return redirect(url_for('author_app.login'))


    
#@author_app.route('/home', methods=('GET', 'POST'))
#def home():
#    return render_template('survey/home.html')

#@author_app.route('/index', methods=('GET', 'POST'))
#def data():
    #with open('/home/babatope/Documents/dietp/diet/author/out.csv', 'r') as myfile:
    #data=myfile.read()
    #json_obj = "/home/babatope/Documents/dietp/diet/author/data.csv"
    #db = con_json.data_b(DB_HOST,DB_USERNAME,DB_PASSWORD,DATABASE_NAME,json_obj)
    #d=db.validate_string()
    #form=UserForm()
#    return con.execute()
@author_app.route('/survey', methods=('GET', 'POST'))
def surveyPlatform():
    if request.method == 'POST':
        firstName = request.form.get('First_Name')  # access the data inside 
        lastName = request.form.get('Last_Name')
        Age= request.form.get('age')
        Gender = request.form.get('gender')
        weight = request.form.get('weight')
        height = request.form.get('height')
        healthType = request.form.get('healthType')
        ethnicGroup = request.form.get('Ethnic')
        question = request.form.get('question')
        #session["name"] = name
        session["ethnicGroup"] = ethnicGroup
        session["healthType"] = healthType
        session["weight"] = weight
        session['height'] = height
        #the_db=tester.execute()
         
        return redirect(url_for('author_app.plan'))
    return render_template('survey/reg.html')

@author_app.route('/plan', methods=('GET', 'POST'))
def plan():
    weight = session.get("weight")
    height = session.get("height")
    w=int(weight)
    h=float(height)
    hi=h/100
    bmi = round(w/(hi*hi), 2)
    #print("Your BMI is: {0} and you are: ".format(bmi), end='')
    ethnicGroup = session.get("ethnicGroup")
    healthType = session.get('healthType')
    healthType_normal = "Normal"
    healthType_obese= "obesity"
    mydb = mysql.connector.connect(
           host="localhost",
           user="Dietitian_app",
           passwd="diet_password",
           database="Dietitians"
        )
   
    #query=("SELECT Name, category, cuisine FROM Dietetic " 
    #"WHERE cuisine = %s Prescribed type = %s")   
    #query= 'SELECT Name,category,cuisine FROM Dietetic WHERE cuisine = ? ethnicGroup AND Prescribed = ? healthType)
    #cursor.execute("SELECT %s FROM table", ",".join(columnList)) 
    #mycursor.execute(query,(ethnicGroup, healthType))
    #mycursor.execute("SELECT cuisine, Prescribed FROM Dietetic")
    Breakfast='Breakfast'
    Lunch='Lunch'
    Dinner = 'Dinner'
    Normal_patient_mor = mycursor.execute('SELECT Name FROM Dietetic WHERE cuisine = %s AND Prescribed = %s AND category = %s',(ethnicGroup,healthType_normal,Breakfast))
    the_breakfast_norm = mycursor.fetchall()
    Normal_patient_lun=mycursor.execute('SELECT Name FROM Dietetic WHERE cuisine = %s AND Prescribed = %s AND category = %s',(ethnicGroup,healthType_normal,Lunch))
    the_lunch_norm = mycursor.fetchall()
    Normal_patient_din=mycursor.execute('SELECT Name FROM Dietetic WHERE cuisine = %s AND Prescribed = %s AND category = %s',(ethnicGroup,healthType_normal,Dinner))
    the_dinner_norm = mycursor.fetchall()
    obese_patient_mor= mycursor.execute('SELECT Name FROM Dietetic WHERE cuisine = %s AND Prescribed = %s AND category = %s',(ethnicGroup,healthType_obese,Breakfast))
    the_breakfast_obese = mycursor.fetchall()
    obese_patient_lun= mycursor.execute('SELECT Name FROM Dietetic WHERE cuisine = %s AND Prescribed = %s AND category = %s',(ethnicGroup,healthType_obese,Lunch))
    the_lunch_obese = mycursor.fetchall()
    obese_patient_din= mycursor.execute('SELECT Name FROM Dietetic WHERE cuisine = %s AND Prescribed = %s AND category = %s',(ethnicGroup,healthType_obese,Dinner))
    the_dinner_obese = mycursor.fetchall()
    data_severe_under = list(zip(the_breakfast_norm,the_lunch_norm,the_dinner_norm))
    data_under = list(zip(the_breakfast_norm,the_lunch_norm,the_dinner_norm))
    data_severe_over = list(zip(the_breakfast_obese,the_lunch_obese,the_dinner_obese))
    data_over = list(zip(the_breakfast_obese,the_lunch_obese,the_dinner_obese))
    if( bmi < 16):
        data_severe_under
    #print("severely underweight")
    elif( bmi>=16 and bmi < 18.5):
        data_under
    #print("underweight")
    elif( bmi >= 25 and bmi < 30):
        data_over 
    #print("overweight")
    elif( bmi >=30):
        data_severe_over
    #print("severely overweight")
    mor=mycursor.execute('SELECT Name FROM Dietetic WHERE cuisine = %s AND Prescribed = %s AND category = %s',(ethnicGroup,healthType,Breakfast))
    the_breakfast = mycursor.fetchall()
    lun=mycursor.execute('SELECT Name FROM Dietetic WHERE cuisine = %s AND Prescribed = %s AND category = %s',(ethnicGroup,healthType,Lunch))
    the_lunch = mycursor.fetchall()
    dinn=mycursor.execute('SELECT Name FROM Dietetic WHERE cuisine = %s AND Prescribed = %s AND category = %s',(ethnicGroup,healthType,Dinner))
    the_dinner = mycursor.fetchall()
    data = list(zip(the_breakfast,the_lunch,the_dinner))
    #print(data)
    #print(the_val)
    #return render_template('survey/results.html', the_breakfast=the_breakfast)
    #the_breakfast = request.args.get('date', None)
    return render_template('survey/home.html',data=data, bmi=bmi, data_severe_under=data_severe_under, data_under=data_under, data_over=data_over, data_severe_over=data_severe_over,healthType=healthType)
@return_500_if_errors
@author_app.route('/search', methods=('GET','POST'))
def search():
        recipe_list=[]
        total_recipe=[]
        a=[]
        search = request.args.get('search')
        e= Edamam(
           food_appid=os.environ.get("APP_ID"),
           food_appkey= os.environ.get("APP_KEY"),
           )     
        foods_list = e.search_food(search)
        #if foods_list==0:
        #    return redirect(url_for('author_app.404'))
        #if foods_list 
        recipes = foods_list["hints"]
       
            
        #with open('data.json', 'w') as outfile:
        #    json.dump(recipes, outfile)
        
        for recipe in recipes:
            name = recipe["food"]["label"]
            nutrients = recipe["food"]["nutrients"]
            recipe_list.append({"name": name, "nutrients": nutrients})
            recipe_list=recipe_list[:1]
            #print(recipe_list)
        for p in recipe_list:
            try:
                p["nutrients"]["CARBS"] = p["nutrients"].pop("CHOCDF")
                p["nutrients"]["ENERGY KCAL"] = p["nutrients"].pop("ENERC_KCAL")
                p["nutrients"]["PROTEIN"] = p["nutrients"].pop("PROCNT")
                p["nutrients"]["FIBRE"] = p["nutrients"].pop("FIBTG")
            except KeyError:
                pass    
            new=p
            total_recipe.append(recipe_list)
        #print(total_recipe)
        return render_template('author/search.html', recipe_list=recipe_list)
       # return redirect(url_for('author_app.404'), total_recipe=total_recipe)

@author_app.errorhandler(Exception)
def all_exception_handler(e):
    error = str(traceback.format_exc())
    print ("There was a problem: {}".format(error))


@author_app.errorhandler(404)
def page_not_found_error(error):
    API_PATH_PREFIX = '/api/'
    if request.path.startswith(API_PATH_PREFIX):
        return jsonify({'error': True, 'msg': 'API endpoint {!r} does not exist on this server'.format(request.path)}), error.code
    return render_template('err_{}.html'.format(error.code)), error.code      
          
      

       




    #for recipe in recipes:
    #    name = recipe["recipe"]["label"]
    #    image = recipe["recipe"]["image"]
    #    url = recipe["recipe"]["url"]
    #    ingredients = recipe["recipe"]["ingredientLines"]
        # icons = []
        # for prod_name, prod_icon in query:
        #     for param in param_list:
        #         if ' '.join(param) in prod_name and prod_icon:
        #             icons.append(prod_icon)
        #             continue

        #recipe_list.append({"name": name, "ingredients": ingredients, "image": image, "url": url})

    #if len(recipe_list) < 4 and len(params) > 1:
     #       get_recipes(params[1:])

    #return recipe_list[:4]




       
