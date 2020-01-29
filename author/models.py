from applications import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
   

    def __init__(self, email, password):
        self.email = email
        self.password = password
       
    def __repr__(self):
        return '<Author %r>' % self.email



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name  = db.Column(db.String(500))
    last_name = db.Column(db.String(120))
    age=db.Column(db.String(30))

    def __init__(self, first_name,last_name,age):
        self.first_name=first_name
        self.last_name=last_name
        self.age=age
       
    def __repr__(self):
        return self.name


















#class Food(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    Food_name  = db.Column(db.String(500))
#    cuisine = db.Column(db.String(120))
#    category = db.Column(db.String(128))
#    Prescribed_type= db.db.Column(db.String(128))
#    def __init__(self, Food_name, cuisine, category, Prescribed_type):
#        self.Food_name = Food_name
#        self.cuisine = cuisine
#        self.category =category
#        self.Prescribed_type=Prescribed_type       

#    def __repr__(self):
#           return "<Food_name={} cuisine={} category={} Prescribed_type={}>".format(self.Food_name,
#                                                                                             self.cuisine,
#                                                                                                  self.category,
#                                                                                                  self.Prescribed_type)

