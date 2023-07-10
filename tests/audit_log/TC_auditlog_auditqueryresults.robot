*** Settings ***
Documentation   test
Library    SeleniumLibrary
Library     test_code.auditlog.AuditResults  WITH NAME  auditlogresult
Library     test_code.auditlog.AuditQuerySearch  WITH NAME  auditlogsearch
Library    Collections
Resource    ./resources/Utilities_Keywords.robot
Resource    ./obj_repo/variables.robot
Force Tags  FMS_Regression
#Test Setup			Launch Auditlog With Query Search On Date
#Suite Setup        XXXXXX
#Suite Teardown		Close All Browsers

*** Variables ***
${FID}  1
${IFID}     000

*** Test Cases ***
#TC_Id_TitelXXXXXXXXXXXXXXXX
TC_001_Verify_all_elements_in Audit Query Results Screen
    [Tags]      Regression  test
    Verify Of All Elements In Audit Query Results Screen

TC_002_Verify Circuit Created Value ID With Searched ID
    [Tags]      Regression  test
    Verify Id In Circuit Created Field With Searched ID  ${FID}

TC_003_Verify_Export Records With Tabel Results Records Count
    [Tags]      Regression  test
    Verify Export Records With Tabel Results Records

TC_004_Verify_Result_Records_With_Given_Search_Id
    [Tags]      Regression  test
    Verify Result Records With Given Search Id   ${FID}

TC_005_Verify_Result_Records_With_InValid_Search_Id
    [Tags]      Regression  test
   Verify No Records Found Msg When User Pass Invalid Input     ${IFID}

TC_006_Verify_Single_Value_Event_Type_Search_Fuctionality
    [Tags]      Regression  test
   Validate Filtered Event Type Records With Single Input Values

TC_007_Verify_Single_Value_Entity_Search_Fuctionality
    [Tags]      Regression  test
   Validate Filtered Entity Records With Single Input Values

TC_008_Verify_Single_Value_User_Search_Fuctionality
    [Tags]      Regression  test
   Validate Filtered User Records With Single Input Values

TC_009_Verify_Single_Value_Action_Search_Fuctionality
    [Tags]      Regression  test
   Validate Filtered Action Records With Single Input Values


TC_010_Verify_Multi_Value_Event_Type_Search_Fuctionality
    [Tags]      Regression  test
   Validate Filtered Event Type Records With Multiple Input Values

TC_011_Verify_Multi_Value_Entity_Search_Fuctionality
    [Tags]      Regression  test
  Validate Filtered Entity Records With Multiple Input Values

TC_012_Verify_Multi_Value_User_Search_Fuctionality
    [Tags]      Regression  test
   Validate Filtered User Records With Multiple Input Values

TC_013_Verify_Multi_Value_Action_Search_Fuctionality
    [Tags]      Regression  test
   Validate Filtered Action Records With Multiple Input Values

TC_014_Verify_Single_Value_In_All_Type_Search_Fuctionality
    [Tags]      Regression  test
   Validate Filtered All Types Records With Single Input Values


TC_015_Verify_Multi_Value_In_All_Type_Search_Fuctionality
    [Tags]      Regression  test
   Validate Filtered All Types Records With Multiple Input Values

TC_016_Verify_New Query_Back_Fuctionality
    [Tags]      Regression  test
   Validate NewQuery Back Button From Audit Result Screen


TC_017_Verify_Sorting_Fuctionality_Query_Result_Screen
    [Tags]      Regression  test
    Validate Sorting Functionality

TC_018_Verify_Pagination_Fuctionality_Query_Result_Screen
    [Tags]      Regression  test
    Validate Pagenation Functionality in Audit Result Screen


*** Keywords ***
Verify Of All Elements In Audit Query Results Screen
   Open Browser And Launch AuditLog Application With Date Search
    Submit Query Button
    auditlogresult.Verification Of All Elements In Audit Results Screen

Verify Id In Circuit Created Field With Searched ID
    [Arguments]   ${FID}
    Open Browser And Launch AuditLog Application With Date Search
    Submit Query Button
    ${IDCheck}=    auditlogresult.Validate FID In Circuit Created Field     ${FID}
     Should Be Equal    Id is matched with CCV  ${IDCheck}

Verify Export Records With Tabel Results Records
        Open Browser And Launch AuditLog Application With Date Search
        Submit Query Button
       ${Check}=  auditlogresult.Validate Export Records With Tabel Results
        Should Be Equal    records count is matched  ${Check}

