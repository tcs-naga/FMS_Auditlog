*** Settings ***
Documentation   test_db
Library    SeleniumLibrary
Library     test_code.Imperium
Library     test_code.database.FmsDatabase  WITH NAME  dbtest
Library    Collections
Force Tags  FMS_Regression
Resource    ./obj_repo/variables.robot
#Suite Setup        XXXXXX
#Suite Teardown		XXXXXX

*** Variables ***

*** Test Cases ***
# TC_Id_Titel
TC_001_Verify Given FID In DB
   # Start Service In Docker     sqlserver
    ${result}=   dbtest.Search And Validate Fid In DB   ${FID}
    ${result}       Convert To String   ${result}[0]
    Should Be Equal        ${result}     ${FID}

TC_002_Verify In DB Craeted Event From API Is Present or Not
   # Start Service In Docker     sqlserver
    ${result}=   dbtest.Search And Validate Event In DB   ${OBJECT_ID}
     Should Contain          ${result}[0]    ${object}

TC_003_Verify In DB Craeted Entity From API Is Present or Not
   # Start Service In Docker     sqlserver
    ${result}=   dbtest.Search And Validate Entity In DB   ${OBJECT_ID}
     Should Contain          ${result}[0]    ${api_entity}

TC_004_Verify In DB Craeted Users From API Is Present or Not
   # Start Service In Docker     sqlserver
    ${result}=   dbtest.Search And Validate User In DB   ${OBJECT_ID}
    Should Contain        ${result}    ${changedByID}

TC_005_Verify In DB Craeted Action From API Is Present or Not
   # Start Service In Docker     sqlserver
    ${result}=   dbtest.Search And Validate Action In DB   ${OBJECT_ID}     ${ACTION}
     Should Be Equal         ${result}     PASS

TC_006_Verify In DB Craeted Exception From API Is Present or Not
   # Start Service In Docker     sqlserver
    ${result}=   dbtest.Search And Validate Exception Log In DB   ${dateTimeUTC}
    Should Be Equal         ${result}[0]    ${userName}
    Should Be Equal     ${result}[1]   ${exceptionDetails}





