import yaml

def load_config(url: str) -> dict:
    with open(url, 'r') as file:
        config = yaml.safe_load(file)
    return config


def load_env(path=".env") -> dict:
    env = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip()
    return env


# env = load_env()

# SECRET_KEY = env.get("SECRET_KEY")

# print("SECRET_KEY =", SECRET_KEY)