Verify Result Records With Given Search Id
      [Arguments]   ${FID}
     Open Browser And Launch AuditLog Application With Date Search
     Submit Query Button
     ${IDCheck}=     auditlogresult.Validate Records With Search FID    ${FID}
     Should Be Equal    Id is matched with results & CCV & tabel count is match with export count  ${IDCheck}

Verify No Records Found Msg When User Pass Invalid Input
        [Arguments]    ${IFID}
        Open Browser And Launch AuditLog Application With Date Search
        Submit Query Button
        ${Check}=   auditlogresult.Validate No Records When Search With Invalid FID  ${IFID}
        Should Be Equal     no records found    ${Check}

Validate Filtered Event Type Records With Single Input Values
        Open Browser And Launch AuditLog Application With Date Search
        Submit Query Button
        ${Results}=     auditlogresult.Validate Event Type With Search Function      ${EVENT}
        Log To Console  ${Results}
        Should Be Equal    ${Results}   PASS

Validate Filtered Entity Records With Single Input Values
        Open Browser And Launch AuditLog Application With Date Search
        Submit Query Button
        ${Results}=     auditlogresult.Validate Entity With Search Function      ${ENTITY}
        Log To Console  ${Results}
        Should Be Equal    ${Results}   PASS

Validate Filtered User Records With Single Input Values
        Open Browser And Launch AuditLog Application With Date Search
        Submit Query Button
        ${Results}=     auditlogresult.Validate User With Search Function      ${USER}
        Log To Console  ${Results}
        Should Be Equal    ${Results}   PASS

Validate Filtered Action Records With Single Input Values
        Open Browser And Launch AuditLog Application With Date Search
        Submit Query Button
        ${Results}=     auditlogresult.Validate Action With Search Function      ${ACTION}
        Log To Console  ${Results}
        Should Be Equal    ${Results}   PASS

Validate Filtered Event Type Records With Multiple Input Values
        Open Browser And Launch AuditLog Application With Date Search
        Submit Query Button
        ${Results}=     auditlogresult.Validate Event Type With Search Function      ${EVENT}       ${EVENT-1}
        Log To Console  ${Results}
        Should Be Equal    ${Results}   PASS

Validate Filtered Entity Records With Multiple Input Values
        Open Browser And Launch AuditLog Application With Date Search
        Submit Query Button
        ${Results}=     auditlogresult.Validate Entity With Search Function     ${ENTITY}   ${ENTITY-1}
        Log To Console  ${Results}
        Should Be Equal    ${Results}   PASS

Validate Filtered User Records With Multiple Input Values
        Open Browser And Launch AuditLog Application With Date Search
        Submit Query Button
        ${Results}=     auditlogresult.Validate User With Search Function      ${USER}      ${USER-1}
        Log To Console  ${Results}
        Should Be Equal    ${Results}   PASS

Validate Filtered Action Records With Multiple Input Values
        Open Browser And Launch AuditLog Application With Date Search
        Submit Query Button
        ${Results}=     auditlogresult.Validate Action With Search Function      ${ACTION}      ${ACTION-1}
        Log To Console  ${Results}
        Should Be Equal    ${Results}   PASS

Validate Filtered All Types Records With Single Input Values
# Types Values should give in order like (event, entity,user,action)
    Open Browser And Launch AuditLog Application With Date Search
        Submit Query Button
        ${Results}=     auditlogresult.Validate All Types With Search Function    ${EVENT}        ${ENTITY}        ${USER}          ${ACTION}
        Log To Console  ${Results}
        Should Be Equal    ${Results}   PASS

Validate Filtered All Types Records With Multiple Input Values
# Types Values should give in order like (event, entity,user,action)
    Open Browser And Launch AuditLog Application With Date Search
        Submit Query Button
        ${Results}=     auditlogresult.Validate All Types With Search Function    ${EVENT}       ${EVENT-1}       ${ENTITY}     ${ENTITY-1}     ${USER}      ${USER-1}      ${ACTION}      ${ACTION-1}
         #Deepanshu
        Log To Console  ${Results}
        Should Be Equal    ${Results}   PASS

Validate NewQuery Back Button From Audit Result Screen
     Open Browser And Launch AuditLog Application With Date Search
     Submit Query Button
     auditlogresult.Validate New Query Btn Functionality

Validate Sorting Functionality
     Open Browser And Launch AuditLog Application With Date Search
     Submit Query Button
     ${Result}      auditlogresult.Validate Sorting Functionality
     Should Be Equal    ${Result}    PASS


Validate Pagenation Functionality in Audit Result Screen
     Open Browser And Launch AuditLog Application With Date Search
     Submit Query Button
     ${Result}      auditlogresult.Validate Pagination Functionality
     Should Be Equal    ${Result}    PASS





