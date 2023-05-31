*** Settings ***
Library    test_code.Imperium
Library     test_code.auditlog.AuditQuerySearch  WITH NAME  auditlog
#Library    test_code.RobotEyes
#Library    test_code.Environment
Documentation   Utilities_Keywords
Library         SeleniumLibrary
Resource       ../Obj_Repo/Global_variables.robot

*** Variables ***
${URL}      https://google.com
${TITLE}    Google
${BROWSER}  Chrome

*** Keywords ***

Simple Search
	[Arguments]		${SearchWord}
	auditlog.Demo    name:q      ${SearchWord}
	#Input Text    name:q    ${SearchWord}
	Press Keys    name:q    ENTER

Go to Google
	#Start Service In Docker  ${BROWSER}
#	Open Browser    ${BROWSER}
#
#	Open Browser     ${URL}   ${BROWSER}
    Open Link  ${URL}  ${TITLE}  in_docker=${False}
	Maximize Browser Window
	Sleep    5s