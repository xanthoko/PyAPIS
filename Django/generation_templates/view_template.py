from file_paths import VIEWS_PATH

VIEWS_FILE_TEMPLATE = """from django.http import JsonResponse

{{ views }}
"""

VIEW_TEMPLATE = """
def basic_view_{{ view_index }}(request{{ path_params }}):
    if request.method == '{{ method }}':
{{ body_params }}
        return JsonResponse({}, status={{ response_code }})
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)\n
"""

REQUIRED_PARAMS_TEMPLATE = """
        try:
{{ params }}
        except KeyError as e:
            return JsonResponse({'error': f'Parameter {e} missing'}, status=400)
"""


def generate_complete_views_file(filled_views_template):
    filled_views_file_template = VIEWS_FILE_TEMPLATE.replace(
        '{{ views }}', filled_views_template)

    with open(VIEWS_PATH, 'w') as f:
        f.write(filled_views_file_template)


def get_view_template_with_data(view_index, per_method_data):
    method = per_method_data['method'].upper()
    response_codes = per_method_data['response_codes']

    v_temp = VIEW_TEMPLATE
    v_temp = v_temp.replace('{{ view_index }}', str(view_index))
    v_temp = v_temp.replace('{{ method }}', method)
    # for now use the first response code
    v_temp = v_temp.replace('{{ response_code }}', response_codes[0])

    path_parameters = [''] + per_method_data['path_parameters']
    v_temp = _replace_path_parameters(v_temp, path_parameters)

    query_parameters = per_method_data['query_parameters']
    body_parameters = per_method_data['body_parameters']
    v_temp = _replace_body_and_query_parameters(v_temp, query_parameters,
                                                body_parameters)

    return v_temp


def get_view_name(index):
    return f'basic_view_{index}'


def _replace_path_parameters(template_string, parameters):
    """
    Args:
        template_string (string): The template to fill
        parameters (list of strings): The path parameters
    """
    str_path_parameters = ', '.join(parameters)
    return template_string.replace('{{ path_params }}', str_path_parameters)


def _replace_body_and_query_parameters(template_string, query_params, body_params):
    """
    Args:
        tempalte_string (string): The template to fill
        query_params (dictionary): Query parameters in the following format.
            {'param': {is_required}(boolean), ...}
        body_params (dictionary): Body parameters in the following format.
            {'param': {is_required}(boolean), ...}
    """
    at_least_one_required_param = any(body_params.values()) or any(
        query_params.values())

    intent = 3 if at_least_one_required_param else 2
    prefix_spaces = _get_prefixed_spaces(intent)

    total_params_str = ''
    for param, required in body_params.items():
        total_params_str += _get_param_declaration_str(True, required, param,
                                                       prefix_spaces)
    for param, required in query_params.items():
        total_params_str += _get_param_declaration_str(False, required, param,
                                                       prefix_spaces)

    if at_least_one_required_param:
        total_params_str = REQUIRED_PARAMS_TEMPLATE.replace(
            '{{ params }}', total_params_str)

    return template_string.replace('{{ body_params }}', total_params_str)


def _get_prefixed_spaces(number_of_intent):
    return '    ' * number_of_intent


def _get_param_declaration_str(is_body, required, parameter, prefix):
    """Produces and returns the declaration of a body or query parameter.

    Args:
        is_body (boolean): If True its body param else query
        required (boolean)
        parameter (string): The parameter name
        prefix (string): The intent spaces
    """
    method = 'POST' if is_body else 'GET'
    if required:
        return f"{prefix}{parameter} = request.{method}['{parameter}']\n"
    else:
        return f"{prefix}{parameter} = request.{method}.get('{parameter}')\n"
