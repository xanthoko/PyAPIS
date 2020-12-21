from file_paths import FA_MAIN_PATH

MAIN_FILE_TEMPLATE = """from typing import Optional

from fastapi import FastAPI, Form

app = FastAPI()

{{ views }}
"""

VIEW_TEMPLATE = """
@app.{{ method }}("{{ path }}", status_code={{ response_code }})
def base_view_{{ view_index }}({{ parameters }}):
    return {}

"""

type_map = {'string': 'str', 'integer': 'int', 'boolean': 'bool'}


def generate_complete_main_file(filled_views_template):
    """Replaces the filled views template to the main template and writes it
    to the main file.

    Args:
        filled_views_template (string): Joined VIEW_TEMPLATE filled with data
    """
    total_main_template = MAIN_FILE_TEMPLATE.replace('{{ views }}',
                                                     filled_views_template)
    with open(FA_MAIN_PATH, 'w') as f:
        f.write(total_main_template)


def get_view_template_with_data(method, path, response_code, index, path_parameters,
                                query_parameters, body_parameters):
    """Fills the VIEW_TEMPLATE with the data given.

    Args:
        method (string): The http method used to access the endpoint
        path (string): The path of the endpoint
        response_code (string)
        index (integer): The index of the view
        path_parameters (list of dictionaries)
        query_parameters (list of dictionaries)
        body_parameters (list of dictionaries)
    """
    total_param_str = _create_total_parameter_str(path_parameters, query_parameters,
                                                  body_parameters)

    v_temp = VIEW_TEMPLATE
    v_temp = v_temp.replace('{{ method }}', method)
    v_temp = v_temp.replace('{{ path }}', path)
    v_temp = v_temp.replace('{{ response_code }}', response_code)
    v_temp = v_temp.replace('{{ view_index }}', str(index))
    v_temp = v_temp.replace('{{ parameters }}', total_param_str)

    return v_temp


def _create_total_parameter_str(path_parameters, query_parameters, body_parameters):
    """Creates the string that contains the information for the parameters of the
    endpoint.

    Args:
        path_parameters (list of dictionaries):  Each dictionary contains the name,
            the type and if the path parameter is required.
        query_parameters (list of dictionaries):  Each dictionary contains the name,
            the type and if the query parameter is required.
        body_parameters (list of dictionaries):  Each dictionary contains the name,
            the type and if the body parameter is required.
    Returns:
        string: The path, query and body paramets separated by comma.
    """
    formated_path_parameters = list(
        map(_dict_param_to_fastapi_param, path_parameters))
    formated_query_parameters = list(
        map(_dict_param_to_fastapi_param, query_parameters))
    formated_body_parameters = list(
        map(_dict_param_to_form_data_param, body_parameters))

    joined_params = formated_path_parameters + formated_query_parameters + \
        formated_body_parameters
    return ', '.join(joined_params)


def _dict_param_to_fastapi_param(parameter_dict):
    """Converts the given dictionary to a FastAPI valid format for query and
    path parameters.

    That is:
        {param_name}: {type}
        username: str
    or if the parameter is optional:
        {param_name}: Optional[{type}] = None
        password: Optional[str] = None

    Args:
        parameter_dict (dictionary): Containe "name", "type" and "required" field
    """
    ftype = type_map[parameter_dict['type']]
    if parameter_dict['required']:
        return f"{parameter_dict['name']}: {ftype}"
    else:
        return f"{parameter_dict['name']}: Optional[{ftype}] = None"


def _dict_param_to_form_data_param(parameter_dict):
    """Converts the given dictionary to a FastAPI valid format for form data
    body parameters.

    That is:
        {param_name}: {type} = Form(...)
        username: str = Form(...)
    or if the parameter is optional:
        {param_name}: Optional[{type}] = Form(None)
        password: Optional[str] = Form(None)

    Args:
        parameter_dict (dictionary): Containe "name", "type" and "required" field
    """
    ftype = type_map[parameter_dict['type']]
    if parameter_dict['required']:
        return f"{parameter_dict['name']}: {ftype} = Form(...)"
    else:
        return f"{parameter_dict['name']}: Optional[{ftype}] = Form(None)"
