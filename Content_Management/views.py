# Django libraries
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import resolve
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Q



# Pyhon special libraries
import json, os
from datetime import datetime
from functools import reduce

# custom imports
from Admin_Management.user_access import user_pages
from Admin_Management.models import CustomUser
from Content_Management.models import Candidate
from Content_Management.models import Skillset
from Content_Management.models import Activities
from Content_Management.models import Positions

from Content_Management.view_formatter import ExtendCandidateProfile

# for test
from urllib import request as urlRequest


#==================================================================


# View for dashboard
class Dashboard(LoginRequiredMixin, View):

    login_url = "/"
    redirect_field_name = "Login"

    template = "Content_Management/dashboard.html"
    context = locals()

    def get(self, request):

        user_properties = user_pages(request.user)
        user_property_values = user_properties.getUserViews()

        self.context["pages"], self.context["access"] = (user_property_values["pages"],
                                                         user_property_values["access"])

        current_url = resolve(request.path_info).url_name

        if current_url in self.context["access"] or self.context["access"] == ["All"]:
            return render(request, self.template, self.context)

        elif "Register" in self.context["access"]:
            return redirect("Register")

        else:
            return redirect("Login")


    def post(self, request):

        # initialize the response object
        response = {
        }

        print(request.POST)

        method = request.POST["submit"]

        if method == "get_activities":

            response = {
                "status": "success",
                "data": []
            }

            if request.user.is_superuser:
                activities = Activities.objects.all().order_by("-created_at")

            else:
                activities = Activities.objects.filter(
                    Q(consultancy=request.user) | Q(consultancy=None)
                ).order_by("-created_at")

            for activity in activities:
                created_at = activity.created_at.strftime("%d/%m/%Y %I:%M %p")
                consultancy_id = (activity.consultancy.id if activity.consultancy else False)
                candidate_id = (activity.candidate.id if activity.candidate else False)
                requirement_id = (activity.requirement.id if activity.requirement else False)
                question_id = (activity.question.id if activity.question else False)
                response['data'].append(
                    {"activities": {
                        "activity": activity.activity,
                        "consultancy_id": consultancy_id,
                        "candidate_id": candidate_id,
                        "requirements_id": requirement_id,
                        "question_id": question_id
                    },
                        "date": created_at}
                )

        return HttpResponse(json.dumps(response), content_type="application/json")



# ===========================================================================
# View for Mange Consultancy
class ManageConsultancy(LoginRequiredMixin, View):

    login_url = "/"
    redirect_field_name = "Login"

    template = "Content_Management/manage_consultancy.html"
    context = locals()

    def get(self, request):

        user_properties = user_pages(request.user)
        user_property_values = user_properties.getUserViews()

        self.context["pages"], self.context["access"] = (user_property_values["pages"],
                                                         user_property_values["access"])

        current_url = resolve(request.path_info).url_name

        if current_url in self.context["access"] or self.context["access"] == ["All"]:
            return render(request, self.template, self.context)

        elif "Register" in self.context["access"]:
            return redirect("Register")

        else:
            return redirect("Login")

    # ===================================================================

    def post(self, request):


        # initialize the response object
        response = {
        }

        print(request.POST)

        method = request.POST["submit"]

        if method == "get_consultancy":
            response = {
                "status": "success",
                "data": []
            }


            # to get the data from the consultancy
            consultancy = CustomUser.objects.filter(~Q(id=request.user.id)).order_by(
                    "is_staff", "-date_joined").distinct()

            # print(consultancy.query)
            for users in consultancy:
                consultancy_name = users.consultancy_name
                website = users.website
                phone_no = users.phone_no
                registered_time = users.date_joined.strftime("%d/%m/%Y %I:%M:%S %p")
                status = users.is_staff

                response['data'].append({
                    "consultancy": {"name":consultancy_name,"id":users.id},
                    "website": website,
                    "phone_no": phone_no,
                    "datetime": registered_time,
                    "status": status
                })


            return HttpResponse(json.dumps(response),
                                content_type="application/json")

        # Update the consultancy from newbie to valid consultancy
        elif method == "update_consultancy":

            response = {
                "status": "no data",
                "data": []
            }

            data = request.POST

            if data:

                consultancy_id = data["filter[id]"]
                try:
                    consultancy = CustomUser.objects.get(pk=int(consultancy_id))
                    activity = ""
                    if consultancy.is_staff:
                        consultancy.is_staff = False
                        activity = "Consultancy Blocked"
                    else:
                        consultancy.is_staff = True
                        activity = "Consultancy Approved"
                    consultancy.save()

                    activities = Activities(consultancy=consultancy,
                                            activity=activity,
                                            )

                    activities.save()
                    response["status"] = "success"
                except:
                    response["status"] = "Invalid consultancy"

            return HttpResponse(json.dumps(response), content_type="application/json")



