from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from django.core import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
from registor.models import UserAccount, UserTransaction, UserNotification
from registor.currencyConversion import convertCurrency
from datetime import datetime
import re
import secrets
import decimal
import json
import requests

# Create your views here.

# This Function will User Our RestFull Api to Get the Convertion From One Currency to Another 
def getCurrencyConvert(From, To, Amount):
    # We Will Gonna Send a Request to Our Api and Return Converted Values to Our User
    return float(requests.get('http://127.0.0.1:8000/conversion/'+ str(From) +'/' + str(To) + '/' + str(Amount) + '/').json()['converted_amount'])

# Display All Notification to the User
def viewNotificationPage(request):

    # First We Check if User Exist or Not
    userEmail = request.session.get("userEmail", "None")
    userKey = request.session.get("privateKey", "None")
    userData = []

    # Redirect User to Sign In Page
    if (userEmail == "None" or userKey == "None"):
        return render(request, "supporting/redirect.html", {"Title": "Access Denied!", "Name": "Sign In Page", "Link": "SignIn"})

    # Try user Email and Key to Verify User
    try:
        # Check if User Exist
        user = UserAccount.objects.get(email=userEmail, private_key=userKey)

        # We Now Sure User is Exist
        # Now We Get All His Imformation
        userData = user

        # Clear User Notifications
        userData.notification_count = 0
        userData.save()

    except:
        # User Does not Exist
        return render(request, "supporting/redirect.html", {"Title": "Invalid User!", "Name": "Sign In Page", "Link": "SignIn"})
    
    # Now We Know That Our User is Verified

    # Get All User Notifications
    notifications = UserNotification.objects.filter(notification_receiver=userData)
    notifications_json = json.loads(serializers.serialize('json', notifications))

    # Convert Our Notifications To Json Format
    allNotifications = []
    # Make All the Data in a Format
    for x in notifications_json:
        allNotifications.append({"Data": x['fields'] , "PK" : x['pk']})
    # Display All Transaction to the Home Page
    allNotifications.reverse()

    # Send All This Data to Our HTML Template
    context = {
        "notificationCount" : userData.notification_count,
        "userFirstName": userData.first_name,
        "userLastName": userData.last_name,
        "totalAmount": userData.currency_type + " " + str(userData.total_amount),
        "currencyType": userData.currency_type,
        "allNotifications": allNotifications
    }

    # Render Our Notification Page
    return render(request, "app/notifications.html", context)

# Display User All the Transactions
def viewTransactionsPage(request):

    # First We Check if User Exist or Not
    userEmail = request.session.get("userEmail", "None")
    userKey = request.session.get("privateKey", "None")
    userData = []

    # Redirect User to Sign In Page
    if (userEmail == "None" or userKey == "None"):
        return render(request, "supporting/redirect.html", {"Title": "Access Denied!", "Name": "Sign In Page", "Link": "SignIn"})

    # Try user Email and Key to Verify User
    try:
        # Check if User Exist
        user = UserAccount.objects.get(email=userEmail, private_key=userKey)

        # We Now Sure User is Exist
        # Now We Get All His Imformation
        userData = user

    except:
        # User Does not Exist
        return render(request, "supporting/redirect.html", {"Title": "Invalid User!", "Name": "Sign In Page", "Link": "SignIn"})

    # We Know Sure User Exist

    # Get All Transaction of User
    transactions = UserTransaction.objects.filter(Q(from_person=userData.email) | Q(
        to_person=userData.email))
    transaction_json = json.loads(serializers.serialize('json', transactions))

    allTransactions = []
    # Make All the Data in a Format
    for x in transaction_json:
        transactionData = x['fields']
        Type = ""
        Reamining = 0.00
        Amount = 0.00
        if userData.email == transactionData['from_person']:
            Type = "Send"
            Reamining = transactionData['sender_balance']
            Amount = transactionData['sender_amount']
        else:
            Type = "Receive"
            Reamining = transactionData['receiver_balance']
            Amount = transactionData['receiver_amount']

        newTransaction = {
            "Type": Type,
            "Date": datetime.strptime(transactionData['transaction_date'], '%Y-%m-%d').strftime('%m/%d/%Y'),
            "Amount": Amount,
            "To": transactionData['to_person'],
            "From": transactionData['from_person'],
            "Remaining": Reamining
        }
        allTransactions.append(newTransaction)

    # Display All Transaction to the Home Page
    allTransactions.reverse()
    context = {
        "notificationCount" : userData.notification_count,
        "userFirstName": userData.first_name,
        "userLastName": userData.last_name,
        "totalAmount": userData.currency_type + " " + str(userData.total_amount),
        "lastTransactions":  allTransactions
    }

    # Render Our Transaction Page
    return render(request, "app/transactions.html", context)

