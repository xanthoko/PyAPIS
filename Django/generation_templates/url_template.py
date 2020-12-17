from file_paths import URLS_PATH

URLS_FILE_TEMPLATE = """from django.contrib import admin
from django.urls import path
from demo import views

urlpatterns = [
    path('admin/', admin.site.urls),
{{ demo_paths }}
]
"""

PATH_TEMPLATE = """    path('{{ url_path }}', views.{{ url_view }}),\n"""


def generate_complete_urls_file(filled_paths_template):
    filled_urls_file_template = URLS_FILE_TEMPLATE.replace(
        '{{ demo_paths }}', filled_paths_template)
    with open(URLS_PATH, 'w') as f:
        f.write(filled_urls_file_template)


def get_path_template_with_data(path, view_name):
    """Replaces {{ url_path }} and {{ url_view }} in path template"""
    p_temp = PATH_TEMPLATE
    p_temp = p_temp.replace('{{ url_path }}', _cleanup_path(path))
    p_temp = p_temp.replace('{{ url_view }}', view_name)
    return p_temp


def _cleanup_path(path):
    """Convert OpenAPI's {path_parameter} to Django's <path_parameter>"""
    path = path.replace('{', '<')
    path = path.replace('}', '>')
    return path
