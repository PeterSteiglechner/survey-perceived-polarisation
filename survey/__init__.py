from otree.api import *
import json
import random
import numpy as np
from itertools import combinations

import time

doc = """
Your app description
"""


def distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


class C(BaseConstants):
    NAME_IN_URL = "survey"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    N_MAX_PRACTICE_RUNS = 5

    LIKERT7 = [
        "Strongly Disagree",
        "Disagree",
        "Somewhat Disagree",
        "Neutral",
        "Somewhat Agree",
        "Agree",
        "Strongly Agree",
    ]
    LIKERT7_de = [
        "Stimme überhaupt nicht zu",
        "Stimme nicht zu",
        "Stimme eher nicht zu",
        "Neutral",
        "Stimme eher zu",
        "Stimme zu",
        "Stimme voll und ganz zu",
    ]

    CANVAS_WIDTH = 550

    QUS = [
        "climate_concern",
        "gay_marriage",
        "rights_indep_integration",
        "econ_inequality",
    ]

    QU_SORTS = [[0, 1, 2, 3], [1, 3, 0, 2], [2, 0, 3, 1], [3, 2, 1, 0]]

    QUESTIONTEXT = {
        "en": dict(
            zip(
                QUS,
                [
                    "I am very concerned about climate change.",
                    "It is good that marriages between two women or two men are allowed.",
                    "Migrants should be given the same rights as natives, regardless of whether they make an effort and integrate.",  # Only migrants who make an effort and integrate should be given the same rights as natives.
                    "Income and wealth differences in Germany are too large.",
                ],
            )
        ),
        "de": dict(
            zip(
                QUS,
                [
                    "Ich bin sehr besorgt über den Klimawandel.",
                    "Es ist gut, dass Ehen zwischen zwei Frauen bzw. zwischen zwei Männern erlaubt sind.",
                    "Migranten und Migrantinnen sollten die gleichen Rechte bekommen wie Einheimische unabhängig davon, ob sie sich anstrengen und integrieren.",
                    "Die Einkommens- und Vermögensunterschiede in Deutschland sind zu groß.",
                ],
            )
        ),
    }
    QUESTIONSHORTTEXT = {
        "en": dict(
            zip(
                QUS,
                [
                    "very concerned about climate change",
                    "support same-sex marriage",
                    "equal rights for migrants regardless of integration",
                    "income and wealth differences too high",
                ],
            )
        ),
        "de": dict(
            zip(
                QUS,
                [
                    "Sehr besorgt über Klimawandel",
                    "Unterstützung für gleichgeschlechtliche Ehe",
                    "Gleiche Rechte für Migranten/-innen unabhängig von deren Integration",
                    "Einkommens- und Vermögensunterschiede zu groß",
                ],
            )
        ),
    }

    QUESTIONNAMES = {
        "en": dict(
            zip(
                QUS,
                [
                    "Opinion about climate change",
                    "Opinion about same-sex marriage",
                    "Opinion about whether equal rights for migrants should be given regardless of their integration efforts",
                    "Opinion about economic inequality",
                ],
            )
        ),
        "de": dict(
            zip(
                QUS,
                [
                    "Die Meinung der Person zum Klimawandel",
                    "Die Meinung der Person zu gleichgeschlechtlicher Ehe",
                    "Die Meinung der Person ob Migranten oder Migrantinnen gleiche Rechte wie Einheimische bekommen sollten unabhängig von deren Integrationsbemühungen",
                    "Die Meinung der Person zu ökonomischer Ungleichheit",
                ],
            )
        ),
    }

    NCONTACTS = 10

    # N_BATCHES = 2
    FRIENDCOLOR = "#ff6600"
    LABELLED = ["Green Party", "AfD", "FDP", "Left Party", "CDU/CSU", "SPD", "BSW"]
    LABELLEDFULL = dict(
        zip(
            LABELLED,
            [
                " (<em>Bündnis90/Die Grünen</em>)",
                "",
                "",
                " (<em>Die Linke</em>)",
                "",
                "",
                " (<em>Bündnis Sarah Wagenknecht</em>)",
            ],
        )
    )

    LABELLED_de = dict(
        zip(LABELLED, ["Grüne", "AfD", "FDP", "Linke", "CDU/CSU", "SPD", "BSW"])
    )
    LABELLEDCOLORS = dict(
        zip(
            LABELLED,
            [
                "#7cbb15",
                "#009de0",
                "#ffcc00",
                "#bd3075",
                "#121212",
                "#d71f1f",
                "#691940",
            ],
        )
    )

    NLABELLED = len(LABELLED)
    MAXSLIDES = 13
    # op
    # id + toc
    # contacts
    # 5 person Op
    # labelled Op + toc
    # MapGame
    # MapTest
    # Map + toc
    # 10 Pairiwse
    # Importance
    # Satis
    # rela
    # demo

    NR_PAIRWISE_CHECKS = 1 + 10 + 7

    FORCED_PAIRS = [("Green Party", "AfD"), ("self", "AfD"), ("self", "Green Party")]

    CHOICES_IDENTITY = [
        "CDU/CSU",
        "AfD",
        "SPD",
        "Green Party",
        "Left Party",
        "BSW",
        "FDP",
        "Other party",
        "No party",
        "Refuse to say/No answer",
    ]

    CHOICES_IDENTITY_DE = [
        "CDU/CSU",
        "AfD",
        "SPD",
        "Bündnis 90/Die Grünen",
        "Die Linke",
        "BSW",
        "FDP",
        "Andere Partei",
        "Keiner Partei",
        "Keine Antwort",
    ]

    # CHOICES_INTEREST = [
    #     "Not at all interested",
    #     "Hardly interested",
    #     "Quite interested",
    #     "Very interested",
    # ]
    # CHOICES_POLARISED = [
    #     "Not at all divided",
    #     "Somewhat divided",
    #     "Very divided",
    #     "Extremely divided",
    # ]

    # OPTIONS_CONTACTS_CLOSE = [
    #     "Not particularly close",
    #     "Somewhat close",
    #     "Close",
    #     "Very close",
    #     "No answer",
    # ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def slider(min, max, label=""):
    return models.IntegerField(
        choices=range(min, max + 1),
        label=label,
        widget=widgets.RadioSelect,
    )


def define_contact(label, n):
    return models.LongStringField(label=label, blank=False, max_length=20)


class Player(BasePlayer):

    #################################
    #####  More information   #####
    #################################

    completed = models.BooleanField(blank=False)

    consent = models.BooleanField(blank=False)

    question_sorting = models.LongStringField(initial="")
    voter_sorting = models.LongStringField(initial="")

    language = models.StringField(
        choices=[["en", "English"], ["de", "Deutsch"]],
        widget=widgets.RadioSelect,
        label="Language / Sprache",
    )

    age = models.IntegerField(label="", min=18, max=100)

    political_interest = slider(0, 100)
    # political_interest = models.StringField(
    #     label="", choices=C.CHOICES_INTEREST, blank=False, widget=widgets.RadioSelect
    # )

    feel_closest_party = models.StringField(
        label="", choices=C.CHOICES_IDENTITY, blank=False, widget=widgets.RadioSelect
    )

    lrscale = slider(-50, +50, label="lrscale")
    # is_secondclosest_party = models.BooleanField(
    #     label="", blank=False, widget=widgets.RadioSelect
    # )

    # feel_secondclosest_party = models.StringField(
    #     label="", choices=C.CHOICES_IDENTITY, blank=False, widget=widgets.RadioSelect
    # )

    party_comment = models.LongStringField(label="", blank=True)

    how_polarised = slider(0, 100)

    importance_comments = models.LongStringField(
        blank=True, label="", initial="", null=True
    )

    #################################
    #####  TIME   #####
    #################################
    visited_toc = models.IntegerField(blank=False, initial=0)

    t_on_consent = models.IntegerField(blank=True)
    t_on_ownOpinion = models.IntegerField(blank=True)
    t_on_identity = models.IntegerField(blank=True)
    t_on_toc1 = models.IntegerField(blank=True)
    t_on_contacts = models.IntegerField(blank=True)
    t_on_contactOpinion = models.IntegerField(blank=True)
    t_on_voterOpinion = models.IntegerField(blank=True)
    t_on_toc2 = models.IntegerField(blank=True)
    t_on_practiceGame_page = models.IntegerField(blank=True)
    t_on_practice_page = models.IntegerField(blank=True)
    t_on_practiceResult_page = models.LongStringField(blank=True, initial="{}")
    t_on_map_page = models.IntegerField(blank=True)
    t_firstDotMoved = models.IntegerField(blank=True)
    # t_on_mapP_page = models.IntegerField(blank=True)
    t_on_toc3 = models.IntegerField(blank=True)
    t_on_pairwiseCheck = models.IntegerField(blank=True)
    t_after_first_check = models.IntegerField(blank=True)
    t_on_importance = models.IntegerField(blank=True)
    t_on_satisfaction = models.IntegerField(blank=True)
    t_on_relationships = models.IntegerField(blank=True)
    t_on_demographics = models.IntegerField(blank=True)
    t_on_success = models.IntegerField(blank=True)

    #################################
    #####  MAP POSITIONS   #####
    #################################

    # JSON data of positions
    positionsGame = models.LongStringField(blank=True)
    positionsTest = models.LongStringField(blank=True)
    positions = models.LongStringField(blank=True)
    min_pair = models.LongStringField(blank=True)
    max_pair = models.LongStringField(blank=True)
    # positions = models.LongStringField(blank=True)

    #################################
    #####  Similarity ratings   #####
    #################################

    valid_pairs = models.LongStringField(blank=True, initial="")
    pairSequence = models.LongStringField(blank=True, initial="")

    n_check = models.IntegerField(initial=1)
    n_checks = models.IntegerField(initial=0)

    satisfaction = slider(0, 100)
    accurateMapping = slider(0, 100)
    satisfaction_text = models.LongStringField(label="", blank=True)

    #################################
    #####  PRACTICE RUN   #####
    #################################

    isTrainingPassed = models.BooleanField(initial=False)  #
    isTrainingCondFvC = models.BooleanField(initial=False)  #
    isTrainingCondSelfvFC = models.BooleanField(initial=False)  #
    isTrainingCondRvFC = models.BooleanField(initial=False)  #
    isTrainingCondRvF = models.BooleanField(initial=False)  #
    attemptPractice = models.IntegerField(initial=0)
    latest_error_msg = models.LongStringField(blank=True, initial="")

    #################################
    #####  RUNNING VARIABLES   #####
    #################################

    current_contact = models.IntegerField(initial=1)
    evaluated_labelledPerson = models.IntegerField(initial=0)
    # current_batch = models.IntegerField(initial=1)
    current_page = models.IntegerField(initial=0)


