import requests


def get_github_projects(
        github_url):

    try:

        username = github_url.rstrip(
            "/"
        ).split("/")[-1]

        api_url = f"https://api.github.com/users/{username}/repos"

        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        repos = response.json()

        if not isinstance(repos, list):
            return []

        projects = []

        for repo in repos[:10]:

            projects.append(
                {
                    "name": repo["name"],
                    "language": repo["language"]
                }
            )

        return projects

    except (requests.RequestException, KeyError, TypeError, ValueError):
        return []