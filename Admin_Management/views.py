from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


from .models import CustomUser
from .forms import LoginForm, RegisterForm
from .user_access import user_pages
from Content_Management.models import Activities


# To show the initial page
class Login(View):

    template = "Admin_Management/login.html"
    context = locals()

    def get(self, request):
        '''
        Get request to access the login page
        :param request:
        :return: template
        '''
        # initially logout with any request
        logout(request)

        login_form = LoginForm()
        register_form = RegisterForm()

        self.context['login_form'] = login_form
        self.context['register_form'] = register_form

        return render(request, self.template, self.context)


    def post(self, request):
        '''
        Post request when login form or registration submits
        :param request:
        :return: httpredirect path
        '''
        logout(request)

        self.login_form = LoginForm(request.POST)

        if self.login_form.is_valid():
            login_credentials = self.login_form.cleaned_data
            admin_name = login_credentials['admin_name']
            password = login_credentials['password']

            if '@' in admin_name:
                try:
                    user = User.objects.get(email=admin_name)
                    admin_name = user.username

                except:
                    pass

            user = authenticate(username=admin_name, password=password)

            if user:
                if user.is_active:

                    login(request, user)
                    messages.success(request, "Login Successfull")
                    return redirect('Dashboard')

        messages.error(request, "Invalid Username or Password")
        return redirect('/?f=login')


# To show the registers vistitor page
class Register(View):


    template = 'Admin_Management/visitors.html'
    context = locals()

    def get(self, request):
        if request.user.is_authenticated():

            user_properties = user_pages(request.user)
            self.context["pages"] = user_properties.getUserViews()["pages"]
            return render(request, self.template, self.context)

        else:
            return redirect("Login")


    def post(self, request):
        '''
        :param request:
        :return: navigete to visitor page
        '''
        self.register_form = RegisterForm(request.POST)

        if self.register_form.is_valid():
            self.register = self.register_form.cleaned_data

            username    = self.register["admin_name"]
            email       = self.register["email"]
            consultancy = self.register["consultancy_name"]
            phone_no    = self.register["phone_no"]
            website     = self.register["website"]
            new_password = self.register["new_password"]
            rpt_password = self.register["rpt_password"]

            if new_password == rpt_password:
                try:
                    custom_user = CustomUser.objects.create_user(username=username,
                                                          email=email,
                                                          password=new_password,
                                                          consultancy_name = consultancy,
                                                          phone_no = phone_no,
                                                          website = website,
                                                          is_staff=False,
                                                          )

                    custom_user.save()
                    user = authenticate(username=username, password=new_password)

                    # Creating activities
                    activities = Activities(consultancy=custom_user,
                                            activity="New Consultancy Registered Waiting for Approval",
                                            )

                    activities.save()

                    login(request, user)

                    user_properties = user_pages(user)
                    self.context["pages"] = user_properties.getUserViews()["pages"]
                    return render(request, self.template, self.context)
                except:
                    messages.warning(request, "The Admin name is Taken!!")




        return redirect("/?f=register")