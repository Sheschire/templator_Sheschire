#!groovy
@Library('gie@develop') _

continuousIntegration(
    builder: 'poetry',
    deployer: 'docker',
    nodeSelection: 'docker-v2',
    skipUnitTests: false,
    skipScmRelease: true,
    applicationName: 'robotframework-templator',
    additionalCredentials: [
        [
            type: 'file',
            id: 'robotframework-secret',
            withEnv: false,
            variable: 'SECRET_PATH',
        ],
    ],
)
