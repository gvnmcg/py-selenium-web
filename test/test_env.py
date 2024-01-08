
from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv()

config = dotenv_values()
print(config)
print(config["SHARE_LOGIN"])