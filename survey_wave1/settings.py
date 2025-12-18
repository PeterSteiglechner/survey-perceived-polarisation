from os import environ

SESSION_CONFIGS = [
    dict(
        name="OpinionPerceptionSurveyWave1",
        app_sequence=["survey_wave1"],
        num_demo_participants=1,
    ),
]


ROOMS = [
    dict(
        name=f"2025JanuaryWave1",
        display_name=f"2025 January Wave 1",
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
