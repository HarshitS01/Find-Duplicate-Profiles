import fuzzywuzzy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# profile class stores the details in each profile:
# first_name
# last_name
# email_field
# date_of_birth
# class_year


class profiles:
    global_profile_id = 0
    all_fields = ["first_name", "last_name",
                  "email_field", "date_of_birth", "class_year"]

    def __init__(self, first_name, last_name, email_field, date_of_birth=None, class_year=None):
        profiles.global_profile_id = profiles.global_profile_id+1
        self.id = profiles.global_profile_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.class_year = class_year
        self.email_field = email_field

    # this method calculates the matching score between 2 profiles
    def get_profile_matching_details(self, profile_2, fields):
        return_data = {}
        set_difference = set(profiles.all_fields) - set(fields)
        ignored_attributes = list(set_difference)
        matching_attributes = []
        non_matching_attributes = []
        match_score = 0
        profile_1_string = None
        profile_2_string = None
        profiles_match = False

        for field in fields:
            if(field == "first_name"):
                ratio = fuzz.ratio(self.first_name, profile_2.first_name)
                if(ratio > 80):
                    match_score += 1
                    matching_attributes.append("first_name")
                else:
                    non_matching_attributes.append("first_name")

            elif(field == "last_name"):
                ratio = fuzz.ratio(self.last_name, profile_2.last_name)
                if(ratio > 80):
                    match_score += 1
                    matching_attributes.append("last_name")
                else:
                    non_matching_attributes.append("last_name")
            elif(field == "email_field"):
                ratio = fuzz.ratio(self.email_field, profile_2.email_field)
                if(ratio > 80):
                    match_score += 1
                    matching_attributes.append("email_field")
                else:
                    non_matching_attributes.append("email_field")
            elif(field == "class_year"):
                # if both profiles have class_year
                if(self.class_year is not None and profile_2.class_year is not None):
                    if(self.class_year == profile_2.class_year):
                        match_score += 1
                        matching_attributes.append("class_year")
                    else:
                        non_matching_attributes.append("class_year")
                        if(match_score != 0):
                            match_score -= 1
                else:
                    ignored_attributes.append("class_year")

            elif(field == "date_of_birth"):
                # if both profiles have date_of_birth
                if(self.date_of_birth is not None and profile_2.date_of_birth is not None):
                    if(self.date_of_birth == profile_2.date_of_birth):
                        match_score += 1
                        matching_attributes.append("date_of_birth")
                    else:
                        non_matching_attributes.append("date_of_birth")
                        if(match_score != 0):
                            match_score -= 1
                else:
                    ignored_attributes.append("date_of_birth")

        ratio = fuzz.ratio(profile_1_string, profile_2_string)

        if(match_score > 1):
            profiles_match = True

        return_data["profiles_match"] = profiles_match
        return_data["match_score"] = match_score
        return_data["matching_attributes"] = matching_attributes
        return_data["non_matching_attributes"] = non_matching_attributes
        return_data["ignored_attributes"] = ignored_attributes

        return return_data


# matching_profiles class stores matching profiles

class matching_profiles:
    global_id = 0

    # constructor compares 2 profiles and if match_score>1 it will store them in memory
    def __init__(self, profile_1, profile_2, response):
        self.id = matching_profiles.global_id
        self.profile_1_id = profile_1.id
        self.profile_2_id = profile_2.id
        self.match_score = response["match_score"]
        self.matching_attributes = response["matching_attributes"]
        self.non_matching_attributes = response["non_matching_attributes"]
        self.ignored_attributes = response["ignored_attributes"]


def find_duplicates(profiles, fields):
    matched_profiles = []
    for i in range(0, len(profiles)-1):
        for j in range(i+1, len(profiles)-1):
            response = profiles[i].get_profile_matching_details(
                profiles[j], fields)
            if(response["profiles_match"]):
                m = matching_profiles(profiles[i], profiles[j], response)
                matched_profiles.append(m)
    return matched_profiles


p1 = profiles("Kanhai", "Shah",
              "knowkanhai@gmail.com", None, None)
p2 = profiles("Kanhail", "Shah",
              "knowkanhai+donotcompare@gmail.com", "1900-10-11", 2012)
response = find_duplicates([p1, p2], ["first_name", "last_name"])
