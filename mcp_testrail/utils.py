import os


def get_env_var(name: str):
    try:
        return os.environ[name]
    except KeyError:
        raise EnvironmentError(f"Missing required environment variable: {name}")
