from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest
import allure

@allure.epic("User cases")
@allure.description('Case for changing user')
class TestUserEdit(BaseCase):
    @allure.step('Creating and modifying a created user')
    def test_edit_just_created_user(self):
        #REGISTER
        register_data = self.prepare_registrarion_data()
        response1 = MyRequests.post("/user/", data=register_data )

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        #LOGIN
        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed name"
        response3 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name})
        Assertions.assert_code_status(response3, 200)

        #GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.step('Editing a user without authorization')
    def test_edit_just_created_user_without_authorization(self):
        # REGISTER
        register_data = self.prepare_registrarion_data()
        response1 = MyRequests.post(
            "/user/",
            data=register_data
        )
        Assertions.assert_code_status(response1,200)
        Assertions.assert_json_has_key(response1,"id")
        user_id = self.get_json_value(response1,"id")
        # EDIT
        new_name = "Changed Name"
        response2 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response2,400)
        Assertions.assert_response_text(response2,"Auth token not supplied")

    @allure.step('Editing a newly created user by another authorized user')
    def test_edit_just_created_user_by_other_authorizated_user(self):
        # REGISTER USER1
        user1_register_data = self.prepare_registrarion_data()
        response1 = MyRequests.post(
            "/user/",
            data=user1_register_data
        )
        Assertions.assert_code_status(response1,200)
        Assertions.assert_json_has_key(response1,"id")
        user1_email = user1_register_data["email"]
        user1_first_name = user1_register_data["firstName"]
        user1_password = user1_register_data["password"]
        user1_user_id = self.get_json_value(response1,"id")

        # REGISTER USER2
        user2_register_data = self.prepare_registrarion_data()
        response2 = MyRequests.post(
            "/user/",
            data=user2_register_data
        )
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")
        user2_email = user2_register_data["email"]
        user2_first_name = user2_register_data["firstName"]
        user2_password = user2_register_data["password"]
        user2_user_id = self.get_json_value(response2, "id")
        # LOGIN BY USER2
        login_data = {
            "email" : user2_email,
            "password" : user2_password
        }
        response3 = MyRequests.post(
            "/user/login",
            data=login_data
        )
        user2_auth_sid = self.get_cookie(response3,"auth_sid")
        user2_token = self.get_header(response3,"x-csrf-token")

        #EDIT USER1 DATA USER2 CHECK THAT USER2 CAN'T EDIT USER1 DATA
        new_name = "Changed Name"
        response4 = MyRequests.put(
            f"/user/{user1_user_id}",
            headers={"x-csrf-token":user2_auth_sid},
            cookies={"auth_sid":user2_token},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response4,400)
        Assertions.assert_response_text(response4,"Auth token not supplied")

        #LOGIN USER1
        login_data = {
            "email": user1_email,
            "password": user1_password
        }
        response5 = MyRequests.post(
            "/user/login",
            data=login_data
        )
        user1_auth_sid = self.get_cookie(response5, "auth_sid")
        user1_token = self.get_header(response5, "x-csrf-token")

        #GET USER1 DATA CHECK THAT USER1 DATA WAS NOT EDITED
        response5 = MyRequests.get(
            f"/user/{user1_user_id}",
            headers={"x-csrf-token": user1_token},
            cookies={"auth_sid": user1_auth_sid},
        )
        Assertions.assert_json_value_by_name(
            response5,
            "firstName",
            user1_first_name,
            "Wrong name of the user after incorrect edit. 'firstName' must not be edited"
        )

    params = {"email", "firstName"}

    @allure.description("Check that the authorized user cannot change his data to data with incorrect parameter")
    @pytest.mark.parametrize("incorrect_parameter", params)
    @allure.step("Editing a newly created user with incorrect data")
    def test_edit_just_created_user_with_incorrect_data(self, incorrect_parameter):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post(
            "/user/",
            data=register_data
        )

        Assertions.assert_code_status(response1,200)
        Assertions.assert_json_has_key(response1,"id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1,"id")


        #LOGIN
        login_data = {
            "email" : email,
            "password" : password
        }

        response2 = MyRequests.post(
            "/user/login",
            data=login_data
        )

        auth_sid = self.get_cookie(response2,"auth_sid")
        token = self.get_header(response2,"x-csrf-token")


        #EDIT
        if incorrect_parameter == "email":
            data_for_edit = {"email" : "email_without_symbol.mail.ru"}
        else:
            data_for_edit = {"firstName": "q"}

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token":token},
            cookies={"auth_sid":auth_sid},
            data=data_for_edit
        )

        Assertions.assert_code_status(response3,400)
        if incorrect_parameter == "email":
            Assertions.assert_response_text(response3,"Invalid email format")
        elif incorrect_parameter == "firstName":
            Assertions.assert_json_value_by_name(
                response3,
                "error",
                "Too short value for field firstName",
                "Wrong error message when short length of response param 'firstName'")

        #GET CHECK THAT USER DATA WAS NOT EDITED WITH INCORRECT PARAMETERS
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            first_name,
            f"'firstName' param must not be changed after incorrect edit request. "
            f"Expect value: {first_name} "
        )
        Assertions.assert_json_value_by_name(
            response4,
            "email",
            email,
            f"'email' param must not be changed after incorrect edit request. "
            f"Expect value: {email} "
        )