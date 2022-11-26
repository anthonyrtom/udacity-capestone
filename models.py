import os
from sqlalchemy import Column, String, create_engine, ForeignKey, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.sql import func

database_path = os.environ.get('DATABASE_URL',"sqlite:///test.db")
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path, testing=False):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    if testing:
        db.create_all()

'''
First the entity model to store information about a tax client,
it has the following attributes:
id - primary key 
entity_name : The name of the entity
entity_type : nature of the entity
entity_tax_number : entity tax number which is unique
entity_accountant : a foreign key to the Accountant assigned
insertion_date : when the record was inserted
'''

class TaxEntity(db.Model):
    __tablename__ = "tax_entity"
    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_name = Column(String(50))
    entity_type = Column(String(50))
    entity_tax_number = Column(Integer)
    entity_accountant = Column(Integer, ForeignKey("accountant.id"), nullable=True)
    insertion_date = db.Column(db.DateTime, nullable=False, default=func.now())

    def format(self):
        return {
            "id": self.id,
            "entity_name": self.entity_name,
            "entity_type": self.entity_type,
            "entity_tax_number": self.entity_tax_number,
            "entity_accountant" : self.entity_accountant,
            "insertion_date" : self.insertion_date
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


'''
The class Accountant has the details of accountant 
that will be assigned to entities.It will be a foreign key in the Entity class
This class has the following attributes:
id - the primary key of the table
name - name of the accountant
designation - whether junior, senior or manager
'''
class Accountant(db.Model):
    __tablename__ = "accountant"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    designation = Column(String(50))

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            "id" : self.id,
            "name": self.name,
            "designation": self.designation
        }