# View User The Entire Home Page With All Functionality
def viewHomePage(request):

    # First We Check if User Exist or Not
    userEmail = request.session.get("userEmail", "None")
    userKey = request.session.get("privateKey", "None")
    userData = []

    # Redirect User to Sign In Page
    if (userEmail == "None" or userKey == "None"):
        return render(request, "supporting/redirect.html", {"Title": "Access Denied!", "Name": "Sign In Page", "Link": "SignIn"})

    # Try user Email and Key to Verify User
    try:
        # Check if User Exist
        user = UserAccount.objects.get(email=userEmail, private_key=userKey)

        # We Now Sure User is Exist
        # Now We Get All His Imformation
        userData = user

    except:
        # User Does not Exist
        return render(request, "supporting/redirect.html", {"Title": "Invalid User!", "Name": "Sign In Page", "Link": "SignIn"})

    context = {
        "notificationCount" : userData.notification_count,
        "userFirstName": userData.first_name,
        "userLastName": userData.last_name,
        "totalAmount": userData.currency_type + " " + str(userData.total_amount),
        "currencyType": userData.currency_type,
        "messageType": "alert alert-danger",
        "messageHeading": "Message Heading",
        "messageDisplay": "none",
        "messageContent": "This is a Alert Message",
        "lastTransactions": []
    }

    # User Send a Post Method To the Home Page
    if request.method == 'POST':

        # Clear the Request Notification if Exists
        if(not request.POST.get("notifyID") == None):
            notify = UserNotification.objects.get(id=int(request.POST.get("notifyID")))
            notify.delete()

        # User Want to Send Some Money to Other Using Email Account
        if (request.POST.get("paymentType") == "sendMoney"):
            
            # Get All the Imformation
            recieverEmail = request.POST.get("userEmail")
            sendAmount = float(request.POST.get("userAmount"))

            # We Check if User Does Have Enough Amount or Not
            if (sendAmount < userData.total_amount):
                # User Have Enough Amount
                try:

                    if recieverEmail == userData.email:
                        raise Exception("Invalid Email Address")

                    # Now We Check if the Reciever Email is Valid or Not
                    receiver = UserAccount.objects.get(email=recieverEmail)

                    # Now Receiver Email is Verified

                    # Now We Make the Payment
                    receiverGets = decimal.Decimal(str(round(getCurrencyConvert(userData.currency_type, receiver.currency_type,sendAmount), 2)))
                    sendAmount = decimal.Decimal(str(sendAmount))
                    currentAmount = receiver.total_amount
                    currentAmount = currentAmount + receiverGets
                    receiver.total_amount = currentAmount
                    receiver.notification_count += 1
                    receiver.save()

                    # Now Remove the Amount from the Send
                    currentAmount = userData.total_amount
                    currentAmount = currentAmount - sendAmount
                    userData.total_amount = currentAmount
                    userData.notification_count += 1
                    userData.save()

                    # Send a Success Message to the Sender
                    context['messageHeading'] = "Send Money Successfully"
                    context['messageContent'] = "You have send " + userData.currency_type + \
                        " " + str(float(sendAmount)) + \
                        " . To the User: " + receiver.email + "."
                    context["messageDisplay"] = "block"
                    context["messageType"] = "alert alert-success"
                    context["totalAmount"] = userData.currency_type + \
                        " " + str(userData.total_amount)

                    # Record the Transaction between the Users
                    transaction = UserTransaction()
                    date_obj = datetime.now()
                    transaction.transaction_date = date_obj.strftime(
                        '%Y-%m-%d')
                    transaction.sender_amount = sendAmount
                    transaction.receiver_amount = receiverGets
                    transaction.from_person = userData.email
                    transaction.to_person = receiver.email
                    transaction.sender_balance = userData.total_amount
                    transaction.receiver_balance = receiver.total_amount
                    transaction.save()

                    # Create Two Notifications: One For Sender and Other for Receiver
                    notification = UserNotification.objects.create(notification_receiver=userData, notification_date= date_obj.strftime('%Y-%m-%d'), notification_msg= "You have send the amount " + userData.currency_type + " " + str(transaction.sender_amount) + " to " + receiver.email, notificatoin_type= "Send", total_amount=transaction.sender_amount, other_person=receiver.email)
                    notification.save()
                    notificationR = UserNotification.objects.create(notification_receiver=receiver, notification_date= date_obj.strftime('%Y-%m-%d'), notification_msg= "You have received amount of " + receiver.currency_type + " " + str(transaction.receiver_amount) + " from " + userData.email, notificatoin_type= "Receive", total_amount=transaction.receiver_amount , other_person=userData.email)
                    notificationR.save()

                    # Send a Redirect
                    return render(request, "supporting/redirect.html", {"Title": "Send Money Successfully", "Name": "Home Page", "Link": "Home"})
                
                # Error Handling
                except Exception as e:
                    context['messageHeading'] = "Invalid Reciever Email"
                    context['messageContent'] = "The Email you entered for amount receive is Invalid. Please Enter a valid receiver email."
                    context["messageDisplay"] = "block"
                    context["messageType"] = "alert alert-danger"

            # User Does not Have Enough Money
            else:
                context['messageHeading'] = "Not Enough Amount"
                context['messageContent'] = "You does not have Enough Amount in your Account for this Payment."
                context["messageDisplay"] = "block"
                context["messageType"] = "alert alert-danger"

        # User Want to Request Some Money to Other Using Email Account
        elif (request.POST.get("paymentType") == "requestMoney"):

            # Get All the Imformation
            recieverEmail = request.POST.get("userEmail")
            sendAmount = float(request.POST.get("userAmount"))

            try:
                # Now We Check if the Reciever Email is Valid or Not
                receiver = UserAccount.objects.get(email=recieverEmail)

                # Send a Request Message to the Sender
                context['messageHeading'] = "Request Money Successfully"
                context['messageContent'] = "You have Request " + userData.currency_type + \
                    " " + str(float(sendAmount)) + \
                    " . from the User: " + receiver.email + "."
                context["messageDisplay"] = "block"
                context["messageType"] = "alert alert-success"
                context["totalAmount"] = userData.currency_type + \
                    " " + str(userData.total_amount)
                

                # Add Notification To Receiver Account
                receiver.notification_count += 1
                receiver.save()

                # Send a Request Notification To Our User
                date_obj = datetime.now()
                notificationR = UserNotification.objects.create(notification_receiver=receiver, notification_date= date_obj.strftime('%Y-%m-%d'), notification_msg = userData.email + " send a request of " + receiver.currency_type + " " + str(round(getCurrencyConvert( userData.currency_type, receiver.currency_type, sendAmount), 2)) +  " from your account. Please Choose do you want to Send Him This Amount." , notificatoin_type= "Request", total_amount=decimal.Decimal(round(getCurrencyConvert(userData.currency_type, receiver.currency_type,sendAmount), 2)), other_person=userData.email)
                notificationR.save()

                # Send a Redirect
                return render(request, "supporting/redirect.html", {"Title": "Request Money Successfully", "Name": "Home Page", "Link": "Home"})
            
            # Error Handling
            except Exception as e:
                context['messageHeading'] = "Invalid Requesting Person Email"
                context['messageContent'] = "The Email you entered for amount requesting is Invalid. Please Enter a valid request email."
                context["messageDisplay"] = "block"
                context["messageType"] = "alert alert-danger"

    # Get All Transaction of User
    transactions = UserTransaction.objects.filter(Q(from_person=userData.email) | Q(
        to_person=userData.email))
    transaction_json = json.loads(serializers.serialize('json', transactions))

    allTransactions = []
    # Make All the Data in a Format
    for x in transaction_json:

        transactionData = x['fields']
        Type = ""
        Reamining = 0.00
        Amount = 0.00
        if userData.email == transactionData['from_person']:
            Type = "Send"
            Reamining = transactionData['sender_balance']
            Amount = transactionData['sender_amount']
        else:
            Type = "Receive"
            Reamining = transactionData['receiver_balance']
            Amount = transactionData['receiver_amount']

        newTransaction = {
            "Type": Type,
            "Date": datetime.strptime(transactionData['transaction_date'], '%Y-%m-%d').strftime('%m/%d/%Y'),
            "Amount": Amount,
            "To": transactionData['to_person'],
            "From": transactionData['from_person'],
            "Remaining": Reamining
        }
        allTransactions.append(newTransaction)

    # Display All Transaction to the Home Page
    allTransactions.reverse()
    context["lastTransactions"] = allTransactions[:5]

    return render(request, "app/home.html", context)

