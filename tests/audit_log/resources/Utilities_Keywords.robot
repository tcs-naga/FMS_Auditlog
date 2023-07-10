*** Settings ***
Library    test_code.Imperium
Library     test_code.auditlog.AuditQuerySearch  WITH NAME  auditlog
#Library    test_code.RobotEyes
#Library    test_code.Environment
Documentation   Utilities_Keywords
Library         SeleniumLibrary
Resource       ../Obj_Repo/Global_variables.robot

*** Variables ***
${URL}      http://localhost:3000/
${TITLE}    Audit Record
${BROWSER}  Chrome

*** Keywords ***

#Simple Search
#	[Arguments]		${SearchWord}
#	auditlog.Demo    name:q      ${SearchWord}
#	#Input Text    name:q    ${SearchWord}
#	Press Keys    name:q    ENTER

Open Browser And Launch AuditLog Application
	#Start Service In Docker  ${BROWSER}
#	Open Browser    ${BROWSER}
#
#	Open Browser     ${URL}   ${BROWSER}
    Open Link  ${URL}  ${TITLE}  in_docker=${False}
	Maximize Browser Window
	Sleep    5s

Open Browser And Launch AuditLog Application With Date Search
	#Start Service In Docker  ${BROWSER}
#	Open Browser    ${BROWSER}
#
#	Open Browser     ${URL}   ${BROWSER}

    Open Link  ${URL}  ${TITLE}  in_docker=${False}
	Maximize Browser Window
	Sleep    5s
	auditlog.Search With Date     ${YEAR}     ${MONTH}    ${DATE}
	Sleep    4s

Submit Query Button
    auditlog.Submit Start Query Btn

Query Search On Multi Category With Multi Options From Query Search Screen
    auditlog.Select Event Or Activity With Values     ${EVENT}          ${EVENT-1}
    auditlog.Select Entity Or Asset With Values       ${ENTITY}       ${ENTITY-1}
    auditlog.Select User With Values              ${USER}         ${USER-1}
    ${Results}      auditlog.Query Search With All Fields In Multi Values   ${EVENT}    ${EVENT-1}     ${ENTITY}    ${ENTITY-1}     ${USER-1}    ${USER}
    Log To Console  ${Results}
    Should Be Equal   ${Results}    PASS

Query Search On Multi Category With Single Options From Query Search Screen
    auditlog.Select Event Or Activity With Values     ${EVENT}
    auditlog.Select Entity Or Asset With Values       ${ENTITY}
    auditlog.Select User With Values             ${USER}
    ${Results}      auditlog.Query Search With All Fields In Multi Values   ${EVENT}         ${ENTITY}           ${USER}
    Log To Console  ${Results}
    Should Be Equal   ${Results}    PASS