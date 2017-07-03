import zconfig as config
import logging
import os
import sys
import traceback

# FIXME: move browser creation somewhere else
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

MARKER = "="*5

class TestCaseMetaClass2(type):

    def __new__(cls,name,bases,dct):

        def wrapped_setup_method(self,method,*args,**kwargs):

            self.fnbase = "%s.%s" % (type(self).__name__, method.__name__)
            self.browser = None

            # add start marker to the log
            self.logger.info("%s TestCase Start: %s" % (MARKER,self.fnbase))

            # setup screenshot file name
            self._setup_test_case_screenshot()

            # start recording video if enabled
            self._start_test_case_recording()

            # setup the browser
            self._start_test_case_browser()

            try:

                # call the user's setup function
                user_setup_method(self,method,*args,**kwargs)

            except Exception as e:

                exc_info = sys.exc_info()

                ## try to get a screenshot to help with debugging
                #if self.screenshotfn is not None:
                #    if hasattr(self,'browser') and self.browser is not None:
                #        try:
                #            self.browser.take_screenshot(self.screenshotfn)
                #        except Exception:
                #            self.logger.debug('Exception ignored: %s %s'
                #                % (sys.exc_info()[1],sys.exc_info()[2]))

                # close the browser
                self._stop_test_case_browser()

                # stop xvfb recording
                self._stop_test_case_recording()

                # add end test marker to the log file
                self.logger.info("%s TestCase End: %s" % (MARKER,self.fnbase))

                raise exc_info[1], None, exc_info[2]


        def wrapped_teardown_method(self,method,*args,**kwargs):

            try:
                user_teardown_method(self,method,*args,**kwargs)

            finally:
                # close the browser
                self._stop_test_case_browser()

                # stop xvfb recording
                self._stop_test_case_recording()

                # add end test marker to the log file
                self.logger.info("%s TestCase End: %s" % (MARKER,self.fnbase))


        # if the TestCase already provides setUp, wrap it
        if 'setup_method' in dct:
            user_setup_method = dct['setup_method']
        else:
            user_setup_method = lambda self,method: None

        dct['setup_method'] = wrapped_setup_method

        # if the TestCase already provides tearDown, wrap it
        if 'teardown_method' in dct:
            user_teardown_method = dct['teardown_method']
        else:
            user_teardown_method = lambda self,method: None

        dct['teardown_method'] = wrapped_teardown_method

        # return the class instance with the replaced setUp/tearDown
        return type.__new__(cls, name, bases, dct)


class TestCase2(object):
    __metaclass__ = TestCaseMetaClass2
    logger = logging.getLogger()

    def _start_test_case_browser(self):
        binary = FirefoxBinary(config.ff_path)
        self.browser = webdriver.Firefox(firefox_binary=binary)


    def _stop_test_case_browser(self):
        if self.browser is not None:
            try:
                self.browser.close()
            except Exception:
                self.logger.debug('Exception ignored: %s\n%s'
                    % (sys.exc_info()[1],traceback.format_exc()))


    def _setup_test_case_screenshot(self):
        if config.screenshot_dir is not None:
            ssdir = os.path.abspath(
                        os.path.expanduser(
                            os.path.expandvars(
                                config.screenshot_dir)))

            self.screenshotfn = os.path.join(ssdir,"%s.png" % (self.fnbase))
        else:
            self.screenshotfn = None


    def _start_test_case_recording(self):
        self.recording = None
        if config.video_dir is not None:
            videodir = os.path.abspath(
                        os.path.expanduser(
                            os.path.expandvars(
                                config.video_dir)))
            self.videofn = os.path.join(videodir,"%s.mp4" % (self.fnbase))
            #self.recording = hubcheck.record.WebRecordXvfb(self.videofn)
            #self.recording.start()


    def _stop_test_case_recording(self):
        if self.recording is not None:
            try:
                self.recording.stop()
            except Exception:
                self.logger.debug('Exception ignored: %s\n%s'
                    % (sys.exc_info()[1],traceback.format_exc()))

