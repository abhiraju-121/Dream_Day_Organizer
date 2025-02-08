from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import ServiceProvider
from user.models import User,Event,BookEvent,Venue,VenueBooking,TransportationBooking,TransportationService,CateringService,CateringBooking,DecorationsBooking,DecorationsService,PhotographyBooking,PhotographyService,BridalGroomServiceBooking,BridalGroomService
from django.contrib.auth import authenticate,login,logout

# Create your views here.


def servicer_home(request):
    return render(request,'servicer_home.html')

def servicer_register(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        company_name=request.POST.get('company_name')
        service_type=request.POST.get('service_type')

        if User.objects.filter(username=username):
            messages.error(request,"Username already exists !!")
            return redirect('servicer_register')
        if confirm_password!=password:
            messages.error(request,"Enter passowrd properly !!")
            return redirect('servicer_register')


        user=User.objects.create_user(username=username,password=password,is_service_provider=True)

        service_provider=ServiceProvider.objects.create(user=user,company_name=company_name,service_type=service_type)
        service_provider.save()
        return redirect('servicer_login')
    
    return render(request, 'servicer_register.html')


def servicer_login(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('servicer_home')
        else:
            messages.error(request,'Invalid Username or Password !!')
            return redirect('servicer_login')
    return render(request,'servicer_login.html')

def servicer_logout(request):
    logout(request)
    return redirect('servicer_login')   
# @login_required
# def servicer_dashboard(request):
#     service_provider = get_object_or_404(ServiceProvider, user=request.user)
#     return render(request, 'servicer_dashboard.html', {'service_provider': service_provider})

@login_required
def service_provider_dashboard(request):
    service_provider = get_object_or_404(ServiceProvider,user=request.user)

    if service_provider.service_type == 'photo_videography':
        return render(request, 'dashboard_photo_videography.html', {'service_provider': service_provider})
    elif service_provider.service_type == 'event_planners':
        return render(request, 'dashboard_event_planners.html', {'service_provider': service_provider})
    elif service_provider.service_type == 'catering':
        return render(request, 'dashboard_catering.html', {'service_provider': service_provider})
    elif service_provider.service_type == 'bride_groom_service':
        return render(request, 'dashboard_bride_groom.html', {'service_provider': service_provider})
    elif service_provider.service_type == 'decoration':
        return render(request, 'dashboard_decoration.html', {'service_provider': service_provider})
    elif service_provider.service_type == 'transportation':
        return render(request, 'dashboard_transportation.html', {'service_provider': service_provider})
    elif service_provider.service_type == 'venue_planners':
        return render(request,'dashboard_venue_planners.html',{'service_provider':service_provider})
    else:
        return redirect('home') 
    

## event ##


@login_required
def service_provider_event_list(request):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    events = Event.objects.filter(service_provider=service_provider)
    return render(request, 'provider_event_list.html', {'events': events})

@login_required
def add_event(request):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        location = request.POST.get("location")
        image = request.FILES.get("image")

        Event.objects.create(
            service_provider=service_provider,
            name=name,
            description=description,
            location=location,
            image=image
        )

        messages.success(request, "Event added successfully.")
        return redirect('service_provider_event_list')

    return render(request, 'provider_add_event.html')

@login_required
def edit_event(request, event_id):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    event = get_object_or_404(Event, id=event_id, service_provider=service_provider)

    if request.method == "POST":
        event.name = request.POST.get("name")
        event.description = request.POST.get("description")
        event.location = request.POST.get("location")

        if "image" in request.FILES:
            event.image = request.FILES.get("image")

        event.save()
        messages.success(request, "Event updated successfully.")
        return redirect('service_provider_event_list')

    return render(request, 'provider_edit_event.html', {'event': event})

@login_required
def delete_event(request, event_id):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    event = get_object_or_404(Event, id=event_id, service_provider=service_provider)
    event.delete()
    messages.success(request, "Event deleted successfully.")
    return redirect('service_provider_event_list')

@login_required
def manage_event_bookings(request):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    bookings = BookEvent.objects.filter(event__service_provider=service_provider)

    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        action = request.POST.get("action")
        booking = get_object_or_404(BookEvent, id=booking_id)

        if action == "approve":
            booking.status = "confirmed"
            booking.save()
            messages.success(request, f"Booking for {booking.user.username} approved.")
        elif action == "reject":
            booking.status = "cancelled"
            booking.save()
            messages.success(request, f"Booking for {booking.user.username} rejected.")
        return redirect('service_provider_manage_bookings')

    return render(request, 'provider_manage_event_booking.html', {'bookings': bookings})


##Venu##

@login_required
def provider_venue_list(request):
    service_provider = ServiceProvider.objects.get(user=request.user)
    venues = Venue.objects.filter(provider=service_provider)
    return render(request, 'venue_list.html', {'venues': venues})

@login_required
def add_venue(request):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)

    if request.method == "POST":
        name = request.POST.get('name')
        image = request.FILES.get('image')
        location = request.POST.get('location')
        capacity = request.POST.get('capacity')
        description = request.POST.get('description')
        available = request.POST.get('available', False) == 'on'

        Venue.objects.create(
            provider=service_provider,
            name=name,
            image=image,
            location=location,
            capacity=capacity,
            description=description,
            available=available
        )
        messages.success(request, "Venue added successfully!")
        return redirect('venue_list')

    return render(request, 'add_venue.html')

@login_required
def edit_venue(request, venue_id):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    venue = get_object_or_404(Venue, id=venue_id, provider=service_provider)

    if request.method == "POST":
        venue.name = request.POST['name']
        if 'image' in request.FILES:
            venue.image = request.FILES.get('image')
        venue.location = request.POST.get('location')
        venue.capacity = request.POST.get('capacity')
        venue.description = request.POST.get('description')
        venue.available = request.POST.get('available', False) == 'on'
        venue.save()

        messages.success(request, "Venue updated successfully!")
        return redirect('venue_list')

    return render(request, 'edit_venue.html', {'venue': venue})

@login_required
def delete_venue(request, venue_id):
    """ Delete a venue """
    venue = get_object_or_404(Venue, id=venue_id, provider=request.user)
    venue.delete()
    messages.success(request, "Venue deleted successfully!")
    return redirect('venue_list')



@login_required
def provider_bookings(request):
    service_provider=get_object_or_404(ServiceProvider,user=request.user)
    bookings = VenueBooking.objects.filter(venue__provider=service_provider)
    return render(request, 'provider_booking_venue.html', {'bookings': bookings})

@login_required
def approve_booking(request, booking_id):
    service_provider=get_object_or_404(ServiceProvider,user=request.user)
    booking = get_object_or_404(VenueBooking, id=booking_id, venue__provider=service_provider)
    booking.status = "Confirmed"
    booking.save()
    messages.success(request, "Booking approved successfully!")
    return redirect('provider_bookings')

@login_required
def reject_booking(request, booking_id):
    service_provider=get_object_or_404(ServiceProvider,user=request.user)
    booking = get_object_or_404(VenueBooking, id=booking_id, venue__provider=service_provider)
    booking.status = "Rejected"
    booking.save()
    messages.error(request, "Booking rejected.")
    return redirect('provider_bookings')


##Transportation##

@login_required
def service_provider_transports(request):
    service_provider=get_object_or_404(ServiceProvider,user=request.user)
    transports = TransportationService.objects.filter(provider=service_provider)
    return render(request, 'transport_provider_list.html', {'transports': transports})

@login_required
def add_transport(request):
    service_provider=get_object_or_404(ServiceProvider,user=request.user)
    if request.method == "POST":
        name = request.POST.get("name")
        image = request.FILES.get("image")
        desc=request.POST.get('desc')
        available = request.POST.get('available', False) == 'on'

        TransportationService.objects.create(
            provider=service_provider,
            name=name,
            image=image,
            desc=desc,
            available=available
        )

        messages.success(request, "Transport service added successfully.")
        return redirect('service_provider_transports')

    return render(request, 'provider_add_transport.html')


@login_required
def edit_transport(request, service_id):
    service_provider = get_object_or_404(ServiceProvider, user=request.user)
    transport = get_object_or_404(TransportationService, id=service_id, provider=service_provider)

    if request.method == "POST":
        transport.name = request.POST.get('name')
        transport.desc = request.POST.get('desc')
        transport.available = request.POST.get('available', False) == 'on'

        if 'image' in request.FILES:
            transport.image = request.FILES.get('image')

        transport.save()
        messages.success(request, "Transport updated successfully!")
        return redirect('service_provider_transports')

    return render(request, 'edit_transport.html', {'transport': transport})


@login_required
def provider_manage_trans_bookings(request):
    service_provider=get_object_or_404(ServiceProvider,user=request.user)
    bookings = TransportationBooking.objects.filter(service__provider=service_provider)
    return render(request, 'provider_manage_trans_booking.html', {'bookings': bookings})

@login_required
def update_booking_status(request, booking_id, status):
    service_provider=get_object_or_404(ServiceProvider,user=request.user)
    booking = get_object_or_404(TransportationBooking, id=booking_id, service__provider=service_provider)

    if status in ['Confirmed', 'Completed']:
        booking.status = status
        booking.save()
        messages.success(request, f"Booking status updated to {status}.")
    elif status == 'Rejected':
        booking.delete()
        messages.success(request, "Booking rejected and removed.")
    return redirect('provider_manage_trans_bookings')

## caterning ##


@login_required
def provider_catering_services_list(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    services = CateringService.objects.filter(provider=provider)
    return render(request, 'provider_catering_list.html', {'services': services})

@login_required
def add_catering_service(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)

    if request.method == 'POST':
        menu_name = request.POST.get('menu_name')
        desc = request.POST.get('desc')
        image = request.FILES.get('image')
        available = request.POST.get('available') == 'on'

        if not menu_name or not desc or not image:
            messages.error(request, "All fields are required!")
            return redirect('add_catering_service')

        CateringService.objects.create(
            provider=provider,
            menu_name=menu_name,
            desc=desc,
            images=image,
            available=available
        )
        messages.success(request, "Catering service added successfully!")
        return redirect('provider_catering_services_list')
    return render(request, 'provider_add_catering_service.html')

@login_required
def edit_catering_service(request, service_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(CateringService, id=service_id, provider=provider)

    if request.method == 'POST':
        service.menu_name = request.POST.get('menu_name')
        service.desc = request.POST.get('desc')
        if request.FILES.get('image'):
            service.images = request.FILES.get('image')
        service.available = request.POST.get('available') == 'on'
        service.save()

        messages.success(request, "Catering service updated successfully!")
        return redirect('provider_catering_services')

    return render(request, 'provider_edit_catering_service.html', {'service': service})

@login_required
def delete_catering_service(request, service_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(CateringService, id=service_id, provider=provider)
    service.delete()
    messages.success(request, "Catering service deleted successfully!")
    return redirect('provider_catering_services')

@login_required
def provider_catering_bookings(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    bookings = CateringBooking.objects.filter(service__provider=provider)
    return render(request, 'provider_catering_bookings.html', {'bookings': bookings})


@login_required
def manage_catering_booking_status(request, booking_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    booking = get_object_or_404(CateringBooking, id=booking_id, service__provider=provider)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Confirmed', 'Completed']:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking status updated to {new_status}!")
        else:
            messages.error(request, "Invalid status selection!")

    return redirect('provider_catering_bookings')




## Decoration ##


@login_required
def provider_decore_list(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    decores = DecorationsService.objects.filter(provider=provider)
    return render(request, 'provider_decore_list.html', {'decores': decores})


@login_required
def add_decore_service(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        image = request.FILES.get('image')
        theme_options=request.POST.get('theme_options')
        available = request.POST.get('available') == 'on'

        if not name or not desc or not image or not theme_options:
            messages.error(request, "All fields are required!")
            return redirect('add_decore_service')

        DecorationsService.objects.create(
            provider=provider,
            name=name,
            desc=desc,
            image=image,
            theme_options=theme_options,
            available=available
        )
        messages.success(request, "Decoration service added successfully!")
        return redirect('provider_decore_list')
    return render(request, 'provider_add_decore_list.html')


@login_required
def edit_deocre_service(request, service_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(DecorationsService, id=service_id, provider=provider)

    if request.method == 'POST':
        service.name = request.POST.get('name')
        service.desc = request.POST.get('desc')
        if request.FILES.get('image'):
            service.image = request.FILES.get('image')

        service.theme_options=request.POST.get('theme_options')
        service.available = request.POST.get('available') == 'on'
        service.save()

        messages.success(request, "Decoration service updated successfully!")
        return redirect('provider_decore_services')

    return render(request, 'provider_edit_decore_service.html', {'service': service})


@login_required
def delete_decore_service(request, service_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(DecorationsService, id=service_id, provider=provider)
    service.delete()
    messages.success(request, "Decoration service deleted successfully!")
    return redirect('provider_decore_services')

@login_required
def provider_decore_bookings(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    bookings = DecorationsBooking.objects.filter(service__provider=provider)
    return render(request, 'provider_decore_bookings.html', {'bookings': bookings})

@login_required
def manage_decore_booking_status(request, booking_id):
    provider=get_object_or_404(ServiceProvider,user=request.user)
    booking = get_object_or_404(DecorationsBooking, id=booking_id, service__provider=provider)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Confirmed', 'Completed']:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking status updated to {new_status}!")
        else:
            messages.error(request, "Invalid status selection!")

    return redirect('provider_catering_bookings')


## Photography & VIdeography ##

@login_required
def provider_photo_video_list(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    photos = PhotographyService.objects.filter(provider=provider)
    return render(request, 'provider_photo_video_list.html', {'photos': photos})


@login_required
def add_photo_video_service(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)

    if request.method == 'POST':
        package_name = request.POST.get('package_name')
        desc = request.POST.get('desc')
        image = request.FILES.get('image')
        includes_video=request.POST.get('includes_video',False) == "on"
        available = request.POST.get('available',False) == 'on'

        if not package_name or not desc or not image or not includes_video:
            messages.error(request, "All fields are required!")
            return redirect('add_photo_video_service')

        PhotographyService.objects.create(
            provider=provider,
            package_name=package_name,
            desc=desc,
            image=image,
            includes_video=includes_video,
            available=available
        )
        messages.success(request, "Photo_video service added successfully!")
        return redirect('provider_photo_video_list')
    return render(request, 'provider_add_photo_video_list.html')


@login_required
def edit_photo_video_service(request, service_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(PhotographyService, id=service_id, provider=provider)

    if request.method == 'POST':
        service.package_name = request.POST.get('package_name')
        service.desc = request.POST.get('desc')
        if request.FILES.get('image'):
            service.image = request.FILES.get('image')

        service.includes_video=request.POST.get('includes_video',False)=="on"
        service.available = request.POST.get('available',False) == 'on'
        service.save()

        messages.success(request, "Photo_video service updated successfully!")
        return redirect('provider_photo_video_list')

    return render(request, 'provider_edit_photo_video_service.html', {'service': service})


@login_required
def delete_photo_video_service(request, service_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(PhotographyService, id=service_id, provider=provider)
    service.delete()
    messages.success(request, "Photo video service deleted successfully!")
    return redirect('provider_photo_video_list')

@login_required
def provider_photo_video_bookings(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    bookings = PhotographyBooking.objects.filter(service__provider=provider)
    return render(request, 'provider_photo_video_bookings.html', {'bookings': bookings})

@login_required
def manage_photo_booking_status(request, booking_id):
    provider=get_object_or_404(ServiceProvider,user=request.user)
    booking = get_object_or_404(PhotographyBooking, id=booking_id, service__provider=provider)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Confirmed', 'Completed']:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking status updated to {new_status}!")
        else:
            messages.error(request, "Invalid status selection!")

    return redirect('provider_photo_video_bookings')


## bride and groom ##


@login_required
def provider_bride_groom_list(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    services = BridalGroomService.objects.filter(provider=provider)
    return render(request, 'provider_bride_groom_list.html', {'services': services})


@login_required
def add_bride_groom_service(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)

    if request.method == 'POST':
        package_name = request.POST.get('package_name')
        desc = request.POST.get('desc')
        image = request.FILES.get('image')
        package_details=request.POST.get('package_details')
        available = request.POST.get('available',False) == 'on'

        if not package_name or not desc or not image or not package_details:
            messages.error(request, "All fields are required!")
            return redirect('add_bride_groom_service')

        BridalGroomService.objects.create(
            provider=provider,
            package_name=package_name,
            desc=desc,
            image=image,
            package_details=package_details,
            available=available
        )
        messages.success(request, "bride_groom service added successfully!")
        return redirect('provider_bride_groom_list')
    return render(request, 'provider_add_bride_groom_list.html')


@login_required
def edit_bride_groom_service(request, service_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(BridalGroomService, id=service_id, provider=provider)

    if request.method == 'POST':
        service.package_name = request.POST.get('package_name')
        service.desc = request.POST.get('desc')
        if request.FILES.get('image'):
            service.image = request.FILES.get('image')

        service.package_details=request.POST.get('package_details')
        service.available = request.POST.get('available',False) == 'on'
        service.save()

        messages.success(request, "bride_groom service updated successfully!")
        return redirect('provider_bride_groom_services')

    return render(request, 'provider_edit_bride_groom_service.html', {'service': service})


@login_required
def delete_bride_groom_service(request, service_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(BridalGroomService, id=service_id, provider=provider)
    service.delete()
    messages.success(request, "bride groom service deleted successfully!")
    return redirect('provider_bride_grom_services')

@login_required
def provider_bride_groom_bookings(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    bookings = BridalGroomServiceBooking.objects.filter(service__provider=provider)
    return render(request, 'provider_bride_groom_bookings.html', {'bookings': bookings})

@login_required
def manage_bride_groom_status(request, booking_id):
    provider=get_object_or_404(ServiceProvider,user=request.user)
    booking = get_object_or_404(BridalGroomServiceBooking, id=booking_id, service__provider=provider)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Confirmed', 'Completed']:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking status updated to {new_status}!")
        else:
            messages.error(request, "Invalid status selection!")

    return redirect('provider_bride_groom_bookings')


