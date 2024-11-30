from user_management.auto_cibus_user import AutoCibusUser
import os
import json


class UserManagementInterface:
    def __init__(self):
        pass

    def validate_user_file_exists(self, user_email, users_path=os.getenv("USERS_PATH")):
        user_name = user_email.lower().split("@")[0]
        all_user_file_names = [file.replace(".json", "") for file in os.listdir(path=users_path)]
        if user_name in all_user_file_names:
            return True
        else:
            print(f"couldn't find user file for {user_email}. Found the next users: {all_user_file_names}")
            return False

    def create_new_user_file(self, new_user: AutoCibusUser, users_path=os.getenv("USERS_PATH")):
        #TODO: validate no user file with same exists
        user_name = new_user.cibus_email.split("@")[0]
        print(user_name)
        with open((users_path + user_name + ".json"), "w", encoding='utf-8') as user_file: #, encoding='utf-8'
            json.dump(new_user.toDICT(), user_file, ensure_ascii=False, indent=4) #, ensure_ascii=False, indent=4
        # with open(f"{users_path}", )

    


if __name__ == '__main__':
    example_user = AutoCibusUser(
        cibus_email="ariel.agra@gmail.com"
    )

    UserManagementInterface().create_new_user_file(new_user=example_user,
                                                   users_path="C:\\personal\\projects\\auto_cibus\\internal\\users_dir\\")

    # UserManagementInterface().validate_user_file_exists(user_email="aridsel.agra@sdgsdgd", users_path="C:\\personal\\projects\\auto_cibus\\internal\\users_dir\\")
