from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import AbstractUser
from . models import User as CustomUser
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . models import Event,BookEvent,ServiceAvailability,VenueBooking,Venue,TransportationBooking,TransportationService,CateringBooking,CateringService,DecorationsBooking,DecorationsService,PhotographyBooking,PhotographyService,BridalGroomService,BridalGroomServiceBooking
from datetime import datetime
from datetime import date

# Create your views here.

def base(request):
    return render(request,'index.html')
def home(request):
    return render(request,'home.html')



def register_user(request):
    if request.method == "POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        phone=request.POST.get('phone')

        if not username or not email or not password or not confirm_password or not phone:
            messages.error(request,'All feild require')
            return redirect('user_register')
        if CustomUser.objects.filter(username=username):
            messages.error(request,"Username already exists !!")
            return redirect('user_register')
        if CustomUser.objects.filter(email=email):
            messages.error(request,"Email already exists !!")
            return redirect('user_register')
        if confirm_password!=password:
            messages.error(request,"Enter passowrd properly !!")
            return redirect('user_register')
        
        user=CustomUser.objects.create_user(username=username,email=email,password=password)
        user.phone=phone
        user.save()
        return redirect('user_login')
    else:
        messages.error(request,'Something went wrong ')
    return render(request,'user_register.html')

def login_user(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user= authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid Username or Password ')
            return redirect('user_login')
    return render(request,'user_login.html')
        

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required
def user_dashboard(request):
    return render(request,'user_dashboard.html')

@login_required
def user_profile(request):
    user=request.user
    if request.method =="POST":
        user.username=request.POST.get('email',user.username)
        user.phone=request.POST.get('phone',user.phone)
        user.email=request.POST.get('username',user.email)
        user.save()
    return render(request,'user_profile.html',{'user':user})


## event ## 


@login_required
def user_event_list(request):
    events = Event.objects.all()  
    return render(request, 'user_event_list.html', {'events': events})

@login_required
def user_book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":

        service_type = request.POST.get("service_type")
        event_date = request.POST.get("event_date")
        customize=request.POST.get('customize')

        is_booked = ServiceAvailability.objects.filter(
            service_type=service_type,
            service_id=event.id,
            booked_date=event_date
        ).exists()

        if is_booked:
            messages.error(request, "This service is already booked for the selected date.")
            return redirect('user_book_event', event_id=event_id)

        BookEvent.objects.create(
            user=request.user,
            event=event,
            our_service=service_type,
            customize=customize,
            status="pending"
        )

        ServiceAvailability.objects.create(
            service_type=service_type,
            service_id=event.id,
            booked_date=event_date
        )

        messages.success(request, "Event booking request submitted. Awaiting confirmation.")
        return redirect('user_event_bookings')

    return render(request, 'user_book_event.html', {'event': event})

@login_required
def user_event_bookings(request):
    bookings = BookEvent.objects.filter(user=request.user)
    return render(request, 'user_bookings_event.html', {'bookings': bookings})


## venu ##

@login_required
def venue_list(request):
    venues = Venue.objects.filter(available=True)
    return render(request, 'user_venue.html', {'venues': venues})

@login_required
def book_venue(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id, available=True)

    if request.method == "POST":
        event_date = request.POST.get('event_date')
        venue_customize=request.POST.get('venue_customize')
        event_date = datetime.strptime(event_date, "%Y-%m-%d").date()

        if event_date < date.today():
            messages.error(request, "You cannot book a venue for a past date.")
            return redirect('book_venue', venue_id=venue_id)
        
        is_booked = ServiceAvailability.objects.filter(
            service_type="Venue", 
            service_id=venue.id, 
            booked_date=event_date
        ).exists()

        if is_booked:
            messages.error(request, "This venue is already booked on the selected date. Please choose another date.")
        else:
            VenueBooking.objects.create(
                user=request.user, 
                venue=venue, 
                event_date=event_date, 
                venue_customize=venue_customize,
                status="Pending"
            )
            ServiceAvailability.objects.create(
                service_type="Venue",
                service_id=venue.id,
                booked_date=event_date
            )

            messages.success(request, "Venue booking request submitted successfully!")
            return redirect('user_bookings')

    return render(request, 'book_venue.html', {'venue': venue})

@login_required
def user_bookings(request):
    bookings = VenueBooking.objects.filter(user=request.user)
    return render(request, 'user_booking_status.html', {'bookings': bookings})


## Transportation ##

@login_required
def user_transport_list(request):
    transports=TransportationService.objects.filter(available=True)
    return render(request, 'user_transport_list.html', {'transports': transports})

@login_required
def user_book_transport(request,service_id):
    service=get_object_or_404(TransportationService,id=service_id,available=True)
    if request.method =="POST":
        vehicle_type = request.POST.get("vehicle_type")
        seats = request.POST.get("seats")
        event_date = request.POST.get("event_date")
        rent_car=request.POST.get('rent_car')

        if date.fromisoformat(event_date)< date.today():
            messages.error(request, "You cannot book a transport for a past date.")
            return redirect('user_book_transport', service_id=service_id)
        
        is_booked = ServiceAvailability.objects.filter(
            service_type="Transportation", 
            service_id=service.id, 
            booked_date=event_date
        ).exists()

        if is_booked:
            messages.error(request, "This Transport is already booked on the selected date. Please choose another date.")
        else:
            TransportationBooking.objects.create(
                user=request.user,
                service=service,
                vehicle_type=vehicle_type,
                seats=seats,
                event_date=event_date,
                rent_car=rent_car,
                status="Pending"
            )

            ServiceAvailability.objects.create(
                service_type='Transportation',
                service_id=service.id,
                booked_date=event_date,
            )
            messages.success(request, "Transport booked successfully. Awaiting approval.")
        return redirect('user_trans_bookings')

    return render(request, 'user_book_transport.html', {'service': service})

@login_required
def user_trans_bookings(request):
    bookings = TransportationBooking.objects.filter(user=request.user)
    return render(request, 'user_transport_bookings.html', {'bookings': bookings})



## caterning ##


@login_required
def user_catering_list(request):
    services = CateringService.objects.filter(available=True)
    return render(request, 'user_catering_list.html', {'services': services})

@login_required
def user_book_catering(request, cater_id):
    service = get_object_or_404(CateringService, id=cater_id,available=True)
    
    if request.method == 'POST':
        event_date = request.POST.get('event_date')
        guests = request.POST.get('guests')
        customize_food=request.POST.get('customize_food')

        if not event_date or not guests or not customize_food:
            messages.error(request, "All fields are required!")
            return redirect('user_book_catering', cater_id=cater_id)

        event_date = date.fromisoformat(event_date)  # Convert string to date
        if event_date < date.today():
            messages.error(request, "Event date must be in the future!")
            return redirect('user_book_catering', cater_id=cater_id)
        
        is_booked = ServiceAvailability.objects.filter(
            service_type="Catering", 
            service_id=service.id, 
            booked_date=event_date
        ).exists()

        if is_booked:
            messages.error(request, "This catering service is already booked on the selected date. Please choose another date.")
        else:
            CateringBooking.objects.create(
                user=request.user,
                service=service,
                event_date=event_date,
                guests=guests,
                customize_food=customize_food,
                status="Pending"
            )

            ServiceAvailability.objects.create(
                service_type='Catering',
                service_id=service.id,
                booked_date=event_date,

            )
            messages.success(request, "catering service service booked successfully!")
        return redirect('user_catering_bookings')

    return render(request, 'user_book_catering.html', {'service': service})

@login_required
def user_catering_bookings(request):
    bookings = CateringBooking.objects.filter(user=request.user)
    return render(request, 'user_catering_bookings.html', {'bookings': bookings})



## Decoration ##


@login_required
def user_decoration_list(request):
    decore = DecorationsService.objects.filter(available=True)
    return render(request, 'user_decoration_list.html', {'decore': decore})


@login_required
def user_book_decore(request, decore_id):
    decore = get_object_or_404(DecorationsService, id=decore_id,available=True)
    
    if request.method == 'POST':
        event_date = request.POST.get('event_date')
        custom_service=request.POST.get('custom_service')

        if not event_date or not custom_service:
            messages.error(request, "All fields are required!")
            return redirect('user_book_decore', decore_id=decore_id)

        event_date = date.fromisoformat(event_date) 
        if event_date < date.today():
            messages.error(request, "Event date must be in the future!")
            return redirect('user_book_decore', decore_id=decore_id)
        
        is_booked = ServiceAvailability.objects.filter(
            service_type="Decorations", 
            service_id=decore.id, 
            booked_date=event_date
        ).exists()

        if is_booked:
            messages.error(request, "This Decore service is already booked on the selected date. Please choose another date.")
        else:
            DecorationsBooking.objects.create(
                user=request.user,
                service=decore,
                custom_service=custom_service,
                event_date=event_date,
                status="Pending"
            )

            ServiceAvailability.objects.create(
                service_type='Decorations',
                service_id=decore.id,
                booked_date=event_date,

            )
            messages.success(request, "Decore service service booked successfully!")
        return redirect('user_decoring_bookings')

    return render(request, 'user_book_decore.html', {'decore': decore})

@login_required
def user_decore_bookings(request):
    bookings = DecorationsBooking.objects.filter(user=request.user)
    return render(request, 'user_decore_bookings.html', {'bookings': bookings})


## Photo&Video graphy ##


@login_required
def user_photo_video_list(request):
    decores = PhotographyService.objects.filter(available=True)
    return render(request, 'user_photo_video_list.html', {'decores': decores})


@login_required
def user_book_photo_video(request, photo_id):
    photos = get_object_or_404(PhotographyService, id=photo_id,available=True)
    
    if request.method == 'POST':
        event_date = request.POST.get('event_date')
        custom_service=request.POST.get('custom_service')

        if not event_date or not custom_service:
            messages.error(request, "All fields are required!")
            return redirect('user_book_photo_video', photo_id=photo_id)

        event_date = date.fromisoformat(event_date) 
        if event_date < date.today():
            messages.error(request, "Event date must be in the future!")
            return redirect('user_book_photo_video', photo_id=photo_id)
        
        is_booked = ServiceAvailability.objects.filter(
            service_type="Photography", 
            service_id=photos.id, 
            booked_date=event_date
        ).exists()

        if is_booked:
            messages.error(request, "This Photo video service is already booked on the selected date. Please choose another date.")
        else:
            PhotographyBooking.objects.create(
                user=request.user,
                service=photos,
                custom_service=custom_service,
                event_date=event_date,
                status="Pending"
            )

            ServiceAvailability.objects.create(
                service_type='Photography',
                service_id=photos.id,
                booked_date=event_date,

            )
            messages.success(request, "photo service service booked successfully!")
        return redirect('user_photo_video_bookings')

    return render(request, 'user_book_photo_video.html', {'photos': photos})

@login_required
def user_photo_video_bookings(request):
    bookings = PhotographyBooking.objects.filter(user=request.user)
    return render(request, 'user_photo_video_bookings.html', {'bookings': bookings})



## Bride Groom Service ##

@login_required
def user_bride_groom_list(request):
    coustumes = BridalGroomService.objects.filter(available=True)
    return render(request, 'user_bride_groom_list.html', {'coustumes': coustumes})


@login_required
def user_bride_groom(request, bride_id):
    coustume = get_object_or_404(BridalGroomService, id=bride_id,available=True)
    
    if request.method == 'POST':
        event_date = request.POST.get('event_date')
        suggest_theme=request.POST.get('suggest_theme')

        if not event_date or not suggest_theme:
            messages.error(request, "All fields are required!")
            return redirect('user_bride_groom', bride_id=bride_id)

        event_date = date.fromisoformat(event_date) 
        if event_date < date.today():
            messages.error(request, "Event date must be in the future!")
            return redirect('user_bride_groom', bride_id=bride_id)
        
        is_booked = ServiceAvailability.objects.filter(
            service_type="BridalGroom", 
            service_id=coustume.id, 
            booked_date=event_date
        ).exists()

        if is_booked:
            messages.error(request, "This bride groom service is already booked on the selected date. Please choose another date.")
        else:
            BridalGroomServiceBooking.objects.create(
                user=request.user,
                service=coustume,
                suggest_theme=suggest_theme,
                event_date=event_date,
                status="Pending"
            )

            ServiceAvailability.objects.create(
                service_type='BridalGroom',
                service_id=coustume.id,
                booked_date=event_date,

            )
            messages.success(request, "bride groom service service booked successfully!")
        return redirect('user_bride_groom_bookings')

    return render(request, 'user_bride_groom.html', {'coustume': coustume})

@login_required
def user_bride_groom_bookings(request):
    bookings = BridalGroomServiceBooking.objects.filter(user=request.user)
    return render(request, 'user_bride_groom_bookings.html', {'bookings': bookings})
