import os
import argparse
from pathlib import Path

from prance import ResolvingParser

from file_paths import DJANGO_PROJECT_PATH, FASTAPI_PROJECT_PATH
from Django.django_parser import DjangoCreator
from FastAPI.fastapi_parser import FastAPICreator


def get_command_line_arguments():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path', help='The path of the OpenAPI yml')
    arg_parser.add_argument('framework', help='The framework to create the API')

    args = arg_parser.parse_args()
    return args.framework, args.input_path


def validate_arguments(framework, yml_path):
    supported_frameworks = ['django', 'fastapi']
    if framework not in supported_frameworks:
        print(f'[ERROR] "{framework}" is not a supported framework')
        exit()

    if not yml_path.endswith('.yml'):
        print('[ERROR] OpenAPI input file must be yml')
        exit()


def generate_django_API(yml_parser):
    if not os.path.exists(DJANGO_PROJECT_PATH):
        project_name = DJANGO_PROJECT_PATH.split('/')[-1]
        os.chdir('Django')
        os.system(f'django-admin startproject {project_name}')
        os.chdir('..')
        print('[INFO] Django project created')

    dc = DjangoCreator(yml_parser.specification)
    dc.parse_endpoints()
    print('[INFO] Djang API generated')


def generate_fastAPI_API(yml_parser):
    Path(FASTAPI_PROJECT_PATH).mkdir(exist_ok=True)
    fc = FastAPICreator(yml_parser.specification)
    fc.parse_endpoints()


if __name__ == '__main__':
    framework, yml_path = get_command_line_arguments()
    validate_arguments(framework, yml_path)

    yml_parser = ResolvingParser(yml_path)

    if framework == 'django':
        generate_django_API(yml_parser)
    elif framework == 'fastapi':
        generate_fastAPI_API(yml_parser)
