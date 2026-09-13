# Custom Tools Collection

Эта коллекция содержит собственные модули и роли для Ansible.

## Содержимое

### Модули
- create_file - создает текстовый файл с заданным содержимым

### Роли
- create_file_role - роль для использования модуля create_file с параметрами по умолчанию

## Установка

ansible-galaxy collection install warret-custom_tools-1.0.0.tar.gz

## Использование

### Пример использования модуля

- name: Create a file
  warret.custom_tools.create_file:
    path: /tmp/test.txt
    content: "Hello World"

### Пример использования роли

- name: Use create_file_role
  ansible.builtin.include_role:
    name: create_file_role
  vars:
    file_path: /tmp/test.txt
    file_content: "Custom content"

## Требования

- Ansible >= 2.10
- Python >= 3.8
