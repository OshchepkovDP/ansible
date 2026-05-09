#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: file_creator
short_description: Creates a text file with specified content
version_added: "1.0.0"
description:
    - Creates a text file on the remote host with specified path and content.
options:
    path:
        description:
            - Path where the file will be created.
        required: true
        type: str
    content:
        description:
            - Content to write into the file.
        required: true
        type: str
author:
    - OshchepkovDP (@https://github.com/OshchepkovDP)
'''

EXAMPLES = r'''
- name: Create a test file
  my_namespace.my_collection.file_creator:
    path: /tmp/test.txt
    content: "Hello, World!"
'''

RETURN = r'''
path:
    description: The path of the created file.
    type: str
    returned: always
    sample: "/tmp/test.txt"
content:
    description: The content written to the file.
    type: str
    returned: always
    sample: "Hello, World!"
changed:
    description: Whether the file was created or updated.
    type: bool
    returned: always
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
        content=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

file_path = module.params['path']
    new_content = module.params['content']

    if module.check_mode:
        result['path'] = file_path
        result['content'] = new_content
        if not os.path.exists(file_path):
            result['changed'] = True
        module.exit_json(**result)

    # Проверяем, существует ли файл и совпадает ли содержимое
    file_exists = os.path.exists(file_path)
    content_matches = False

    if file_exists:
        try:
            with open(file_path, 'r', encoding='utf-8' ) as f:
                existing_content = f.read()
            content_matches = existing_content == new_content
        except Exception:
            pass

    # Определяем, нужно ли менять файл
    if not file_exists or not content_matches:
        result['changed'] = True
        try:
            dir_path = os.path.dirname(file_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        except Exception as e:
            module.fail_json(msg=f'Failed to write file: {str(e)}', **result)

    result['path'] = file_path
    result['content'] = new_content

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
