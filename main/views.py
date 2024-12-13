from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from .models import *


def index(request):
    return render(request, "main/index.html")


def explore(request):
    query = request.GET.get('q', '')
    event_type = request.GET.get('event_type', '')
    price_filter = request.GET.get('price', '')
    status_filter = request.GET.get('status', '')

    events = Event.objects.all()
    
    if query:
        events = events.filter(Q(name__icontains=query) | Q(location__icontains=query))
    if event_type:
        events = events.filter(eventtype=event_type)
    if price_filter == 'free':
        events = events.filter(price=0)
    elif price_filter == 'paid':
        events = events.filter(price__gt=0)
    if status_filter == 'upcoming':
        events = events.filter(starttime__gt=timezone.now())
    elif status_filter == 'live':
        events = events.filter(starttime__lte=timezone.now(), endtime__gte=timezone.now())
    elif status_filter == 'completed':
        events = events.filter(endtime__lt=timezone.now())

    paginator = Paginator(events, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/explore.html', {
        'page_obj': page_obj,
        'query': query,
        'event_type': event_type,
        'price_filter': price_filter,
        'status_filter': status_filter,
    })


def login_view(request):
    if request.method == "POST":
        post_data = request.POST
        user = authenticate(request, username=post_data["username"], password=post_data["password"])

        if user is None:
            messages.error(request, "Invalid credentials.")
            return render(request, "main/login.html")
        else:
            login(request, user=user)
            return redirect("explore")
    else:
        if request.user.is_authenticated:
            return redirect("explore")
        else:
            return render(request, "main/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            messages.warning(request, "Passwords do not match.")
            return render(request, "main/signup.html")

        try:
            user = User.objects.create_user(
                first_name = request.POST["first_name"],
                last_name = request.POST["last_name"],
                username = username, 
                email = email, 
                password = password,
                image = request.FILES.get('image')
            )
            user.save()
        except IntegrityError:
            messages.warning(request, "Username unavailable.")
            return render(request, "main/signup.html")
        
        login(request, user)
        messages.success(request, f"🌟 Welcome, {user.full_name}! Thanks for signing up.")
        return redirect("index")
    else:
        if request.user.is_authenticated:
            return redirect("index")
        else:
            return render(request, "main/signup.html")
        

def profile(request, username):
    try:
        profile = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "main/error.html", {
            "message": "User does not exist."
        })

    return render(request, "main/profile.html", {
        "profile": profile
    })


@login_required(login_url="login")
def update_profile(request):
    if request.method == "GET":
        return render(request, "main/update_profile.html")
    else:
        post_data = request.POST
        image = request.FILES.get('image')
        current_user = request.user

        current_user.first_name = post_data['first_name']
        current_user.last_name = post_data['last_name']
        current_user.email = post_data['email']
        if image:
            current_user.image = image
        current_user.save()

        messages.success(request, "Your profile has been updated successfully!")

        return redirect("profile", username=current_user.username)


def event_details(request, event_id):
    event = Event.objects.filter(pk=event_id).first()

    if not event:
        return render(request, "main/error.html", {
            "message": "Event not found."
        })

    attendance = None
    eventrequest = None
    rating = None
    
    if request.user.is_authenticated:
        attendance = Attendee.objects.filter(event=event, user=request.user).first()
        eventrequest = EventRequest.objects.filter(event=event, requester=request.user).first()
        rating = EventRating.objects.filter(event=event, user=request.user).first()

    return render(request, "main/event_details.html", {
        "event": event,
        "attendees": event.attendees.all(),
        "eventrequest": eventrequest,
        "attendance": attendance,
        "rating": rating,
        "rating_range": list(range(1, 6))
    })
    

@login_required(login_url="login")
def create_event(request):
    if request.method == "GET":
        return render(request, "main/create_event.html")
    else:
        post_data = request.POST
        thumbnail = request.FILES.get('thumbnail')

        new_event = Event(
            name = post_data['name'],
            organizer = request.user,
            starttime = post_data['starttime'],
            endtime = post_data['endtime'],
            price = float(post_data['price']) if post_data['price'] != '' else 0,
            thumbnail = thumbnail,
            description = post_data['description'],
            eventtype = post_data['eventtype'],
            location = post_data['location']
        )

        new_event.save()
        messages.success(request, f"Event '{new_event.name}' has been created successfully!")
        return redirect("event_details", event_id=new_event.id)
    

@login_required(login_url="login")
def edit_event(request, event_id):
    event = Event.objects.filter(pk=event_id).first()

    if not event:
        return render(request, "main/error.html", {
            "message": "Event not found."
        })

    if request.method == "GET":
        if event.organizer != request.user:
            messages.warning(request, "You're not authorized to edit this event.")
            return redirect("event_details", event_id=event.id)
        
        return render(request, "main/edit_event.html", {
            "event": event
        })
    else:
        post_data = request.POST
        thumbnail = request.FILES.get('thumbnail')

        event.name = post_data['name']
        event.starttime = post_data['starttime']
        event.endtime = post_data['endtime']
        event.price = float(post_data['price']) if post_data['price'] != '' else 0
        if thumbnail:
            event.thumbnail = thumbnail
        event.description = post_data['description']
        event.eventtype = post_data['eventtype']
        event.location = post_data['location']

        event.save()

        return redirect("event_details", event_id=event.id)
    

