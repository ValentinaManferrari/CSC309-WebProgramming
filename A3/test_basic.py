"""

CSC309 Fall 2022
Assignment 3
University of Toronto

Note:
Passing this test will not guarantee full or
even **partial** marks at final tests!!!

You are still responsible for making sure that
all your endpoints, fields, and error messages
exactly match the handout.
"""

import unittest
# TODO: pip install requests
import requests
import random
import re

class PreTest(unittest.TestCase):
    def setUp(self):
        self.num = random.randint(1, 1000000)

        url_register = "http://localhost:8000/accounts/register/"
        data_register = {"username": "test_" + str(self.num), "password1": "iamatester", "password2": "iamatester",
                         "email": "hanxianxu.huang@utoronto.ca", "first_name": "Han Xian Xu", "last_name": "Huang"}
        res1_post = requests.post(url_register, data=data_register)

        # TODO: Comment out Line 32 - 48 if you haven't implemented "/accounts/login/"
        url_login = "http://localhost:8000/accounts/login/"
        data_login = {"username": "test_" + str(self.num), "password": "iamatester"}
        res2_post = requests.post(url_login, data=data_login, allow_redirects=False)
        self.cookies = res2_post.cookies.get_dict()

        # TODO: Comment out Line 38 - 48 if you haven't implemented "/banks/add/"
        url_add_bank = "http://localhost:8000/banks/add/"
        data_add_bank = {"name": "Test", "description": "Test", "inst_num": "000", "swift_code": "TESTAAA1"}
        res5_post = requests.post(url_add_bank, data=data_add_bank, allow_redirects=False, cookies=self.cookies)
        self.bank_id = re.search(r"/banks/([0-9]*)/details/", res5_post.headers["Location"]).group(1)

        # TODO: Comment out Line 44 - 48 if you haven't implemented "/banks/<bank_id>/branches/add/"
        url_add_branch = "http://localhost:8000/banks/" + self.bank_id + "/branches/add/"
        data_add_branch = {"name": "Test", "transit_num": "12345", "address": "UTM", "email": "br@utoronto.ca",
                           "capacity": 10}
        res9_post = requests.post(url_add_branch, data=data_add_branch, allow_redirects=False, cookies=self.cookies)
        self.branch_id = re.search(r"/banks/branch/([0-9]*)/details/", res9_post.headers["Location"]).group(1)

    def test_register(self):
        num = random.randint(1, 1000000)

        url_register = "http://localhost:8000/accounts/register/"
        data_register = {"username": "test_" + str(num), "password1": "iamatester", "password2": "iamatester",
                         "email": "hanxianxu.huang@utoronto.ca", "first_name": "Han Xian Xu", "last_name": "Huang"}
        res1_get = requests.get(url_register)
        res1_post = requests.post(url_register, data=data_register)
        self.assertEqual(200, res1_get.status_code)
        self.assertEqual(200, res1_post.status_code)

    def test_login(self):
        url_login = "http://localhost:8000/accounts/login/"
        data_login = {"username": "test_" + str(self.num), "password": "iamatester"}
        res2_get = requests.get(url_login)
        res2_post = requests.post(url_login, data=data_login, allow_redirects=False)
        self.assertEqual(200, res2_get.status_code)
        self.assertEqual(302, res2_post.status_code)

    def test_view_profile(self):
        url_view_profile = "http://localhost:8000/accounts/profile/view/"
        res3 = requests.get(url_view_profile, cookies=self.cookies)
        self.assertEqual(200, res3.status_code)

    def test_edit_profile(self):
        url_edit_profile = "http://localhost:8000/accounts/profile/edit/"
        data_edit_profile = {"password1": "iamatester", "password2": "iamatester", "email": "hanxianxu.huang@utoronto.ca",
                             "first_name": "Han Xian Xu", "last_name": "Huang"}
        res4_get = requests.get(url_edit_profile, cookies=self.cookies)
        res4_post = requests.post(url_edit_profile, data=data_edit_profile, allow_redirects=False, cookies=self.cookies)
        self.assertEqual(200, res4_get.status_code)
        self.assertEqual(302, res4_post.status_code)

    def test_add_bank(self):
        url_add_bank = "http://localhost:8000/banks/add/"
        data_add_bank = {"name": "Test", "description": "Test", "inst_num": "000", "swift_code": "TESTAAA1"}
        res5_get = requests.get(url_add_bank, cookies=self.cookies)
        res5_post = requests.post(url_add_bank, data=data_add_bank, allow_redirects=False, cookies=self.cookies)
        self.assertEqual(200, res5_get.status_code)
        self.assertEqual(302, res5_post.status_code)

    def test_all_banks(self):
        url_all_banks = "http://localhost:8000/banks/all/"
        res6 = requests.get(url_all_banks)
        self.assertEqual(200, res6.status_code)

    def test_all_branches(self):
        url_all_branches = "http://localhost:8000/banks/" + self.bank_id + "/branches/all/"
        res7 = requests.get(url_all_branches)
        self.assertEqual(200, res7.status_code)

    def test_bank_details(self):
        url_bank_details = "http://localhost:8000/banks/" + self.bank_id + "/details/"
        res8 = requests.get(url_bank_details)
        self.assertEqual(200, res8.status_code)

    def test_add_branch(self):
        url_add_branch = "http://localhost:8000/banks/" + self.bank_id + "/branches/add/"
        data_add_branch = {"name": "Test", "transit_num": "12345", "address": "UTM", "email": "br@utoronto.ca",
                           "capacity": 10}
        res9_get = requests.get(url_add_branch, cookies=self.cookies)
        res9_post = requests.post(url_add_branch, data=data_add_branch, allow_redirects=False, cookies=self.cookies)
        self.assertEqual(200, res9_get.status_code)
        self.assertEqual(302, res9_post.status_code)

    def test_branch_details(self):
        url_branch_details = "http://localhost:8000/banks/branch/" + self.branch_id + "/details/"
        res10 = requests.get(url_branch_details)
        self.assertEqual(200, res10.status_code)

    def test_logout(self):
        url_logout = "http://localhost:8000/accounts/logout/"
        res12 = requests.get(url_logout)
        self.assertEqual(200, res12.status_code)


if __name__ == '__main__':
    unittest.main()