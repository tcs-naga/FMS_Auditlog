*** Settings ***
Library     test_code.auditlog.AuditAPI  WITH NAME  auditlogapi
Library    RequestsLibrary
Library    Collections
Library    json
Resource    ./obj_repo/variables.robot
Library    DateTime
#Library     DataDriver    file=test_data/file_upload/Testdata.xlsx     sheet_name =audit_api
*** Variables ***

*** Test Cases ***

#CreateAudit API__________________________________________________________________________________________________________________
TC_001_Verify CreateAudit API In Post Method
    [Tags]      Regression  test
    Execute Create Audit Post Method


TC_002_Verify Audit API Get Status Code
    [Tags]      Regression  test
    Validate Audit API Get Status Code

TC_003_Verify Audit API Content With Given Value
    [Tags]      Regression  test
    Validate Get API Content With Given Value

TC_004_Verify Header Values From Content In Audit API
    [Tags]      Regression  test
    Validate Header Values From Get API In Content

TC_005_Verify Create Audit API In Update Patch Method
    [Tags]      Regression  test
    Execute Update Audit Patch Method

TC_006_Verify Create Audit API In Delte Method
    [Tags]      Regression  test

    Execute Delete Audit Del Method

TC_007_Verify Create Audit API In Archive Patch Method
    [Tags]      Regression  test
    Execute Create Audit Archive Patch API Method

TC_008_Verify Create Audit API In UnArchive Patch Method
    [Tags]      Regression  test
    Execute Create Audit UnArchive Patch API Method

#AuditRecordDetails API_______________________________________________________________

TC_009_Verify AuditRecordDetails API In Post Method
    [Tags]      Regression  test
    Execute AuditRecordDetails Post Method

TC_010_Verify AuditRecordDetails API Get Status Code
     [Tags]      Regression  test
    Validate Given Audit Record Details Url Api Get Status Code

#ExceptionLogger----------------------------------------------------------------------
TC_011_Verify ExceptionLogger API Post Method
    [Tags]      Regression  test
    Execute ExceptionLogger Audit Post Method

#UserActivityDetails----------------------------------------------------------------------
TC_012_Verify UserActivityDetails API Get Method
    [Tags]      Regression  test
    Validate Given User Activity Details Api Get Status Code

#UserDetails----------------------------------------------------------------------
TC_013_Verify UserDetails API Get Method
    [Tags]      Regression  test
    Validate Get Status Code For User Details With Headers Api

*** Keywords ***
#POST
Execute Create Audit Post Method

      ${RequestBody}=   Create Dictionary   assignment_Event=${assignment_Event}       material= ${material}       eventName=${eventName}      source=${source}
      ${BODY}=   Create Dictionary   objectid=${OBJECT_ID}   changedByType=${changedByType}   object=${object}  entity=${api_entity}  changedByID=${changedByID}    requestBody=${RequestBody}       requestURL=${requestURL}
      Sleep    3
      ${req_json}    Json.Dumps     ${BODY}
      Sleep    3
      ${result}=    auditlogapi.Post API Method    ${CREATE_AUDIT_POST_URL}    ${req_json}
      Sleep    3
      Should Be Equal    ${result}[status_code]     201

Execute AuditRecordDetails Post Method
      ${result}=    auditlogapi.Audit Record Post API Method    ${AUDIT_RECORD_DETAILS_URL}
      Sleep    3
      Should Be Equal    ${result}[status_code]     200

Execute ExceptionLogger Audit Post Method
     ${BODY}=   Create Dictionary   objectid=${OBJECT_ID}   dateTimeUTC=${dateTimeUTC}   userName=${userName}  exceptionChannel=${exceptionChannel}  exceptionDetails=${exceptionDetails}
      Sleep   5
      ${req_json}    Json.Dumps     ${BODY}
      Sleep    5
      ${result}=    auditlogapi.Post API Method    ${EXCEPTION_LOGGER_AUDIT_URL}    ${req_json}
      Sleep    5
      Should Be Equal    ${result}[status_code]     200

#PATCH

