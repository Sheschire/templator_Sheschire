*** Settings ***
Documentation    The root initialization file.
Resource    index.robot
Suite Setup    Run Keywords    Init Google Services
...    AND    Run Keywords    Set JDD Global Variables

