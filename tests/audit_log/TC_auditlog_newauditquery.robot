*** Settings ***
Documentation   Test cases for audit query search screen
Library    SeleniumLibrary
Library         Collections
Library     test_code.auditlog.AuditQuerySearch  WITH NAME  auditlog
Resource    ./resources/Utilities_Keywords.robot
Resource    ./obj_repo/variables.robot
Force Tags  FMS_Regression
#Test Setup			Open Browser And Launch AuditLog Application
Test Teardown       Close All Browsers
#Suite Setup        XXXXXX
#Suite Teardown		Close All Browsers

*** Variables ***

*** Test Cases ***
# TC_Id_Titel

TC_001_Verify_all_elements_in Audit Query Search
    [Tags]      Regression  test
    Verify Of All Elements In Audit Query Search

TC_002_Verify_Query_Search_With_Date
    [Tags]      Regression  test
    Query Search With Date      ${YEAR}     ${MONTH}    ${DATE}

TC_003_Verify_Query_Search_With_User
    [Tags]      Regression  test

    Query Serach With User  ${USER}


TC_004_Verify_Query_Search_With_Multiple_User
    [Tags]      Regression  test

    Query Serach With Multiple User  #${USER}

TC_005_Verify_Query_Search_With_Event
    [Tags]      Regression  test

  Query Serach With Event Or Activity  #${EVENT}

TC_006_Verify_Query_Search_With_Multiple_Event
    [Tags]      Regression  test

  Query Serach With Multiple Event Or Activity  #${EVENT}


TC_007_Verify_Query_Search_With_Entity
    [Tags]      Regression  test

    Query Search With Entity Or Asset   #${ENTITY}


TC_008_Verify_Query_Search_With_Multiple_Entity
    [Tags]      Regression  test

    Query Search With Multiple Entity Or Asset   #${ENTITY}

    Query Search With All Fields     ${EVENT}   ${ENTITY}   ${USER}

TC_009_Verify_Query_Search_In_All_Fields_With_Multi_Options
    [Tags]      Regression  test
    Query Search In All Fields With Multi Options

TC_010_Verify_Query_Search_In_All_Fields_With_Single_Options
    [Tags]      Regression  test
    Query Search In All Fields With Single Options


*** Keywords ***

Verify Of All Elements In Audit Query Search

    Open Browser And Launch AuditLog Application
    auditlog.Verification Of All Elements In Audit Query Search

Query Serach With User
    [Arguments]  ${USER}
    Open Browser And Launch AuditLog Application With Date Search
    ${User_Results}=  auditlog.Query Search With User     ${USER}
    Should Be Equal       ${User_Results}   PASS

Query Serach With Multiple User
    #[Arguments]  ${USER}    ${USER-1}
    Open Browser And Launch AuditLog Application With Date Search
    ${User_Results}=  auditlog.Query Search With User     ${USER}     ${USER-1}
    Should Be Equal       ${User_Results}   PASS


Query Serach With Event Or Activity
      #[Arguments]  ${EVENT}
      Open Browser And Launch AuditLog Application With Date Search
      ${Event_Results}=    auditlog.Query Search With Event Or Activity    ${EVENT}
      Log To Console    ${Event_Results}
      Should Be Equal    ${Event_Results}   PASS

Query Serach With Multiple Event Or Activity
      Open Browser And Launch AuditLog Application With Date Search
      ${Event_Results}=    auditlog.Query Search With Event Or Activity    ${EVENT}     ${EVENT-1}
      Log To Console    ${Event_Results}
      Should Be Equal    ${Event_Results}   PASS

Query Search With Entity Or Asset
    #[Arguments]  ${ENTITY}
    Open Browser And Launch AuditLog Application With Date Search
    ${Entity_Results}=    auditlog.Query Search With Entity Or Asset  ${ENTITY}
    Log To Console    ${Entity_Results}
    Should Be Equal     ${Entity_Results}   PASS


Query Search With Multiple Entity Or Asset
    #[Arguments]  ${ENTITY}      ${ENTITY-1}
    Open Browser And Launch AuditLog Application With Date Search
    ${Entity_Results}=    auditlog.Query Search With Entity Or Asset  ${ENTITY}     ${ENTITY-1}
    Log To Console    ${Entity_Results}
    Should Be Equal     ${Entity_Results}   PASS


Query Search With Date
    [Arguments]     ${YEAR}     ${MONTH}    ${DATE}
    Open Browser And Launch AuditLog Application
    ${Date_Results}   auditlog.Query Search With Date     ${YEAR}     ${MONTH}    ${DATE}
    Log To Console   ${Date_Results}
    Should Be Equal    ${Date_Results}[1][records_count_app]    ${Date_Results}[1][records_count_export]


Query Search In All Fields With Multi Options
    Open Browser And Launch AuditLog Application With Date Search
   Query Search On Multi Category With Multi Options From Query Search Screen

Query Search In All Fields With Single Options
    Open Browser And Launch AuditLog Application With Date Search
    Query Search On Multi Category With Single Options From Query Search Screen