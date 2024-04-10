*** Settings ***
Documentation    The root initialization file.
Resource    ../../src/u_iris/templator/rf-resources/index.resource


*** Variables ***
# robocop: disable=5101-IRIS-NAMING
${HTTP_PROXY}    %{HTTP_PROXY=}
${HTTPS_PROXY}    %{HTTPS_PROXY=}
${NO_PROXY}    %{RF_NO_PROXY}
# robocop: enable=5101-IRIS-NAMING
${SHEET_ID}    
${GOOGLE_ACCOUNT}    %{RF_GOOGLE_ACCOUNT}
${DEV_MODE_ENABLED}    %{RF_DEV_MODE_ENABLED=false}



*** Keywords ***
# robocop: disable=5100-IRIS-NAMING
# robocop: disable=0310
Set JDD Global Variables
    [Documentation]    Ce mot clé permet de récupérer un JJD depuis Google Seeet
    ${config}    JDD.Recuperation JDD    Config
    @{list}    String.Split String    ${config.activeTabs}    separator=,
    FOR    ${i}    IN    @{list}
        ${i}    String.Remove String Using Regexp    ${i}    ^\ |\ $
        ${temp}    JDD.Recuperation JDD    ${i}
        BuiltIn.Set Global Variable    ${${i}}    ${temp}
    END


