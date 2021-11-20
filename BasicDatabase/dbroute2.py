# """
#    https://account.mongodb.com/account/login
   
#    sudo pip3 install Flask-WTF
# """


from flask import Flask, render_template, redirect
from pymongo import MongoClient
from sampleClasses import *

# config system
app = Flask(__name__)

# secret key is used to make the client-side sessions secure
app.config.update(dict(SECRET_KEY='yoursecretkey'))
#client = MongoClient('mongodb+srv://myuser:mypassword@cluster0-34sac.mongodb.net/sample_mflix?retryWrites=true&w=majority')
client = MongoClient('mongodb+srv://rebecca96dmello:9881411765rmD#@cluster0.20egu.mongodb.net/sample_mflix?ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=true&w=majority')
db = client.TaskManager             # TaskManager is the name of the database


# db points to the database. db.settings points to the collection name "settings" inside the database collection
# it inserts 1 document if 'task_id' is not found
if db.settings.find({'name': 'task_id'}).count() <= 0:
    print("task_id Not found, creating....")
    db.settings.insert_one({'name':'task_id', 'value':0})

# updates the "settings" collection by incrementing the task_id by 1
def updateTaskID(value):
    task_id = db.settings.find_one()['value']
    task_id += value
    db.settings.update_one(
        {'name':'task_id'},
        {'$set':
            {'value':task_id}
        })

def createTask(form):
    title = form.title.data
    priority = form.priority.data
    shortdesc = form.shortdesc.data
    task_id = db.settings.find_one()['value']
    
    task = {'id':task_id, 'title':title, 'shortdesc':shortdesc, 'priority':priority}

    db.tasks.insert_one(task)
    updateTaskID(1)
    return redirect('/')

def deleteTask(form):
    key = form.key.data
    title = form.title.data

    if(key):
        db.tasks.delete_many({'id':int(key)})
    else:
        db.tasks.delete_many({'title':title})

    return redirect('/')

def updateTask(form):
    key = form.key.data
    shortdesc = form.shortdesc.data
    
    db.tasks.update_one(
        {"id": int(key)},
        {"$set":
            {"shortdesc": shortdesc}
        }
    )

    return redirect('/')

def resetTask(form):
    db.tasks.drop()
    db.settings.drop()
    db.settings.insert_one({'name':'task_id', 'value':0})
    return redirect('/')


@app.route('/', methods=['GET','POST'])
def main():
    # create form
    cform = CreateTask(prefix='createTask')
    dform = DeleteTask(prefix='deleteTask')
    uform = UpdateTask(prefix='updateTask')       # prefix – If provided, all fields will have their name prefixed with the value, got to view source <label for="updateTask-key">Task Key</label><br>
    reset = ResetTask(prefix='resetTask')

    # response
    if cform.validate_on_submit():
        return createTask(cform)                           # this calls the createTask function (above)
    if dform.validate_on_submit():
        return deleteTask(dform)
    if uform.validate_on_submit():
        return updateTask(uform)
    if reset.validate_on_submit():
        return resetTask(reset)

    # read all data
    docs = db.tasks.find()
    data = []
    for i in docs:
        data.append(i)

    # cform (This would be the variable used in sampleClasses.py) = cform (This refers to the form that was created. cform = CreateTask(prefix='createform'))
    return render_template('home.html', cform = cform, dform = dform, uform = uform, data = data, reset = reset)



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