# Logout a User and Redirect to SignIn Page
def viewLogoutPage(request):
    request.session.flush()
    return render(request, "supporting/redirect.html", {"Title": "Logout From Paypal", "Name": "Sign In Page", "Link": "SignIn"})

# This View Will Handle Sign In Page and Its Requests
def viewSignInPage(request):

    # Check if the Form is Submitted or Not
    if request.method == 'POST':

        # Send a Default Login Page
        context = {
            "messageType": "alert alert-success",
            "messageHeading": "Message Heading",
            "messageDisplay": "block",
            "messageContent": "This is a Alert Message"
        }

        # Try to Login User
        try:
            # Get User Email and Password
            userEmail = request.POST.get('userEmail')
            userPassword = request.POST.get('userPassword')

            # Check if User Exist
            user = UserAccount.objects.get(email=userEmail)

            # Check if User Password is Valid or Not
            if (not check_password(userPassword, user.password)):
                raise UserAccount.DoesNotExist(
                    "User Password is Invalid. Please Enter Correct Password")

            # Create a Unique Key For Our Session
            user.private_key = secrets.token_hex(32)

            # Save This Uniqe Key IN the Database
            user.save()

            # User is Exist
            request.session['userEmail'] = userEmail
            request.session['privateKey'] = user.private_key
            return redirect("Home")

        except UserAccount.DoesNotExist:

            # user does not exist
            context = {
                "messageType": "alert alert-danger",
                "messageHeading": "Not Existed",
                "messageDisplay": "block",
                "messageContent": "Your Account does not exist. Check Your Email and Password!"
            }

        return render(request, "accountsForm/signIn.html", context)

    else:

        # Send a Default Login Page
        context = {
            "messageType": "alert alert-danger",
            "messageHeading": "Message Heading",
            "messageDisplay": "none",
            "messageContent": "This is a Alert Message"
        }
        return render(request, "accountsForm/signIn.html", context)

