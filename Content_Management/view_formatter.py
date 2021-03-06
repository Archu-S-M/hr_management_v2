'''
The file to add extra formatting to the views
'''


from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Q



# Python special libraries
import os
from datetime import datetime
from functools import reduce

# custom imports
from Admin_Management.models import CustomUser
from Content_Management.models import Candidate
from Content_Management.models import Skillset
from Content_Management.models import Activities
from Content_Management.models import Positions


'''
Class for the extended view of consultancy
'''
class ExtendCandidateProfile:


    post_dt_format1 = "%d/%m/%Y %I:%M %p"
    post_dt_format2 = "%d/%m/%Y %I:%M %P"

    video_extensions = ["mp4", "mpeg4", "mp3", "wav", "ogg"]
    resume_extensions = ["pdf", "doc", "docx"]

    def __init__(self):
        '''
        Initialization of requests
        :param request:
        '''


    # --------------------------------------------------------------
    # [FUNCTION form validation and database update]
    # ==============================================================
    def validate_create_or_update(self, request, data):
        '''
        custom functions for form validation
        :param request:
        :param data:
        :return response:
        '''

        new_video_name = "#"
        new_resume_name = "#"

        # initializes the response object
        response = {
            "errors": [],
            "info": [],
            "message": {},
            "video_url": new_video_name,
            "resume_url": new_resume_name,
        }

        # Get all the form field values
        # ----------------------------
        save_type = True if data["save_type"] == "true" else False
        position_name = data["position"]
        name = data["name"]
        age = data["age"]
        experience = data["experience"]
        email = data["email"]
        no = data["contact_no"]
        skill_set = data.getlist("skills")
        interview_time = data["interview_time"]
        current_ctc = data["current_ctc"]
        expected_ctc = data["expected_ctc"]
        preferred_location = data["location"]
        notice_period = data["notice_period"]

        if request.user.is_superuser:
            status = data["status"]

        # initialize file values empty
        # --------------------------------
        interview_video = candidate_resume = resume_name = video_name = False

        # check the interview time in valid date format
        # -----------------------------------------------
        try:

            interview_time = datetime.strptime(interview_time,
                                               self.post_dt_format1)
        except:

            try:
                interview_time = datetime.strptime(interview_time,
                                                   self.post_dt_format2)
            except:

                response["errors"].append("Interview time in an invalid format")

        # get the uploaded files
        # -----------------------------
        try:
            if request.FILES:
                if "resume" in request.FILES:
                    candidate_resume = request.FILES['resume']
                else:
                    candidate_resume = None
                if "interview_video" in request.FILES:
                    interview_video = request.FILES['interview_video']
                else:
                    interview_video = None


                # change the file names before move into the media directory
                # The directory will contains the file names with email id as the postscript
                # ----------------------------------------------------------------------
                if interview_video:
                    video_name = interview_video.name

                    if video_name and video_name != '#':
                        extension = video_name.split(".")[-1]
                        new_video_name = ""

                        # check for valid extension [VIDEO/AUDIO]
                        # ---------------------------
                        if extension not in self.video_extensions:
                            response["errors"].append("Video/Audio Format not supported "
                                                    "(Current = %s Expected = .mp4/.mp3/.wav/.ogg)"
                                                    % extension)
                        else:
                            date_time = datetime.today().strftime("%d_%m_%Y_%H_%M_%S")
                            new_video_name = "Interview-%s_%s.%s" % (email, date_time, extension)


                        # check the video in a valid size (50 MB)
                        # ------------------------------------------
                        if interview_video.size > 52428800:
                            response["errors"].append("Video/Audio Size exceed (max-size 50MB)")

                    else:
                        response["info"].append("Video/Audio is not Uploaded")

                else:
                    response["info"].append("Video/Audio is not Uploaded")


                if candidate_resume:
                    # find the resume name and extension
                    # ----------------------------------
                    resume_name = candidate_resume.name

                    if resume_name and resume_name != "#":
                        extension = resume_name.split(".")[-1]
                        new_resume_name = ""

                        # check for  valid extension [RESUME]
                        # -------------------------------
                        if extension not in self.resume_extensions:
                            response["errors"].append("Resume format not supported (Expected .pdf/.doc/.docx)")
                        else:
                            date_time = datetime.today().strftime("%d_%m_%Y_%H_%M_%S")
                            new_resume_name = "Resume-%s_%s.%s" % (email, date_time, extension)

                        # check the resume in a valid size (1 MB)
                        # -----------------------------------------
                        if candidate_resume.size > 1048576:
                            response["errors"].append("Resume Size exceed (max-size 1MB)")

                    else:
                        response["info"].append("Resume is not Uploaded")
                else:
                    response["info"].append("Resume is not Uploaded")


                # move the files to the media directory only if no errors
                # --------------------------------------------------------
                if not response["errors"]:
                    fs = FileSystemStorage()
                    if video_name and video_name != "#":
                        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, new_video_name)):
                            os.remove(os.path.join(settings.MEDIA_ROOT, new_video_name))

                        video = fs.save(new_video_name, interview_video)


                    if resume_name and resume_name != "#":
                        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, new_resume_name)):
                            os.remove(os.path.join(settings.MEDIA_ROOT, new_resume_name))
                        resume = fs.save(new_resume_name, candidate_resume)
            else:
                response["info"].append("No files uploaded")
        except Exception as e:
            response["info"].append("No files uploaded %s" % str(e))

        # ================================================================================
        # save the values to the database if no errors while processing form data
        # ================================================================================

        if not response["errors"]:
            user_id = request.user.id

            consultancy = CustomUser.objects.get(pk=user_id)
            # if the save type is true the user is a new user
            # print(save_type)
            if not save_type:
                try:
                    candidate = Candidate.objects.get(consultancy=consultancy,
                                                      candidate_email=email)

                    position = Positions.objects.get(position_name=position_name)

                    if request.user.is_superuser:
                        candidate.candidate_status = status

                    candidate.position = position
                    candidate.candidate_name = name
                    candidate.candidate_email = email
                    candidate.candidate_age = age
                    candidate.candidate_contact_no = no
                    candidate.candidate_experience = experience
                    candidate.candidate_interview_time = interview_time
                    candidate.current_ctc = current_ctc
                    candidate.expected_ctc = expected_ctc
                    candidate.preferred_location = preferred_location
                    candidate.notice_period = notice_period
                    if new_video_name != "#":
                        candidate.candidate_interview = new_video_name
                    else:
                        new_video_name = candidate.candidate_interview
                    if new_resume_name != "#":
                        candidate.candidate_resume = new_resume_name
                    else:
                        new_resume_name = candidate.candidate_resume

                    candidate.save()
                    try:
                        Skillset.objects.filter(candidate=candidate).delete()
                        for skills in skill_set:
                            skill_set_instance = Skillset(candidate=candidate,
                                                          candidate_skill=skills)
                            skill_set_instance.save()
                    except:
                        pass

                    activities = Activities(consultancy=consultancy,
                                            candidate=candidate,
                                            activity="Candidate Details Updated",
                                            )

                    activities.save()

                except:

                    if request.user.is_superuser:
                        candidate = Candidate.objects.get(candidate_email=email)
                        candidate.candidate_status = status
                        candidate.save()

                    response["message"]["error"] = ("You are not authorized to update the candidate <br>"
                                                    "Belongs to some other User<br>"
                                                    "Only the candidate status can be changed")



            else:

                position = Positions.objects.get(position_name=position_name)

                candidate = Candidate(position=position,
                                      candidate_name=name,
                                      candidate_email=email,
                                      candidate_age=age,
                                      candidate_contact_no=no,
                                      candidate_experience=experience,
                                      candidate_interview_time=interview_time,
                                      current_ctc=current_ctc,
                                      expected_ctc=expected_ctc,
                                      preferred_location=preferred_location,
                                      notice_period=notice_period,
                                      candidate_interview=new_video_name,
                                      candidate_resume=new_resume_name,
                                      consultancy=consultancy)

                if request.user.is_superuser:
                    candidate.candidate_status = status


                candidate.save()

                # adding skill sets in the table
                for skills in skill_set:
                    skill_set_instance = Skillset(candidate=candidate,
                                                  candidate_skill=skills)
                    skill_set_instance.save()

                activities = Activities(consultancy=consultancy,
                                        candidate=candidate,
                                        activity="New Candidate Created",
                                        )

                activities.save()

        # ================================================================================
        # render and give the new values to the posted page

        # ================================================================================
        if not response["errors"]:
            # response["errors"] = []
            # response["info"] = []
            response["video_url"] = '/media/%s' % new_video_name
            response["resume_url"] = '/media/%s' % new_resume_name
            if not response["message"]:
                response["message"] = {"success": "Successfully Added Information"}

        # return the response object with status
        # print(response)
        return response

    # [FUNCTION generate the full details of the candidate]
    # ===============================================================================
    def get_full_details(self, request, data):
        '''
        :param request:
        :param data:
        :return: response dict
        '''

        # initialize the response directory
        # -----------------------------------

        response = {
            "candidate_details": {
                "position":"",
                "status": "",
                "candidate_name": "",
                "age": "",
                "experience": "",
                "location": "",
                "current_ctc": "",
                "expected_ctc": "",
                "email": "",
                "contact_no": "",
                "skills": [],
                "notice_period": "",
                "interview_time": "",
                "resume_url": "#",
                "video_url": "#"
            }
        }

        # ------------------------------------------
        candidate_id = int(data["id"])

        # consultancy = CustomUser.objects.get(pk=request.user.id)
        candidate = Candidate.objects.get(pk=candidate_id)
        skills = Skillset.objects.filter(candidate=candidate)

        skill_arr = skills.values_list("candidate_skill", flat=True)

        if request.user.is_superuser:
            response["candidate_details"]["status"] = candidate.candidate_status
        response["candidate_details"]["position"] = candidate.position.position_name
        response["candidate_details"]["candidate_name"] = candidate.candidate_name
        response["candidate_details"]["age"] = candidate.candidate_age
        response["candidate_details"]["experience"] = candidate.candidate_experience
        response["candidate_details"]["location"] = candidate.preferred_location
        response["candidate_details"]["current_ctc"] = candidate.current_ctc
        response["candidate_details"]["expected_ctc"] = candidate.expected_ctc
        response["candidate_details"]["email"] = candidate.candidate_email
        response["candidate_details"]["contact_no"] = candidate.candidate_contact_no
        response["candidate_details"]["notice_period"] = candidate.notice_period
        response["candidate_details"]["skills"] = list(skill_arr)

        interview_time = candidate.candidate_interview_time
        interview_time = interview_time.strftime(self.post_dt_format1)
        response["candidate_details"]["interview_time"] = interview_time
        response["candidate_details"]["resume_url"] = '/media/' + candidate.candidate_resume
        response["candidate_details"]["video_url"] = '/media/' + candidate.candidate_interview

        # print(response)
        return response

    # [FUNCTION generate the filtered data from the values of filters]
    # ================================================================================
    def get_filtered_data(self, request, data):

        '''
        :param self:
        :param request:
        :param data:
        :return: response dictionary
        '''

        # ---------------------------------
        notice_dict = {
            "IMMEDIATE" : "Immediate",
            "2WEEK": "2 Weeks",
            "1MONTH": "1 Month",
            "2MONTHS": "2 Months",
            "MORE": "More"
        }

        # initialize a response dictionary
        # ---------------------------------
        response = {
            "candidate_details": []
        }

        # query for other objects
        filter_queries = {}

        # Query for the skills [May be multiple]
        # -----------------------
        skill_query = Q()
        skill_array = []

        if data["skills"]:
            skill_array = data["skills"].split(",")
            skill_query = reduce(lambda q, value: q | Q(candidate_skill=str(value)), skill_array, Q())


        experience = data["experience"]
        location = data["location"]
        consultancy_id = data["consultancy"]
        position_id = data["position"]
        status = data["status"]

        if experience:
            filter_queries["candidate__candidate_experience"] = experience
        if location:
            filter_queries["candidate__preferred_location"] = location
        if consultancy_id:
            filter_queries["candidate__consultancy__id"] = consultancy_id
        if position_id:
            filter_queries["candidate__position__id"] = position_id
        if status:
            filter_queries["candidate__candidate_status"] = status

        if not request.user.is_superuser:
            candidate = Skillset.objects.filter(
                candidate__consultancy=request.user).filter(
                skill_query).filter(
                **filter_queries).select_related()

        else:
            candidate = Skillset.objects.filter(
                skill_query).filter(
                **filter_queries).select_related()


        candidate_temp_array = {}
        candidate_details = [skills for skills in candidate]

        # rearranging the data for better mapping
        for can in candidate_details:
            consultancy_name = can.candidate.consultancy.consultancy_name
            consultancy_name = consultancy_name if consultancy_name else "Mine"
            name = can.candidate.candidate_name
            skill = can.candidate_skill
            experience = can.candidate.candidate_experience
            id = can.candidate.pk
            current_ctc = can.candidate.current_ctc
            expected_ctc = can.candidate.expected_ctc
            notice = can.candidate.notice_period
            candidate_status = can.candidate.candidate_status

            if id not in candidate_temp_array:
                candidate_temp_array[id] = {"name": "",
                                            "skills": "",
                                            "experience": ""
                                            }
            candidate_temp_array[id]["consultancy"] = consultancy_name
            candidate_temp_array[id]["name"] = name
            candidate_temp_array[id]["skills"] += (skill if not candidate_temp_array[id]["skills"]
                                                   else ", %s" % skill)
            candidate_temp_array[id]["experience"] = "%s Year(s)" % str(experience)
            candidate_temp_array[id]["current_ctc"] = "%s Lakhs/Anum." % str(current_ctc)
            candidate_temp_array[id]["expected_ctc"] = "%s Lakhs/Anum." % str(expected_ctc)
            candidate_temp_array[id]["notice"] = notice_dict[notice]
            candidate_temp_array[id]["status"] = candidate_status


        # arrange the data in response format
        for id in candidate_temp_array:
            temp = {"candidate": {"name": candidate_temp_array[id]["name"],
                                  "id": id,
                                  },
                    "experience": candidate_temp_array[id]["experience"],
                    "skills": candidate_temp_array[id]["skills"],
                    "current_ctc": candidate_temp_array[id]["current_ctc"],
                    "expected_ctc": candidate_temp_array[id]["expected_ctc"],
                    "notice": candidate_temp_array[id]["notice"],
                    "consultancy": candidate_temp_array[id]["consultancy"],
                    "status": candidate_temp_array[id]["status"]
                    }

            response["candidate_details"].append(temp)



        response["candidate_details"] = self.custom_ordering(skill_array,
                                                             response["candidate_details"])


        # -----------------------
        # return the responses

        return response

    # [FUNCTION to fill the filters with valid data]
    # --------------------------------------------------

    def fill_filters(self, request, data=None):
        '''

        :param request:
        :param data:
        :return: reponse dict
        '''

        # initialize the response
        # -----------------------
        response = {
            "position": [],
            "consultancy": [],
            "skills": [],
            "locations": [],
            "experience": []
        }

        # ---------
        if data:

            # get the value of the filter
            filter_name = data["filter"]

            # ----------------------------------------------------------
            # to get the position
            if filter_name == "position":
                positions = Positions.objects.all().order_by("position_name")

                for position in positions:
                    response[filter_name].append({"label": position.position_name,
                                                  "value": position.id})


            # ----------------------------------------------------------
            # to get the filters for the consultancy

            if filter_name == "consultancy":
                '''yet to code'''
                if request.user.is_superuser:
                    consultancy = CustomUser.objects.all()
                    for con_objects in consultancy:
                        consultancy_name = con_objects.consultancy_name
                        consultancy_pk = con_objects.pk
                        if consultancy_name in ["null", None, "None"]:
                            consultancy_name = "All"
                            consultancy_pk = ""

                        response[filter_name].append({"label": consultancy_name,
                                                      "value": consultancy_pk})

                else:
                    user_id = request.user.id
                    consultancy = CustomUser.objects.get(pk=user_id)
                    consultancy_name = consultancy.consultancy_name
                    consultancy_pk = consultancy.pk

                    response[filter_name].append({"label": consultancy_name,
                                                  "value": consultancy_pk})

            # ----------------------------------------------------------
            # to get the filters for the candidate preferred location
            if filter_name == "skills":
                if request.user.is_superuser:
                    skills = Skillset.objects.all()
                else:

                    skills = Skillset.objects.filter(
                        candidate__consultancy=request.user)

                skills = skills.values_list(
                    "candidate_skill", flat=True).order_by(
                    "candidate_skill").distinct()

                for skill in skills:
                    response[filter_name].append({"label": skill, "value": skill})

            # ---------------------------------------------------------
            # to get the filters for the candidate preferred location
            if filter_name == "locations":

                if request.user.is_superuser:
                    locations = Candidate.objects.all()
                else:
                    locations = Candidate.objects.filter(
                        consultancy=request.user)
                locations = locations.values_list(
                    "preferred_location", flat=True).order_by(
                    "preferred_location").distinct()

                for location in locations:
                    # print(location)
                    response[filter_name].append({"label": location,
                                                  "value": location})

            # ---------------------------------------------------------
            # to get the filters for the candidate preferred experience
            if filter_name == "experience":

                if request.user.is_superuser:
                    experiences = Candidate.objects.all()
                else:
                    experiences = Candidate.objects.filter(consultancy=request.user)
                experiences = experiences.values_list(
                    "candidate_experience", flat=True).order_by(
                    "candidate_experience").distinct()

                for experience in experiences:
                    response[filter_name].append({"label": str(experience) +
                                                           " Year(s)", "value": experience})

        return response

    # ======================================================================================
    # custom function to sort the candidate details according to the rearrangement of skills
    # ======================================================================================
    def custom_ordering(self, priority_val=[], list_data=[]):
        '''
        :param priority_val:
        :param list_data:
        :return: list_data (sorted)
        '''
        # print(priority_val)
        if priority_val and list_data:
            for val in priority_val[::-1]:
                list_data = sorted(list_data,
                                   key=lambda k: (val.lower() not in k["skills"].lower()))

        # print(list_data)
        return (list_data)
