from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import request
from flask import jsonify

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@planning-db:3306/planning' #database connection
app.config['SQLALCHEMY_ECHO'] = False       
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    MonthStartDate = db.Column(db.SmallInteger)
    DayStartDate = db.Column(db.SmallInteger)
    MonthEndDate = db.Column(db.SmallInteger)
    DayEndDate = db.Column(db.SmallInteger)
    Resources = db.Column(db.Float)
    idHeadMember = db.Column(db.Integer)
    Publish = db.Column(db.String(200))
    Description = db.Column(db.String(500))

@app.route('/plan', methods=['GET']) #get all the plans
def get_plans():
    plans = Plan.query.all()
    output = []

    for plan in plans:
        plan_data = {}
        plan_data['id'] = plan.id
        plan_data['MonthStartDate'] = plan.MonthStartDate
        plan_data['DayStartDate'] = plan.DayStartDate
        plan_data['MonthEndDate'] = plan.MonthEndDate
        plan_data['DayEndDate'] = plan.DayEndDate
        plan_data['Resources'] = plan.Resources
        plan_data['idHeadMember'] = plan.idHeadMember
        plan_data['Publish'] = plan.Publish
        plan_data['Description'] = plan.Description
        output.append(plan_data)

    return jsonify(output)

@app.route('/plan/<plan_id>', methods=['GET'])# get just one of the plan with the given id
def get_one_plan(plan_id):
    plan = Plan.query.filter_by(id=plan_id).first()

    if not plan:
        return jsonify({'message':'no plan found'})

    plan_data = {}
    output = []
    plan_data['id'] = plan.id
    plan_data['MonthStartDate'] = plan.MonthStartDate
    plan_data['DayStartDate'] = plan.DayStartDate
    plan_data['MonthEndDate'] = plan.MonthEndDate
    plan_data['DayEndDate'] = plan.DayEndDate
    plan_data['Resources'] = plan.Resources
    plan_data['idHeadMember'] = plan.idHeadMember
    plan_data['Publish'] = plan.Publish
    plan_data['Description'] = plan.Description
    output.append(plan_data)

    return jsonify(output)

@app.route('/plan',methods=['POST']) # create a new plan register in the db
def create_plan():
    data = request.get_json() #the incoming data in json
    new_plan = Plan(MonthStartDate=data['MonthStartDate'],DayStartDate=data['DayStartDate']
              ,MonthEndDate=data['MonthEndDate'],DayEndDate=data['DayEndDate'],Resources=data['Resources']
              ,idHeadMember=data['idHeadMember'],Publish=data['Publish'],Description=data['Description'])
    db.session.add(new_plan)
    db.session.commit()

    return jsonify(data)

@app.route('/plan/<plan_id>', methods=['PUT']) # update the plan with the corresponding id given
def update_plan(plan_id):
    plan = Plan.query.filter_by(id=plan_id).first()
    data = request.get_json() #the incoming data in json

    plan.MonthStartDate = data['MonthStartDate']
    plan.DayStartDate=data['DayStartDate']
    plan.MonthEndDate=data['MonthEndDate']
    plan.DayEndDate=data['DayEndDate']
    plan.Resources=data['Resources']
    plan.idHeadMember=data['idHeadMember']
    plan.Publish=data['Publish']
    plan.Description=data['Description']

    if not plan:
        return jsonify({'message':'no plan found'})

    db.session.commit()
    
    return jsonify({'message':'updated info'})

@app.route('/plan/<plan_id>', methods=['DELETE']) # delete the given plan
def delete_plan(plan_id):
    plan = Plan.query.filter_by(id=plan_id).first()

    if not plan:
        return jsonify({'message':'no plan found'})

    db.session.delete(plan)
    db.session.commit()

    return jsonify({'message':'the plan has been deleted'})

if __name__=='__main__':
    app.run( port=3002, host= '0.0.0.0')
    manager.run()