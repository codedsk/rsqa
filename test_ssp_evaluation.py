import pytest
import sys
import os
import re

from ztestcase import TestCase2
from zpage import Page
from zssp_signup_form import SSPSignUpForm
from zexceptions import TimeoutException


pytestmark = [ pytest.mark.website,
               pytest.mark.ssp_eval
             ]


class TestSSPEvalForm(TestCase2):

    def setup_method(self,method):

        # setup a web browser
        url = 'https://www.rstudio.com/products/shiny-server-pro/evaluation/'
        self.browser.get(url)


    def teardown_method(self,method):
        pass


    def test_valid_inputs(self):
        """
        submit the form with valid inputs, check the landing page url
        """

        # load a page object for the signup form
        page = Page(self.browser)
        po = SSPSignUpForm(page)

        # populate the form with some data
        data = {
            'firstname' : 'pete',
            'lastname'  : 'purdue',
            'email'     : 'pete@purdue.edu',
            'company'   : 'Purdue University',
            'country'   : 'Good Ol\' US of A'
        }

        page.set_page_load_marker()
        po.submit_form(data)
        page.wait_for_page_to_load()

        # FIXME: resolve timing issue with loading pages by using
        # page.set_page_load_marker() and page.wait_for_page_to_load()
        # inside po.submit_form()

        landing_url = 'https://www.rstudio.com/products/shiny/download-commercial/'
        assert self.browser.current_url == landing_url


    def test_invalid_email(self):
        """
        submit the form with invalid email, check for error msg
        """

        # load a page object for the signup form
        po = SSPSignUpForm(Page(self.browser))

        # populate the form with some data
        data = {
            'firstname' : 'pete',
            'lastname'  : 'purdue',
            'email'     : 'petepurdue.edu',
            'company'   : 'Purdue University',
            'country'   : 'Good Ol\' US of A'
        }

        po.submit_form(data)

        # wait for the error message to appear
        try:
            po.errorMsg.wait_until_visible()
        except TimeoutException:
            pass

        assert po.errorMsg.is_displayed()
        assert po.get_error_info != ""

