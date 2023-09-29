from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest

class TestUserRegister(BaseCase):
    def test_create_user_successfuly(self):
        data = self.prepare_registrarion_data()
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")


    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registrarion_data(email)
        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    parameters = {
        'username',
        'firstName',
        'lastName',
        'email',
        'password',
    }

    @pytest.mark.parametrize("missing_param", parameters)
    def test_create_user_with_missing_parameters(self, missing_param):
        data = self.prepare_registrarion_data()
        data.pop(missing_param, None)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missing_param}", \
            f"Unexpected response content: {response.content}"

    names = {
        # username with 1 symbol:
        "q",
        # username with 250 symbols:
        """qqqqaefeafaeaefqqqqaaaaaaaaaaaaffffffffffqqqqqqqqqqqqqqqqqqqqafaefaefaefaefeafaefaefaefeafaefeafaefqqqqqqqqqq
           wwwwwwwddddddddddddddddddddddddddwwwwwwwwwwwwwwwfffffffffffffffffffffffffffffffffffwwwafeafaefafefaefaefaefae
           asdasfafafdsafafadfadsfasdfasfasfsaasdasdasdfasfasdasdasdasdasdasdasfadfdfagdafadfewdfeafaefeeeeeeeeeeeeeeeee"""
    }
    @pytest.mark.parametrize("name", names)
    def test_create_user_with_different_username_str_length(self, name):
        data = self.prepare_registrarion_data(username=name)
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert_text = "long" if len(name) > 250 else "short"
        assert response.content.decode("utf-8") == f"The value of 'username' field is too {assert_text}", \
            f"Unexpected response content: {response.content}"