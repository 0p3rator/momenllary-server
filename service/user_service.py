from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import json
import uuid
from flask_login import UserMixin

PROFILE_FILE = "profiles.json"

class User(UserMixin):
    def __init__(self, username):
        self.__username = username
        self.__password_hash = self.get_password_hash()
        self.__id = self.get_id()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        #save to json tempor
        #print 1
        self.__password_hash = generate_password_hash(password)

        with open(PROFILE_FILE, 'w+') as f:
            try:
                profiles = json.load(f)
            except ValueError:
                profiles = {}
            profiles[self.__username] = [self.__password_hash,
                                       self.__id]
            f.write(json.dumps(profiles))

    def verify_password(self, password):
        if self.__password_hash is None:
            return False
        return check_password_hash(self.__password_hash, password)

    def get_password_hash(self):
        """try to get password hash from file.

        :return password_hash: if the there is corresponding user in
                the file, return password hash.
                None: if there is no corresponding user, return None.
        """
        try:
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                user_info = user_profiles.get(self.__username, None)
                if user_info is not None:
                    return user_info[0]
        except IOError:
            return None
        except ValueError:
            return None
        return None

    def get_id(self):
        """get user id from profile file, if not exist, it will
        generate a uuid for the user.
        """
        if self.__username is not None:
            try:
                with open(PROFILE_FILE) as f:
                    user_profiles = json.load(f)
                    if self.__username in user_profiles:
                        return user_profiles[self.__username][1]
            except IOError:
                pass
            except ValueError:
                pass
        return unicode(uuid.uuid4())

    @staticmethod
    def get(user_id):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        if not user_id:
            return None
        try:
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                for user_name, profile in user_profiles.iteritems():
                    if profile[1] == user_id:
                        return User(user_name)
        except:
            return None
        return None

if __name__ == '__main__':
    user1 = User('changyu')
    user1.password = 'Aaa'