Execute Update Audit Patch Method

      ${RequestBody_U}=   Create Dictionary   assignment_Event=${assignment_Event_u}       material= ${material_u}       eventName=${eventName_u}      source=${source_u}
      ${BODY}=   Create Dictionary   objectid=${OBJECT_ID}   changedByType=${changedByType_u}   object=${object_u}  entity=${api_entity_u}  changedByID=${changedByID_u}    requestBody=${RequestBody_U}       requestURL=${requestURL_u}
      Sleep    3
      ${req_json}    Json.Dumps     ${BODY}
      Sleep    3
      ${result}=    auditlogapi.Patch API Method    ${UPDATE_AUDIT_POST_URL}    ${req_json}
      Sleep    3
      Should Be Equal    ${result}[status_code]     200

Execute Create Audit Archive Patch API Method
      ${RequestBody}=   Create Dictionary   assignment_Event=${assignment_Event}       material= ${material}       eventName=${eventName}      source=${source}
      ${BODY}=   Create Dictionary   objectid=${OBJECT_ID}   changedByType=${changedByType}   object=${object}  entity=${api_entity}  changedByID=${changedByID}    requestBody=${RequestBody}       requestURL=${requestURL}
      Sleep    3
      ${req_json}    Json.Dumps     ${BODY}
      Sleep    3
      ${result}=    auditlogapi.Patch API Method    ${ARCHIVE_AUDIT_URL}    ${req_json}
      Sleep    3
      Should Be Equal    ${result}[status_code]     200

Execute Create Audit UnArchive Patch API Method
      ${RequestBody}=   Create Dictionary   assignment_Event=${assignment_Event}       material= ${material}       eventName=${eventName}      source=${source}
      ${BODY}=   Create Dictionary   objectid=${OBJECT_ID}   changedByType=${changedByType}   object=${object}  entity=${api_entity}  changedByID=${changedByID}    requestBody=${RequestBody}       requestURL=${requestURL}
      Sleep    5
      ${req_json}    Json.Dumps     ${BODY}
      Sleep    5
      ${result}=    auditlogapi.Patch API Method    ${UNARCHIVE_AUDIT_URL}    ${req_json}
      Sleep    5
      Should Be Equal    ${result}[status_code]     200

#DEL
Execute Delete Audit Del Method
      ${RequestBody}=   Create Dictionary   assignment_Event=${assignment_Event}       material= ${material}       eventName=${eventName}      source=${source}
      ${BODY}=   Create Dictionary   objectid=${OBJECT_ID}   changedByType=${changedByType}   object=${object}  entity=${api_entity}  changedByID=${changedByID}    requestBody=${RequestBody}       requestURL=${requestURL}
      Sleep    5
      ${req_json}    Json.Dumps     ${BODY}
      Sleep    5
      ${result}=    auditlogapi.Delete API Method    ${DELETE_AUDIT_URL}     data=${req_json}
      Sleep    5
      Should Be Equal    ${result}[status_code]     200

#GET
Validate Audit API Get Status Code
    ${result}=    auditlogapi.Get API Method   ${AUDIT_GET_URL}

    Should Be Equal    ${result}[status_code]     200

Validate Get API Content With Given Value
    Create Session    apisession    ${AUDIT_GET_URL}
    ${response}=    Get Request     apisession  ${AUDIT_GET_URL}
    Sleep    1
    ${CONTENT_RESULT}=  Convert To String    ${response.content}
    Sleep    2
    Should Contain    ${CONTENT_RESULT}     ${VALUE}

Validate Header Values From Get API In Content

    Create Session    apisession    ${AUDIT_GET_URL}
    ${response}=    Get Request     apisession   ${AUDIT_GET_URL}
    ${content_type_value}=  Get From Dictionary     ${response.headers}     ${CONTENT_KEY}
    Should Be Equal    ${content_type_value}   ${CONTENT_VALUE}

Validate Given Audit Record Details Url Api Get Status Code
    ${result}=    auditlogapi.Audit Record Get API Method       ${AUDIT_RECORD_DETAILS_GET_URL}
    Should Be Equal    ${result}[status_code]     200

Validate Given User Activity Details Api Get Status Code
    ${result}=    auditlogapi.Audit Record Get API Method       ${USER_ACTIVITY_DETAILS_GET_URL}
    Should Be Equal    ${result}[status_code]     200

Validate Get Status Code For User Details With Headers Api
    ${result}=    auditlogapi.Get API Method With User Details Headers      ${USER_DETAILS_GET_URL}
    Should Be Equal    ${result}[status_code]     200
