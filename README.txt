Requirements:

Flask==0.10.1
Flask-PyMongo==0.3.1
Jinja2==2.7.3
MarkupSafe==0.23
Werkzeug==0.10.4
gnureadline==6.3.3
ipdb==0.8
ipython==3.1.0
itsdangerous==0.24
pymongo==2.8
wsgiref==0.1.2


Accepted data formats: JSON

API USAGE:

Tips:

Return all tips:
Method: GET
URL: /safetytips/api/v1.0/tips/
Body: none


Return a single tip:
Method: GET
URL: /safetytips/api/v1.0/tips/<int:tip_id>
Body: none


Create new tip:
Method: POST
URL: /safetytips/api/v1.0/tips/
Body: JSON
example:
{ "message": "Bilbo Baggins was seen on campus wreaking havoc after having too much apple brandy at the Inn.",
 "username": "gandalfthegrey"}


Update a tip:
Method: PUT
URL: /safetytips/api/v1.0/tips/<int:tip_id>
Body: JSON
example:
{“message”: ”Frodo Baggins has moved in to subdue his crazy uncle Bilbo.”,
 "username": "gandalfthegrey"}


Delete a tip:
Method: DELETE
URL: /safetytips/api/v1.0/tips/<int:tip_id>
Body: none