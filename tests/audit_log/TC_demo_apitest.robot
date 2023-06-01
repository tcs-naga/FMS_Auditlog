*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${BASE_URL}  https://reqres.in/api/users

#${REL_URL)
${VALUE}   ?id=2

*** Test Cases ***
##########  Get

Verify Given API
    Create Session    apisession    ${BASE_URL}
    ${response}=    Get Request     apisession  ${BASE_URL} ${VALUE}
    Log To Console    ${response}
    Log To Console    ${response.status_code}
    Log To Console    ${response.content}
    Log To Console    ${response.headers}

Verify Given API Status Code

    Create Session    apisession    ${BASE_URL}
    ${response}=    Get Request     apisession  ${BASE_URL} ${VALUE}
    Log To Console    ${response.status_code}
    ${STATUS_CODE}=  Convert To String  ${response.status_code}
    Should Be Equal    ${STATUS_CODE}   200

Verify Given API In Content

     Create Session    apisession    ${BASE_URL}
    ${response}=    Get Request     apisession  ${BASE_URL} ${VALUE}
    ${CONTENT_RESULT}=  Convert To String    ${response.content}
    Should Contain    ${CONTENT_RESULT}     2

Verify Header Values From Given API In Content

     Create Session    apisession    ${BASE_URL}
    ${response}=    Get Request     apisession  ${BASE_URL} ${VALUE}
    ${content_type_value}=  Get From Dictionary     ${response.headers}     Content-Type
    Should Be Equal    ${content_type_value}    application/json; charset=utf-8

##########  POST

Verify API In Post Method
     Create Session    apisession    ${BASE_URL}
     ${BODY}=   Create Dictionary    name= morpheus   job=leader
     ${HEADER}=   Create Dictionary    Content-Type=application/json
     ${Post_Response}=  Post Request    apisession       ${BASE_URL}      data=${BODY}        headers=${HEADER}

     Log To Console    ${Post_Response.status_code}