#################################
#####  OWN POLITICAL OPINIONS   #####
#################################
for q in C.QUS:
    setattr(Player, f"own_{q}", slider(-100, 100))

#################################
#####  CONTACTS & CONTACTS' POLITICAL OPINIONS   #####
#################################
for n in range(1, C.NCONTACTS + 1):
    setattr(Player, f"contact{n}", define_contact(f"Contact {n}: ", n))
    setattr(Player, f"contact{n}_socialCloseness", slider(0, 100))
    for q in C.QUS:
        setattr(Player, f"contact{n}_{q}", slider(-100, 100))

#################################
#####  LABELLED INDIVIDS' POLITICAL OPINIONS   #####
#################################
for name in C.LABELLED:
    for q in C.QUS:
        setattr(Player, f"{name.replace(' ', '')}_{q}", slider(-100, 100))


#################################
#####  PAIRWISE SIMILARITY RATING   #####
#################################
for n in range(1, C.NR_PAIRWISE_CHECKS + 1):
    # setattr(Player, f"checkPair{n}_dot1", models.LongStringField(blank=True))
    # setattr(Player, f"checkPair{n}_dot2", models.LongStringField(blank=True))
    setattr(Player, f"similarityPair{n}", slider(0, 100))

###########################
####  Importance
###########################
for q in C.QUS:
    setattr(Player, f"importance_{q}", slider(0, 100))


#################################

#################################

#################################


#################################
#####       PAGES           #####
#################################


#################################
#####  Introduction   #####
#################################
class slide01_Introduction(Page):
    form_model = "player"
    form_fields = ["consent", "language"]

    @staticmethod
    def vars_for_template(player: Player):
        player.t_on_consent = int(time.time())

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.question_sorting = json.dumps(
            C.QU_SORTS[np.random.choice(range(len(C.QU_SORTS)))]
        )
        voters = list(np.random.choice(C.LABELLED, replace=False, size=len(C.LABELLED)))
        player.voter_sorting = json.dumps(voters)
        player.t_on_ownOpinion = int(time.time())
        player.current_page += 1


