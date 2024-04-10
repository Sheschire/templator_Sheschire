#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @license UNLICENSED
# @copyright U IRIS. All rights reserved.
# @author Florian Daguin <florian.daguin@systeme-u.fr>

# @file PyInvoke tasks file.
# @see https://github.com/pyinvoke/invoke
# @see http://docs.pyinvoke.org/en/stable/getting-started.html?#defining-and-running-task-functions # noqa: E501

# flake8: noqa WPS202,WPS210,WPS226

"""PyInvoke tasks file."""

from invoke import task, Exit

from dotenv import load_dotenv


@task(iterable=['env_file'])
def load_env(context, env_file=None):
    """Load environment variables.

    Args:
        env_file (List[str]): The path to the .env file(s). Defaults to:
            - 'atest/env/default.env'
            - 'atest/env/default.secret.env'
    """
    if not env_file:
        paths = ['atest/env/default.env', 'atest/env/default.secret.env']
    else:
        paths = env_file
    for file in paths:
        load_dotenv(dotenv_path=file, override=False)

@task()
def create_report(context, input_path='out'):
    """Generate a Robot Framework report.
    
    Args:
        input_path (str): The input directory where the Robot Framework
            artifacts will be used to generate a report. Defaults to 'out'.
    """
    with context.cd(input_path):
        context.run(
            'robotmetrics --metrics-report-name robotmetrics.html',
        )

@task(iterable=['env_file', 'suite', 'test', 'exclude'])
def run(context,
    runner="robot",
    output_path='out',
    log_level="TRACE",
    test_path='atest/suites',
    env_file=None,
    test=None,
    suite=None,
    enable_reporting_tool=False,
    exclude=None
    ):
    """Launch Robot Framework test suite(s) or test case(s).

    Args:
        runner (str): The runner that will run the test suite(s). One of:
            - 'robot'
            - 'pabot'
            Defaults to 'robot'.
        output_path (str): The output directory where the results will be
            exported. Defaults to 'out'.
        log_level (str): Threshold level for logging. Available levels: TRACE,
            DEBUG, INFO, WARN, NONE (no logging). Defaults to 'TRACE'.
        test_path (str): The path to the test suite(s). Defaults to
            'atest/suites'.
        env_file (List[str]): The path to the .env file(s). Defaults to:
            - 'atest/env/default.env'
            - 'atest/env/default.secret.env'
        enable_reporting_tool (bool): Whether to enable the third-party
            reporting tool or not.
        test (str): Select tests by name or by long name containing also
            parent suite name like 'Parent.Test'. Name is case and space
            insensitive.
        suite (str): Select suites by name. When this option is used
            with --test, only tests in matching suites and also matching
            other filtering criteria are selected. Name can be a simple
            pattern similarly as with --test and it can contain parent
            name separated with a dot.
        exclude (str): Select test cases not to run by tag. Similarly
            as name with --test, tag is case and space insensitive and it is
            possible to use patterns with `*`, `?` and `[]` as wildcards. Tags
            and patterns can also be combined together with `AND`, `OR`, and
            `NOT` operators.
            Examples: --exclude foo --exclude bar*
                      --exclude fooANDbar*
    """
    valid_runner: tuple[str, str] = ('robot','pabot')
    if runner not in valid_runner:
        raise Exit('Runner must be one of: {0}'.format(
            ', '.join(map(str,valid_runner)))
        )

    # @todo Refactor.
    test_to_string = ''
    suite_to_string = ''
    exclude_to_string = ''
    if test:
        test_formatted = ['--test "{0}" '.format(t) for t in test]
        test_to_string = ' '.join(map(str, test_formatted))
    if suite:
        suite_formatted = ['--suite "{0}" '.format(s) for s in suite]
        suite_to_string = ' '.join(map(str, suite_formatted))
    if exclude:
        exclude_formatted = ['--exclude "{0}" '.format(e) for e in exclude]
        exclude_to_string = ' '.join(map(str, exclude_formatted))

    load_env(context, env_file=env_file)
    TEST_RUN_COMMAND_TEMPLATE: str = ("{runner} "
        "--outputdir {output_path} "
        "--loglevel {log_level} "
        "{suite} "
        "{test} "
        "{exclude_to_string} "
        "{test_path}")
    context.run(
        TEST_RUN_COMMAND_TEMPLATE.format(
            runner=runner,
            output_path=output_path,
            log_level=log_level,
            test_path=test_path,
            suite=suite_to_string,
            test=test_to_string,
            exclude_to_string=exclude_to_string,
        ),
    )

    if enable_reporting_tool:
        create_report(context, input_path=output_path)
