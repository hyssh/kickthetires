import json

class User_profile:
    def __init__(self, userid, username, gender, age, picture_url):
        self.userid = userid
        self.username = username
        self.gender = gender
        self.age = age
        self.picture_url = picture_url
        
    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)
    
    def get_userid(self):
        return self.userid
    
    def get_username(self):
        return self.username
    
    def get_gender(self):
        return self.gender
    
    def get_age(self):
        return self.age
    
    def get_picture_url(self):
        return self.picture_url
    
    def to_json(self) -> str:
        return {"userid": self.userid, "username":self.username,"gender":self.gender,"age":self.age,"picture_url":self.picture_url}
    
    def __str__(self):
        return f"{self.username}"


class User_profile_manager:
    def __init__(self, filepath="../data/user_profiles.json"):
        self.user_profiles = []

        with open(filepath, "r") as json_file:
            json_data = json.load(json_file)
        
        # add user profiles to list as USER_PROFILE objects
        for data in json_data:
            user_profile = User_profile.from_json(data)
            self.user_profiles.append(user_profile)    
        
    def get_user_profile_list(self):
        return self.user_profiles

    def add_user_profile(self, user_profile):
        # add USER_PROFILE object to list
        self.user_profiles.append(user_profile)

    # def remove_user_profile(self, username):
    #     for user_profile in self.user_profiles:
    #         if user_profile.username == username:
    #             self.user_profiles.remove(user_profile)
    #             return True
    #     return False
    
    def get_user_profile(self, userid : str):
        for profile in self.user_profiles:
            if profile.userid == userid:
                return profile
        return None
    
