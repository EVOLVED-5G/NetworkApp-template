# import re
# import sys
# import requests
# import logging

# from requests.auth import HTTPBasicAuth

# MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

# module_name = '{{ cookiecutter.module_name }}'

# if not re.match(MODULE_REGEX, module_name):
#     print('ERROR: %s is not a valid Python module name!' % module_name)

#     # exits with status 1 to indicate failure
#     sys.exit(1)

# my_token = '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'
# payload = {"name": "{{cookiecutter.repo_slug}}","private":"true"}
# head = {'Authorization': 'token {}'.format(my_token)}
# r = requests.post('https://api.github.com/user/repos',headers=head, json=payload)
# print(r)