#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
import logging.config

pkg_root = os.path.realpath(os.path.join(os.path.realpath(__file__),
                                         os.path.pardir))
sys.path.append(pkg_root)

print(pkg_root)

# os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

log_cnf = os.path.join(pkg_root, 'conf', 'logging.cnf')
logging.config.fileConfig(log_cnf, disable_existing_loggers=False)
logging.basicConfig()
LOG = logging.getLogger(__name__)


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sweetshop.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
