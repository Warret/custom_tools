#!/usr/bin/python3

# Copyright: (c) 2024, Your Name <your.email@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: create_file

short_description: Creates a text file with specified content.

version_added: "1.0.0"

description: 
    - This module creates a text file on the remote host at the specified path with the given content.

options:
    path:
        description: The absolute path where the file should be created.
        required: true
        type: str
    content:
        description: The content to write into the file.
        required: true
        type: str

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Create a simple text file
- name: Create a test file
  warret.observability_tools.create_file:
    path: /tmp/test_file.txt
    content: "Hello, Ansible!"
'''

RETURN = r'''
path:
    description: The path of the created file.
    type: str
    returned: always
    sample: '/tmp/test_file.txt'
content_length:
    description: The length of the content written to the file.
    type: int
    returned: always
    sample: 15
'''

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        path='',
        content_length=0
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    file_path = module.params['path']
    content = module.params['content']

    # Check mode: just report what would happen
    if module.check_mode:
        if not os.path.exists(file_path):
            result['changed'] = True
        module.exit_json(**result)

    # Actual execution
    if not os.path.exists(file_path):
        result['changed'] = True
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            result['path'] = file_path
            result['content_length'] = len(content)
        except Exception as e:
            module.fail_json(msg=f"Failed to create file: {str(e)}", **result)
    else:
        # Проверка идемпотентности: читаем файл и сравниваем содержимое
        try:
            with open(file_path, 'r') as f:
                existing_content = f.read()
            if existing_content != content:
                result['changed'] = True
                with open(file_path, 'w') as f:
                    f.write(content)
            result['path'] = file_path
            result['content_length'] = len(content)
        except Exception as e:
            module.fail_json(msg=f"Failed to read/modify file: {str(e)}", **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()