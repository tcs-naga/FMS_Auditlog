*** Settings ***
#Library         ../test_data/file_upload/FMS/test_data.py
*** Variables ***
${URL}          https://www.fmgl.com.au/
${BROWSER}  Chrome
# ------------->TC_auditlog_newauditquery.robot
${YEAR}     2023
${MONTH}    July
${DATE}     5
${EVENT}    AUT_TEST_EVENT_1
${ENTITY}   AUT_TEST_ENTITY_1
${USER}     AUT_TEST_USER_1
${ACTION}   Insert

${EVENT-1}      AUT_TEST_EVENT_1_U
${ENTITY-1}     AUT_TEST_ENTITY_1_U
${USER-1}      AUT_TEST_USER_1_U
${ACTION-1}   Update

# ------------->TC_auditlog_auditqueryresults.robot
${IFID}     0000
${FID}      1

#######################>>> API Varaiable <<<#####################################
${BASE_URL}     http://localhost:5000
${OBJECT_ID}    9BD037FC-8EC3-4EEB-9C99-5F8001049EED
${VALUE}   AUT_TEST_USER_1
${CONTENT_KEY}      Server
${CONTENT_VALUE}     Kestrel

#--------AUDIT----------------------------
${AUDIT_GET_URL}       ${BASE_URL}/Audit

#--------AUDIT_RECORD_DETAILS----------------------------
#POST
${AUDIT_RECORD_DETAILS_URL}    ${BASE_URL}/AuditRecordDetails
${pageNumber}   0
${pageSize}     0
${utcStartDateTime}	    2023-06-27T07:20:54.372Z
${utcEndDateTime}	    2023-06-27T07:20:54.372Z
${isExportToExcel}	    true
${sortColumn}		    string
${sortOrder}            string
@{actions} =           stringtest
@{auditRecordID} =            stringtest
@{actions} =            stringtest
@{users}=              stringtest
@{assets}=              stringtest
@{entity_}=             stringtest
${&}=   &


${AUDIT_RECORD_DETAILS_GET_URL}=     ${BASE_URL}/AuditRecordDetails?UtcStartDateTime=${utcStartDateTime}${&}UtcEndDateTime=${utcEndDateTime}${&}AuditRecordID=${auditRecordID}${&}Actions=${actions}${&}Users=${users}${&}Assets=${assets}${&}Entity=${entity_}${&}IsExportToExcel=${isExportToExcel}${&}SortColumn=${sortColumn}${&}SortOrder=${sortOrder}${&}PageNumber=${pageNumber}${&}PageSize=${pageSize}

#CreateAudit
#-------------CREATE_AUDIT--------------------------
${CREATE_AUDIT_POST_URL}    ${BASE_URL}/CreateAudit
@{auditRecordID}
${changedByType}	AUT_TEST_CI_1
${object}	        AUT_TEST_EVENT_1
${api_entity}	    AUT_TEST_ENTITY_1
${changedByID}	    AUT_TEST_USER_1
#
${assignment_Event}  AUT_TEST_Assignment_Event
${material}         AUT_TEST_Material
${eventName}        AUT_TEST_EventName
${source}           AUT_TEST_Source

${requestURL}       AUT_TEST_RU_1

#-------------Update_AUDIT--------------------------
${UPDATE_AUDIT_POST_URL}    ${CREATE_AUDIT_POST_URL}/update

${changedByType_u}	    AUT_TEST_CI_1_U
${object_u}	            AUT_TEST_EVENT_1_U
${api_entity_u}	        AUT_TEST_ENTITY_1_U
${changedByID_u}	    AUT_TEST_USER_1_U
${assignment_Event_u}  AUT_TEST_Assignment_Event_U
${material_u}         AUT_TEST_Material_U
${eventName_u}        AUT_TEST_EventName_U
${source_u}           AUT_TEST_Source_U

${requestURL_u}         AUT_TEST_RU_1_U

#____________________________________
${DELETE_AUDIT_URL}   ${BASE_URL}/CreateAudit/delete
#__________________________________________________
${ARCHIVE_AUDIT_URL}   ${BASE_URL}/CreateAudit/Archive
${UNARCHIVE_AUDIT_URL}  ${BASE_URL}/CreateAudit/UnArchive

#--ExceptionLogger
${EXCEPTION_LOGGER_AUDIT_URL}     ${BASE_URL}/ExceptionLogger
${dateTimeUTC}          2023-06-30T05:21:32.203Z
${userName}             AUT_TEST_XXXXX
${exceptionChannel}     AUT_TEST_EXPCHANNEL_THIS IS AUTOMATION INJECT EXCEPTION
${exceptionDetails}     AUT_TEST_EXPDETAILS_THIS IS AUTOMATION INJECT EXCEPTION

#--UserActivityDetails
#GET
${USER_ACTIVITY_DETAILS_GET_URL_VALUE}      2023-04-30T04%3A47%3A06.476Z
${USER_ACTIVITY_DETAILS_GET_URL}        ${BASE_URL}/UserActivityDetails?userActivitySearchCriteria=${USER_ACTIVITY_DETAILS_GET_URL_VALUE}

#--UserDetails
${USER_DETAILS_GET_URL}        ${BASE_URL}/UserDetails

