from django.shortcuts import render, HttpResponse, redirect

from .forms import UserRegistrationForm, UserLoginForm, NewTicketForm, UpdateTicketForm
from django.contrib.auth import authenticate, get_user_model, login, logout


import requests, json

auth_token="9446933330c7f886fbdf16782906a9e0" #YOUR_AUTH_TOKEN
org_id="60001280952" #YOUR_ORGANISATION_ID


#All Tickets
def all_ticket(request):
    params="sortBy=-modifiedTime&limit=4"

    headers={
        "Authorization":auth_token,
        "orgId":org_id,
        "contentType": "application/json; charset=utf-8"
    }

    apiRequest=requests.get('https://desk.zoho.in/api/v1/tickets?'+params, headers=headers)

    if apiRequest.status_code == 200:
        print("Request Successful,Response:")
        jData = json.loads(apiRequest.content)
        data = jData['data']
        print(data)
    else:
        print("Request not successful,Response code ",apiRequest.status_code," \nResponse : ",apiRequest.content)


    context = {
        'data' : data
    }

    return render(request, 'all_ticket.html', context)





#New Ticket

def create_ticket(request):
    if not request.user.is_authenticated:
        return redirect('login')

    headers={
        "Authorization":auth_token,
        "orgId":org_id,
        "contentType": "application/json; charset=utf-8"
    }

    initial_dict = {
        "name" : request.user.first_name + " " + request.user.last_name,
        "email" : request.user.email,
    }

    form = NewTicketForm(initial=initial_dict)

    if request.method == 'POST': 
        form = NewTicketForm(request.POST)
        if form.is_valid():
            firstName = request.user.first_name
            lastName = request.user.last_name
            # department = form.cleaned_data.get('department')
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            category = form.cleaned_data.get('category')
            description = form.cleaned_data.get('description')
            priority = form.cleaned_data.get('priority')

            ticket_data={
                "departmentId":"7189000000051431",
                # "department":department,
                "contact":{
                    "firstName" : firstName,
                    "lastName" : lastName,
                    "email" : email,
                    "phone" : "123",
                },
                "subject":subject,
                "description":description,
                "category":category,
                "priority":priority,
            }

            apiRequest=requests.post('https://desk.zoho.in/api/v1/tickets', headers=headers,data=json.dumps(ticket_data))

            if apiRequest.status_code == 200:
                print("Request Successful,Response:")
                print(apiRequest.content)
                print(json.loads(apiRequest.content))
                return redirect("all_ticket")
            else:
                print("Request not successful,Response code ",apiRequest.status_code," \nResponse : ",apiRequest.content)


    context = {
        'form': form,
    }

    return render(request, 'create_ticket.html', context)



#Update Ticket

def update_ticket(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    ticket_id=str(pk) #TICKET_ID_TO_UPDATE
    form = UpdateTicketForm()
    if request.method == 'POST': 
        form = UpdateTicketForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            description = form.cleaned_data.get('description')
            priority = form.cleaned_data.get('priority')

            ticket_data={
                    "subject":subject,
                    "priority":priority,
                    "description":description
            }

            headers={
                "Authorization":auth_token,
                "orgId":org_id,
                "contentType": "application/json; charset=utf-8"
            }

            if ticket_id:

                apiRequest=requests.patch('https://desk.zoho.in/api/v1/tickets/'+ticket_id, headers=headers,data=json.dumps(ticket_data))

                if apiRequest.status_code == 200:
                    print("Request Successful,Response:")
                    print(apiRequest.content)
                    return redirect('all_ticket')
                else:
                    print("Request not successful,Response code ",apiRequest.status_code," \nResponse : ",apiRequest.content)

            else:
                print("Ticket ID is missing")

    context = {
        'form' : form,
        'pk' : pk,
    }

    return render(request, 'update_ticket.html', context)

    


    



def single_ticket(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
        
    ticket_id = str(pk)

    headers={
        "Authorization":auth_token,
        "orgId":org_id,
        "contentType": "application/json; charset=utf-8"
    }

    if ticket_id:

        apiRequest=requests.get('https://desk.zoho.in/api/v1/tickets/'+ticket_id, headers=headers)

        if apiRequest.status_code == 200:
            print("Request Successful,Response:")
            jData = json.loads(apiRequest.content)
            print(jData)
        else:
            print("Request not successful,Response code ",apiRequest.status_code," \nResponse : ",apiRequest.content)

    else:
        print("Ticket ID is missing")

    
    context = {
        'd' : jData
    }


    return render(request, 'single_ticket.html', context)



def userLogin(request):
    if request.method == 'POST': 
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('all_ticket')

    else:
        form = UserLoginForm()
                

    context = {
        'form': form,
    }

    return render(request, "login.html", context)


def userSignup(request):
    if request.method == 'POST': 
        form = UserRegistrationForm(request.POST) 
        if form.is_valid(): 
            user = form.save() 
            pass1 = form.cleaned_data.get('password')
            user.set_password(pass1)
            user.save()
            return redirect('login')

    else: 
        form = UserRegistrationForm() 
    
    context = {
        'form': form,
    }

    return render(request, "signup.html", context)


def logout_view(request):
    logout(request)
    return redirect('login')