@require_POST
def delete_event(request, event_id):
    event = Event.objects.filter(pk=event_id).first()

    if event == None:
        messages.warning(request, "Event not found!")
        return redirect("explore")
    elif event.organizer != request.user:
        messages.warning(request, "You are not authorized to delete the event.")
        return redirect("event_details", event_id=event_id)
    else:
        event.delete()
        messages.success(request, "Event has been deleted successfully!")
        return redirect("explore")
    

@login_required(login_url="login")
def register_event(request, event_id):
    event = Event.objects.filter(id=event_id).first()

    if not event:
        return render(request, "main/error.html", {
            "message": "Event not found."
        })
    
    if not event.is_notstarted:
        messages.info(request, "Registrations closed!")
        return redirect("event_details", event_id=event.id)

    if request.method == 'GET':
        return render(request, "main/payment.html", {"event": event})

    elif request.method == 'POST':
        if event.isfree:
            Attendee.objects.get_or_create(user=request.user, event=event)
            messages.success(request, "Registered successfully!")
            return redirect("event_details", event_id=event.id)

        card_details = request.POST.get("card-details", "").strip()

        if not card_details or len(card_details) != 16 or not card_details.isdigit():
            messages.error(request, "Invalid card details. Please enter a 16-digit mock card number.")
            return redirect("register_event", event_id=event_id)

        try:
            payment = Payment(
                user=request.user,
                event=event,
                amount=event.price,
                card_details=card_details,
                status='Success',
            )
            payment.save()

            Attendee.objects.get_or_create(user=request.user, event=event)
            messages.success(request, "Payment complete! You have been registered successfully.")
            return redirect("event_details", event_id=event.id)

        except Exception as e:
            messages.error(request, "Try again. Payment faild.")
            return redirect("register_event", event_id=event_id)
    

@login_required(login_url="login")
@require_POST
def submit_event_request(request, event_id):
    event = Event.objects.get(id=event_id)
    er = EventRequest(
        requester = request.user,
        event = event,
        status = 'Pending'
    )
    er.save()
    messages.success(request, "Request submitted.")
    return redirect("event_details", event_id=event_id)


@login_required(login_url="login")
@require_POST
@csrf_exempt
def accept_event_request(request, er_id):
    er = EventRequest.objects.get(id=er_id)
    event = Event.objects.get(id=er.event.id)

    if event.organizer != request.user:
        return JsonResponse({
            "status": 400,
            "message": "You are not authorized to perform this action"
        })

    er.status = 'Accepted'
    er.save()

    if event.isfree:
        attendee = Attendee(user=er.requester, event=event)
        attendee.save()

    return JsonResponse({
        "status": 200,
        "message": "Accepted",
        "event_id": event.id,
        "event_name": event.name
    })


@login_required(login_url="login")
@require_POST
@csrf_exempt
def decline_event_request(request, er_id):
    er = EventRequest.objects.get(id=er_id)
    event = Event.objects.get(id=er.event.id)

    if event.organizer != request.user:
        return JsonResponse({
            "status": 400,
            "message": "You are not authorized to perform this action"
        })

    er.status = 'Declined'
    er.save()

    return JsonResponse({
        "status": 200,
        "message": "Declined",
        "event_id": event.id,
        "event_name": event.name
    })


@login_required(login_url="login")
@require_POST
def rate_event(request, event_id):
    event = Event.objects.get(id=event_id)
    attendance = Attendee.objects.filter(user=request.user, event=event, attended="Yes").first()

    if attendance == None:
        messages.info(request, 'Only attended users can submit a feedback for an event.')
        return redirect("event_details", event_id=event_id)
    
    rating = EventRating(user=request.user, event=event, value=int(request.POST['rating']))
    rating.save()
    messages.success(request, "Thank you for the feedback.")

    return redirect("event_details", event_id=event_id)


@login_required(login_url="login")
@require_POST
def confirm_attendance(request, event_id):
    event = Event.objects.get(id=event_id)
    attendance = Attendee.objects.filter(user=request.user, event=event, attended="Unknown").first()

    if attendance == None:
        messages.info(request, 'Only registered people can mark attendance.')
        return redirect("event_details", event_id=event_id)
    
    attendance.attended = request.POST['attended']
    attendance.save()
    messages.success(request, 'Thank you for the confirmation.')

    return redirect("event_details", event_id=event_id)


def settings(request):
    return render(request, "main/settings.html")


@login_required(login_url="login")
def change_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        password = request.POST.get('password')

        if not request.user.check_password(password):
            messages.error(request, "The password you entered is incorrect.")
        elif User.objects.filter(username=new_username).exists():
            messages.error(request, "This username is already taken. Please choose another.")
        else:
            request.user.username = new_username
            request.user.save()
            messages.success(request, "Your username has been updated successfully.")
            return redirect('settings')
    else:
        return render(request, 'main/change_username.html')


@login_required(login_url="login")
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, "The current password you entered is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "The new passwords do not match.")
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "Your password has been updated successfully.")
            return redirect('settings')

    return render(request, 'main/change_password.html')


@login_required(login_url="login")
def delete_account(request):
    if request.method == "GET":
        return render(request, "main/delete_account.html")
    
    password = request.POST.get("password")
    if not request.user.check_password(password):
        messages.error(request, "Incorrect password. Account not deleted.")
        return redirect("delete-account")
    
    request.user.delete()
    messages.success(request, "Your account has been deleted successfully.")
    return redirect("index")
