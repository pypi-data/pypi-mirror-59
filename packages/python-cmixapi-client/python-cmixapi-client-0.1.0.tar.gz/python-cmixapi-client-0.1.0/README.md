# python-cmixapi-client

<a href="https://github.com/dynata/python-cmixapi-client/actions"><img alt="GitHub Actions status" src="https://github.com/dynata/python-cmixapi-client/workflows/python-tests/badge.svg"></a>

A Python client library for the [Dynata Cmix API](https://wiki2.criticalmix.net/display/CA/Getting+started).

## Setup

    Something here

## Example Usage

    cmix = CmixAPI(
        username="test_username",
        password="test_password",
        client_id="test_client_id",
        client_secret="test_client_secret"
    )
    cmix.authenticate()
    surveys = cmix.get_surveys('closed')

## Supported API Functions

    authenticate(*args, **kwargs)
    fetch_banner_filter(survey_id, question_a, question_b, response_id)
    fetch_raw_results(survey_id, payload)
    get_surveys(status, *args, **kwargs)
    get_survey_definition(survey_id)
    get_survey_xml(survey_id)
    get_survey_test_url(survey_id)
    get_survey_respondents(survey_id, respondent_type, live)
    get_survey_status(survey_id)
    get_survey_completes(survey_id)
    create_export_archive(survey_id, export_type)
    get_archive_status(survey_id, archive_id, layout_id)
    update_project(project_id, status=None)
    create_survey(xml_string)

## Contributing

Information on [contributing](CONTRIBUTING.md).

## Testing

To run the tests,

    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    pytest
    deactivate

to run the tests for this project.
