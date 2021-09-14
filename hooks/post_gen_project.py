# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

"""
Cookiecutter-Git Post Project Generation Hook Module.
"""
import base64
from contextlib import contextmanager
import errno
import getpass
import json
import os
import requests
import shutil

if os.name == "nt":

    def quote(arg):
        # https://stackoverflow.com/a/29215357
        if re.search(r'(["\s])', arg):
            arg = '"' + arg.replace('"', r"\"") + '"'
        meta_chars = '()%!^"<>&|'
        meta_re = re.compile(
            "(" + "|".join(re.escape(char) for char in list(meta_chars)) + ")"
        )
        meta_map = {char: "^%s" % char for char in meta_chars}

        def escape_meta_chars(m):
            char = m.group(1)
            return meta_map[char]

        return meta_re.sub(escape_meta_chars, arg)


else:
    try:  # py34, py35, py36, py37
        from shlex import quote
    except ImportError:  # py27
        from pipes import quote

from invoke import Result, run, UnexpectedExit
import requests

class PostGenProjectHook(object):
    """
    Post Project Generation Class Hook.
    """
    create_remote_url = None
    github_repos_url = "https://api.github.com/orgs/EVOLVED-5G/repos"
    github_add_collaborator_url = "https://api.github.com/repos/pencinarsanz-atos/{{cookiecutter.repo_slug}}/collaborators/{{cookiecutter.git_username_collaborator}}"
    git_my_token = "{{cookiecutter.token_repo}}" 
    head = {'Authorization': 'token {}'.format(git_my_token)}
    payload = {"name": "{{cookiecutter.repo_slug}}","private":"true"}
    remote_message_base = "Also see: https://{}/{}/{}"
    success_message_base = "\n\nSuccess! Your project was created here:\n{}\n{}\nThanks for using cookiecutter-git! :)\n\n"
    repo_dirpath = os.getcwd()
    cookiecutter_json_filepath = os.path.join(
        repo_dirpath, "cookiecutter.json"
    )
    raw_repo_slug_dirpath = os.path.join(
        repo_dirpath, "{% raw %}{{cookiecutter.repo_slug}}{% endraw %}"
    )
    github_dirpath = os.path.join(repo_dirpath, ".github")
    hooks_dirpath = os.path.join(repo_dirpath, "hooks")

    def __init__(self, *args, **kwargs):
        """
        Initializes the class instance.
        """
        self.result = self._get_cookiecutter_result()
        self.git_email = self.result.get("git_email")
        self.git_ignore = self.result.get("git_ignore")
        self.git_name = self.result.get("git_name")
        self.make_dirs = self.result.get("make_dirs")
        self.remote_namespace = self.result.get("remote_namespace")
        self.remote_protocol = self.result.get("remote_protocol")
        self.remote_provider = str(self.result.get("remote_provider")).lower()
        self.remote_username = self.result.get("remote_username")
        self.repo_slug = self.result.get("repo_slug")
        self.repo_summary = self.result.get("repo_summary")
        self.repo_tagline = self.result.get("repo_tagline")
        self.remote_data = {
            "name": self.repo_slug,
            "description": self.repo_tagline,
        }

        self.remote_repo = self.remote_provider != "none"
        self.remote_message = (
            self.remote_message_base.format(
                self.remote_provider, self.remote_namespace, self.repo_slug
            )
            if self.remote_repo
            else ""
        )
        self.success_message = self.success_message_base.format(
            self.repo_dirpath, self.remote_message
        )

    def git_create_remote_repo(self):
        """
        Creates a remote repo 
        """
        r = requests.post(self.github_repos_url,headers=self.head, json=self.payload)
        print("repo creado", r)


    @staticmethod
    def git_init():
        """
        Runs git init.
        """
        run("git init")

    @staticmethod
    def git_add():
        """
        Runs git add all.
        """
        # `git add -A`
        run("git add --all")
        print("He pasado por aqui")

    @staticmethod
    def git_commit(message="Initial commit"):
        """
        Runs git commit with an initial message.

        :param message:
        """
        command = "git commit --message {}".format(quote(message))
        if os.name == "nt":
            # See https://github.com/NathanUrwin/cookiecutter-git/issues/43
            with git_disable_gpgsign():
                run(command)
        else:
            # `git commit -m "Initial commit"`
            run(command)

    @staticmethod
    def _get_cookiecutter_result():
        """
        Removes as much jinja2 templating from the hook as possible.
        """
        # http://flask.pocoo.org/docs/latest/templating/#standard-filters
        try:
            result = json.loads("""{{ cookiecutter | tojson() }}""")
        # current temp hack around for `pipenv run pytest -s`
        except json.JSONDecodeError:
            result = {}
            repo_dirpath = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
            json_filepath = os.path.join(repo_dirpath, "cookiecutter.json")
            with open(json_filepath) as f:
                for k, v in json.loads(f.read()).items():
                    result[k] = v
                    if isinstance(v, list):
                        result[k] = v[0]
        return result

    def git_remote_add(self):
        """
        Adds the git remote origin url with included password.
        """
        run(
            "git remote add origin git@github.com:{{cookiecutter.remote_username}}/{{cookiecutter.repo_slug}}.git"
        )

    def git_push(self):
        """
        Pushes the git remote and sets as upstream.
        """
        command= "git push -u origin master"

        run(command)

    def git_repo(self):
        """
        Adds a .gitignore, initial commit, and remote repo.
        """
        self.git_init()
        self.git_add()
        self.git_commit()
        if self.remote_repo:
            self.git_create_remote_repo()
            self.git_remote_add()
            self.git_push()

    def add_collaborator_repo(self):
        """

        Add collaborator is optional

        """
        # if {{cookiecutter.add_collaborator}} == 'yes': 
        r1 = requests.put(self.github_add_collaborator_url,headers=self.head)
        print (r1)


    def run(self):
        """
        Sets up the project dirs, and git repo.
        """
        self.git_repo()
        self.add_collaborator_repo()
        print(self.success_message)


def main():
    """
    Runs the post gen project hook main entry point.
    """
    PostGenProjectHook().run()


# This is required! Don't remove!!
if __name__ == "__main__":
    main()
