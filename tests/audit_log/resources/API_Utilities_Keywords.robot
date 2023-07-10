*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Keywords ***
#
#Validate Get Status Code for Given API
#       [Arguments]		${URL}
#       Create Session    apisession     ${URL}
#       ${response}=    Get Request     apisession  ${URL}
#       ${STATUS_CODE}=  Convert To String  ${response.status_code}
#       Should Be Equal    ${STATUS_CODE}   200
#
#Validate Content Values In Given API
#        [Arguments]		${URL}  ${Value}
#        Create Session    apisession    ${URL}
#        ${response}=    Get Request     apisession  ${URL}
#        ${CONTENT_RESULT}=  Convert To String    ${response.content}
#        Should Contain    ${CONTENT_RESULT}     ${Value}
#
Verify Header Values From Given API In Content

     [Arguments]		${URL}  ${Key}  ${Value}
     Create Session    apisession    ${URL}
     ${response}=    Get Request     apisession  ${URL}
     ${content_type_value}=  Get From Dictionary     ${response.headers}     ${Key}
     Should Be Equal    ${content_type_value}    ${Value}