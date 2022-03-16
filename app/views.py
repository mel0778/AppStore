from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.
def index(request):
    """Shows the main page"""

    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM buyer WHERE username = %s", [request.POST['username']])

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buyer ORDER BY username")
        customers = cursor.fetchall()

    result_dict = {'records': buyer}

    return render(request,'app/index.html',result_dict)

# Create your views here.
def view(request, cust_username):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buyer WHERE username = %s", [cust_username])
        customer = cursor.fetchone()
    result_dict = {'cust': buyer}

    return render(request,'app/view.html',result_dict)

# Create your views here.
def add(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM buyer WHERE username = %s", [request.POST['username']])
            current = cursor.fetchone()
            ## No customer with same id
            if current == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO buyer VALUES (%s, %s, %s, %s, %s)"
                        , [request.POST['name'], request.POST['phone_num'], request.POST['hall'],
                           request.POST['wallet_balance'] , request.POST['username'] ])
                return redirect('index')    
            else:
                status = 'Buyer with username %s already exists' % (request.POST['username'])


    context['status'] = status
 
    return render(request, "app/add.html", context)

# Create your views here.
def edit(request, cust_username):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buyer WHERE username = %s", [cust_username])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE customers SET name = %s, phone_num = %s, hall = %s, wallet_balance = %s, username = %s WHERE username = %s"
                    , [request.POST['name'], request.POST['phone_num'], request.POST['hall'],
                           request.POST['wallet_balance'] , request.POST['username'], cust_username ])
            status = 'Customer edited successfully!'
            cursor.execute("SELECT * FROM buyer WHERE username = %s", [cust_username])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit.html", context)
