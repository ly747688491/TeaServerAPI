from config.setting import setting

TORTOISE_ORM = {
    "connections": {
        "default": setting.DB_URL,
    },
    "apps": {
        "models": {"models": setting.DB_MODELS, "default_connection": "default"},
    },
}
