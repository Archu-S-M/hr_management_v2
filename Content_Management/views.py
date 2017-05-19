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
from PyPDF2 import PdfFileReader, PdfFileWriter
from datetime import datetime
from functools import reduce

# custom imports
from Admin_Management.user_access import user_pages
from Admin_Management.models import CustomUser
from Content_Management.models import Candidate
from Content_Management.models import Skillset
from Content_Management.models import Activities
from Content_Management.models import Positions
from Content_Management.models import MasterSkills
from Content_Management.models import Questions

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
                position_id = (activity.position.id if activity.position else False)
                question_id = (activity.question.id if activity.question else False)
                response['data'].append(
                    {"activities": {
                        "activity": activity.activity,
                        "consultancy_id": consultancy_id,
                        "candidate_id": candidate_id,
                        "requirements_id": position_id,
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

        # print(request.POST)

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

    video_extensions = ["mp4", "mpeg4"]
    resume_extensions = ["pdf", "doc", "docx"]

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
            "method": "Create/Update"
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

        elif post_method == "Delete":

            candidate_id = request.POST["email"]
            # only super user can delete a candidate
            if not request.user.is_superuser:
                response["errors"].append("You are not authorized to do this operation")
                return HttpResponse(json.dumps(response), content_type="application/json")
            else:
                try:
                    candidate = Candidate.objects.get(candidate_email=candidate_id).delete()
                    response["message"] = {"success" : "Successfully Deleted"}
                    response["method"] = "Delete"
                except:
                    response["errors"].append("Unable to delete this candidate")

                return HttpResponse(json.dumps(response), content_type="application/json")


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


    def post(self, request):

        response = {
            "data" : [],
            "message": "",
            "msg_type": "danger"
        }


        # valid extensions
        ext = ["pdf"]

        # print(request.POST)

        method = request.POST["post_for"]

        # to get the position filter values
        # =======================================================================
        if method == "get_position_filter":

            positions = Positions.objects.all().order_by("position_name")

            for position in positions:

                response["data"].append({
                    "label": position.position_name,
                    "value": position.id
                })


        # to get the questions according to the position
        # =======================================================================

        if method == "get_questions":

            position_id = request.POST["position_id"]
            question_name = "#"
            question_id = 0

            if int(position_id) != 0:
                if Questions.objects.filter(position_id=int(position_id)).exists():
                    questions = Questions.objects.get(position_id=int(position_id))

                    if questions:
                        question_name = questions.question
                        question_id = questions.id



            response["data"] = {
                "question_url": "/media/%s" % question_name,
                "question_id": question_id
            }

            print(response)
        # to upload the questionnaire
        # =======================================================================
        if method == "upload_questionnaire":

            question_id = request.POST["question_id"]
            position_id = request.POST["position_id"]

            new_question_name = "#"

            if request.FILES:

                question_file = request.FILES["questions"]
                question_file_name = question_file.name
                # print(question_file_name)

                if question_file_name and question_file_name != "#":
                    # checking the extensions
                    extension = question_file_name.split(".")[-1]
                    if extension not in ext:
                        response["message"] = "Question is not in the recommended format"
                        response["msg_type"] = "danger"
                        return HttpResponse(json.dumps(response), content_type="application/json")
                    else:

                        if int(question_id) != 0 or int(position_id) != 0:
                            # for valid question file
                            new_question_name = "Question-%s.%s" % (str(position_id), extension)

                            fs = FileSystemStorage()
                            if question_file_name and question_file_name != "#":
                                if os.path.isfile(os.path.join(settings.MEDIA_ROOT, new_question_name)):
                                    os.remove(os.path.join(settings.MEDIA_ROOT, new_question_name))

                                q = fs.save(new_question_name, question_file)


                            # to update question
                            if int(question_id) != 0:
                                question = Questions.objects.get(pk=int(question_id))
                                question.question = new_question_name
                                question.save()

                            # to add question
                            elif int(question_id) == 0 and int(position_id) != 0:
                                if not Questions.objects.filter(position_id=int(position_id)).exists():
                                    question = Questions(question=new_question_name,
                                                         position_id=int(position_id))
                                    question.save()
                                else:
                                    question = Questions.objects.get(position_id=int(position_id))
                                    question.question = new_question_name
                                    question.save()


                            response["message"] = "Successfully added questions"
                            response["msg_type"] = "success"


                        else:
                            response["message"] = "Select a position to add or update"
                            response["msg_type"] = "danger"


                else:
                    response["message"] = "No changes detected"
                    response["msg_type"] = "info"

            else:
                response["message"] = "No changes detected"
                response["msg_type"] = "info"

            response["data"] = {
                "question_url": "/media/%s" % new_question_name
            }

        return HttpResponse(json.dumps(response), content_type="application/json")

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
        :return response:
        '''

        response = {
            "data": [],
            "message": False,
            "msg_type": ""

        }

        # print(request.POST)
        method = request.POST["post_for"]


        # Get the position details
        if method == "get_position":
            positions = Positions.objects.all().order_by("-updated_at")

            for position in positions:
                response["data"].append({
                    "position": {
                        "name": position.position_name,
                        "id": position.id
                    },
                    "description": position.position_desc,
                    "state": position.position_state,
                    "date": position.updated_at.strftime("%d/%m/%Y %I:%M %p"),
                    "operations": True

                })

            return HttpResponse(json.dumps(response), content_type="application/json")

        # ----------------------------------------------------------------------------
        # get the position filter
        if method == "get_position_filter":

            positions = Positions.objects.all()
            for position in positions:
                response["data"].append(
                    {"label": position.position_name, "value": position.id}
                )

            return HttpResponse(json.dumps(response), content_type="application/json")

        # -------------------------------------------
        # get the skills
        if method == "get_skills":

            position = request.POST["position"]


            if int(position) != 0:
                skills = MasterSkills.objects.filter(position_id=int(position)).order_by("-updated_at")
            else:
                skills = MasterSkills.objects.all().order_by("-updated_at")



            for skill in skills:
                response["data"].append({
                    "skill": {
                        "name": skill.skill,
                        "id": skill.id
                    },
                    "description": skill.description,
                    "date": skill.updated_at.strftime("%d/%m/%Y %I:%M %p"),
                    "operations": True

                })

            return HttpResponse(json.dumps(response), content_type="application/json")

        # -------------------------------------------
        # Add skills
        if method == "add_skill":
            position = request.POST["position_id"]
            skill_name = request.POST["skill_name"]
            skill_desc = request.POST["skill_description"]

            exists = MasterSkills.objects.filter(skill__iexact=skill_name, position_id=int(position)).exists()

            if exists:
                response["message"] = "Skill already available for this position; Please check the table"
                response["msg_type"] = "warning"

            else:
                if int(position) != 0:
                    skill = MasterSkills(position_id=position,
                                         skill=skill_name,
                                         description=skill_desc,
                                         )
                    skill.save()
                    response["message"] = "Successfully Added new skill for the position"
                    response["msg_type"] = "success"
                else:
                    response["message"] = "No Positions to add Skills add a position first"
                    response["msg_type"] = "warning"



            return HttpResponse(json.dumps(response), content_type="application/json")


        # -------------------------------------------
        # Add positions
        if method == "add_position":
            position_name = request.POST["position_name"]
            position_desc = request.POST["description"]

            exists = Positions.objects.filter(position_name__iexact=position_name).exists()

            if exists:
                response["message"] = "Position already exists. Please add a new one"
            else:
                position = Positions(position_name=position_name,
                                     position_desc=position_desc,
                                    )
                position.save()

                activity = Activities(position=position,
                                      activity="Created New Position"
                                      )
                activity.save()

                response["message"] = "Successfully added new position"
                response["msg_type"] = "success"

            return HttpResponse(json.dumps(response), content_type="application/json")

        # -------------------------------------------
        # Update the skill details
        if method == "update_skill":

            skill_name = request.POST["skill"]
            skill_id = request.POST["id"]
            description = request.POST["skill_description"]
            # position = request.POST["position_id"]


            skill = MasterSkills.objects.get(pk=int(skill_id))
            skill.skill = skill_name
            skill.description = description
            # skill.position_id = int(position)

            skill.save()

            response["message"] = "Successfully Updated"
            response["msg_type"] = "success"

            return HttpResponse(json.dumps(response), content_type="application/json")


        # -------------------------------------------
        # Update the posiion details
        if method == "update_position":

            position_name = request.POST["position"]
            position_id = request.POST["id"]
            state = "Open" if "position_state" in request.POST else "Closed"
            # print(state)
            description = request.POST["description"]

            position = Positions.objects.get(pk=int(position_id))
            position.position_name = position_name
            position.position_desc = description
            position.position_state = state

            position.save()

            response["message"] = "Successfully Updated"
            response["msg_type"] = "success"

            activity = Activities(position=position,
                                  activity="Position Updated"
                                  )
            activity.save()

            return HttpResponse(json.dumps(response), content_type="application/json")

        # ------------------------------------------
        # delete the skills
        if method == "delete_skill":
            skill_id = request.POST["skill_id"]

            try:
                MasterSkills.objects.filter(pk=int(skill_id)).delete()
                response["message"] = "Successfully deleted skill"
                response["msg_type"] = "success"
            except:
                response["message"] = "Skill does not exists"
                response["msg_type"] = "danger"

            return HttpResponse(json.dumps(response), content_type="application/json")


        # ------------------------------------------
        # delete the positions
        if method == "delete_position":
            position_id = request.POST["position_id"]

            try:
                Positions.objects.filter(pk=int(position_id)).delete()
                response["message"] = "Successfully deleted position"
                response["msg_type"] = "success"
            except:
                response["message"] = "position does not exists"
                response["msg_type"] = "danger"

            return HttpResponse(json.dumps(response), content_type="application/json")



        return HttpResponse(json.dumps({"message" : "Invalid Post Request",
                                        "msg_type" : "danger"}),
                            content_type="application/json")