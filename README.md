# Employee Management System

Application for management employees write in Django.

## Getting Started

1. Create a virtualenv
2. Install Django 3.0
3. Install requirements.txt - pip install -r requirements.txt
4. Run the server

## Built With

* Django 
* JavaScript
* HTML
* CSS

## Features

### Users

* Four type of users (director, supervisor, employee, hr(human resources))

### Leaves

* Adding Vacation (Vacation leave, Occasional holidays, Vacation on demand, Vacation childcare, Unpaid leave)
* Check status of vacation (pending, rejected, accepted)
* The data from Vacation Leaves is displayed on the calendar
* All employees have vacation limits
* The limits change after your supervisor accepts your vacation request
* Generate .xls files with employee vacation limits or vacation leave
* Notifiactions for all users Etc. when employee add request for vacation leave, notifications will be send for supervisor

### Regulation

* Adding regulation by HR user
* The sent regulation have to read before accept
* User have to accept the regulation before he can access the entire system

## Inspiration

This application was created because I wanted to create something that might be useful to someone and not another todolist

## Application development

In the near future I would like add:

* Chat
* Charts

## Some screenshots from application

### Dashboard page  

![alt text](https://raw.githubusercontent.com/marcmas/employeemanagementsystem/master/ems_dashboard.png) 

### Add leave page  

![alt text](https://raw.githubusercontent.com/marcmas/employeemanagementsystem/master/ems_add_leave.png)
