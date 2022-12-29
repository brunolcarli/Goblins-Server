#!/usr/bin/env python
# import os
# import sys

# if __name__ == '__main__':
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_server.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)


import os
import pathlib
import sys

# Append directory where `channels_graphqlws` package resides.
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game_server.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that
        # the issue is really that Django is missing to avoid masking
        # other exceptions on Python 2.
        try:
            import django  # pylint: disable=unused-import
        except ImportError as ex:
            raise ImportError(
                "Could not import Django. Are you sure it is installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from ex
        raise
    execute_from_command_line(sys.argv)