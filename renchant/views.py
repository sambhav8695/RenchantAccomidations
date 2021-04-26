from django.shortcuts import render, reverse;from django.http import HttpResponseRedirect
from .models import Property, Gallery, Services, Testmonials, CarasoulData, City
from django.contrib import messages
from django.views.generic import ListView
from django.core.mail import EmailMessage
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from captcha.fields import ReCaptchaField
# Create your views here.


class Index(ListView):
    template_name = 'renchant/index.html'
    context_object_name = 'properties'
    paginate_by = 2



    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data()
        cities = City.objects.all()
        context["cities"] = cities
        city = self.request.GET.get('city')
        if city:
            context['city'] = city
        display = self.request.GET.get('display')
        if display:
            context['display'] = display
        sort_ = self.request.GET.get('sort')
        if sort_:
            context['sort'] = sort_
        return context

    def get_queryset(self):
        q_set = Property.objects.all()
        if self.request.GET.get('city'):
            q_set = q_set.filter(city__icontains=self.request.GET['city'])

        if self.request.GET.get('display'):
            display = self.request.GET['display']
            if display == 'new':
                q_set = q_set.filter(is_new=True)
            elif display == 'existing':
                q_set = q_set.filter(is_new=False)

        if self.request.GET.get('sort'):
            if self.request.GET['sort'] == 'ascending':
                q_set = q_set.order_by('price')
            else:
                q_set = q_set.order_by('-price')
        else:
            q_set = q_set.order_by('-price')
        return q_set


class AddProperty(LoginRequiredMixin, View):
    login_url = '/accounts/login'
    def get(self , request):
        cities = City.objects.all()
        return render(request, 'renchant/authenticated/add_property.html', {'cities':cities})

    def post(self, request):
        profile = request.user.profile
        name = request.POST['name']
        location = request.POST['location']
        city = request.POST['city']
        price = str(request.POST['price'])
        beds = int(request.POST['beds'])
        baths = int(request.POST['baths'])
        sq_feet = float(request.POST['sq_feet'])
        info = request.POST['info']
        google_map_link = request.POST["google_map_link"]

        is_new = True

        images = request.FILES.getlist('images')
        image = images[0]

        property = Property(
            profile=profile,
            name=name,
            location=location,
            city=city,
            price=price,
            beds=beds,
            baths=baths,
            sq_feet=sq_feet,
            google_map_link=google_map_link,
            info=info,
            image=image,
            is_new=is_new
        )

        property.save()

        for i in images:
            image = Gallery(
                property=property,
                image=i,
            )

            image.save()

        messages.success(request, "Successfully added Property")

        message = f'''
        NAME: {profile.user.username}
        PROPERTY: {name}
        CITY: {city}
        LOCATION: {location}
        MAP : {google_map_link}
        PRICE: {price}
        BEDS: {beds}
        BATHS: {baths}
        SQ FEET: {sq_feet}
        '''

        subject = "NEW PROPERTY ADDED TO RENCHANT (VERIFY IT)"
        #'sambhav8695@gmail.com'
        email_obj = EmailMessage(subject, message, settings.EMAIL_HOST_USER_NAME, settings.EMAIL_RECEIVERS)
        #images = request.FILES.getlist('images')
        # i = 0
        # for document in request.FILES.getlist('images'):
        #     email_obj.attach(f"{i}", document.read(), document.content_type)
        #     i += 1
        for document in property.gallery_set.all():
            email_obj.attach_file(document.image.path)

        email_obj.send()
        return HttpResponseRedirect(reverse('add_property'))

def add_property_for_user(request):
    profile = request.user.profile
    pk = request.POST.get('pk')
    property = Property.objects.get(pk=int(pk))
    property_ = PropertiesOfUser(profile=profile, property=property)
    property_.save()
    return HttpResponseRedirect(reverse('details', args=(int(pk),)))


class PropertyListOwner(LoginRequiredMixin, ListView):
    login_url = '/accounts/login'
    template_name = 'renchant/authenticated/index.html'
    context_object_name = 'properties'
    paginate_by = 4

    def get_queryset(self):
        profile = self.request.user.profile
        q_set = profile.property_set.all()
        return q_set


class DetailProperty(LoginRequiredMixin, View):

    def validate_user_property(self, profile, pk):
        property = Property.objects.get(pk=pk)
        if property.profile == profile:
            gallery = property.gallery_set.all()
            return True, property, gallery
        else:
            return False, None, None

    def get(self, request, pk):
        profile = request.user.profile
        _ , property, gallery =  self.validate_user_property(profile, pk)
        if _:
            return render(request, 'renchant/authenticated/details.html', {'property':property,'images':gallery})
        else:
            messages.error(request, "cannot access others property")
            return HttpResponseRedirect(reverse('logout'))

    def post(self, request, pk):
        profile = request.user.profile
        _, property, gallery = self.validate_user_property(profile, pk)
        if _:
            name = request.POST['name']
            price = str(request.POST['price'])
            baths = int(request.POST['baths'])
            beds = int(request.POST['beds'])
            sq_feet = float(request.POST['sq_feet'])

            property.name = name
            property.price = price
            property.baths = baths
            property.beds = beds
            property.sq_feet = sq_feet
            property.save()
            return HttpResponseRedirect(reverse('auth_property_details', args=(property.pk,)))
        else:
            messages.error(request, "cannot access others property")
            return HttpResponseRedirect(reverse('logout'))


class Payment(View):
    def get(self, request):
        return render(request, 'renchant/payment.html')

def about(request):
    services = Services.objects.all()
    testmonials = Testmonials.objects.all()
    carasoul_data = CarasoulData.objects.all()
    return render(request, 'renchant/about.html', {'services':services, 'testmonials':testmonials, 'carasoul_data':carasoul_data})

def details(request, pk):
    property = Property.objects.get(pk=pk)
    images = property.gallery_set.all()

    return render(request, 'renchant/details.html', {'property':property, 'images':images})

def schedule_property(request):
    pk = request.POST["pk"]
    property = Property.objects.get(pk=pk)
    profile = request.user.profile

    subject = f"{profile.user.username} has scheduled for {property.name}"

    message = f'''
    USER DETAILS
    Name: {profile.user.username}
    EMAIL : {profile.user.email}
    PHONE NUMBER : {profile.phonenumber}


    PROPERTY DETAILS
    NAME : {property.name}
    CITY : {property.city}
    LOCATION : {property.location}
    GOOGLE MAP : {property.google_map_link}
    PRICE : {property.price}
    BEDS : {property.beds}
    BATHS : {property.baths}
    SQ FEET : {property.sq_feet}
    '''

    email_obj = EmailMessage(subject, message, settings.EMAIL_HOST_USER_NAME, settings.EMAIL_RECEIVERS)
    email_obj.send()
    messages.success(request, " Our executive will get back to you soon to schedule your visit")
    return HttpResponseRedirect(reverse('details', args=(int(pk),)))


class Contact(View):
    def get(self, request):
        captcha = ReCaptchaField(attrs={'theme' : 'clean'})
        return render(request, 'renchant/contact.html')

    def post(self, request):
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        subject = request.POST['subject']
        message = request.POST['message']
        message = f'''
        NAME: {full_name}
        MOBILE: {phone_number}
        EMAIL: {email}
        MESSAGE: {message}
        '''

        #sambhav8695@gmail.com
        email_obj = EmailMessage(subject, message, settings.EMAIL_HOST_USER_NAME, settings.EMAIL_RECEIVERS)
        email_obj.send()
        messages.success(request, "Details send to us we will contact you within 3 days")
        return HttpResponseRedirect(reverse('contact'))
