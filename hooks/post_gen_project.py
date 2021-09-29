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
    github_add_collaborator_url = " https://api.github.com/repos/EVOLVED-5G/{{cookiecutter.repo_name}}/collaborators/{{cookiecutter.git_username_collaborator}}"
    git_my_token = "{{cookiecutter.token_repo}}" 
    head = {'Authorization': 'token {}'.format(git_my_token)}
    payload_create_repo = {"name": "{{cookiecutter.repo_name}}","private":"true"}
    payload_permission_collaborator = {"permissions": "{{cookiecutter.collaborator_permissions}}"}
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
        self.add_collaborator = self.result.get("add_collaborator")
        self.collaborator_permissions = self.result.get("collaborator_permissions")
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
        command = "git commit -m 'Creation of a new NetApp {{cookiecutter.netapp_name}}'"
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

    def add_collaborator_repo(self):
        """
        Add collaborator is optional
        """
        if self.add_collaborator == 'yes': 
            response = requests.put(self.github_add_collaborator_url,headers=self.head)
            response.raise_for_status()
            payload = response.json()
            X = json.dumps(payload)
            print ("Contributor added",response)
            invited_id = json.loads (X)
            
            git_id_invited_collaborator = invited_id['id']

            if self.collaborator_permissions != 'write':
                git_url_permission_collaborator = f"https://api.github.com/repos/EVOLVED-5G/{{cookiecutter.repo_name}}/invitations/{git_id_invited_collaborator}"
                print(git_url_permission_collaborator)

                response_permission = requests.patch (git_url_permission_collaborator, headers=self.head, json=self.payload_permission_collaborator)
                print (response_permission)
                print("Collaborator with permission of", self.collaborator_permissions)

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
