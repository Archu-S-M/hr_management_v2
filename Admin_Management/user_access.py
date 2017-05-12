from django.contrib.auth.models import User
'''
the script to get the user access to a particular module
'''


# Class to get the default pages for users according to the permission
class user_pages():

    user_views = {}

    def __init__(self, user):
        self.user_views["pages"] = [{"name": "Dashboard",
                                    "url": "Dashboard",
                                    "child": [],
                                    "icon": "fa fa-table fa-fw"},

                                    {"name": "Manage Consultancy",
                                     "url": "ManageConsultancy",
                                     "child":[],
                                     "icon": "fa fa-building fa-fw"},

                                    {"name": "Candidate Profile",
                                     "url": "CandidateProfile",
                                     "child": [],
                                     "icon": "fa fa-users fa-fw"},

                                    {"name": "Requirements",
                                     "url": None,
                                     "child": [{"name": "Questionnaire",
                                                "url": "Questionnaire",
                                                "child": [],
                                                "icon": ""},

                                               {"name": "Candidate Eligibility",
                                                "url": "Eligibility",
                                                "child": [],
                                                "icon": ""},
                                               ],
                                     "icon": "fa fa-lightbulb-o fa-fw"},

                                    {"name": "Settings",
                                     "url": "Settings",
                                     "child": [],
                                     "icon": "fa fa-cogs fa-fw"},

                                    ]
        self.user = user

    def getUserViews(self):


        # If the user is Hr
        if self.user.is_superuser:
            self.user_views["access"] = ["All"]
            self.user_views["permissions"] = [{"Dashboard": ["view","update"]},
                                              {"ManageConsultancy": ["view","update","delete"]},
                                              {"CandidateProfile": ["view"]},
                                              {"Questionnaire": ["view","update","create","delete"]},
                                              {"Eligibility": ["view", "update", "create","delete"]},
                                              {"Settings": ["view", "update", "create","delete"]},
                                            ]
            return self.user_views

        # If the user is consultant
        elif self.user.is_staff:

            page_1, _, page_2, page_3, *_ = self.user_views["pages"]

            self.user_views["pages"] = [page_1, page_2, page_3]
            self.user_views["access"] = [page_1["url"], page_2["url"],
                                         page_3["url"], page_3["child"][0]["url"],
                                         page_3["child"][1]["url"]]
            self.user_views["permissions"] = [{"Dashboard": ["view"]},
                                              {"CandidateProfile": ["view","create","update","delete"]},
                                              {"Questionnaire": ["view"]},
                                              {"Eligibility": ["view"]},
                                             ]

            return self.user_views

        # If the user is gust/new Registration
        else:

            self.user_views["pages"] = []
            self.user_views["access"] = ["Register"]
            # pages = [page_1, page_2]
            return self.user_views