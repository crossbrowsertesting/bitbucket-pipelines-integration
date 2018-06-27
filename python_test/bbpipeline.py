#Bitbucket Pipeline Example, derived from https://github.com/crossbrowsertesting/selenium-python

import unittest
from selenium import webdriver
import requests
import os

class BasicTest(unittest.TestCase):
    def setUp(self):
        print(os.getenv('CBT_USERNAME'), os.getenv('CBT_AUTHKEY'))
        # Put your username and authey below
        # You can find your authkey at crossbrowsertesting.com/account
        self.username = os.getenv('CBT_USERNAME')
        self.authkey  = os.getenv('CBT_AUTHKEY')

        self.api_session = requests.Session()
        self.api_session.auth = (self.username,self.authkey)

        self.test_result = None

        caps = {}

        caps['name'] = 'BitBucket Pipeline'
        caps['build'] = '1.0'
        caps['browserName'] = 'Safari'
        caps['version'] = '11'
        caps['platform'] = 'Mac OSX 10.13'
        caps['screenResolution'] = '1366x768'
        caps['record_video'] = 'true'
        caps['record_network'] = 'true' 

        # start the remote browser on our server
        self.driver = webdriver.Remote(
            desired_capabilities=caps,
            command_executor="http://%s:%s@hub.crossbrowsertesting.com:80/wd/hub"%(self.username,self.authkey)
        )

        self.driver.implicitly_wait(20)

    def test_CBT(self):
        # We wrap this all in a try/except so we can set pass/fail at the end
        try:
            # load the page url
            print('Loading URL...')
            self.driver.get('http://local:8080/python_test/testpage.html')
            
            #check the title
            print('Checking title...')
            self.assertEqual("Test page", self.driver.title)

            # if we are still in the try block after all of our assertions that 
            # means our test has had no failures, so we set the status to "pass"
            self.test_result = 'pass'

        except AssertionError as e:

            # if any assertions are false, we take a snapshot of the screen, log 
            # the error message, and set the score to "during tearDown()".
            print('Failed.')
            tunnels = self.api_session.get('https://crossbrowsertesting.com/api/v3/tunnels?num=10&active=true').json()
            tunnel = tunnels[0].tunnel_id
            #kill tunnel
            self.api_session.delete('https://crossbrowsertesting.com/api/v3/tunnels/' + tunnel)
            snapshot_hash = self.api_session.post('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id + '/snapshots').json()['hash']
            self.api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id + '/snapshots/' + snapshot_hash,
                data={'description':"AssertionError: " + str(e)})
            self.test_result = 'fail'
            raise

    def tearDown(self):
        print("Done with session %s" % self.driver.session_id)
        self.driver.quit()
        # Here we make the api call to set the test's score.
        # Pass it it passes, fail if an assertion fails, unset if the test didn't finish
        if self.test_result is not None:
            self.api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + self.driver.session_id, 
                data={'action':'set_score', 'score':self.test_result})


if __name__ == '__main__':
    unittest.main()
