#!/usr/bin/env python
"""
Main entry point for the CookCLI python implementation.

The terminal version includes a few commands.
This should simply start a flask service
"""
import sys
import os

import flask_app

def print_help():
    """Print usage"""
    print("Usage: mainfile.py")
    print()


if __name__ == "__main__":
    ip = "0.0.0.0"
    if len(sys.argv) > 1:
      ip = sys.argv[2]
    flask_app.main(ip=ip)
