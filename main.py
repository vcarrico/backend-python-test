"""AlayaNotes.

Usage:
  main.py [runserver]
  main.py initdb
"""
import sys

from alayatodo import app
from manage import manager


if __name__ == '__main__':
    arg = sys.argv[1:]
    if not arg:
        app.run(use_reloader=True)
    else:
        manager.run()
