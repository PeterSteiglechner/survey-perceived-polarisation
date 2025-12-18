from os import environ

SESSION_CONFIGS = [
    dict(
        name="OpinionPerceptionSurveyWave2",
        app_sequence=["survey_wave2"],
        num_demo_participants=1,
    ),
]

ROOMS = [
    dict(
        name="2025JanuaryWave2",
        display_name="2025 Januray Wave 2",
    )
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

LANGUAGE_CODE = "en"
REAL_WORLD_CURRENCY_CODE = "EUR"
USE_POINTS = False

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

DEMO_PAGE_INTRO_HTML = ""

SECRET_KEY = environ.get("OTREE_SECRET_KEY", "dev-secret-key")
