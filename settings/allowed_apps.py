"""
Manages and auto-installs apps for project.
"""

# User Class Imports.
from settings.reusable_settings import *


APP_DIR = os.path.join(BASE_DIR, 'apps')

debug_print('')


# Django base apps, any 3rd party add-on apps, and CAE_Home app.
# All other CAE Apps should be defined under the "Allowed_CAE_Apps" setting.
INSTALLED_APPS = [
    'cae_home.apps.CaeHomeConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


# List of allowed apps to automatically install.
# Formatted as a dictionary of sub-dictionary values.
# If a third party app is already installed, it will safely be ignored.
ALLOWED_CAE_PROJECTS = {
    # 'Example_Project': {
    #     'url-prefix': 'root_url',
    #     'site': {
    #         'index': 'example:index',
    #         'name': 'Example',
    #     },
    #     'related_apps': {
    #         'example_project_app_1': {},
    #         'example_project_app_2': {},
    #     },
    #     'third_party_apps': [
    #         'example_third_party',
    #     ],
    # },

    'CAE_Web': {
        'url-prefix': 'caeweb',
        'site': {
            'index': 'cae_web_core:index',
            'name': 'CAE Web',
        },
        'related_apps': {
            'cae_web_core': {},
            'cae_web_audio_visual': {},
            'cae_web_inventory': {},
            'cae_web_virus': {},
        },
        'third_party_apps': [
            'schedule',     # django-scheduler
        ],
    },

    'CICO': {
        'url-prefix': 'cico',
        'site': {
            'index': '',
            'name': 'Check In Check Out',
        },
        'related_apps': {
            'cico_core': {},
        },
        'third_party_apps': {},
    },

    'CAEMon_Web': {
        'url-prefix': 'caemon',
        'site': {
            'index': '',
            'name': 'CAEMon Web',
        },
        'related_apps': {
            'caemon_web_core': {},
        },
        'third_party_apps': {},
    },
}


# Automatically populated for automatic url generation on home page. Do not edit.
INSTALLED_CAE_PROJECTS = {}

# Logic to automatically install a given allowed app, if found.
# First iterate through list of all project folders within the apps folder.
debug_print('Automatically Installed Apps:')
project_folder_list = [
    x for x in os.listdir(APP_DIR) if os.path.isdir(os.path.join(APP_DIR, x)) and not x.startswith('__')
]
installed_app_count = 1
excluded_project_list = []
for project_name in project_folder_list:

    # Check that project is defined through settings.
    if project_name in ALLOWED_CAE_PROJECTS.keys():
        debug_print('   {0}Included Project{1}: {2}'.format(ConsoleColors.bold_blue, ConsoleColors.reset, project_name))

        # Grab all app folders within given project.
        project_folder = os.path.join(APP_DIR, project_name)
        app_folder_list = [
            x for x in os.listdir(project_folder)
            if os.path.isdir(os.path.join(project_folder, x)) and not x.startswith('.git')
        ]
        excluded_app_list = []

        # Iterate through project apps.
        for app_name in app_folder_list:

            # Check that app is defined through settings.
            try:
                if app_name in ALLOWED_CAE_PROJECTS[project_name]['related_apps']:
                    app = 'apps.{0}.{1}'.format(project_name, app_name)
                    INSTALLED_APPS.insert(1, app)
                    INSTALLED_CAE_PROJECTS[project_name] = ALLOWED_CAE_PROJECTS[project_name]
                    INSTALLED_CAE_PROJECTS[project_name]['related_apps'][app_name] = app
                    debug_print('       {0}Included App{1}: {2:<25}   {0}Url{1}: .../{3}/{2}/'.format(
                        ConsoleColors.bold_blue,
                        ConsoleColors.reset,
                        app_name,
                        INSTALLED_CAE_PROJECTS[project_name]['url-prefix']
                    ))
                    installed_app_count += 1
                else:
                    # App not allowed through settings.
                    excluded_app_list.append(app_name)
            except KeyError:
                # No related apps key. All apps automatically excluded.
                excluded_app_list.append(app_name)

        for app_name in excluded_app_list:
            debug_print('       {0}Excluded App{1}: {2}'.format(ConsoleColors.bold_red, ConsoleColors.reset, app_name))

        # Add any third party apps.
        for third_party_app in ALLOWED_CAE_PROJECTS[project_name].get('third_party_apps', []):
            if third_party_app in INSTALLED_APPS:
                debug_print('       Ignoring Third Party App: {0:<14}  Already Installed.'.format(third_party_app))
                continue
            INSTALLED_APPS.insert(installed_app_count, third_party_app)
            debug_print('       {0}Included Third Party App{1}: {2}'.format(
                ConsoleColors.bold_blue,
                ConsoleColors.reset,
                third_party_app
            ))

    else:
        # Project folder not allowed through settings.
        excluded_project_list.append(project_name)


for project_name in excluded_project_list:
    debug_print('   {0}Excluded Project{1}: {2}'.format(ConsoleColors.bold_red, ConsoleColors.reset, project_name))


debug_print('')
