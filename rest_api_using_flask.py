#!/usr/bin/python3
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from json import dumps
from json2html import *

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__, template_folder='.')
api = Api(app)


class Employees(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from employees") # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID
    
    def post(self):
        conn = db_connect.connect()
        print(request.json)
        LastName = request.json['LastName']
        FirstName = request.json['FirstName']
        Title = request.json['Title']
        ReportsTo = request.json['ReportsTo']
        BirthDate = request.json['BirthDate']
        HireDate = request.json['HireDate']
        Address = request.json['Address']
        City = request.json['City']
        State = request.json['State']
        Country = request.json['Country']
        PostalCode = request.json['PostalCode']
        Phone = request.json['Phone']
        Fax = request.json['Fax']
        Email = request.json['Email']
        query = conn.execute("insert into employees values(null,'{0}','{1}','{2}','{3}', \
                             '{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}', \
                             '{13}')".format(LastName,FirstName,Title,
                             ReportsTo, BirthDate, HireDate, Address,
                             City, State, Country, PostalCode, Phone, Fax,
                             Email))
        return {'status':'success'}

    
class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

    
class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

@app.route('/')
class Request_Parm(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('EmployeeId', default=-1, type=str, required=False)
        parser.add_argument('Email', default='', type=str, required=False)
        args = parser.parse_args()
        
        conn = db_connect.connect()
        print(args['EmployeeId'])
        print(args['Email'])
        query = conn.execute("select * from employees where EmployeeId =%d or Email ='%s' " %( int(args['EmployeeId']), args['Email']) )
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        html_data = json2html.convert(json = result)
        
        #html_head = """ <html>   <head></head>     <body>%s</body>     </html>    """
        #html_data = html_head %( html_data )
        return render_template('result.html', render=result)
        
        
 
api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3
api.add_resource(Request_Parm, '/param', endpoint='param')


if __name__ == '__main__':
     app.run(host='0.0.0.0', use_reloader=True)