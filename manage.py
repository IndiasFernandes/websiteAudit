#!/usr/bin/env python
# This shebang line specifies the interpreter path. It tells the system to use the Python interpreter
# to run this script. This line is especially useful when the script is executable.

"""Django's command-line utility for administrative tasks."""
# This is a docstring providing a brief description of the script. It indicates that this script is
# Django's utility for handling command-line tasks related to administrative activities.

import os
import sys
# These are imports of Python's built-in modules. 'os' is used for interacting with the operating system,
# and 'sys' is used for accessing system-specific parameters and functions.

def main():
    """Run administrative tasks."""
    # This is the main function of the script. It's where the script starts executing.
    # The docstring indicates its purpose - to run administrative tasks.

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websiteAudit.settings')
    # This line sets the default environment variable 'DJANGO_SETTINGS_MODULE'.
    # 'websiteAudit.settings' refers to the settings module for your Django project.
    # This tells Django which settings to use. If the environment variable is already set,
    # this call does nothing and the existing value is kept.

    try:
        from django.core.management import execute_from_command_line
        # This line attempts to import the 'execute_from_command_line' function from Django's management module.
        # This function is used to execute the command-line actions received from the sys.argv.
    except ImportError as exc:
        # If the import fails, an ImportError is raised. This could happen if Django isn't installed.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        # The script raises a new ImportError with a custom message. The message is a helpful note
        # indicating possible reasons for the import failure - either Django isn't installed,
        # or it's not on the PYTHONPATH, or maybe the virtual environment isn't activated.

    execute_from_command_line(sys.argv)
    # This line calls the 'execute_from_command_line' function with 'sys.argv' as the argument.
    # 'sys.argv' is a list in Python, which contains the command-line arguments passed to the script.
    # This function parses and executes the command-line arguments (like 'runserver', 'migrate', etc.).

if __name__ == '__main__':
    main()
    # This is a common Python idiom. It checks if the script is being run directly (not being imported)
    # and if so, it calls the main function. This means that if this script is run as a script,
    # the main function will execute. If this script is imported as a module in another script,
    # the main function will not automatically run.
