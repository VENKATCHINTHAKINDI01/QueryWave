from app.utils.config_loader import ConfigLoader

config = ConfigLoader()

app_config = config.load("app_config.yaml")
model_config = config.load("model_config.yaml")
tool_config = config.load("tool_config.yaml")
