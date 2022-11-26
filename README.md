# Brief Project Background and motivation
Accountant API is is an API for an Accounting firm
to store the details of their tax clients as well
as the accountants assigned to each one of those clients
and the levels of the accountants whether Junior,Senior or Manager.
There are two models (Accountant- to store accountant name and designation and Taxentity
to store the client name, type of client, assigned accountant and the date of inserting the record)

## What the project should accomplish
Models includes at least…
* Two classes with primary keys at at least two attributes each
One-to-many or many-to-many relationships between classes
## Endpoints includes at least…
* Two GET requests
* One POST request
* One PATCH request
* One DELETE request
## Roles includes at least…
* Two roles with different permissions
* Permissions specified for all endpoints
## Tests includes at least…
* One test for success behavior of each endpoint
* One test for error behavior of each endpoint
* At least two tests of RBAC for each role
* =================================================
## Project Dependencies
**Python python-3.10.8**
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)




# Running things locally
##### First install a virtual environment and activate it
`pip install virtualenv`
`virtualenv myenv`
`source myenv/scripts/activate`

##### Installing dependencies
`pip install -r requirements`

## Key Dependencies & Platforms
+ Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

+ SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database.

+ Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.

+ Auth0 is the authentication and authorization system we'll use to handle users with different roles.

+ PostgreSQL this project is integrated with a popular relational database PostgreSQL

+ Heroku is the cloud platform used for deployment

##### Start the server locally
`export FLASK_APP=app`
`export FLASK_ENV=development` # enables debug mode
An alternative to setup all the environment varibales will be:
`source setup.sh`
`python3 app.py`

##### Running the server on Heroku
The server is live on already deployed and live:
[https://antony-udacity-capestone.herokuapp.com]
There are two tokens in setup.sh which can be used to test the endpoints
`source setup.sh`
`curl -H "Authorization: Bearer ${accountant_token}" https://antony-udacity-capestone.herokuapp.com/accountants`
This will return all accountants in the database

# API Documentation
## Roles
**Financial Accountant**
* Permissions
    1. get:accountants - get a list of accountants
    2. patch:accountants - patch an existing accountant
    3. post:accountants - post a new accountant

**Tax Accountant**
* Permissions
    1. delete:taxentities - delete a tax client
    2. get:taxentities - get the tax entities
    3. patch:taxentities - patch an existing tax entity
    4. post:taxentities - post a new tax entity

As stated above, two bearer tokens for testing are in the setup.sh
They are named
`accountant_token` # for testing all accountants endpoints
and
`taxentity_token` #for testing all tax entities endpoints

# Endpoints
- POST "/accountants"
- GET "/accountants"
- PATCH "/accountants/id"
- POST "/taxentities"
- PATCH "/taxentities/id"
- DELETE "/taxentities/id"
- GET "/taxentities/id"

## POST "/accountants"
+ Post a new accountant
+ Roles based authentication: post:accountants
+ Request Arguments:
   Body: JSON Object containing "name": String and "designation": string
+ returns an json with two keys: "success" and "accountant" like below
`{"success": True, "accountant": accountant.id}`

## POST "/taxentities"
+ Post a new tax entity
+ Roles based authentication: post:taxentities
+ Request Arguments:
   Body: JSON Object "entity_name": string
            "entity_type": string,
            "entity_tax_number": integer,
            "entity_accountant": integer
+ returns an json with two keys: "success" and "tax_entity"
`{"success":True, "tax_entity":tax_entity.id}`

## PATCH "/taxentities/id"
+ Patch an existing tax entity
+ Roles based authentication: patch:taxentities
+ Request Arguments:
   Body: JSON Object "entity_name": string
            "entity_type": string,
            "entity_tax_number": integer,
            "entity_accountant": integer
    one can supply only the attribute to patch or all the attributes
+ returns an json with two keys: "success" and "tax_entity"
`{"success":True, "tax_entity":tax_entity.id}`

## PATCH "/accountants/id"
+ Patch an existing accountant
+ Roles based authentication: patch:accountants
+ Request Arguments:
   Body: JSON Object containing "name": String and "designation": string
+ returns an json with two keys: "success" and "patch"
`{"success":success,"patch":id}`

## GET "/taxentities"
+ Get tax entities
+ Roles based authentication: get:taxentities
+ Request Arguments:
   Body: None
+ returns an json with three keys: "success","tax_entities" and "count"
`{"success":True, "tax_entities":formatted_tax_entities, "count":len(formatted_tax_entities)}`

## GET "/accountants"
+ Get all accountants
+ Roles based authentication: get:accountants
+ Request Arguments:
   Body: None
+ returns an json with three keys: "success","accountants" and "count"
`{"success":True, "accountants":formatted_accountants, "count":len(formatted_accountants)}`

## DELETE "/taxentities/id"
+ Delete an accountant with the specified id
+ Roles based authentication: delete:taxentities
+ Request Arguments:
   Body: None
+ returns an json with two keys: "success","delete" 
`{"success":True, "delete":id}`

