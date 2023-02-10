#!/usr/bin/env python

"""Tests for `test_report_diff` package."""
import pytest
from click.testing import CliRunner
from test_report_diff import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_help_option():
    """Test help option"""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    with open('data/commandline_output/help_option.txt', 'r') as f:
        assert f.read() == help_result.output


def test_unsupported_type():
    """Test unsupported report type"""
    runner = CliRunner()
    help_result = runner.invoke(
        cli.main,
        ['data/cucumber/old.json', 'data/cucumber/new.json', 'test']
    )
    assert help_result.exit_code == 0
    with open('data/commandline_output/unsupported_report_type.txt', 'r') as f:
        assert f.read() == help_result.output


def test_cucumber_report_diff():
    """Test cucumber report diff"""
    runner = CliRunner()
    cucumber_data_dir = 'data/cucumber'
    help_result = runner.invoke(
        cli.main,
        [
            f'{cucumber_data_dir}/old.json',
            f'{cucumber_data_dir}/new.json',
            'cucumber'
        ]
    )
    assert help_result.exit_code == 0
    with open('data/commandline_output/cucumber_report_diff.txt', 'r') as f:
        expected_report = f.read()
    with open('data/commandline_output/cucumber_report_diff_variant_1.txt', 'r') as f:
        assert f.read() == help_result.output or expected_report == help_result.output


def test_allure_report_diff():
    """Test allure report diff"""
    from os import getcwd, path
    runner = CliRunner()
    allure_data_dir = path.join(getcwd(), 'data/allure')
    help_result = runner.invoke(
        cli.main,
        [
            f'{allure_data_dir}/old_report',
            f'{allure_data_dir}/new_report',
            'allure'
        ]
    )
    assert help_result.exit_code == 0
    with open('data/commandline_output/allure_report_diff.txt', 'r') as f:
        assert f.read() == help_result.output
