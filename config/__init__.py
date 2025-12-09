from utils.load_config import load_config, load_env
import os

current_path = os.getcwd()
cfg_path = os.path.join(current_path, "config/config.yaml")
env_path = os.path.join(current_path, "config/.env")


env = load_env(env_path)
SECRET_KEY = env["SECRET_KEY"]
ALGORITHM = env["ALGORITHM"]
DATABASE_URL = env["DATABASE_URL"]

config_all = load_config(url= cfg_path)
CFG_TOKEN : dict       = config_all["CFG_TOKEN"]
CFG_REDIS : dict       = config_all["CFG_REDIS"]
CFG_SOCKET : dict      = config_all["CFG_SOCKET"]
CFG_SERVER : dict      = config_all["CFG_SERVER"]

