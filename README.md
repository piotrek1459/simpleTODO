# TO-DO

## Video Demo:  https://youtu.be/Wg59VBgZURw

## Description:

###### About:
This is to-do list with login/register system.
This project covers CRUD functionalities.
You can add, update and also delete tasks.
I used Flask and Bootstrap in order to create this web-based application.
This application is minimalist in style because I wanted to pay more attention to the backend site.

###### Register/Login:
Login is required to use this app.
You can create your account and then login.
It is based on simple if else block with methods post and get.
I choose sqlite3 because it is simple and light database and it really works well with Flask.
Of course all validation is done on the backend site.
In register there are validations for repetitions of username and matching confirmation with password. 
Password is stored in database as a hash.
In order to do so I used werkzeug.security library.
Functions
check_password_hash 
and
generate_password_hash 
come in handy here.
If everything went right user is registered and automatically logged in.
In login there is simple SELECT query and if username and password are ok then user is logged in.

###### Index
This is main part of this app.
It contains to-do list and all functionalities.
In right corner the user can log out.
User can add task by clicking plus sign, update them by clicking on task title and delete them by clicking X sign.
Completed tasks have checked checkbox and line-through them.

###### Index fuctions:
To acces index page you need to be logged in.
I used @login_required from flask documentation.
I also used session from flask in order to be able to store user session.

###### Add Task:
By clicking on plus user is redirected to adding form.
Title box is required the rest is optional.
User can always back by clicking arrow.
By clicking add task is added in database by post method.

###### Add Task functions:
It is based on simple if else block with methods post and get.

###### Update Task:
By clicking on task title user is redirected to updating form.
In there user can change title add/change description and mark task as completed.
By clicking save changes are saved in database by post method.
If user click arrow changes are not saved.

###### Update Task functions:
It is based on simple if else block with methods post and get.

###### Delete Task
By clicking X sign the task is deleted from database.
Then user is redirected to index page.

###### Delete Task functions:
In order to delete task I created route which has one task to delelete task.
It has only one method: post.
It is simply connecting to the database and delete row from database.




