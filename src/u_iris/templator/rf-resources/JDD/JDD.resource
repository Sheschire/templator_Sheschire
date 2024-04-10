*** Settings ***
Documentation    Keywords utilities.
Resource    ../index.resource


*** Keywords ***
Init Google Services
    [Documentation]    Initialisation Google Services
    OperatingSystem.Create File    ${TEMPDIR}/google_account.json    ${GOOGLE_ACCOUNT}
    RPA.Cloud.Google.Init Sheets    ${TEMPDIR}/google_account.json

Recuperation JDD
    [Documentation]    Ce mot clé permet de récupérer un JJD depuis Google Seeet
    [Arguments]    ${feuille}
    ${spreadsheet_content}    RPA.Cloud.Google.Get Sheet Values
    ...    ${SHEET_ID}
    ...    ${feuille}!A1:Z10000
    ${alldatavalues}    Builtin.Set Variable    ${spreadsheet_content['values']}
    ${data}    BuiltIn.Create Dictionary
    ${length}    BuiltIn.Get Length    ${alldatavalues}
    FOR    ${i}    IN RANGE    ${length}
        TRY
            Collections.Set To Dictionary    ${data}    ${alldatavalues}[${i}][0]    ${alldatavalues}[${i}][1]
        EXCEPT    List *    type=glob
            Collections.Set To Dictionary    ${data}    ${alldatavalues}[${i}][0]    ${EMPTY}
        END
    END
    RETURN    ${data}
