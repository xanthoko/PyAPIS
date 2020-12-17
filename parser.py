import os
import argparse

from prance import ResolvingParser

from file_paths import DJANGO_PROJECT_PATH
from Django.django_parser import DjangoCreator


def get_framework_from_arguments():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('framework', help="The framework to create the API")

    args = arg_parser.parse_args()
    return args.framework


def generate_django_API():
    if not os.path.exists(DJANGO_PROJECT_PATH):
        project_name = DJANGO_PROJECT_PATH.split('/')[-1]
        os.chdir('Django')
        os.system(f'django-admin startproject {project_name}')
        os.chdir('..')
        print('[INFO] Django project created')

    dc = DjangoCreator(yml_parser.specification)
    dc.parse_endpoints()
    print('[INFO] Djang API generated')


def validate_given_framework(framework):
    supported_frameworks = ['django']
    if framework not in supported_frameworks:
        print(f'[ERROR] "{framework}" is not a supported framework')
        exit()


if __name__ == '__main__':
    yml_parser = ResolvingParser('test_simple.yml')
    framework = get_framework_from_arguments()
    validate_given_framework(framework)

    if framework == 'django':
        generate_django_API()
