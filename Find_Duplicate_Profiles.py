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

    def __init__(self, first_name, last_name, email_field, date_of_birth=None, class_year=None):
        profiles.global_profile_id = profiles.global_profile_id+1
        self.id = profiles.global_profile_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.class_year = class_year
        self.email_field = email_field

    # this method calculates the matching score between 2 profiles
    def get_profile_matching_score(self, profile_2):
        match_score = 0
        profile_1_string = self.first_name+self.last_name + \
            self.email_field  # concatinating first_name+last_name+email_field
        profile_2_string = profile_2.first_name + \
            profile_2.last_name+profile_2.email_field  # concatinating first_name+last_name+email_field

        # fuzz.ratio() compares 2 strings and return their match percantage
        ratio = fuzz.ratio(profile_1_string, profile_2_string)

        if(ratio > 80):
            match_score += 1

        # if both profiles have class_year
        if(self.class_year is not None and profile_2.class_year is not None):
            if(self.class_year == profile_2.class_year):
                match_score += 1
            else:
                if(match_score != 0):
                    match_score -= 1

        # if both profiles have date_of_birth
        if(self.date_of_birth is not None and profile_2.date_of_birth is not None):
            if(self.date_of_birth == profile_2.date_of_birth):
                match_score += 1
            else:
                if(match_score != 0):
                    match_score -= 1
        return match_score


# matching_profiles class stores matching profiles

class matching_profiles:
    global_id = 0

    # constructor compares 2 profiles and if match_score>1 it will store them in memory
    def __init__(self, profile_1, profile_2):
        match_score = profile_1.get_profile_matching_score(profile_2)
        if(match_score > 1):
            matching_profiles.global_id = matching_profiles.global_id+1
            self.id = matching_profiles.global_id
            self.profile_1_id = profile_1.id
            self.profile_2_id = profile_2.id


# Str_A = 'FuzzyWuzzy is a lifesaver!'
# Str_B = 'fuzzy wuzzy is a LIFE SAVER.'
# ratio = fuzz.ratio(Str_A.lower(), Str_B.lower())
# print('Similarity score: {}'.format(ratio))
# print("fff")
p1 = profiles("Harshu", "Shrivastava",
              "hs3101.harshit@gmail.com", None, 2022)
p2 = profiles("Harshit", "Shrivastava",
              "hs3101.harshit@gmail.com", "2022-01-01", 2022)
m1 = matching_profiles(p1, p2)