#################################
#####  Overview   #####
#################################
class slide00_toc(Page):
    form_model = "player"
    form_fields = []

    @staticmethod
    def is_displayed(player):
        return player.consent

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        n_checks = {0: 1, 1: 3, 2: 4}[player.visited_toc]
        checks = ["<span saclass='checkmark'>✅</span>  "] * n_checks + [
            "<span saclass='checkmark upcoming'>⬜</span>  "
        ] * 6
        hl = {0: [0, 1, 1, 0, 0, 0], 1: [0, 0, 0, 1, 0, 0], 2: [0, 0, 0, 0, 1, 1]}[
            player.visited_toc
        ]
        hls = ["" if not hl_li else " class='upcoming'" for hl_li in hl]
        if lan == "en":
            items = f"<ul><li{hls[0]}>{checks[0]}Your own political opinions and identity</li><li{hls[1]}>{checks[1]}How you think your social contacts view these political issues</li><li{hls[2]}>{checks[2]}How you think typical voters view these political issues</li><li{hls[3]}>{checks[3]}Placing these individuals on a political map<br><em>(with two short practice examples first)</em></li><li{hls[4]}>{checks[4]}Evaluating the political similarity of a few pairs of individuals</li><li{hls[5]}>{checks[5]}A few final questions about the survey, your social contacts, and yourself</li></ul>"
            if player.visited_toc == 0:
                i1 = "Thank you very much for your responses so far!<br>Below you can find an overview of the remaining tasks in this survey. On the next pages, we will continute with the ones highlighted in <b class='upcoming'>yellow</b>."  # i1 = "➡️ In the following slides, we continue with your evaluations of the political views of your social contacts and typical voters."
                i2 = ""
            if player.visited_toc == 1:
                i1 = "Thank you very much for your evaluations of the political views of other individuals!"  # ➡️ In the following part, we will ask you to place people on a political map based on how similar or different you perceive their political views to be."
                i2 = "➡️ To prepare for the main task in which we ask you to place people on your own personal political map, we will begin with <strong>two short practice rounds</strong>."
            if player.visited_toc == 2:
                i1 = "Thank you very much for creating your own personal political map!"
                i2 = "➡️ To help us better understand your political map, we ask you to again evaluate the political similarity between a few (randomly selected) pairs of individuals. Then, we will close this survey with a few short more general questions."
        else:
            items = f"<ul><li{hls[0]}>{checks[0]}Ihre eigenen politischen Einstellungen und Identität</li>   <li{hls[1]}>{checks[1]}Ihre Einschätzungen über die politischen Ansichten von Personen, die Sie gut kennen</li> <li{hls[2]}>{checks[2]}Ihre Einschätzungen über die politischen Ansichten typischer Wählerinnen und Wähler</li>  <li{hls[3]}>{checks[3]}Die genannten Personen auf einer politischen Karte verorten<br>(inklusive zwei kurzer Übungsaufgaben)</li> <li{hls[4]}>{checks[4]}Einschätzungen über die politische Ähnlichkeit einzelner Personen zueinander</li>  <li{hls[5]}>{checks[5]}Abschlussfragen zur Umfrage, zu Ihren sozialen Kontakten und zu Ihrer Person</li></ul>"
            if player.visited_toc == 0:
                i1 = "Vielen Dank für Ihre Antworten bisher!<br>Unten finden Sie eine Übersicht der noch anstehenden Aufgaben in dieser Umfrage. Auf den nächsten Seiten werden wir mit den <b class='upcoming'>gelb</b> markierten fortfahren."  # ➡️ In den folgenden Seiten geht es um Ihre Einschätzungen zu den politischen Ansichten von Ihren sozialen Kontakten und von typischen Wählern oder Wählerinnen."
                i2 = ""
            if player.visited_toc == 1:
                i1 = "Vielen Dank für Ihre Einschätzungen über die politischen Ansichten von anderen Personen!"  # ➡️ Im folgenden Teil werden wir Sie bitten, Personen auf einer politischen Karte zu platzieren, je nachdem, wie ähnlich oder unterschiedlich Sie deren politische Ansichten wahrnehmen."
                i2 = "➡️ Zur Vorbereitung auf die eigentliche Aufgabe, in der wir Sie bitten werden die Personen auf einer persönlichen politischen Karte zu verorten, beginnen wir mit <strong>zwei kurzen Übungsaufgaben</strong>."
            if player.visited_toc == 2:
                i1 = "Vielen Dank für das Erstellen Ihrer persönlichen politischen Karte!"
                i2 = "➡️ Um uns dabei zu helfen Ihre Daten besser zu verstehen, bitten wir Sie zunächst nochmals die politische Ähnlichkeit einiger (zufällig ausgewählte) Personenpaare einzuschätzen. Danach beenden wir die Umfrage mit ein paar kurzen generellen Fragen."
        return {
            "lan_en": lan == "en",
            "maxslides": C.MAXSLIDES,
            "page_title": "Your Progress" if lan == "en" else "Ihr Fortschritt",
            "items": items,
            # "overview": (
            #     "<p>What you will do in this survey:</p>"
            #     if lan == 'en'
            #     else "<p>Was Sie in dieser Umfrage :</p>"
            # ),
            "instruction_text1": i1,
            "instruction_text2": i2,
            # "thanks": "<p>Thank you for your participation!</p>" if lan=='en' else "<p>Thank you for your participation!</p>",
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.visited_toc += 1
        if player.visited_toc == 1:
            player.t_on_contacts = int(time.time())
        if player.visited_toc == 2:
            player.t_on_practiceGame_page = int(time.time())
        if player.visited_toc == 3:
            player.t_on_pairwiseCheck = int(time.time())


#################################
#####  Own opinions   #####
#################################
class slide02_Opinions(Page):
    form_model = "player"
    form_fields = [f"own_{q}" for q in C.QUS]

    @staticmethod
    def is_displayed(player: Player):
        return player.consent

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        questions = [C.QUS[i] for i in json.loads(player.question_sorting)]

        fields = [f"own_{q}" for q in questions]
        questions = [C.QUESTIONTEXT[player.language][q] for q in questions]
        field_question_pairs = []
        for field, question in zip(fields, questions):
            field_question_pairs.append(
                {
                    "field_name": field,
                    "question_text": question,
                    "first_label": C.LIKERT7[0] if lan == "en" else C.LIKERT7_de[0],
                    "neutral_label": C.LIKERT7[3] if lan == "en" else C.LIKERT7_de[3],
                    "last_label": C.LIKERT7[6] if lan == "en" else C.LIKERT7_de[6],
                }
            )
        return {
            "lan_en": lan == "en",
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "field_question_pairs": field_question_pairs,
            "page_title": (
                "Your political views"
                if player.language == "en"
                else "Ihre politischen Ansichten"
            ),
            "instruction_text": (
                "<p>At the beginning of this survey, we are interested in your own political opinions. </p><p>Please indicate to what extent you agree or disagree with the following statements.</p><p> There are no right or wrong answers; we are most interested in which response option is most aligned with your views.</p>"
                if player.language == "en"
                else "<p>Zum Start dieser Umfrage interessieren wir uns für Ihre eigenen politischen Ansichten.</p><p> Bitte geben Sie an, inwieweit Sie den folgenden Aussagen zustimmen oder nicht zustimmen.</p><p>Es gibt keine richtigen oder falschen Antworten. Wir interessieren uns dafür welche Antwortmöglichkeit am ehesten Ihren Ansichten entspricht.</p>"
            ),
            "table_head": (
                "Your responses" if player.language == "en" else "Ihre Antworten"
            ),
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.current_page += 1
        valid_pairs = list(
            combinations(
                ["self"]
                + [f"contact{c}" for c in range(1, C.NCONTACTS + 1)]
                + C.LABELLED,
                2,
            )
        )
        valid_pairs = [tuple(v) for v in valid_pairs if not v in C.FORCED_PAIRS]
        player.valid_pairs = json.dumps(valid_pairs)
        player.n_checks = 1 + C.NCONTACTS + len(C.LABELLED)
        player.t_on_identity = int(time.time())


#################################
#####  IDENTITY   #####
#################################
class slide02a_Identity(Page):
    form_model = "player"
    form_fields = [
        "feel_closest_party",
        "lrscale",
        # "is_secondclosest_party",
        # "feel_secondclosest_party",
        "party_comment",
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.consent

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        question = (
            "In politics people sometimes talk of 'left' and 'right'. Where would you place yourself on this scale, where 0 means the left and 10 means the right?"
            if lan == "en"
            else "In der Politik spricht man manchmal von 'links' und 'rechts'. Wo auf der Skala von -5 bis 5 würden Sie sich selbst einstufen,  wenn -5 für links steht und 5 für rechts?"
        )
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "page_title": (
                "Your Political Identity" if lan == "en" else "Politische Identität"
            ),
            "qu_identity": (
                "Do you feel closer to one of the political parties in Germany than the others? If so, which one?"
                if lan == "en"
                else "Gibt es eine bestimmte politische Partei in Deutschland, der Sie sich politisch näher fühlen als allen anderen Parteien? Welcher?"
            ),
            "choices_identity": dict(
                zip(
                    C.CHOICES_IDENTITY,
                    (C.CHOICES_IDENTITY if lan == "en" else C.CHOICES_IDENTITY_DE),
                )
            ),
            "qu_party_comment": (
                "Would you like to add anything to the question above? (optional):"
                if lan == "en"
                else "Möchten Sie etwas zu dieser Frage ergänzen? (optional)"
            ),
            "lr_question": question,
            "lr_first_label": "left" if lan == "en" else "links",
            "lr_last_label": "right" if lan == "en" else "rechts",
            # "lr_choices": dict(zip(np.arange(0, 10.1, 1), np.arange(0, 10.1, 1))),
            "partytext": (
                "In the following, we will use<ul style='font-size: 8pt; color: grey'><li><em>Green party</em> for the party Bündnis 90/Die Grünen</li><li><em>Left party</em> for the party Die Linke</li><li>Note: <em>BSW</em> for Bündnis Sarah Wagenknecht</li></ul>"
                if lan == "en"
                else "Im folgenden benutzen wir<ul style='font-size: 8pt; color: grey'><li><em>Grüne</em> für die Partei Bündnis 90/Die Grünen</li><li><em>Linke</em> für die Partei Die Linke</li><li><em>BSW</em> steht für Bündnis Sarah Wagenknecht</li></ul>"
            ),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.t_on_toc1 = int(time.time())
        player.current_page += 1


#################################
#####  Contacts   #####
#################################
class slide03_Contacts(Page):
    form_model = "player"
    form_fields = [f"contact{n}" for n in range(1, C.NCONTACTS + 1)]

    @staticmethod
    def is_displayed(player: Player):
        return player.consent

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        contact_fields = []
        for n in range(1, C.NCONTACTS + 1):
            contact_fields.append(
                {
                    "name": f"contact{n}",
                    "label": f"Contact {n}:" if lan == "en" else f"Kontakt {n}:",
                }
            )
        return {
            "lan_en": lan == "en",
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "ncontacts": C.NCONTACTS,
            "contact_fields": contact_fields,
            "page_title": "Social Contacts" if lan == "en" else "Soziale Kontakte",
            "instruction_text": (
                f"<p>Think about <strong>{C.NCONTACTS} social contacts</strong> that you know well. This can include friends, family members, co-workers, ... or a mix.</p><p>Please write down their names or initials so that you are later able to recognise them (we will not use/store that information).</p>"
                if lan == "en"
                else f"<p>Denken Sie nun an <strong>{C.NCONTACTS} soziale Kontakte</strong>, die Sie gut kennen. Das können Freunde, Freundinnen, Familienmitglieder, Kollegen, etc. oder eine Mischung sein.</p><p>Bitte notieren Sie die Namen oder Initialen dieser Kontakte in den Feldern unten, so dass Sie die Kontakte später wiedererkennen (wir werden diese Informationen nicht speichern oder verwenden).</p>"
            ),
            "reminder": (
                "On the following pages we will ask you to evaluate the opinions of these contacts. To make this easier, think of people that you do know well!"
                if lan == "en"
                else "Auf den folgenden Seiten werden wir Sie bitten, die politischen Meinungen dieser Kontakte zu schätzen. Um die Aufgabe leichter zu machen, wählen Sie Kontakte, die sie gut kennen!"
            ),
            # "instruction2": (
            #     "➡️ In the next slides, we will ask you what you think these people would respond to the political questions from the previous slide."
            #     if lan == "en"
            #     else "➡️ In den folgenden Seiten, fragen wir Sie was diese Personen Ihrer Meinung nach auf die politischen Fragen antworten würden."
            # ),
        }

    @staticmethod
    def error_message(player: Player, values):
        contacts = [v.strip() for v in values.values() if v.strip()]
        if len(contacts) < C.NCONTACTS:
            return (
                "Please fill in all contact fields!"
                if player.language == "en"
                else "Bitte füllen Sie alle Felder aus!"
            )
        if len(set(contacts)) < len(contacts):
            return (
                "Each contact must be unique. Please correct duplicates. You can use nicknames, initials, or anything that you will later recognise."
                if player.language == "en"
                else "Jeder Kontakt muss einen eindeutigen Namen haben. Bitte korrigieren Sie Duplikate. Sie können Spitznamen, Initialien oder alles benutzen, was Sie später wiedererkennen."
            )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.t_on_contactOpinion = int(time.time())
        player.current_page += 1


#################################
#####  Person Opinions   #####
#################################


class slide04_ContactsOpinions(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language

        # start = 1 if player.current_batch == 1 else 6
        # end = 5 if player.current_batch == 1 else 10

        pillname = (
            lambda name: f"<span class='pill' style='background-color: {C.FRIENDCOLOR}; color: white;'>{name}</span>"
        )
        contacts = [
            {
                "id": f"contact{i}",
                "name": ("Your contact " if lan == "en" else "Ihr Kontakt ")
                + pillname(getattr(player, f"contact{i}"))
                + (
                    " would most likely respond with..."
                    if lan == "en"
                    else " würde am ehesten wohl so antworten..."
                ),
            }
            for i in range(1, C.NCONTACTS + 1)
        ]

        questions = []
        for q in [C.QUS[i] for i in json.loads(player.question_sorting)]:
            questions.append(
                {
                    "prefix": f"{q}",
                    "text": C.QUESTIONTEXT[lan][q],
                }
            )

        return dict(
            lan_en=(lan == "en"),
            maxslides=C.MAXSLIDES,
            nslide=player.current_page,  # (f"{player.current_page}{'a' if player.current_batch==1 else 'b'} "),
            page_title=(
                f"Political Opinions of Your Contacts"
                if lan == "en"
                else "Politische Meinungen Ihrer Kontakte"
            ),  # + ("I" if player.current_batch == 1 else "II"),
            # instruction_text_batch=(
            #     "Please note: On the next page, we will ask you about your evaluations of the other five contacts."
            #     if lan == "en"
            #     else "Hinweis: Auf der nächsten Seite bitten wir Sie um Ihre Einschätzung der fünf weiteren Kontakte."
            # ),
            instruction_bestguess=(
                "We know that it is not always easy to estimate others' responses. For each statement, please indicate the option that <em>you</em> believe the respective person would be most likely to choose."
                if lan == "en"
                else "Wir wissen, dass es nicht immer leicht ist, die Antworten anderer einzuschätzen. Bitte geben Sie für jedes der Statements die Option an, von der <em>Sie</em> am ehesten glauben, dass die jeweilige Person sie auswählen würde."
            ),
            instruction_text=(
                f"Thinking about your contacts, how do you think each of them would respond to the political questions?"
                if lan == "en"
                else f"Denken Sie nun an Ihre Kontakte. Wie würden Ihrer Meinung nach diese Personen jeweils die politischen Fragen beantworten?"
            ),
            contacts=contacts,
            questions=questions,
            color=C.FRIENDCOLOR,
            would_respond=(
                f"I think the responses of {pillname('my contacts')} would be..."
                if lan == "en"
                else f"Ich denke, die Antworten meiner Kontakte {pillname('meiner Kontakte')} wären..."
            ),
            first_label=(
                "Strongly Disagree" if lan == "en" else "Stimme überhaupt nicht zu"
            ),  # Strongly Disagree
            neutral_label="Neutral" if lan == "en" else "Neutral",
            last_label=(
                "Strongly Agree" if lan == "en" else "Stimme voll und ganz zu"
            ),  # Strongly Agree
        )

    @staticmethod
    def get_form_fields(player: Player):
        # start = 1 if player.current_batch == 1 else 6
        # end = 5 if player.current_batch == 1 else 10

        fields = []
        for q in [C.QUS[i] for i in json.loads(player.question_sorting)]:
            for i in range(1, C.NCONTACTS + 1):
                fields.append(f"contact{i}_{q}")
        return fields

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # player.current_batch += 1
        player.t_on_voterOpinion = int(time.time())
        # if player.current_batch == C.N_BATCHES + 1:
        player.current_page += 1

    @staticmethod
    def is_displayed(player: Player):
        return player.consent  # & (player.current_batch < (C.N_BATCHES + 1))


class slide04b_VotersOpinions(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language

        pillname = (
            lambda x, color: f"<span class='pill' style='background-color: {color}; color: {'#424949' if x=='FDP' or color==C.LABELLEDCOLORS['FDP'] or color=="#dddddd" else 'white'};'><strong>{x}</strong></span>"
        )
        voter_sorting = json.loads(player.voter_sorting)
        voters = [
            {
                "id": p.replace(" ", ""),
                "name": (
                    f"The typical {pillname(p+' voter', C.LABELLEDCOLORS[p])} would most likely respond with:"
                    if lan == "en"
                    else f"Der/Die {pillname(C.LABELLED_de[p], C.LABELLEDCOLORS[p])} Wähler/Wählerin würde am ehesten wohl so antworten:"
                ),
                "color": C.LABELLEDCOLORS[p],
                "textcolor": "#424949" if p == "FDP" else "white",
            }
            for p in voter_sorting
        ]

        questions = []
        for q in [C.QUS[i] for i in json.loads(player.question_sorting)]:
            questions.append(
                {
                    "prefix": f"{q}",
                    "text": C.QUESTIONTEXT[lan][q],
                }
            )
        partylist = ", ".join(
            [
                pillname((p if lan == "en" else C.LABELLED_de[p]), C.LABELLEDCOLORS[p])
                + (C.LABELLEDFULL[p])
                for p in voter_sorting
            ]
        )
        return dict(
            lan_en=(lan == "en"),
            maxslides=C.MAXSLIDES,
            nslide=player.current_page,
            page_title=(
                f"Political Opinions of Typical Voters"
                if lan == "en"
                else "Politische Meinungen Typischer Wähler/Wählerinnen"
            ),
            instruction_text=(
                f"Thinking about seven individuals, who represent the voters of each of the political parties in Germany – {partylist} –, how do you think each of them would respond to the political questions?"
                if lan == "en"
                else f"Denken Sie nun an sieben Personen, die repräsentativ für die Wähler und Wählerinnen der jeweiligen politischen Parteien in Deutschland – {partylist} – stehen. Wie würden Ihrer Meinung nach diese Personen jeweils die politischen Fragen beantworten?"
            ),
            contacts=voters,
            questions=questions,
            would_respond=(
                f"I think the responses of {pillname('these voters', "grey")} would be..."
                if lan == "en"
                else f"Ich denke, die Antworten {pillname('dieser Wähler/Wählerinnen', "#dddddd")} wären..."
            ),
            first_label=(
                "Strongly Disagree" if lan == "en" else "Stimme überhaupt nicht zu"
            ),  # Strongly Disagree
            neutral_label="Neutral" if lan == "en" else "Neutral",
            last_label=(
                "Strongly Agree" if lan == "en" else "Stimme voll und ganz zu"
            ),  # Strongly Agree
        )

    @staticmethod
    def get_form_fields(player: Player):
        fields = []
        for q in [C.QUS[i] for i in json.loads(player.question_sorting)]:
            for p in json.loads(player.voter_sorting):
                fields.append(f"{p.replace(' ', '')}_{q}")
        return fields

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.t_on_toc2 = int(time.time())
        player.current_page += 1

    @staticmethod
    def is_displayed(player: Player):
        return player.consent


#################################
#####  Play Practice Run   #####
#################################
class slide05a_MapGame(Page):
    form_model = "player"
    form_fields = ["positionsGame"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.positionsGame = player.positionsGame
        player.t_on_practice_page = int(time.time())
        player.current_page += 1

    @staticmethod
    def is_displayed(player):
        return player.consent

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        init_dots = [
            {
                "dottype": "food",
                "varname": "lasagne",
                "name_disp": ("Lasagne" if lan == "en" else "Lasagne"),
                "x": 330,
                "y": 50,
                "color": "#d97565   ",
            },
            {
                "dottype": "food",
                "varname": "pizza",
                "name_disp": "Pizza Margherita" if lan == "en" else "Pizza Margherita",
                "x": 330,
                "y": 100,
                "color": "#d97565",
            },
            {
                "dottype": "food",
                "varname": "spaghetticarbo",
                "name_disp": (
                    "Spaghetti Carbonara" if lan == "en" else "Spaghetti Carbonara"
                ),
                "x": 330,
                "y": 150,
                "color": "#d97565",
            },
        ]
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "dots": init_dots,
            "page_title": (
                "Political Mapping – Practice round 1"
                if lan == "en"
                else "Politische Karte – Übungsrunde 1"
            ),
            "lan": lan,
            "instruction_text2": (
                "Imagine you have to place the following meals – Lasagne, Spaghetti Carbonara, and Pizza Margherita – in a room (the rectangle below)."
                if lan == "en"
                else "Stellen Sie sich vor, Sie müssten die folgenden Gerichte – Lasagne, Spaghetti Carbonara und Pizza Margherita – in einem Raum platzieren (das Rechteck unten)."
            ),
            "instruction_text3": (
                "<p><ul><li><strong>Place meals closer together if you perceive them as similar.</strong></li><li><strong>Place meals farther apart if you perceive them as different.</strong></li></ul>"
                if lan == "en"
                else "<p><ul><li>Platzieren Sie Gerichte <strong>näher beieinander</strong>, wenn Sie diese als <strong>ähnlich</strong> wahrnehmen.</li><li>Platzieren Sie Gerichte <strong>weiter auseinander</strong>, wenn Sie diese als <strong>unterschiedlich</strong> wahrnehmen.</li></ul>"
            ),
            "detailed_instructions_1": (
                "<details><summary>Technical Instructions (if needed)</summary><ul><li>You will start with several points on the right side.</li><li>Drag these one by one into the rectangle and place them as described above.</li><li>You can re-position any dot at any time until you are satisfied with the arrangement.</li></ul>"
                if lan == "en"
                else "<details><summary>Technische Anleitung (falls benötigt)</summary><ul><li>Sie beginnen mit mehreren Punkten auf der rechten Seite.</li><li>Ziehen Sie diese nacheinander in das Rechteck und ordnen Sie die Punkte wie oben beschrieben an.</li><li>Sie können jeden Punkt verschieben bis Sie mit der Anordnung zufrieden sind.</li></ul></details>"
            ),
            "tomato": (
                "<em>Example:</em> A participant who dislikes tomatoes might arrange the dishes quite differently compared to a person, who dislikes meat"
                if lan == "en"
                else "<em>Beispiel:</em> Eine Person, die keine Tomaten mag, würde die Gerichte vermutlich anders anordnen als jemand, der kein Fleisch isst"
            ),
            "no_wrong_answers": (
                f"<ul><li>There are of course NO right or wrong answers here</li><li>We are interested in your <strong>personal perceptions</strong> in this survey</li></ul>"
                if lan == "en"
                else "<ul><li>Es gibt hier natürlich weder falsche noch richtige Antworten</li><li>Wir sind in dieser Umfrage ausschließlich an <strong>Ihrer persönlichen Einschätzung</strong> interessiert</li></ul>"
            ),
            "all_dots_instr": (
                "All dots must be within the square boundary to proceed."
                if lan == "en"
                else "Um fortzufahren müssen alle Punkte im Rechteck platziert werden."
            ),
        }


#################################
#####  Practice Run   #####
#################################
class slide05a_MapTest(Page):
    form_model = "player"
    form_fields = ["positionsTest"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.positionsTest = player.positionsTest

        t_on_results = json.loads(player.t_on_practiceResult_page)
        assert type(t_on_results) == dict
        t_on_results[player.attemptPractice] = int(time.time())
        player.t_on_practiceResult_page = json.dumps(t_on_results)

        player.attemptPractice += 1

    @staticmethod
    def is_displayed(player):
        return player.consent and (not player.isTrainingPassed)

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.attemptPractice == 0:
            init_dots = [
                {
                    "dottype": "self",
                    "varname": "self",
                    "name_disp": "Self" if lan == "en" else "Ich",
                    "x": 330,
                    "y": 50,
                    "color": "grey",
                },
                {
                    "dottype": "friend",
                    "varname": "friend",
                    "name_disp": "Friend" if lan == "en" else "Freund",
                    "x": 330,
                    "y": 100,
                    "color": "blue",
                },
                {
                    "dottype": "coworker",
                    "varname": "coworker",
                    "name_disp": "Co-Worker" if lan == "en" else "Kollegin",
                    "x": 330,
                    "y": 150,
                    "color": "blue",
                },
                {
                    "dottype": "relative",
                    "varname": "relative",
                    "name_disp": "Relative" if lan == "en" else "Verwandter",
                    "x": 330,
                    "y": 200,
                    "color": "blue",
                },
            ]
        else:
            init_dots = json.loads(getattr(player, "positionsTest", []))
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "dots": init_dots,
            "page_title": (
                "Political Mapping – Practice round 2"
                if lan == "en"
                else "Politische Karte – Übungsrunde 2"
            ),
            "lan": lan,
            "instruction_text1": (
                "In the <strong>second practice round</strong> we now focus on perception of political similarity."
                if lan == "en"
                else "In der <strong>zweiten Übungsrunde</strong> geht es nun um Wahrnehmungen politischer Ähnlichkeit."
            ),
            "instruction_text2": (
                "Imagine you, a friend, a co-worker, and your relative are in a room (the rectangle below)."
                if lan == "en"
                else "Stellen Sie sich vor, Sie sind zusammen mit einem Freund, einer Arbeitskollegin und einem Verwandten in einem Raum (das Rechteck unten)."
            ),
            "instruction_text3": (
                "<p>Arrange the people in the room based on how <em>you</em> see their political views:</p><ul><li><strong>Place individuals closer together if you perceive them as <em>politically</em> similar.</strong></li><li><strong>Place individuals farther apart if you perceive them as <em>politically</em> different.</strong></li></ul>"
                if lan == "en"
                else "<p>Ordnen Sie die Personen im Raum so an, wie <em>Sie</em> deren politische Ansichten wahrnehmen:</p><ul> <li>Platzieren Sie Personen <strong>näher beieinander</strong>, wenn Sie diese als <strong><em>politisch</em> ähnlich</strong> wahrnehmen.</li><li>Platzieren Sie Personen <strong>weiter auseinander</strong>, wenn Sie diese als <strong><em>politisch</em> unterschiedlich</strong> wahrnehmen.</li></ul>"
            ),
            "disclaimer": (
                "<p>This is a practice round – some arrangements match the instructions below, others do not. When you click <em>Next</em>, we will show you whether your arrangement meets all the instructions."
                if lan == "en"
                else "<p>Dies ist eine Übungsrunde – einige Anordnungen entsprechen den untenstehenden Anweisungen, andere nicht. Wenn Sie auf <em>Weiter</em> klicken, erfahren Sie, ob Ihre Anordnung alle Vorgaben erfüllt.</p>"
            ),  # In the main task on the next slide, there will be NO right or wrong answers — only your personal perception will matter.</p> #  Im Hauptteil auf der nächsten Seite wird es dagegegen KEINE richtigen oder falschen Antworten geben – nur Ihre persönliche Wahrnehmung wird relevant sein.
            "detailed_instructions_1": (
                "<h3>Practice Round Step-by-Step Instructions</h4><p>Drag the points on the right side one by one into the rectangle as described in the following instructions:</p>"
                if lan == "en"
                else "<h3>Übungsrunde Schritt-für-Schritt Anleitung</h4> <p>Ziehen Sie die Punkte auf der rechten Seite nacheinander in das Rechteck, wie in der folgenden Anleitung beschrieben:</p>"
            ),
            "detailed_instructions_2": (
                (
                    "<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Step 1:</strong> 'Self'</summary><p>Place the point <strong>Self</strong> somewhere within the rectangle – it represents your own political views.</p></details>"
                    + "<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Step 2:</strong> 'Friend'</summary><p>Place the point <strong>Friend</strong> near you – they share similar views.</p></details>"
                    + "<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Step 3:</strong> 'Co-worker'</summary><p>Place <strong>Co-worker</strong> farther away, as they often have different opinions – but closer to <strong>Self</strong> than to <strong>Friend</strong>, because you perceive an even greater political difference between Co-worker and Friend.</p></details>"
                    + "<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Step 4:</strong> 'Relative'</summary><p>Your <strong>Relative</strong> has very different political views – place them far from <strong>Self</strong>, but somewhat closer to <strong>Friend</strong> and <strong>Co-worker</strong>, as you feel they share some opinions with them.</p></details>"
                )
                if lan == "en"
                else (
                    "<details  open style='margin-bottom: 0em;'> <summary  style='white-space: nowrap;'><strong>Schritt 1:</strong> 'Ich'</summary> <p>Platzieren Sie den Punkt <strong>Ich</strong> irgendwo im Rechteck – er steht für Ihre politischen Ansichten.</p></details>"
                    + "<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Schritt 2:</strong> 'Freund'</summary><p>Setzen Sie den Punkt <strong>Freund</strong> in Ihre Nähe – er teilt ähnliche Ansichten wie Sie.</p></details>"
                    + "<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Schritt 3:</strong> 'Kollegin'</summary><p>Platzieren Sie <strong>Kollegin</strong> weiter entfernt, da sie oft anderer Meinung als Sie ist – aber näher bei <strong>Ich</strong> als bei <strong>Freund</strong>, weil Sie zwischen der Kollegin und dem Freund einen noch größeren politischen Unterschied wahrnehmen.</p></p></details>"
                    + "<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Schritt 4:</strong> 'Verwandter'</summary><p>Der <strong>Verwandte</strong> denkt politisch ganz anders – setzen Sie ihn weit weg von <strong>Ich</strong>, aber etwas näher an <strong>Freund</strong> und <strong>Kollegin</strong>, da Sie finden, dass der Verwandte in manchen Punkten deren Ansichten teilt.</p></details>"
                )
            ),
            "all_dots_instr": (
                "All dots must be within the square boundary to proceed. You can re-position any dot at any time until you are satisfied with the arrangement."
                if lan == "en"
                else "Um fortzufahren müssen alle Punkte im Rechteck platziert werden. Sie können jeden Punkt verschieben bis Sie mit der Anordnung zufrieden sind."
            ),
            "latest_error_msg": (
                "<p><strong>Error(s) in your previous attempt:</strong></p>"
                if lan == "en"
                else "<p><strong>Fehler in Ihrem vorherigen Versuch:</strong></p>"
            )
            + player.latest_error_msg,
            "show_error_msg": player.attemptPractice > 0,
        }


#################################
#####  Practice Run Results   #####
#################################
class slide05b_MapTestResult(Page):

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language

        pos = json.loads(player.positionsTest)
        pos = {p["varname"]: [p["x"], p["y"]] for p in pos}
        # calculate distances
        dF = distance(pos["self"], pos["friend"])
        dC = distance(pos["self"], pos["coworker"])
        dR = distance(pos["self"], pos["relative"])
        dFR = distance(pos["friend"], pos["relative"])
        dFC = distance(pos["friend"], pos["coworker"])
        dCR = distance(pos["coworker"], pos["relative"])
        # check conditions
        player.isTrainingCondFvC = bool(dF < dC)  # Rule 2
        player.isTrainingCondSelfvFC = bool(dFC > dC)  # Rule 3
        player.isTrainingCondRvF = bool(dR > dF)  # Rule 4
        player.isTrainingCondRvFC = bool((dFR < dR) and (dCR < dR))  # Rule 6.
        isTrainingPassed = (
            player.isTrainingCondFvC
            & player.isTrainingCondSelfvFC
            & player.isTrainingCondRvFC
            & player.isTrainingCondRvF
        )
        player.isTrainingPassed = isTrainingPassed

        errors = ""
        if lan == "en":
            errors += (
                r"- <em>Instructions 2/3: </em> The distance between 'Self' and 'Co-worker' should be larger than the distance between 'Self' and 'Friend'. <br>"
                if player.isTrainingCondFvC == 0
                else ""
            )
            errors += (
                r"- <em>Instruction 2/3: </em> The distance between 'Friend' and 'Co-worker' should be larger than the distance between 'Self' and 'Co-worker'. <br>"
                if player.isTrainingCondSelfvFC == 0
                else ""
            )
            errors += (
                r"- <em>Instruction 4: </em> The distance between 'Self' and 'Relative' should be larger than the distance between 'Self' and 'Friend'. <br>"
                if player.isTrainingCondRvF == 0
                else ""
            )
            errors += (
                r"- <em>Instruction 4: </em> The distance between 'Self' and 'Relative' should be larger than the distances between 'Friend' and 'Relative' and between 'Co-worker' and 'Relative'. <br>"
                if player.isTrainingCondRvFC == 0
                else ""
            )
        else:
            errors += (
                r"- <em>Schritt 2/3: </em> Die Distanz zwischen 'Ich' und 'Kollegin' sollte größer sein als die Distanz zwischen 'Ich' und 'Freund'. <br>"
                if player.isTrainingCondFvC == 0
                else ""
            )
            errors += (
                r"- <em>Schritt 2/3: </em>Die Distanz zwischen 'Freund' und 'Kollegin' sollte größer sein als die Distanz zwischen 'Ich' und 'Kollegin'. <br>"
                if player.isTrainingCondSelfvFC == 0
                else ""
            )
            errors += (
                r"- <em>Schritt 4: </em> Die Distanz zwischen 'Ich' und 'Verwandter' sollte größer sein als die Distanz zwischen 'Ich' und 'Freund'. <br>"
                if player.isTrainingCondRvF == 0
                else ""
            )
            errors += (
                r"- <em>Schritt 4: </em> Die Distanz zwischen 'Ich' und 'Verwandter' sollte größer sein als die Distanzen zwischen 'Freund' und 'Verwandter' sowie 'Kollegin' und 'Verwandter'. <br>"
                if player.isTrainingCondRvFC == 0
                else ""
            )

        player.latest_error_msg = errors

        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "passed": player.isTrainingPassed,
            "button_msg": (
                (
                    "Continue"
                    if player.isTrainingPassed
                    else (
                        "Continue Anyway"
                        if player.attemptPractice == C.N_MAX_PRACTICE_RUNS
                        else "Repeat Training"
                    )
                )
                if lan == "en"
                else (
                    "Weiter"
                    if player.isTrainingPassed
                    else (
                        "Trotzdem weiter"
                        if player.attemptPractice == C.N_MAX_PRACTICE_RUNS
                        else "Wiederhole Training"
                    )
                )
            ),
            "attempt_msg": (
                f"Attempt {player.attemptPractice} of {C.N_MAX_PRACTICE_RUNS}"
                if lan == "en"
                else f"Versuch {player.attemptPractice} von {C.N_MAX_PRACTICE_RUNS}"
            ),
            "page_title": (
                "Political Mapping – Practice round 2 – Results"
                if lan == "en"
                else "Politische Karte – Übungsrunde 2 – Ergebnis"
            ),
            "success_msg": (
                "<strong>Well done!</strong> Your arrangement fulfills all criteria."
                if lan == "en"
                else "<strong>Gut gemacht!</strong> Ihre Anordnung der Punkte erfüllt alle Kriterien."
            ),
            "error_msg": (
                f"<strong>Your arrangement does not meet all steps of the instructions:</strong></p><p style='white-space: pre-line;'>{errors}</p><p>Please repeat the training and try to arrange the dots so that all criteria are fulfilled.</p>"
                if lan == "en"
                else f"<strong>Ihre Anordnung erfüllt nicht alle Schritte der Anleitung:</strong></p><p style='white-space: pre-line;'>{errors}</p><p>Bitte wiederholen Sie das Training und versuchen Sie, die Punkte so anzuordnen, dass alle Kriterien erfüllt sind.</p>"
            ),
            "img_help": not (player.attemptPractice <= 1 or player.isTrainingPassed),
            "img_help_text": "<p>"
            + (
                "Below you can find one possible arrangement of the dots that fulfills all criteria:"
                if lan == "en"
                else "Unten sehen Sie eine mögliche Anordnung der Punkte, die alle Kriterien erfüllt:"
            )
            + ":</p>",
            "img_source": f"correctTraining_{lan}.png",
        }

    @staticmethod
    def is_displayed(player: Player):
        return (
            player.consent
            and (player.attemptPractice <= C.N_MAX_PRACTICE_RUNS)
            and (
                (not player.isTrainingPassed)
                or (player.isTrainingPassed and player.attemptPractice == 0)
            )
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.t_on_map_page = int(time.time())
        if player.isTrainingPassed:
            player.current_page += 1


#################################
#####  Spatial Arrangement Mapping   #####
#################################
class slide06_SPaM(Page):
    form_model = "player"
    form_fields = ["positions"]

    @staticmethod
    def before_next_page(player, timeout_happened):

        valid_pairs = json.loads(player.valid_pairs)
        valid_pairs = [tuple(v) for v in valid_pairs]
        dots = json.loads(player.positions)
        dotpos = {p["varname"]: np.array([p["x"], p["y"]]) for p in dots}
        dotnames = list(dotpos.keys())
        pairs = list(combinations(dotnames, 2))
        dists = [distance(dotpos[d1], dotpos[d2]) for d1, d2 in pairs]
        fixedPairs = []
        min_pair = pairs[np.argmin(dists)]
        if not min_pair in C.FORCED_PAIRS:
            fixedPairs.append(min_pair)
            if min_pair in valid_pairs:
                valid_pairs.remove(min_pair)
        max_pair = pairs[np.argmax(dists)]
        if not max_pair in C.FORCED_PAIRS:
            fixedPairs.append(max_pair)
            if max_pair in valid_pairs:
                valid_pairs.remove(max_pair)
        player.min_pair = json.dumps(min_pair)
        player.max_pair = json.dumps(max_pair)
        fixedPairs.extend(C.FORCED_PAIRS)
        random.shuffle(valid_pairs)
        pairSequence = (
            fixedPairs + valid_pairs[: (C.NR_PAIRWISE_CHECKS - len(fixedPairs))]
        )
        random.shuffle(pairSequence)
        player.pairSequence = json.dumps(pairSequence)

        dots_t_first_moved = [d["t_first_moved"] for d in dots]
        player.t_firstDotMoved = min(dots_t_first_moved)
        player.t_on_toc3 = int(time.time())
        player.current_page += 1

    @staticmethod
    def is_displayed(player: Player):
        return player.consent & player.isTrainingPassed

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        displ_names = (
            ["Self" if lan == "en" else "Ich"]
            + [getattr(player, f"contact{f}") for f in range(1, C.NCONTACTS + 1)]
            + [
                f"{v+' voter' if lan=='en' else C.LABELLED_de[v]+' Wähler/Wählerin'}"
                for v in C.LABELLED
            ]
        )
        types = (
            ["self"] + ["contact"] * C.NCONTACTS + ["labelledPerson"] * len(C.LABELLED)
        )
        varnames = (
            ["self"]
            + [f"contact{f}" for f in range(1, C.NCONTACTS + 1)]
            + [f"{v}" for v in C.LABELLED]
        )
        init_dots = [
            {
                "dottype": dottype,
                "varname": varname,
                "name_disp": name,
                "x": 376 + 80 * (dottype == "labelledPerson"),
                "y": 32
                + (i - (dottype == "labelledPerson") * (C.NCONTACTS + 0.45)) * 42,
                "descr": "",
                "t_first_moved": -1,
                "t_last_moved": -1,
            }
            for i, (dottype, varname, name) in enumerate(
                zip(types, varnames, displ_names)
            )
        ]
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "dots": init_dots,
            "canvas_height": C.CANVAS_WIDTH,
            "canvas_width_parkingLot": C.CANVAS_WIDTH + 170,
            "page_title": (
                "Your Personal Political Map"
                if lan == "en"
                else "Ihre Persönliche Politische Karte"
            ),
            "instru1": (
                "We now continue to the main task in this survey."
                if lan == "en"
                else "Wir beginnen nun mit dem Hauptteil dieser Umfrage."
            ),
            "instruRoom": (
                "Imagine you, your social contacts, and typical voters of the German parties are in a room (the rectangle below)."
                if lan == "en"
                else "Stellen Sie sich vor, Sie sind zusammen mit Ihren Kontakten und mit jeweils den typischen Wählern oder Wählerinnen der vorher genannten Parteien in einem Raum (das Rechteck unten)."
            ),
            "instru_main": (
                "<p>Arrange the people in the room based on how <em>you</em> see their political views about questions regarding climate change, migration, inequality and diversity:</p><ul><li><strong>Place individuals closer together if you perceive them as politically similar.</strong></li><li><strong>Place individuals farther apart if you perceive them as politically different.</strong></li></ul>"
                if lan == "en"
                else "<p>Ordnen Sie die Personen im Raum so an, wie <em>Sie</em> deren politische Ansichten zu Fragen über Klimawandel, Migration, Ungleichheit und Vielfalt wahrnehmen:</p><ul> <li>Platzieren Sie Personen <strong>näher beieinander</strong>, wenn Sie diese als <strong>politisch ähnlich</strong> wahrnehmen.</li><li>Platzieren Sie Personen <strong>weiter auseinander</strong>, wenn Sie diese als <strong>politisch unterschiedlich</strong> wahrnehmen.</li></ul>"
            ),
            "no_wrong_answers": (
                f"<p>There are NO right or wrong answers — we are interested in your personal perception.</p>"
                if lan == "en"
                else "<p>Es gibt weder falsche noch richtige Antworten – wir sind an Ihrer persönliche Einschätzung interessiert.</p>"
            ),
            # "instru_click": (
            #     "<summary style='white-space: nowrap;'><strong>Helping lines</strong></summary>If you want you can activate helping lines. When you click on one of the dots, circles will appear that might help you evaluate how well your arrangement reflects your sense of political similarity. You can scale the circles by moving the small arrows <strong><></strong>."
            #     if lan == 'en'
            #     else "<summary style='white-space: nowrap;'><strong>Hilfslinien</strong></summary>Wenn Sie möchten, können Sie unten Hilfslinien aktivieren: Beim Klicken auf einen Punkt erscheinen Kreis, die Ihnen dabei helfen könnten einzuschätzen, wie gut Ihre Anordnung Ihre Wahrnehmung politischer Ähnlichkeit widerspiegelt. Die Kreise lassen sich über die kleinen Pfeile <strong><></strong> skalieren."
            # ),
            "all_dots_instr": (
                "All dots must be within the square boundary to proceed. You can re-position any dot at any time until you are satisfied with the arrangement."
                if lan == "en"
                else "Um fortzufahren müssen alle Punkte im Rechteck platziert werden. Sie können jeden Punkt verschieben bis Sie mit der Anordnung zufrieden sind."
            ),
            # "labelClose": "similar" if lan == 'en' else "ähnlich",
            # "labelFar": "different" if lan == 'en' else "unterschiedlich",
            # "helping_lines": (
            #     "Show helping lines" if lan == 'en' else "Hilfslinien anzeigen"
            # ),
        }


#################################
#####  Pairwise similiarty ratings   #####
#################################
class slide08_PlausibilityCheck_Pairs(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return (
            (player.consent)
            and (player.n_check <= (player.n_checks))
            and player.isTrainingPassed
        )

    @staticmethod
    def get_form_fields(player: Player):
        i = player.n_check
        return [f"similarityPair{i}"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.n_check == 1:
            player.t_after_first_check = int(time.time())
        player.n_check += 1
        if player.n_check == player.n_checks:
            player.t_on_importance = int(time.time())
            player.current_page += 1

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language

        def get_descr(p):
            if "contact" in p:
                plabel = (
                    f"your contact <span class='pill' style='background-color: {C.FRIENDCOLOR}; color: white;'><strong>"
                    if lan == "en"
                    else f"Ihr Kontakt <span class='pill' style='background-color: {C.FRIENDCOLOR}; color: white;'><strong>"
                )
                plabel += f"{getattr(player, p)}</strong></span>"
            elif p == "self":
                plabel = (
                    f"<span class='pill' style='background-color: #808080; color: white;'><strong>yourself</strong></span>"
                    if lan == "en"
                    else f"<span class='pill' style='background-color: #808080; color: white;'><strong>Sie selbst</strong></span>"
                )
            elif p in C.LABELLED:
                plabel = (
                    f"a typical <span class='pill' style='background-color: {C.LABELLEDCOLORS[p]}; color: {'white' if not p=='FDP' else '#424949'};'><strong>{p} voter</strong></span>"
                    if lan == "en"
                    else f"eine typische Person, die <span class='pill' style='background-color: {C.LABELLEDCOLORS[p]}; color: {'white' if not p=='FDP' else '#424949'};'><strong>{C.LABELLED_de[p]} wählt</strong></span>"
                    # {'die ' if p=='Green Party' or p=='Left Party' else ''}
                )
            else:
                print(p)
            return plabel

        pairSequence = json.loads(player.pairSequence)
        pair = pairSequence[player.n_check - 1]
        p1, p2 = (pair[0], pair[1]) if np.random.random() < 0.5 else (pair[1], pair[0])
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "p1": p1,
            "p2": p2,
            "current_check": f"similarityPair{player.n_check}",
            "page_title": (
                f"Pairwise comparison of political views – {player.n_check} of {player.n_checks}"
                if lan == "en"
                else f"Paarweiser Vergleich politischer Meinungen {player.n_check} von {player.n_checks}"
            ),
            "instru1": (
                f"<p>Now consider the following pair of individuals:</p>"
                if lan == "en"
                else f"<p>Denken Sie nun an die jeweils folgenden beiden Personen:</p>"
            ),
            "instru2": (
                f"<ol><li style='font-size:18px;'>{get_descr(p1)}</li><li style='font-size:18px;'>{get_descr(p2)}</li></ol>"
                if lan == "en"
                else f"<ol><li style='font-size:18px;'>{get_descr(p1)}</li><li style='font-size:18px;'>{get_descr(p2)}</li></ol>"
            ),
            "question": (
                "<p>In <em>your</em> opinion, how similar are these two individuals overall in their political views on migration, climate change, inequality and diversity?</p>"
                if lan == "en"
                else "<p>Wie ähnlich sind sich diese beiden Personen <em>Ihrer Meinung nach</em> insgesamt in ihren politischen Ansichten zu Migration, Klimawandel, Ungleichheit und Vielfalt?</p>"
            ),
            # "Ithink": "",  # "Your estimate:" if lan == 'en' else "Ihre Einschätzung:",
            # "img1": p1_dot["dottype"] == "P",
            # "img2": p2_dot["dottype"] == "P",
            # "choices": list(range(0, 11)),
            "similarity_min": 0,
            "similarity_max": 100,
            "similarity_min_label": (
                # "Extremely different" if lan == "en" else "Extrem unterschiedlich"
                "Not at all similar"
                if lan == "en"
                else "Überhaupt nicht ähnlich"
            ),
            # "similarity_neutral_label": ("Neutral" if lan == "en" else "Neutral"),
            "similarity_max_label": (
                "Extremely similar" if lan == "en" else "Extrem ähnlich"
            ),
            "completedPairs": player.n_check - 1,
            "final": player.n_check == player.n_checks,
            "pairs": pairSequence,
            "pair_indices": list(range(player.n_checks)),
        }


class slide09_Importance(Page):
    form_model = "player"
    form_fields = [f"importance_{q}" for q in C.QUS] + ["importance_comments"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.t_on_satisfaction = int(time.time())
        player.current_page += 1

    @staticmethod
    def is_displayed(player: Player):
        return player.consent and player.isTrainingPassed

    @staticmethod
    def vars_for_template(player):
        lan = player.language
        questions = [C.QUS[i] for i in json.loads(player.question_sorting)]
        fields = [f"importance_{q}" for q in questions]
        questions = [C.QUESTIONNAMES[player.language][q] for q in questions]

        field_question_pairs = []
        for field, question in zip(fields, questions):
            field_question_pairs.append(
                {
                    "field_name": field,
                    "question_text": question,
                    "first_label": (
                        "not important at all"
                        if lan == "en"
                        else "überhaupt nicht wichtig"
                    ),  # Strongly Disagree
                    "last_label": (
                        "extremely important" if lan == "en" else "extrem wichtig"
                    ),  # Strongly Agree
                    # "choices": dict(
                    #    zip(np.arange(0, 101), np.arange(0, 101))
                    # ),  # dict(zip(range(1, 8), labels)),  # 1-7 mapping
                }
            )
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "field_question_pairs": field_question_pairs,
            "page_title": (
                "Key Political Topics for You"
                if lan == "en"
                else "Wichtige Politische Themen für Sie"
            ),
            "table_head": (
                "Importance of topics for you"
                if lan == "en"
                else "Wichtigkeit der Themen für Sie"
            ),
            "question": (
                "Please rate how <b>important</b> each of the four political topics was when you evaluated the political similarity of individuals or arranged the dots in the square!"
                if lan == "en"
                else "Bitte schätzen Sie wie <b>wichtig</b> jedes der vier politischen Themen für Sie war als Sie die politische Ähnlichkeit der Personenpaare bewertet bzw. als Sie die jeweiligen Punkte im Viereck platziert haben!"
            ),
            "explain_text": (
                "You can add further comments or explanations here (optional):"
                if lan == "en"
                else "Sie können hier weitere Anmerkungen oder Erklärungen hinzufügen (optional):"
            ),
        }


#################################
#####  Overall Satisfaction with Map   #####
#################################
class slide10_Satisfaction(Page):
    form_model = "player"
    form_fields = ["satisfaction_text", "satisfaction", "accurateMapping"]

    @staticmethod
    def is_displayed(player: Player):
        return player.consent and player.isTrainingPassed

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        questions = [C.QUS[i] for i in json.loads(player.question_sorting)]

        def get_ops(prefix, questions):
            return {q: getattr(player, f"{prefix}{q}", "NA") or "NA" for q in questions}

        def format_ops(ops_dict, lan):
            return "; ".join(
                f"{C.QUESTIONSHORTTEXT[lan][q]}: {val if lan=='en' else val }"
                for q, val in ops_dict.items()
            )

        pos = json.loads(player.positions) if player.positions else []

        # Write dot descriptions of Self, Contacts, Labelled, and past Personas
        # p_ops = json.loads(player.ps)
        dot_descrs = {
            "self": format_ops(
                get_ops(
                    "own_", [C.QUS[i] for i in json.loads(player.question_sorting)]
                ),
                lan,
            )
        }
        for f in range(1, C.NCONTACTS + 1):
            dot_descrs[f"contact{f}"] = format_ops(
                get_ops(f"contact{f}_", questions), lan
            )
        for v in C.LABELLED:
            dot_descrs[f"{v}"] = format_ops(
                get_ops(f"{v.replace(' ','')}_", questions), lan
            )
        # for currP in json.loads(player.ps).keys():
        #     currP_op = [p_ops[currP][q] for q in questions]
        #     currP_op = ["" if str(op) == "nan" else op for op in currP_op]
        #     dot_descrs[currP] = "; ".join(
        #         [
        #             f"{C.QUESTIONSHORTTEXT[lan][q]}: {op if lan=='en' else op}"
        #             for q, op in zip(questions, currP_op)
        #         ]
        #     )

        # Prepare initial dot data
        init_dots = [
            {
                "varname": p["varname"],
                "name_disp": p["name_disp"],
                "x": p["x"],
                "y": p["y"],
                "dottype": p["dottype"],
                "descr": dot_descrs.get(p["varname"], ""),
            }
            for p in pos
        ]
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "dots": init_dots,
            "page_title": (
                "Overall satisfaction with your map"
                if lan == "en"
                else "Zufriedenheit mit Ihrer Anordnung"
            ),
            "instru1": (
                "Below we show the political map you created."
                if lan == "en"
                else "Im Folgenden finden Sie die von Ihnen erstellte persönliche politische Karte."
            ),
            "instru2": (
                "Note: If you click on one of the dots in the square, a popup will appear that shows how you evaluated that person's probable answers to the political questions."
                if lan == "en"
                else "Hinweis: Wenn Sie auf einen der Punkte im Rechteck klicken, erscheint ein Fenster, dass Ihnen zeigt, wie Sie die wahrscheinlichen Antworten dieser Person auf die politische Fragen eingeschätzt haben."
            ),
            "question": (
                "<p>How satisfied are you with your arrangement? </p>"
                if lan == "en"
                else "<p>Wie zufrieden sind Sie mit Ihrer Anordnung?</p>"
            ),
            "questionaccurateMapping": (
                "<p>Does the arrangement reflect how you perceive the political similarities and differences between the individuals?</p>"
                if lan == "en"
                else "<p>Spiegelt Ihre Anordnung Ihre Wahrnehmung der politischen Ähnlichkeiten und Unterschiede der Personen wider?</p>"
            ),
            "explain_text": (
                "If you would like, you can add further comments or explanations here (optional):"
                if lan == "en"
                else "Falls Sie möchten, können Sie hier weitere Anmerkungen oder Erklärungen hinzufügen (optional):"
            ),
            # "choices": list(range(0, 11)),
            "satisfaction_canvas_width": 400,
            "canvas_width": C.CANVAS_WIDTH,
            "satisfaction_min": 0,
            "satisfaction_max": 100,
            "satisfaction_min_label": (
                "Not satisfied at all (0)" if lan == "en" else "Gar nicht zufrieden (0)"
            ),
            "satisfaction_max_label": (
                "Very satisfied (10)" if lan == "en" else "Sehr zufrieden (10)"
            ),
            "acc_min": 0,
            "acc_max": 100,
            "acc_min_label": (
                "Not accurate at all (0)"
                if lan == "en"
                else "Trifft überhaupt nicht zu (0)"
            ),
            "acc_max_label": (
                "Completely accurate (10)"
                if lan == "en"
                else "Trifft voll und ganz zu (10)"
            ),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.t_on_relationships = int(time.time())
        player.current_page += 1


#################################
#####  Social Relationships   #####
#################################
class slide11_Relationships(Page):
    form_model = "player"
    form_fields = [f"contact{n}_socialCloseness" for n in range(1, C.NCONTACTS + 1)]

    @staticmethod
    def is_displayed(player: Player):
        return player.consent and player.isTrainingPassed

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        # fields = [f"contact{n}_socialCloseness" for n in range(1, C.NCONTACTS + 1)]
        contacts = [
            {
                "id": f"contact{i}",
                "name": (
                    f"Your relation with <span class='pill' style='background-color: {C.FRIENDCOLOR}; color: white;'><strong>{getattr(player, f'contact{i}')}</strong></span>"
                    if lan == "en"
                    else f"Ihre Beziehung zu <span class='pill' style='background-color: {C.FRIENDCOLOR}; color: white;'><strong>{getattr(player, f'contact{i}')}</strong></span>"
                ),
            }
            for i in range(1, C.NCONTACTS + 1)
        ]

        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "color": C.FRIENDCOLOR,
            "page_title": (
                "<em>Social</em> Closeness to the named people"
                if lan == "en"
                else "<em>Soziale</em> Nähe zu den genannten Personen"
            ),
            "contacts": contacts,
            "qu_closeness": (
                "How would you rate in general the closeness of the social relationship between you and the individuals you named previously – regardless of political views?"
                if lan == "en"
                else "Wie würden Sie allgemein die Nähe der sozialen Beziehung zwischen Ihnen und den Personen, die sie genannt haben, einschätzen – unabhängig von politischen Ansichten? "
            ),
            "disclaimer": (
                "All your responses are linked to generic names <em>Person 1</em>, <em>Person 2</em>, etc. To protect privacy, we do <strong>not store</strong> the actual names or initials."
                if lan == "en"
                else "Alle Ihre Antworten werden generischen Bezeichnungen wie <em>Person 1</em>, <em>Person 2</em> usw. zugeordnet. Zum Schutz der Privatsphäre werden die von Ihnen angegebenen Namen oder Initialen <strong>nicht gespeichert</strong>.."
            ),
            "closeness_min": 0,
            "closeness_max": 100,
            "closeness_min_label": (
                "Not particularly close" if lan == "en" else "Nicht besonders nah"
            ),
            "closeness_max_label": "Extremely close" if lan == "en" else "Extrem nah",
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.t_on_demographics = int(time.time())
        player.current_page += 1


#################################
#####  Demographics   #####
#################################
class slide12_Demographics(Page):
    form_model = "player"
    form_fields = [
        "age",
        "political_interest",
        "how_polarised",
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.consent and player.isTrainingPassed

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "page_title": (
                "Final questions" if lan == "en" else "Abschließende Fragen"
            ),
            "qu_age": "How old are you?" if lan == "en" else "Wie alt sind Sie?",
            "qu_interest": (
                "How interested would you say you are in politics – are you..."
                if lan == "en"
                else "Wie sehr sind Sie persönlich an Politik interessiert? Sind Sie ...?"
            ),
            "interest_min": 0,
            "interest_max": 100,
            "interest_min_label": (
                "Not at all interested"
                if lan == "en"
                else "Überhaupt nicht interessiert"
            ),
            "interest_max_label": (
                "Very interested" if lan == "en" else "Sehr interessiert"
            ),
            "polarised_min": 0,
            "polarised_max": 100,
            "polarised_min_label": (
                "Not at all divided" if lan == "en" else "Überhaupt nicht gespalten"
            ),
            "polarised_max_label": (
                "Extremely divided" if lan == "en" else "Extrem gespalten"
            ),
            "qu_polarization": (
                "What do you think: How politically divided are the people in your country these days?"
                if lan == "en"
                else "Was denken Sie: Wie politisch gespalten sind die Menschen in Ihrem Land heutzutage?"
            ),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.t_on_success = int(time.time())
        player.completed = True
        player.current_page += 1


#################################
#####  Success   #####
#################################
class slideSuccess(Page):
    form_model = "player"
    form_fields = ["completed"]

    @staticmethod
    def vars_for_template(player: Player):
        return {
            "lan_en": player.language == "en",
        }

    def is_displayed(player: Player):
        return player.consent and player.isTrainingPassed


#################################
#####  Fail   #####
#################################
class slideFail(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return (not player.consent) or (not player.completed)

    @staticmethod
    def vars_for_template(player: Player):
        return {"lan_en": player.language == "en"}


#################################
#####  SEQUENCE   #####
#################################
page_sequence = (
    [
        slide01_Introduction,
        slide02_Opinions,
        slide02a_Identity,
        slide00_toc,
        slide03_Contacts,
    ]
    # + [slide04_PersonOpinion] * (C.NCONTACTS + len(C.LABELLED))
    + [slide04_ContactsOpinions]  # * C.N_BATCHES
    + [slide04b_VotersOpinions]
    + [slide00_toc]
    + [slide05a_MapGame]
    + [slide05a_MapTest, slide05b_MapTestResult] * C.N_MAX_PRACTICE_RUNS
    + [slide06_SPaM]
    # + [slide07_SPaM_personas] * C.NPS_MAX
    + [slide00_toc]
    + [slide08_PlausibilityCheck_Pairs] * C.NR_PAIRWISE_CHECKS
    + [
        slide09_Importance,
        slide10_Satisfaction,
        slide11_Relationships,
        slide12_Demographics,
        slideSuccess,
        slideFail,
    ]
)

# print("Total slides: ", len(page_sequence), 3+C.NCONTACTS+len(C.LABELLED)+2+1+1+1+1+4)
