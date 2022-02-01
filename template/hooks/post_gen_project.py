"""
Cookiecutter-Git Post Project Generation Hook Module.
"""
import json
import os
import requests

from invoke import Result, run, UnexpectedExit


class PostGenProjectHook(object):
    """
    Post Project Generation Class Hook.
    """
    github_repos_url = "https://api.github.com/orgs/EVOLVED-5G/repos"
    git_my_token = "{{cookiecutter.token_repo}}" 
    head = {'Authorization': 'token {}'.format(git_my_token)}
    payload_create_repo = {"name": "{{cookiecutter.repo_name}}", "public": "true"}
    remote_message_base = "Also see: https://{}/{}/{}"
    success_message_base = "\n\nSuccess! Your project was created here:\n{}\n{}\n"
    repo_dirpath = os.getcwd()
    cookiecutter_json_filepath = os.path.join(
        repo_dirpath, "cookiecutter.json"
    )
    raw_repo_name_dirpath = os.path.join(
        repo_dirpath, "{% raw %}{{cookiecutter.repo_name}}{% endraw %}"
    )
    hooks_dirpath = os.path.join(repo_dirpath, "hooks")

    def __init__(self, *args, **kwargs):
        """
        Initializes the class instance.
        """
        self.result = self._get_cookiecutter_result()
        self.git_ignore = self.result.get("git_ignore")
        self.make_dirs = self.result.get("make_dirs")
        self.remote_provider = "github.com"
        self.repo_name = self.result.get("repo_name")
        self.remote_message = (
            self.remote_message_base.format(
                self.remote_provider, "EVOLVED-5G", self.repo_name
            )
        )
        self.success_message = self.success_message_base.format(
            self.repo_dirpath, self.remote_message
        )

    def git_create_remote_repo(self):
        """
        Creates a remote repo 
        """
        r = requests.post(self.github_repos_url,headers=self.head, json=self.payload_create_repo)
        print("Repository created", r)


    @staticmethod
    def git_init():
        """
        Runs git init.
        """
        command = "git init"
        run(command)

    @staticmethod
    def git_add():
        """
        Runs git add all.
        """
        command = "git add --all"
        run(command)

    @staticmethod
    def git_commit():
        """
        Runs git commit.
        """
        command = "git commit -m \"Creation of a new NetApp {{cookiecutter.netapp_name}}\""
        run(command)

    @staticmethod
    def _get_cookiecutter_result():
        """
        Removes as much jinja2 templating from the hook as possible.
        """
        try:
            result = json.loads("""{{ cookiecutter | tojson() }}""")
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
        command = "git remote add origin git@github.com:EVOLVED-5G/{{cookiecutter.repo_name}}.git"
        run(command)

    def git_push(self):
        """
        Pushes the git remote and sets as upstream.
        """
        command = "git push -u origin master"
        run(command)

    def git_checkout(self):
        """
        create new branch about master
        """
        command = "git checkout -b evolved5g"
        run(command)

    def git_push_evolved5g(self):
        """
        Push branch evolved5g
        """
        command = "git push -u origin evolved5g"
        run(command)

    def git_repo(self):
        """
        Adds a .gitignore, initial commit, and remote repo.
        """
        self.git_init()
        self.git_add()
        self.git_commit()
        self.git_create_remote_repo()
        self.git_remote_add()
        self.git_push()
        self.git_checkout()
        self.git_push_evolved5g()

    def run(self):
        """
        Sets up the project dirs, and git repo.
        """
        self.git_repo()
        print(self.success_message)


def main():
    """
    Runs the post gen project hook main entry point.
    """
    PostGenProjectHook().run()


# This is required! Don't remove!!
if __name__ == "__main__":
    main()
