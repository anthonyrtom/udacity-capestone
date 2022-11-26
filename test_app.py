import os
import json
import unittest
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, TaxEntity, Accountant
from app import create_app
from auth import AuthError

#Get bearer tokens from the environment varibales
accountant_token = os.environ.get("accountant_token")
taxentity_token = os.environ.get("taxentity_token")

accountant_token = "Bearer " + accountant_token
accountant_header = {"Authorization":accountant_token}

taxentity_token = "Bearer " + taxentity_token
taxtentity_header = {"Authorization":taxentity_token}

class TaxTestCase(unittest.TestCase):
    #This class represents Taxentity test case

    def setUp(self):
        #initialize app and test variables
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_PATH = "sqlite:///test.db" # we will use sqllite for testing
        #self.DB_PATH='postgresql://postgres:pass123@localhost:5432/taxentitydb'
        
        setup_db(self.app, self.DB_PATH, True)
        #some data to use for tests
        self.new_accountant = {"name":"John Doe", "designation":"Manager"}
        self.new_taxentity = {"entity_name":"Tontrans Pty Ltd","entity_type":"Company","entity_tax_number":930145600}

        #bind the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            
        
    def tearDown(self):
        """Executed after reach test"""
        pass
        
    def test_post_accountant_success(self):
        """This tests posting an accountant"""
        #get number of accountants before the addition
        #then the count after addition should be more
        counter_before = len(Accountant.query.all())
        response = self.client().post("/accountants", json=self.new_accountant, headers=accountant_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"], True)
        self.assertGreater(len(Accountant.query.all()),counter_before)

    def test_post_accountant_infor_missing(self):
        #this will test posting when designation is not available
        #if name or designation is missing in the json provided
        #then return 400
        self.new_acc_missing = {"name":"John Doe"}
        response = self.client().post("/accountants", json=self.new_acc_missing, headers=accountant_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code,400)
        self.assertEqual(data["success"], False)

    def test_get_accountants_success(self):
        #Test for getting accountants, if no accountants return 404
        #first create an accountant
        accountant = Accountant(name="Foo Bar", designation="Junior")
        accountant.insert()
        response = self.client().get('/accountants', headers=accountant_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"], True)

    def test_get_accountants_not_allowed_405(self):
        #supply an unknown route in getting accountants
        response = self.client().get('/accountants/1000000', headers=accountant_header)
        self.assertEqual(response.status_code,405)
    
    def test_patch_accountant_success(self):
        #Testing a succesful patch
        self.name = {"name":"Foo"}
        #first create an accountant
        accountant = Accountant(name="Foo Bar", designation="Junior")
        accountant.insert()
        id = accountant.id
        response = self.client().patch('/accountants/{}'.format(id), json=self.name, headers=accountant_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"], True)
    
    def test_patch_no_data(self):
        #Test the endpoint if no name and designation is provided
        #It should return success:False
        response = self.client().patch('/accountants/1',headers=accountant_header)
        data = json.loads(response.data)
        self.assertEqual(data["success"], False)

    def test_post_taxentity_success(self):
        #Test a successful post to tax entity
        response = self.client().post("/taxentities", json=self.new_taxentity, headers=taxtentity_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"], True)
        

    def test_post_taxentity_missing_infor(self):
        #Test an unsuccessful post where some data is missing return 400
        self.new_taxentity_missing = {"entity_type":"Company","entity_tax_number":930145600}
        count_before = len(TaxEntity.query.all())
        response = self.client().post("/taxentities", json=self.new_taxentity_missing, headers=taxtentity_header)
        count_after = len(TaxEntity.query.all())
        self.assertEqual(response.status_code,400)
        self.assertEqual(count_before,count_after)
    
    def test_get_taxentities_success(self):
        #Test a successful retrieval of entities
        #insert one entity for the test first
        taxentity = TaxEntity(entity_name="Fool Pty Ltd", entity_type="Trust",entity_tax_number=900450)
        taxentity.insert()
        response = self.client().get('/taxentities', headers=taxtentity_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"], True)

    def test_get_taxentities_405(self):
        #Test a non existant route for get
        response = self.client().get('/taxentities/1000000', headers=taxtentity_header)
        self.assertEqual(response.status_code,405)

    def test_delete_taxentities(self):
        #Test a succusful deletion
        #Lets insert first a question
        taxentity = TaxEntity(entity_name="Fool Pty Ltd", entity_type="Trust",entity_tax_number=900450)
        taxentity.insert()
        id = taxentity.id
        response = self.client().delete("/taxentities/{}".format(id), headers=taxtentity_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"], True)
        self.assertEqual(int(data["delete"]), id)
    
    def test_delete_404(self):
        taxentity = TaxEntity(entity_name="Fool Pty Ltd", entity_type="Trust",entity_tax_number=900450)
        taxentity.insert() #insert one record for good measure
        id = 10000000 #a very big number which wont be there during testing
        response = self.client().delete("/taxentities/{}".format(id), headers=taxtentity_header)
        self.assertEqual(response.status_code,404)

    def test_patch_taxentity_success(self):
        #test for a successful patch
        taxentity = TaxEntity(entity_name="Fool Pty Ltd", entity_type="Trust",entity_tax_number=900450)
        taxentity.insert() #insert one record for good measure
        id = taxentity.id
        new_details = {"entity_name":"Proxies Pty Ltd", "entity_type":"Trust"}
        response = self.client().patch("/taxentities/{}".format(id),json=new_details, headers=taxtentity_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data["tax_entity"], id)

    def test_patch_taxentity_404(self):
        #test an unsuccessful patch where the taxentity id is not available
        id = 10000000
        response = self.client().patch("/taxentities/{}".format(id), headers=taxtentity_header)
        self.assertEqual(response.status_code,404)

    def test_app_home_success(self):
        # Test the home page
        response = self.client().get('/')
        self.assertEqual(response.status_code,200)

    def test_app_home_Not_found_404(self):
        # Test unsuccessful
        response = self.client().get('/fooo')
        self.assertEqual(response.status_code,404)

if __name__ == "__main__":
    unittest.main()