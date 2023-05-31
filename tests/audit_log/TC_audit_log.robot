*** Settings ***
Documentation   test
Library    SeleniumLibrary
Library     test_code.auditlog.AuditQuerySearch  WITHNAME  auditlog
Library    Collections
Resource    ./resources/Utilities_Keywords.robot
Force Tags  FMS_Regression

Test Setup			Go to Google
#Suite Setup        XXXXXX
Suite Teardown		Close All Browsers

*** Variables ***

*** Test Cases ***
# TC_Id_Titel
TC_001_Verify_all_elements_in Audit Query Search
    [Tags]      Regression  test
    Verify Of All Elements In Audit Query Search

TC_002_Simple_example Search_in_Audit Query Search
    [Tags]      Regression  test
    Simple Search		FMG

*** Keywords ***

Verify Of All Elements In Audit Query Search

    auditlog.Verification Of All Elements In Audit Query Search