# This View Will Handle Registor Page and Its Requests
def viewSignUpPage(request):

    # Check if the Form is Submitted or Not
    if request.method == 'POST':

        # Display Some Info to the User
        context = {
            "messageType": "alert alert-success",
            "messageHeading": "Account Created",
            "messageDisplay": "block",
            "messageContent": "Your Account Have been Successfully Created! Now Go to Login Page."
        }

        # Do something with the POST data
        try:
            # Get All the User Imformation
            userName = request.POST.get('userName')
            userFirstName = request.POST.get('userFirstName')
            userLastName = request.POST.get('userLastName')
            userEmail = request.POST.get('userEmail')
            userPassword = request.POST.get('userPassword')
            userCurrency = request.POST.get("userCurrency")

            # Check user Email is Valid or Not
            if (not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', userEmail)):
                raise Exception("Please Enter a Valid Email Address!")

            # Check if User Name is Valid or Not
            if (userFirstName == "" or userLastName == "" or userName == ""):
                raise Exception("Please Enter a Valid Data.")

            # Check If Our Password is Strong Enough
            validate_password(userPassword)

            # Ecnode Our Password With a Added Salt for Extra Security
            userPassword = make_password(userPassword)

            # After the Check The User Account Must have to Saved
            user = UserAccount(user_name=userName, first_name=userFirstName, last_name=userLastName, email=userEmail, password=userPassword,
                               currency_type=userCurrency, total_amount=round(getCurrencyConvert('USD', userCurrency,1000), 2))
            user.created_at = datetime.now()
            user.private_key = secrets.token_hex(32)
            user.save()

        except Exception as e:
            # Send a Default Login Page
            context = {
                "messageType": "alert alert-danger",
                "messageHeading": "Error Occured!",
                "messageDisplay": "block",
                "messageContent": str(e)
            }
        return render(request, "accountsForm/signUp.html", context)

    else:

        # Send a Default Login Page
        context = {
            "messageType": "alert alert-danger",
            "messageHeading": "Message Heading",
            "messageDisplay": "none",
            "messageContent": "This is a Alert Message"
        }
        return render(request, "accountsForm/signUp.html", context)

# This will will be use as a RestFull api to convert Currencies
def conversionView(request, from_currency, to_currency, amount):
    amount = float(amount)
    converted_amount = round(convertCurrency(amount, from_currency, to_currency),0)
    response = {
        'from_currency': from_currency,
        'to_currency': to_currency,
        'amount': amount,
        'converted_amount': converted_amount,
    }
    return JsonResponse(response)

# Display Terms and Conditions
def viewTermsAndConditions(request):
    return render(request, "accountsForm/terms.html")

def redirectToSignIn(request):
    return redirect("/SignIn")