# ===========================================================================
# View for candidate profile
class CandidateProfile(LoginRequiredMixin, View):

    login_url = "/"
    redirect_field_name = "Login"


    post_dt_format1 = "%d/%m/%Y %I:%M %p"
    post_dt_format2 = "%d/%m/%Y %I:%M %P"

    video_extensions = ["mp4","mpeg4"]
    resume_extensions = ["pdf","doc","docx"]

    template = "Content_Management/candidate_profile.html"
    context = locals()


    def get(self, request):

        '''
        to get the get request and show the templates for profile page
        :param request:
        :return: rendered page
        '''

        self.context["candidate_data"] = {"name": "name"}
        user_properties = user_pages(request.user)
        user_property_values = user_properties.getUserViews()
        self.context["pages"], self.context["access"] = (user_property_values["pages"],
                                                         user_property_values["access"])
        current_url = resolve(request.path_info).url_name
        if current_url in self.context["access"] or self.context["access"] == ["All"]:
            return render(request, self.template, self.context)

        elif "Register" in self.context["access"]:
            return redirect("Register")

        else:
            return redirect("Login")



    # Uploading or updating candidate profiles
    def post(self, request):

        # response set for the post request
        # -------------------------------------
        response = {
            "errors": [],
            "info": [],
            "message": [],
            "video_url": "#",
            "resume_url": "#",
        }

        # print(request.POST)

        # get the data from the request
        # ==================================
        data = request.POST
        # ==================================

        post_method = data["submit"]

        # condition to check whether is the new candidate or updating the existing one!
        # ==================================================
        if post_method == "Create/Update":
            response = ExtendCandidateProfile().validate_create_or_update(request, data)
            return HttpResponse(json.dumps(response), content_type="application/json")

        elif post_method == "Activate/Deactivate":

            '''Yet to code'''

        elif post_method == "get_filtered_data":
            response = ExtendCandidateProfile().get_filtered_data(request, data)
            return HttpResponse(json.dumps(response), content_type="application/json")

        elif post_method == "get_full_details":
            response = ExtendCandidateProfile().get_full_details(request, data)
            return HttpResponse(json.dumps(response), content_type="application/json")

        elif post_method == "fill_filters":
            response = ExtendCandidateProfile().fill_filters(request, data)
            return HttpResponse(json.dumps(response), content_type="application/json")

        return redirect("CandidateProfile")




# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# View for questionnaire
class Questionnaire(LoginRequiredMixin, View):

    login_url = "/"
    redirect_field_name = "Login"

    template = "Content_Management/questionnaire.html"
    context = locals()

    def get(self, request):

        user_properties = user_pages(request.user)
        user_property_values = user_properties.getUserViews()

        self.context["pages"], self.context["access"] = (user_property_values["pages"],
                                                         user_property_values["access"])

        current_url = resolve(request.path_info).url_name

        if current_url in self.context["access"] or self.context["access"] == ["All"]:
            return render(request, self.template, self.context)

        elif "Register" in self.context["access"]:
            return redirect("Register")

        else:
            return redirect("Login")

# ===========================================================================
# View for Candidates requirements
class Requirements(LoginRequiredMixin, View):

    login_url = "/"
    redirect_field_name = "Login"

    template = "Content_Management/requirements.html"
    context = locals()

    def get(self, request):

        user_properties = user_pages(request.user)
        user_property_values = user_properties.getUserViews()

        self.context["pages"], self.context["access"] = (user_property_values["pages"],
                                                         user_property_values["access"])

        current_url = resolve(request.path_info).url_name

        if current_url in self.context["access"] or self.context["access"] == ["All"]:
            return render(request, self.template, self.context)

        elif "Register" in self.context["access"]:
            return redirect("Register")

        else:
            return redirect("Login")

    # ================================================================================
    def post(self, request):

        '''
        Post values for the requirements
        :param request:
        :return:
        '''