import logging
import re

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from zwidget import Widget



class Button(Widget):


    def __init__(self, owner, locatordict, onClick=None):
        super(Button,self).__init__(owner, locatordict)
        self.onClick = onClick


    @property
    def value(self):
        e = self.wait_until_present()
        return e.get_attribute('value')


    def click(self):
        self.logger.info("clicking %s" % (self.locators['base']))
        e = self.wait_until_present()
        e.click()

        # perform "after-click" actions
        if self.onClick is not None:
            return self.onClick()


class Link(Widget):


    def __init__(self, owner, locatordict, onClick=None):
        super(Link,self).__init__(owner, locatordict)
        self.onClick = onClick


    def text(self):
        e = self.wait_until_present()
        return e.text


    def click(self):
        self.logger.info("clicking %s" % (self.locators['base']))
        e = self.wait_until_visible()

        # use action chains to move the mouse to the element
        # this helps us avoid accidentally clicking drop down menus
        # that open up when the mouse moves over them.
        #
        # some elements don't seem to be able to be scrolled into view
        # when using move_to_element_with_offset(e,1,1). in these cases
        # we could fiddle around with the offset to try to get them to
        # work, but its probably just easier to use move_to_element(e)
        # to get to the center of the element and hope it doesnt trigger
        # any popup menus. This is why we catch MoveTargetOutOfBoundsException
        # exceptions and retry the move.

        try:
            self.logger.debug("moving the mouse to element offset")
            ActionChains(self._browser)\
            .move_to_element_with_offset(e,1,1)\
            .perform()
        except MoveTargetOutOfBoundsException:
            self.logger.debug("moving the mouse to element offset failed")
            self.logger.debug("moving the mouse to element center")
            ActionChains(self._browser)\
            .move_to_element(e)\
            .perform()

        e.click()

        # perform "after-click" actions
        if self.onClick is not None:
            return self.onClick()

    def get_attribute(self,attribute):

        e = self.wait_until_present()

        # look for the attribute in this object
        self.logger.debug("looking for attribute in object: %s" % (attribute))
        v = super(Link,self).get_attribute(attribute)

        if v is None:
            # if it is not there, check for the attribute in the
            # anchor tag underneath this element in the HTML DOM
            try:
                self.logger.debug("looking for attribute in anchor tag")
                v = e.find_element_by_css_selector('a')\
                     .get_attribute(attribute)
            except NoSuchElementException:
                pass

        return v


class Text(Widget):
    """represents typeable <input> elements
       like those with state text or file

       click_focus determins whether the object should
       first click on the element to make sure it is in focus
       before sending keys to it. This is good for elements
       of state text, but will not work for elements of state
       file because clicking the element will popup a file
       browser.
    """

    def __init__(self, owner, locatordict, click_focus=True):
        super(Text,self).__init__(owner,locatordict)
        self.click_focus = click_focus


    @property
    def value(self):
        e = self.wait_until_present()
        return e.get_attribute('value')


    @value.setter
    def value(self, val):
        e = self.wait_until_present()

        if self.click_focus is True:
            # hover mouse over upper left corner of the element
            # we use the action chain to help avoid java script drop down menus
            # that get in the way of us clicking the element. this is especially
            # bad on nees.org
            ActionChains(self._browser)\
            .move_to_element_with_offset(e,0,0)\
            .perform()

            e.click()

        # some elements raise error when we use the clear() function.
        # we could try sending 's but that seems to be troublesome sometimes.
        # send 's is good for example, when clearing a body element
        # within an iframe for the WikiTextArea object.
        # instead of sending individual backspaces,
        # we try to highlight and replace
        e.send_keys(Keys.CONTROL,'a')
        self.logger.info("typing into %s" % (self.locators['base']))
        self.logger.debug("typing '%s' in %s" % (val,self.locators['base']))
        e.send_keys(val)


    def append(self,val):
        self.logger.info("appending into %s" % (self.locators['base']))
        self.logger.debug("appending '%s' in %s" % (val,self.locators['base']))
        # check for presence instead of visibility because some upload buttons
        # use the text widget to fill in the name of the file to be uploaded.
        # in these cases, the element does not seem to be visible, only present.
        e = self.wait_until_present()
        e.send_keys(val)

