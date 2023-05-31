*** Settings ***
Library    test_code.Imperium
Library    test_code.RobotEyes
Library    test_code.Environment
Library    SeleniumLibrary
Library    Collections

Force Tags  regression

Test Setup			Go to G
Suite Teardown		Close All Browsers

*** Variables ***
${URL}    https://google.com
${TITLE}  Google
#${BROWSER}      Chrome
*** Test Cases ***

Simple example Search
    Simple Search		Rajesh


*** Keywords ***
Simple Search
	[Arguments]		${SearchWord}
	Input Text    name:q    ${SearchWord}
	Press Keys    name:q    ENTER

Go to G
	Start Service In Docker  ${BROWSER}
    Open Link  ${URL}  ${TITLE}  in_docker=${TRUE}
	Maximize Browser Window
	Sleep    5s

