#docker
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json
import psycopg2
from sqlalchemy.dialects import postgresql
from sqlalchemy import Table, Column, String, MetaData,Integer,Date,Numeric,Boolean,ForeignKey,TEXT,VARBINARY,VARCHAR,DATE,DECIMAL,BIGINT
from sqlalchemy.orm import relationship,aliased, backref,scoped_session, sessionmaker
from flask import Flask
from flask_marshmallow import Marshmallow
from flask import Flask,request,render_template,url_for,jsonify,redirect,flash
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


app = Flask(__name__)


ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get('SQLALCHEMY_DATABASE_URI')
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql+psycopg2://postgres:1111@localhost:5432/arananlar1_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


#Create table
class Terrorists(db.Model):
    __tablename__ = 'Interpol_Terorists'
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.VARCHAR)
    sex_id = db.Column(db.VARCHAR(3))
    date_of_birth = db.Column(db.DATE)
    place_of_birt= db.Column(db.VARCHAR)
    country_of_birth_id =db.Column(db.VARCHAR)
    weight=db.Column(db.DECIMAL)
    height=db.Column(db.DECIMAL)
    distinguishing_marks =db.Column(db.TEXT)
    eyes_colors_id=db.Column(db.VARCHAR)
    hairs_id=db.Column(db.VARCHAR)
    entity_id=db.Column(db.VARCHAR)
    print("Users table added to python_app database.")

    def __init__(self,forename,sex_id,date_of_birth,place_of_birth,country_of_birth_id,weight,height,distinguishing_marks,eyes_colors_id,hairs_id,entity_id):
      self.forename=forename
      self.sex_id=sex_id
      self.date_of_birth=date_of_birth
      self.place_of_birt=place_of_birth
      self.country_of_birth_id=country_of_birth_id
      self.weight=weight
      self.height=height
      self.distinguishing_marks=distinguishing_marks
      self.eyes_colors_id=eyes_colors_id
      self.hairs_id=hairs_id
      self.entity_id=entity_id

 
    
class languages(db.Model):
      __tablename__ = 'Interpol_Languages'
      id = db.Column(db.Integer, primary_key=True,autoincrement=True) #autoincriement==Used as more than one primarykey in more than one table in relational tables
      languages_id = db.Column(db.BIGINT, db.ForeignKey('Interpol_Terorists.id'))
      languages_spoken_ids= db.Column(db.VARCHAR(30))
      terrorists=db.relationship("Terrorists",backref=db.backref('Interpol_Languages'),lazy='subquery') #one to many relationship
      print("Users table added to python_app database.")

      def __init__(self, languages_spoken_ids):
             self.languages_spoken_ids=languages_spoken_ids

class languagestSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model=languages
        include_fk = True
        load_instance = True             
    fields=(' languages_spoken_ids')
               
class Nations(db.Model):
    __tablename__ = 'Interpol_Nations'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nationalities_id=db.Column(db.BIGINT, db.ForeignKey('Interpol_Terorists.id'))
    nationalities=db.Column(db.VARCHAR(15))
    terrorists=db.relationship("Terrorists", backref=db.backref('Interpol_Nations'),lazy='subquery') #one to many relationship
    print("Users table added to python_app database.")
    def __init__(self, nationalities):
             self.nationalities=nationalities

class NationsSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model=Nations
        include_fk = True
        load_instance = True              
    fields=('nationalities')

class Warrants(db.Model):
    __tablename__ = 'Interpolarrest_Warrants'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    arrest_warrants_id=db.Column(db.BIGINT, db.ForeignKey('Interpol_Terorists.id'))
    issuing_country_id=db.Column(db.VARCHAR(10))
    charge=db.Column(db.TEXT)
    charge_translation=db.Column(db.TEXT)
    terrorists=db.relationship("Terrorists", backref=db.backref('Interpolarrest_Warrants'),lazy='subquery') #one to many relationship
    print("Users table added to python_app database.")

    def __init__(self, issuing_country_id,charge,charge_translation):
          self.issuing_country_id= issuing_country_id
          self.charge=charge
          self.charge_translation=charge_translation

class WarrantsSchema(ma.SQLAlchemyAutoSchema):
  

    class Meta:
        model=Warrants
        include_fk = True
        load_instance = True          
    fields=('issuing_country_id','charge','charge_translation')

class Photo(db.Model):
    __tablename__ = 'Interpol_Teror_Images'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    images_id=db.Column(db.BIGINT, db.ForeignKey('Interpol_Terorists.id', ondelete='CASCADE'), nullable=False) 
    picture_id =db.Column(db.VARCHAR(20))
    picture_url=db.Column(db.VARCHAR)
    images_file = db.Column(db.TEXT)
    terrorists=db.relationship("Terrorists", backref=db.backref('Interpol_Teror_Images', passive_deletes=True),lazy='subquery') #one to many relationship , passive deletes==to delete data in the table to which it is backward-relational
    print("Users table added to python_app database.")

    def __init__(self,picture_id,picture_url,images_file):
          self.picture_id= picture_id
          self.picture_url=picture_url
          self.images_file=images_file   

class PhotoSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model=Photo
        include_fk = True
        load_instance = True 
    fields=('images_file')

class TerroristSchema(ma.SQLAlchemyAutoSchema):
    weight=fields.Str()
    height=fields.Str()
    #languagess= ma.Nested(languagestSchema,many=True)
    #nationss=ma.Nested(NationsSchema,many=True)
    #warrantss= ma.Nested(WarrantsSchema,many=True)
    #photos= ma.Nested(PhotoSchema,many=True)
    class Meta:
        model=Terrorists
        load_instance = True 
    #fields=('forename','sex_id','date_of_birth','place_of_birth','country_of_birth_id','weight','height','distinguishing_marks','eyes_colors_id','hairs_id','entity_id') 

 #engine = create_engine('postgresql+psycopg2://postgres:1111@localhost:5432/arananlar1_db',encoding='utf-8-sig', echo=True) #database connections urls

'''@app.route("/ready")
def test():
    conn = psycopg2.connect("dbname=arananlar1_db user=postgres host=postgres port=5432 password=1111 connect_timeout=1") 
    conn.close()'''
@app.route('/terroristsdatabase',methods=['GET'])
def index():
    terrorists=(db.session.query(Terrorists,languages,Nations,Warrants,Photo).join(languages).join(Nations).join(Warrants).join(Photo).filter(Terrorists.id==languages.languages_id).filter(Terrorists.id==Nations.nationalities_id).filter(Terrorists.id==Warrants.arrest_warrants_id).filter(Terrorists.id==Photo.images_id)).all()
    terrorists_db=[{Terrorists.__tablename__:p[0],languages.__tablename__:p[1],Nations.__tablename__:p[2],Warrants.__tablename__:p[3],Photo.__tablename__:p[4]} for p in terrorists]
    DynamicSchema = ma.Schema.from_dict({
        Terrorists.__tablename__: 
            ma.Nested( TerroristSchema, dump_only=True),
        languages.__tablename__: 
            ma.Nested(languagestSchema, dump_only=True),
        Nations.__tablename__:
            ma.Nested(NationsSchema,dump_only=True),
        Warrants.__tablename__:
            ma.Nested(WarrantsSchema,dump_only=True),
        Photo.__tablename__:
             ma.Nested(PhotoSchema,dump_only=True)            
        })
    terroroistsschema= DynamicSchema(many=True)
    output=terroroistsschema.dump(terrorists_db)
    return jsonify({'data': output})

#app.env = "development"

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    #app.run(debug=True,host='0.0.0.0', port=5000)
    app.run(debug=True,host='0.0.0.0')
  
