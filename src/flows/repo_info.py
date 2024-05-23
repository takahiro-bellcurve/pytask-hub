import httpx
from prefect import flow


@flow
def get_repo_info():
    url = "https://api.github.com/repos/PrefectHQ/prefect"
    response = httpx.get(url)
    response.raise_for_status()
    repo = response.json()
    print("PrefectHQ/prefect repository statistics 🤓:")
    print(f"Stars 🌠 : {repo['stargazers_count']}")
    print(f"Forks 🍴 : {repo['forks_count']}")

if __name__ == "__main__":
    get_repo_info.from_source(
        source="https://github.com/takahiro-bellcurve/pytask-hub.git",
        entrypoint="src/flows/repo_info.py:get_repo_info"
    ).deploy(
        name="my-first-deployment",
        work_pool_name="pytask-hub",
        cron="0 10 * * *",
    )
