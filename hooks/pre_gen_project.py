#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os, sys

os.system("git config --global user.email {{cookiecutter.git_email}}")
os.system("git config --global user.name {{cookiecutter.remote_username}}")

print("He añadido los git config")