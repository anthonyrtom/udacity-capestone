import os
from flask import Flask, request, abort, jsonify
from models import setup_db
from flask_cors import CORS
from models import Accountant, TaxEntity
from auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    #CORS(app, resources={r"/*": {"origins": "*"}})
    
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/")
    def home():
        return "Life is sweat, with all its ups and downs.You may be going through a lot today but it will pass. By Antony"

    #This is an endpoint to add an accountant
    #A successful request should contain the name of the
    #new accountant and their designation (Junior, senior or manager)
    #It requires a permission of "post:accountant"
    #a success request success:True and the ID of the newly created accountant
    @app.route("/accountants", methods=["POST"])
    @requires_auth("post:accountants")
    def post_accountant(payload):
        body = request.get_json()
        is_request_complete = "name" in body and "designation" in body
        if is_request_complete:
            name = body.get("name", None)
            designation = body.get("designation", None)
        else:
            return jsonify({"success":False}),400
        try:
            accountant = Accountant(name=name,designation=designation)
            accountant.insert()
            return jsonify({"success": True,"accountant": accountant.id}),200
        except:
            abort(400)

    #Endpoint to retrieve all accountants
    #The end point gets all accountants in the database
    #the required authorisation is
    #the method returns a json object of the accountants and a success true otherwise it aborts with a 404
    #The permission required is "get:accountants"
    @app.route("/accountants", methods=["GET"])
    @requires_auth("get:accountants")
    def get_accountants(payload):
        all_accountants = Accountant.query.all()
        if len(all_accountants)==0:
            abort(404)
        formatted_accountants = [accountant.format() for accountant in all_accountants]
        
        return jsonify({"success":True, "accountants":formatted_accountants, "count":len(formatted_accountants)}),200

    #A method to patch the name, designation or both
    #It receives an accountant Id then patches the accountant otherwise a 404 is returned
    #if the accountant Id is not found. The method returns success true
    #The permission required is "patch:accountants"
    @app.route("/accountants/<id>", methods=["PATCH"])
    @requires_auth("patch:accountants")
    def patch_accountant(payload, id):
        success = False #to check if any successful change was done
        accountant = Accountant.query.get(id)
        if accountant is None:
            abort(404)
        
        body = request.get_json()
        if body is None:
            abort(400)
        if 'name' in body:
            accountant.name = body.get('name')
            success = True
        if 'designation' in body:
            accountant.designation = body.get('designation')
            success = True
        try:
            accountant.update()
            return jsonify({"success":success,"patch":id}),200
        except:
            abort(422)

    '''
    The Tax entity has a post method. If all mandatory attributes
    are found in the request method then a success is returned and 
    if not a 400 for bad request error is raised
    A successful call will return a json object with success true and
    the id of the newly created Tax entity
    #The permission required is "post:taxentities"
    '''
    @app.route("/taxentities", methods=["POST"])
    @requires_auth("post:taxentities")
    def post_taxentity(payload):
        body = request.get_json()
        if body is None:
            abort(404)
        is_valid_request = True #start with true and check each and change to false
        if "entity_name" not in body:
            is_valid_request = False
        elif "entity_type" not in body:
            is_valid_request = False
        elif "entity_tax_number" not in body:
            is_valid_request = False
        else:
            pass

        if not is_valid_request: #Some arguements missing abort
            abort(400)
        entity_name = body.get("entity_name", None)
        entity_type = body.get("entity_type", None)
        entity_tax_number = body.get("entity_tax_number", None)
        entity_accountant = body.get("entity_accountant", None)

        try:
            tax_entity = TaxEntity(entity_name=entity_name, entity_type=entity_type, entity_tax_number=entity_tax_number, entity_accountant=entity_accountant)
            tax_entity.insert()
            return jsonify({"success":True, "tax_entity":tax_entity.id}),200
        except:
            abort(422)

    '''
    The route is a get that returns a formatted Tax entity as a json
    An unsuccessful request returns 404
    #The permission required is "get:taxentities"
    '''
    @app.route("/taxentities", methods=["GET"])
    @requires_auth("get:taxentities")
    def get_tax_entities(payload):
        all_tax_entities = TaxEntity.query.all()
        if len(all_tax_entities)==0:
            abort(404)
        formatted_tax_entities = [tax_entity.format() for tax_entity in all_tax_entities]
        
        return jsonify({"success":True, "tax_entities":formatted_tax_entities, "count":len(formatted_tax_entities)}),200

    #The route deletes a tax_entity
    #The permission required is "delete:taxentities"
    #a successful deletion returns success:True
    #a 404 is returned or 422 otherwise
    @app.route("/taxentities/<id>", methods=["DELETE"])
    @requires_auth("delete:taxentities")
    def delete_tax_entity(payload, id):
        tax_entity = TaxEntity.query.get(id)
        if tax_entity is None:
            abort(404)
        try:
            tax_entity.delete()
            return jsonify({"success":True, "delete":id}),200
        except:
            abort(422)

    #The route patches a tax entity with an arguement as arguement
    #If the ID is invalid a 404 abort is returned
    #The permission required is "patch:taxentities"
    @app.route("/taxentities/<id>", methods=["PATCH"])
    @requires_auth("patch:taxentities")
    def patch_tax_entity(payload, id):
        tax_entity = TaxEntity.query.get(id)
        if tax_entity is None:
            abort(404)
        body = request.get_json()
        if body is None:
            abort(400)
        try:
            if "entity_name" in body:
                tax_entity.entity_name = body.get("entity_name")
                tax_entity.update()
            if "entity_type" in body:
                tax_entity.entity_type = body.get("entity_type")
                tax_entity.update()
            if "entity_tax_number" in body:
                tax_entity.entity_tax_number = body.get("entity_tax_number")
                tax_entity.update()
            if "entity_accountant" in body:
                acc_extract = int(body.get("entity_accountant"))
                accountant = Accountant.query.filter_by(id=acc_extract).one_or_none()
                if not accountant is None: #just to make sure the accountant is there in the other table
                    tax_entity.entity_accountant = body.get("entity_accountant")                
                    tax_entity.update()
            return jsonify({"success":True,"tax_entity":tax_entity.id}),200
        except Exception as err:
            #print(err)
            abort(422)

    #=================================================
    #Error handlers
    #Error handle for not found
    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({"success": False, "error": 404,
                            "message": "resource not found"}), 404, )

    #Error handle for unprocessable request
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                        "message": "unprocessable"}),
            422,
        )

    #Error handle for bad request
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400,
                        "message": "bad request"}), 400

    #Error handle for internal server error
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"success": False, "error": 500,
                        "message": "internal server error"}), 500

    return app

app = create_app()
if __name__ == '__main__':
    app.run()