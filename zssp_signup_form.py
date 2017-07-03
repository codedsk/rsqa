from zformbase import FormBase
from zelement import Text
from zelement import Link
from zelement import Button

class SSPSignUpForm(FormBase):
    def __init__(self, owner, locatordict={}):
        super(SSPSignUpForm,self).__init__(owner,locatordict)

        # update this object's locator
        self.locators.update(SSPSignUpForm_Locators.locators)

        # update the locators with those from the owner
        self.update_locators_from_owner()

        # setup page object's components
        self.firstname       = Text(self,{'base':'firstname'})
        self.lastname        = Text(self,{'base':'lastname'})
        self.email           = Text(self,{'base':'email'})
        self.company         = Text(self,{'base':'company'})
        self.country         = Text(self,{'base':'country'})
        self.eula            = Link(self,{'base':'eula'})
        self.privacy         = Link(self,{'base':'privacy'})
        self.errorMsg        = Text(self,{'base':'errorMsg'})

        self.fields += ['firstname', 'lastname', 'email', 'company', 'country']

        # update the component's locators with this objects overrides
        self._updateLocators()

    def get_error_info(self):
        return self.errorMsg.value


class SSPSignUpForm_Locators_Base(object):
    """locators for SSPSignUpForm object"""

    locators = {
        'base'           : "css=#mktoForm_1553",
        'firstname'      : "css=#FirstName",
        'lastname'       : "css=#LastName",
        'email'          : "css=#Email",
        'company'        : "css=#Company",
        'country'        : "css=#Country",
        'eula'           : "css=.mktoFormRow a:nth-of-type(1)",
        'privacy'        : "css=.mktoFormRow a:nth-of-type(2)",
        'errorMsg'       : "css=.mktoErrorMsg",
        'submit'         : "css=#mktoForm_1553 [type='submit']",
    }


SSPSignUpForm_Locators = SSPSignUpForm_Locators_Base()
