# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.ant -t test_ant_base.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.ant.testing.COLLECTIVE_ANT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/ant/tests/robot/test_ant_base.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a ant_base
  Given a logged-in site administrator
    and an add  form
   When I type 'My ant_base' into the title field
    and I submit the form
   Then a ant_base with the title 'My ant_base' has been created

Scenario: As a site administrator I can view a ant_base
  Given a logged-in site administrator
    and a ant_base 'My ant_base'
   When I go to the ant_base view
   Then I can see the ant_base title 'My ant_base'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add  form
  Go To  ${PLONE_URL}/++add++

a ant_base 'My ant_base'
  Create content  type=  id=my-ant_base  title=My ant_base

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the ant_base view
  Go To  ${PLONE_URL}/my-ant_base
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a ant_base with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the ant_base title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
