from otree.api import *
import json
import pandas as pd
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

    LIKERT7_string_noNA = [
        "Strongly Disagree",
        "Disagree",
        "Somewhat Disagree",
        "Neutral",
        "Somewhat Agree",
        "Agree",
        "Strongly Agree",
    ]
    LIKERT7_string_noNA_de = [
        "Stimme überhaupt nicht zu",
        "Stimme nicht zu",
        "Stimme eher nicht zu",
        "Neutral",
        "Stimme eher zu",
        "Stimme zu",
        "Stimme voll und ganz zu",
    ]
    # LIKERT5_string_noNA = [
    #     "Strongly agree",
    #     "Agree",
    #     "Neutral",
    #     "Disagree",
    #     "Strongly disagree",
    # ]
    # LIKERT5_string_noNA_de = [
    #     "Stimme voll und ganz zu",
    #     "Stimme eher zu",
    #     "Teils/teils",
    #     "Stimme eher nicht zu",
    #     "Stimme überhaupt nicht zu",
    # # ]
    # LIKERT5_transde = dict(zip(LIKERT5_string_noNA, LIKERT5_string_noNA_de))
    # LIKERT5_transde["NA"] = "NA"
    # LIKERT5_transde[""] = ""

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
                    "The differences in income and in wealth in Germany are too high.",
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

    NCONTACTS = 3  # 6
    FRIENDCOLOR = "#ff6600"
    LABELLED = ["Green Party", "AfD", "FDP", "Left Party", "CDU/CSU", "SPD", "BSW"]
    LABELLED_de = dict(
        zip(LABELLED, ["Grünen", "AfD", "FDP", "Linken", "CDU/CSU", "SPD", "BSW"])
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
    LABELLED = list(np.random.choice(LABELLED, replace=False, size=len(LABELLED)))

    NLABELLED = len(LABELLED)
    MAXSLIDES = 5 + NLABELLED + NCONTACTS + 2 + 8

    # NPS_MAX = 8

    # NR_P_CHECKS = 0
    # OPTIONS_P_CHECKS = [
    #     "<strong>Strongly disagree.</strong><br>This does not reflect my views at all.",
    #     "<strong>Disagree.</strong><br>It somewhat misrepresents my views.",
    #     "<strong>Neutral.</strong><br>I neither agree nor disagree.",
    #     "<strong>Agree.</strong><br>This mostly reflects my views.",
    #     "<strong>Strongly agree.</strong><br>This accurately reflects my views.",
    # ]
    # OPTIONS_P_CHECKS_DE = [
    #     "Trifft überhaupt nicht zu",
    #     "Trifft eher nicht zu",
    #     "Trifft eher zu",
    #     "Trifft voll und ganz zu",
    # ]
    # OPTIONS_P_CHECKS = [
    #     "Not accurate at all",
    #     "Mostly not accurate",
    #     "Mostly accurate",
    #     "Completely accurate",
    # ]

    NR_PAIRWISE_CHECKS = 1 + 6 + 7 + 4 + 4
    # OPTIONS_OTHER_CHECKS = list(range(0, 11))
    # CHOICES_TOPICS = [qname for q, qname in QUESTIONNAMES["en"].items()] + [
    #     "Were there any other topics or relevant factors? Please write them in the text box below."
    # ]
    CHOICES_INTEREST = [
        "Not at all interested",
        "Hardly interested",
        "Quite interested",
        "Very interested",
    ]

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

    CHOICES_POLARISED = [
        "Not at all divided",
        "Somewhat divided",
        "Very divided",
        "Extremely divided",
    ]

    OPTIONS_CONTACTS_CLOSE = [
        "Not particularly close",
        "Somewhat close",
        "Close",
        "Very close",
        "No answer",
    ]

    CHOICES_SATISFACTION_DE = [
        "Trifft überhaupt nicht zu",
        "Trifft eher nicht zu",
        "Trifft eher zu",
        "Trifft voll und ganz zu",
    ]
    CHOICES_SATISFACTION = [
        "Not accurate at all",
        "Mostly not accurate",
        "Mostly accurate",
        "Completely accurate",
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_field(label, language="en"):
    return models.StringField(
        choices=[[i, i] for i in np.arange(-100, 101)],
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

    language = models.StringField(
        choices=[["en", "English"], ["de", "Deutsch"]],
        widget=widgets.RadioSelect,
        label="Language / Sprache",
    )

    age = models.IntegerField(label="", min=18, max=100)

    political_interest = models.StringField(
        label="", choices=C.CHOICES_INTEREST, blank=False, widget=widgets.RadioSelect
    )

    feel_closest_party = models.StringField(
        label="", choices=C.CHOICES_IDENTITY, blank=False, widget=widgets.RadioSelect
    )

    lrscale = models.IntegerField(
        choices=[[i, i] for i in np.arange(0, 10.1, 1)],
        label="lrscale",
        widget=widgets.RadioSelect,
    )
    # is_secondclosest_party = models.BooleanField(
    #     label="", blank=False, widget=widgets.RadioSelect
    # )

    # feel_secondclosest_party = models.StringField(
    #     label="", choices=C.CHOICES_IDENTITY, blank=False, widget=widgets.RadioSelect
    # )

    party_comment = models.LongStringField(label="", blank=True)

    how_polarised = models.StringField(
        label="", choices=C.CHOICES_POLARISED, blank=False, widget=widgets.RadioSelect
    )

    # topic_importance = models.LongStringField(
    #     label="",
    #     blank=True,
    # )
    
    importance_comments = models.LongStringField(
        blank=True, label="", initial="", null=True
    )

    #################################
    #####  TIME   #####
    #################################
    t_on_intro = models.IntegerField(blank=True)
    t_on_opinion = models.IntegerField(blank=True)
    t_on_identity = models.IntegerField(blank=True)
    visited_toc = models.IntegerField(blank=False, initial=0)
    t_on_toc1 = models.IntegerField(blank=True)
    t_on_contacts = models.IntegerField(blank=True)
    t_on_personOpinion = models.LongStringField(blank=True, initial="{}")
    t_on_toc2 = models.IntegerField(blank=True)
    t_on_practiceGame_page = models.IntegerField(blank=True)
    t_on_practice_page = models.IntegerField(blank=True)
    t_on_practiceResult_page = models.LongStringField(blank=True, initial="{}")
    t_on_map_page = models.IntegerField(blank=True)
    # t_on_mapP_page = models.IntegerField(blank=True)
    t_on_toc3 = models.IntegerField(blank=True)
    t_on_check_page = models.IntegerField(blank=True)
    t_after_first_check = models.IntegerField(blank=True)
    t_after_last_check = models.IntegerField(blank=True)
    t_on_importance = models.IntegerField(blank=True)
    t_on_satisfaction = models.IntegerField(blank=True)
    t_on_relationships = models.IntegerField(blank=True)
    t_on_demographics = models.IntegerField(blank=True)
    t_on_success = models.IntegerField(blank=True)

    #################################
    #####  MAP POSITIONS   #####
    #################################

    ps = models.LongStringField(blank=True)  # the personas

    # JSON data of positions
    positionsGame = models.LongStringField(blank=True)
    positionsTest = models.LongStringField(blank=True)
    positions = models.LongStringField(blank=True)
    # positions = models.LongStringField(blank=True)

    #################################
    #####  Similarity ratings   #####
    #################################

    valid_pairs = models.LongStringField(blank=True, initial="")
    n_check = models.IntegerField(initial=1)
    n_checks = models.IntegerField(initial=0)

    satisfaction = models.IntegerField()
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
    # ps_placed = models.IntegerField(initial=0)
    which_contact_type = models.StringField(
        initial="contact"
    )  # 'contact' or 'labelledPerson'


#################################
#####  OWN POLITICAL OPINIONS   #####
#################################
for q in C.QUS:
    setattr(Player, f"own_{q}", make_field(""))

#################################
#####  CONTACTS & CONTACTS' POLITICAL OPINIONS   #####
#################################
for n in range(1, C.NCONTACTS + 1):
    setattr(Player, f"contact{n}", define_contact(f"Contact {n}: ", n))
    setattr(
        Player,
        f"contact{n}_socialCloseness",
        models.StringField(
            choices=C.OPTIONS_CONTACTS_CLOSE,
            label="",
            widget=widgets.RadioSelect,
            blank=False,
        ),
    )
    for q in C.QUS:
        setattr(Player, f"contact{n}_{q}", make_field(""))

#################################
#####  LABELLED INDIVIDS' POLITICAL OPINIONS   #####
#################################
for name in C.LABELLED:
    for q in C.QUS:
        setattr(Player, f"{name.replace(' ', '')}_{q}", make_field(""))


#################################
#####  PAIRWISE SIMILARITY RATING   #####
#################################
for n in range(1, C.NR_PAIRWISE_CHECKS + 1):
    setattr(Player, f"checkPair{n}_dot1", models.LongStringField(blank=True))
    setattr(Player, f"checkPair{n}_dot2", models.LongStringField(blank=True))
    setattr(
        Player,
        f"checkPair{n}",
        models.StringField(
            choices=range(100),
            label="",
            widget=widgets.RadioSelect,
            blank=False,
        ),
    )

###########################
####  Importance
###########################
for q in C.QUS:
    setattr(Player, f"importance_{q}", models.IntegerField(blank=False))


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
        player.t_on_intro = int(time.time())

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.question_sorting = json.dumps(
            C.QU_SORTS[np.random.choice(range(len(C.QU_SORTS)))]
        )
        player.t_on_opinion = int(time.time())


#################################
#####  Overview   #####
#################################
class slide00_toc(Page):
    form_model = "player"
    form_fields = []

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        n_checks = {0: 1, 1: 3, 2: 4}[player.visited_toc]
        checks = ["<span saclass='checkmark'>✅</span>  "] * n_checks + [
            "<span saclass='checkmark upcoming'>🔜</span>  "
        ] * 6
        if lan == 'en':
            items = f"<ul><li>{checks[0]}Your own political opinions and identity</li><li>{checks[1]}How you think your social contacts view these political issues</li><li>{checks[2]}How you think typical voters view these political issues</li><li>{checks[3]}Placing these individuals on a political map<br><em>(with two short practice examples first)</em></li><li>{checks[4]}Evaluating the political similarity of a few pairs of individuals</li><li>{checks[5]}A few final questions about survey and about yourself</li></ul>"
            if player.visited_toc == 0:
                i1 = "➡️ In the following slides, we continue with your evaluations of the political views of your social contacts and typical voters."
                i2 = ""
            if player.visited_toc == 1:
                i1 = "➡️ In the following part, we will ask you to place people on a political map based on how similar or different you perceive their political views to be."
                i2 = "To prepare for this main task, we will begin with <strong>two short practice rounds</strong>."
            if player.visited_toc == 2:
                i1 = "Thank you very much for creating your own personal political map!"
                i2 = "➡️ In the following, we ask you to again evaluate the political similarity of a few (randomly selected) pairs of individuals."
        else:
            items = f"<ul><li>{checks[0]}Ihre eigenen politischen Einstellungen und Identität</li>   <li>{checks[1]}Ihre Einschätzungen über die politischen Ansichten von Personen, die Sie gut kennen</li> <li>{checks[2]}Ihre Einschätzungen über die politischen Ansichten typischer Wählerinnen und Wähler</li>  <li>{checks[3]}Die genannten Personen auf einer politischen Karte verorten<br><em>(inklusive zwei kurzer Übungsbeispiele)</em></li> <li>{checks[4]}Einschätzungen über die politische Ähnlichkeit einzelner Personen zueinander</li>  <li>{checks[5]}Abschlussfragen zur Umfrage und zu Ihrer Person</li></ul>"
            if player.visited_toc == 0:
                i1 = "➡️ In den folgenden Seiten geht es um Ihre Einschätzungen zu den politischen Ansichten von Ihren sozialen Kontakten und von typischen Wählern oder Wählerinnen."
                i2 = ""
            if player.visited_toc == 1:
                i1 = "➡️ Im folgenden Teil werden wir Sie bitten, Personen auf einer politischen Karte zu platzieren, je nachdem, wie ähnlich oder unterschiedlich Sie deren politische Ansichten wahrnehmen."
                i2 = "Zur Vorbereitung auf die eigentliche Aufgabe beginnen wir mit <strong>zwei kurzen Übungsrunden</strong>."
            if player.visited_toc == 2:
                i1 = "Vielen Dank für das Erstellen Ihrer persönlichen politischen Karte!"
                i2 = "➡️ Im Folgenden bitten wir Sie nochmals die politische Ähnlichkeit einiger (zufällig ausgewählte) Personenpaare zu bewerten."
        return {
            "lan_en": lan == "en",
            "maxslides": C.MAXSLIDES,
            "page_title": "Progress" if lan == 'en' else "Fortschritt",
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
        if player.visited_toc==1:
            player.t_on_contacts = int(time.time())
        if player.visited_toc==2:
            player.t_on_practiceGame_page = int(time.time())
        if player.visited_toc==3:
            player.t_on_check_page = int(time.time())


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
            if lan == 'en':
                labels = C.LIKERT7_string_noNA
            else:
                labels = C.LIKERT7_string_noNA_de

            field_question_pairs.append(
                {
                    "field_name": field,
                    "question_text": question,
                    "first_label": labels[0],  # Strongly Disagree
                    "neutral_label": labels[3],  # Neutral
                    "last_label": labels[6],  # Strongly Agree
                    "choices": dict(
                        zip(np.arange(-100, 101), np.arange(-100, 101))
                    ), 
                }
            )
        return {
            "lan_en": lan == "en",
            "maxslides": C.MAXSLIDES,
            "nslide": 2,
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
        questions = [C.QUS[i] for i in json.loads(player.question_sorting)]

        ps = {}
        n = 1
        for q in questions:
            ownOps = dict(
                zip(questions, [getattr(player, f"own_{q}", "NA") for q in questions])
            )
            if ownOps[q] == "Neutral":
                ownOps[q] = "Agree"
                ps[f"P{n}"] = dict(ownOps)
                n += 1
                ownOps[q] = "Disagree"
                ps[f"P{n}"] = dict(ownOps)
                n += 1
            else:
                if (ownOps[q] == "Disagree") or (ownOps[q] == "Strongly disagree"):
                    ownOps[q] = "Agree"
                elif (ownOps[q] == "Agree") or (ownOps[q] == "Strongly agree"):
                    ownOps[q] = "Disagree"
                else:
                    print("error")
                ps[f"P{n}"] = dict(ownOps)
                n += 1
        player.ps = json.dumps(ps)
        player.valid_pairs = json.dumps(
            list(
                combinations(
                    ["self"]
                    + [f"contact{c}" for c in range(1, C.NCONTACTS + 1)]
                    + C.LABELLED,
                    # + list(ps.keys()),
                    2,
                )
            )
        )

        player.n_checks = 1 + C.NCONTACTS + len(ps) + len(C.LABELLED)
        player.t_on_identity = int(time.time())


#################################
#####  Demographics   #####
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
            if lan == 'en'
            else "In der Politik spricht man manchmal von 'links' und 'rechts'. Wo auf der Skala von 0 bis 10 würden Sie sich selbst einstufen,  wenn 0 für links steht und 10 für rechts?"
        )
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": 3 + len(C.LABELLED) + C.NCONTACTS + 2 + 2 + 5,
            "lan_en": lan == "en",
            "page_title": (
                "Your Political Identity" if lan == 'en' else "Politische Identität"
            ),
            "qu_identity": (
                "Do you feel closer to one of the political parties in Germany than the others? If so, which one?"
                if lan == 'en'
                else "Gibt es eine bestimmte politische Partei in Deutschland, der Sie sich politisch näher fühlen als allen anderen Parteien? Welcher?"
            ),
            "choices_identity": dict(
                zip(
                    C.CHOICES_IDENTITY,
                    (
                        C.CHOICES_IDENTITY
                        if lan == 'en'
                        else [
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
                    ),
                )
            ),
            "qu_party_comment": (
                "Would you like to add anything to the question above? (optional):"
                if lan == 'en'
                else "Möchten Sie etwas zu dieser Frage ergänzen? (optional)"
            ),
            "lr_question": question,
            "lr_first_label": "left" if lan == 'en' else "links",
            "lr_last_label": "right" if lan == 'en' else "rechts",
            "lr_choices": dict(zip(np.arange(0, 10.1, 1), np.arange(0, 10.1, 1))),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.t_on_toc1 = int(time.time())


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
                    "label": f"Contact {n}:" if lan == 'en' else f"Kontakt {n}:",
                }
            )
        return {
            "lan_en": lan == "en",
            "maxslides": C.MAXSLIDES,
            "nslide": 3,
            "ncontacts": C.NCONTACTS,
            "contact_fields": contact_fields,
            "page_title": "Social Contacts" if lan == 'en' else "Soziale Kontakte",
            "instruction_text": (
                f"<p>Think about <strong>{C.NCONTACTS} social contacts</strong> that you know well. This can include friends, family members, Co-workers, ....</p><p>Please write down their names or initials so that you are later able to recognise them (we will not use/store that information).</p>"
                if lan == 'en'
                else f"<p>Denken Sie nun an <strong>{C.NCONTACTS} soziale Kontakte</strong>, die Sie gut kennen. Das können Freunde, Freundinnen, Familienmitglieder, Kollegen, etc. sein.</p><p>Bitte notieren Sie die Namen oder Initialen dieser Kontakte in den Feldern unten, so dass Sie diese später wiedererkennen (wir werden diese Informationen nicht speichern oder verwenden).</p>"
            ),
            "instruction2": (
                "<p>In the next slides, we will ask you what you think these people would respond to the political questions from the previous slide.</p>"
                if lan == 'en'
                else "<p>In den folgenden Seiten, fragen wir Sie was diese Personen Ihrer Meinung nach auf die politischen Fragen antworten würden.</p>"
            ),
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
    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #     player.t_on_personOpinion = int(time.time())

#################################
#####  Person Opinions   #####
#################################
class slide04_PersonOpinion(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        times_dict = json.loads(player.t_on_personOpinion)
        print(times_dict)
        times_dict[
            player.which_contact_type
            + (
                str(player.current_contact)
                if player.which_contact_type == "contact"
                else str(player.evaluated_labelledPerson)
            )
        ] = int(time.time())
        player.t_on_personOpinion = json.dumps(times_dict)

        lan = player.language
        if player.which_contact_type == "contact":
            idx = player.current_contact
            name = getattr(player, f"contact{idx}")
            prefix = f"contact{idx}_"
            displName = f"{name}"
            displName1 = f"Ihren Kontakt <strong>{name}</strong>"
            displName3 = f"<strong>{name}</strong>"
            displName4 = f"von <strong>{name}</strong>"
            color = C.FRIENDCOLOR  # contact color
        else:  # mode == 'labelledPerson'
            idx = player.evaluated_labelledPerson
            name = C.LABELLED[idx]
            prefix = f"{name.replace(' ','')}_"
            displName = (
                f"a typical {name} voter"
                if lan == 'en'
                else f"{C.LABELLED_de[name]} Wähler/-in"
            )
            displName4 = "the person"
            color = C.LABELLEDCOLORS[name]
            if lan == "de":
                displName1 = f"eine typische Wählerin oder einen typischen Wähler {'des' if name=='BSW' else 'der'} <strong>{C.LABELLED_de[name]}</strong>"
                displName3 = f"Wähler/Wählerin {'des' if name=='BSW' else 'der'} {C.LABELLED_de[name]}"
                displName4 = f"der Person"
        fields = [
            f"{prefix}{q}"
            for q in [C.QUS[i] for i in json.loads(player.question_sorting)]
        ]
        questions = [
            C.QUESTIONTEXT[lan][q]
            for q in [C.QUS[i] for i in json.loads(player.question_sorting)]
        ]
        field_question_pairs = []
        for field, question in zip(fields, questions):
            # choices = dict(
            #     zip(
            #         C.LIKERT5_string_noNA[::-1],
            #         (
            #             C.LIKERT5_string_noNA[::-1]
            #             if lan == 'en'
            #             else C.LIKERT5_string_noNA_de[::-1]
            #         ),
            #     )
            # )  # convert list of tuples to dict
            if lan == 'en':
                labels = C.LIKERT7_string_noNA
            else:
                labels = C.LIKERT7_string_noNA_de

            field_question_pairs.append(
                {
                    "field_name": field,
                    "question_text": question,
                    "first_label": labels[0],  # Strongly Disagree
                    "neutral_label": labels[3],  # Neutral
                    "last_label": labels[6],  # Strongly Agree
                }
            )
        return {
            "lan_en": lan == "en",
            "maxslides": C.MAXSLIDES,
            "nslide": 3
            + idx
            + (1 + C.NCONTACTS if player.which_contact_type == "labelledPerson" else 0),
            "name": name,
            "color": color,
            "person_type": player.which_contact_type,
            "fields": fields,
            "questions": questions,
            "would_respond": (
                f"I think {displName4} would respond with:"
                if lan == 'en'
                else f"Ich denke, die Antwort {displName4} wäre:"
            ),
            "field_question_pairs": field_question_pairs,
            "page_title": (
                "Political Opinions of Others"
                if lan == 'en'
                else "Politische Meinungen von anderen Menschen"
            ),
            "instruction_text": (
                f"Thinking about <strong>{displName}</strong>, how do you think <strong>{displName}</strong> would respond to the political questions?"
                if lan == 'en'
                else f"Denken Sie nun an {displName1}. Wie würde er/sie die politischen Fragen beantworten?"
            ),
            "table_head": (
                f"<strong>{displName}</strong>'s responses"
                if lan == 'en'
                else f"Antworten von <strong>{displName3}</strong>"
            ),
        }

    @staticmethod
    def get_form_fields(player: Player):
        if player.which_contact_type == "contact":
            prefix = f"contact{player.current_contact}_"
        else:
            name = C.LABELLED[player.evaluated_labelledPerson]
            prefix = f"{name.replace(' ', '')}_"
        return [
            f"{prefix}{q}"
            for q in [C.QUS[i] for i in json.loads(player.question_sorting)]
        ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.which_contact_type == "contact":
            player.current_contact += 1
        else:
            player.evaluated_labelledPerson += 1
        if player.current_contact > C.NCONTACTS:
            player.which_contact_type = "labelledPerson"

        player.t_on_toc2 = int(time.time())

    @staticmethod
    def is_displayed(player: Player):
        if not player.consent:
            return False
        if player.which_contact_type == "contact":
            return player.current_contact <= C.NCONTACTS
        else:
            return player.evaluated_labelledPerson <= len(C.LABELLED)


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
                "name_disp": (
                    "Lasagne" if lan == 'en' else "Lasagne"
                ),
                "x": 330,
                "y": 50,
                "color": "#d97565   ",
            },
            {
                "dottype": "food",
                "varname": "pizza",
                "name_disp": "Pizza Margherita" if lan == 'en' else "Pizza Margherita",
                "x": 330,
                "y": 100,
                "color": "#d97565",
            },
            {
                "dottype": "food",
                "varname": "spaghetticarbo",
                "name_disp": (
                    "Spaghetti Carbonara" if lan == 'en' else "Spaghetti Carbonara"
                ),
                "x": 330,
                "y": 150,
                "color": "#d97565",
            },
        ]
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": 3 + len(C.LABELLED) + C.NCONTACTS + 1,
            "lan_en": lan == "en",
            "dots": init_dots,
            "page_title": (
                "Political Mapping – Practice round 1"
                if lan == 'en'
                else "Politisches Mapping – Übungsrunde 1"
            ),
            "lan": lan,
            "instruction_text2": (
                "Imagine you have to place the following meals – Lasagne, Spaghetti Carbonara, and Pizza Margherita – in a room (the rectangle below)."
                if lan == 'en'
                else "Stellen Sie sich vor, Sie müssten die folgenden Gerichte – Lasagne, Spaghetti Carbonara, und Pizza Margherita – in einem Raum platzieren (das Rechteck unten)."
            ),
            "instruction_text3": (
                "<p><ul><li><strong>Place meals closer together if you perceive them as similar.</strong></li><li><strong>Place meals farther apart if you perceive them as different.</strong></li></ul>"
                if lan == 'en'
                else "<p><ul><li>Platzieren Sie Gerichte <strong>näher beieinander</strong>, wenn Sie diese als <strong>ähnlich</strong> wahrnehmen.</li><li>Platzieren Sie Gerichte <strong>weiter auseinander</strong>, wenn Sie diese als <strong>unterschiedlich</strong> wahrnehmen.</li></ul>"
            ),
            "detailed_instructions_1": (
                "<ul><li>You will start with several points on the right side.</li><li>Drag these one by one into the rectangle and place them as described above.</li><li>You can re-position any dot at any time until you are satisfied with the arrangement.</li></ul>"
                if lan == 'en'
                else "<ul><li>Sie beginnen mit mehreren Punkten auf der rechten Seite.</li><li>Ziehen Sie diese nacheinander in das Rechteck und ordnen Sie die Punkte wie oben beschrieben an.</li><li>Sie können jeden Punkt verschieben bis Sie mit der Anordnung zufrieden sind.</li></ul>"
            ),
            "no_wrong_answers": (
                f"<ul><li>There are of course NO right or wrong answers here</li><li>For example, two participants might arrange the dishes quite differently, if one dislikes meat the other tomatoes</li><li>We are interested in your <strong>personal perceptions</strong> in this survey</li></ul>"
                if lan == 'en'
                else "<ul><li>Es gibt hier natürlich weder falsche noch richtige Antworten</li><li>Zwei Personen würden die Gerichte vermutlich ziemlich unterschiedlich anordnen, wenn die eine kein Fleisch, die andere keine Tomaten mag</li><li>Wir sind in dieser Umfrage ausschließlich an <strong>Ihrer persönlichen Einschätzung</strong> interessiert</li></ul>"
            ),
            "all_dots_instr": (
                "All dots must be within the square boundary to proceed."
                if lan == 'en'
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
                    "name_disp": "Self" if lan == 'en' else "Ich",
                    "x": 330,
                    "y": 50,
                    "color": "grey",
                },
                {
                    "dottype": "friend",
                    "varname": "friend",
                    "name_disp": "Friend" if lan == 'en' else "Freund",
                    "x": 330,
                    "y": 100,
                    "color": "blue",
                },
                {
                    "dottype": "coworker",
                    "varname": "coworker",
                    "name_disp": "Co-Worker" if lan == 'en' else "Kollegin",
                    "x": 330,
                    "y": 150,
                    "color": "blue",
                },
                {
                    "dottype": "relative",
                    "varname": "relative",
                    "name_disp": "Relative" if lan == 'en' else "Verwandter",
                    "x": 330,
                    "y": 200,
                    "color": "blue",
                },
            ]
        else:
            init_dots = json.loads(getattr(player, "positionsTest", []))
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": 3 + len(C.LABELLED) + C.NCONTACTS + 1,
            "lan_en": lan == "en",
            "dots": init_dots,
            "page_title": (
                "Political Mapping – Practice round"
                if lan == 'en'
                else "Politisches Mapping – Übungsrunde"
            ),
            "lan": lan,
            "instruction_text1": (
                "In the <strong>second practice round</strong> we now focus on perception of political similarity."
                if lan == 'en'
                else "In der <strong>zweiten Übungsrunde</strong> geht es nun um Wahrnehmungen politischer Ähnlichkeit."
            ),
            "instruction_text2": (
                "Imagine you, a friend, a co-worker, and your relative are in a room (the rectangle below)."
                if lan == 'en'
                else "Stellen Sie sich vor, Sie sind zusammen mit einem Freund, einer Arbeitskollegin und einem Verwandten in einem Raum (das Rechteck unten)."
            ),
            "instruction_text3": (
                "<p>Arrange the people in the room based on how <em>you</em> see their political views:</p><ul><li><strong>Place individuals closer together if you perceive them as <em>politically</em> similar.</strong></li><li><strong>Place individuals farther apart if you perceive them as <em>politically</em> different.</strong></li></ul>"
                if lan == 'en'
                else "<p>Ordnen Sie die Personen im Raum so an, wie <em>Sie</em> deren politische Ansichten wahrnehmen:</p><ul> <li>Platzieren Sie Personen <strong>näher beieinander</strong>, wenn Sie diese als <strong><em>politisch</em> ähnlich</strong> wahrnehmen.</li><li>Platzieren Sie Personen <strong>weiter auseinander</strong>, wenn Sie diese als <strong><em>politisch</em> unterschiedlich</strong> wahrnehmen.</li></ul>"
            ),
            "disclaimer": (
                "<p>This is a practice round – some arrangements match the instructions below, others do not. When you click <em>Next</em>, we will show you whether your arrangement meets all the instructions."
                if lan == 'en'
                else "<p>Dies ist eine Übungsrunde – einige Anordnungen entsprechen den untenstehenden Anweisungen, andere nicht. Wenn Sie auf <em>Weiter</em> klicken, erfahren Sie, ob Ihre Anordnung alle Vorgaben erfüllt.</p>"
            ),  # In the main task on the next slide, there will be NO right or wrong answers — only your personal perception will matter.</p> #  Im Hauptteil auf der nächsten Seite wird es dagegegen KEINE richtigen oder falschen Antworten geben – nur Ihre persönliche Wahrnehmung wird relevant sein.
            "detailed_instructions_1": (
                "<h3>Practice Round Step-by-Step Instructions</h4><p>Drag the points on the right side one by one into the rectangle as described in the following instructions:</p>"
                if lan == 'en'
                else "<h3>Übungsrunde Schritt-für-Schritt Anleitung</h4> <p>Ziehen Sie die Punkte auf der rechten Seite nacheinander in das Rechteck, wie in der folgenden Anleitung beschrieben:</p>"
            ),
            "detailed_instructions_2": (
                (
                    "<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Step 1:</strong> 'Self'</summary><p>Place the point <strong>Self</strong> somewhere within the rectangle – it represents your own political views.</p></details>"
                    + "<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Step 2:</strong> 'Friend'</summary><p>Place the point <strong>Friend</strong> near you – they share similar views.</p></details>"
                    + "<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Step 3:</strong> 'Co-worker'</summary><p>Place <strong>Co-worker</strong> farther away, as they often have different opinions – but closer to <strong>Self</strong> than to <strong>Friend</strong>, because you perceive an even greater political difference between Co-worker and Friend.</p></details>"
                    + "<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Step 4:</strong> 'Relative'</summary><p>Your <strong>Relative</strong> has very different political views – place them far from <strong>Me</strong>, but somewhat closer to <strong>Friend</strong> and <strong>Co-worker</strong>, as you feel they share some opinions with them.</p></details>"
                )
                if lan == 'en'
                else (
                    "<details  open style='margin-bottom: 0em;'> <summary  style='white-space: nowrap;'><strong>Schritt 1:</strong> 'Ich'</summary> <p>Platzieren Sie den Punkt <strong>Ich</strong> irgendwo im Rechteck – er steht für Ihre politischen Ansichten.</p></details>"
                    + "<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Schritt 2:</strong> 'Freund'</summary><p>Setzen Sie den Punkt <strong>Freund</strong> in Ihre Nähe – er teilt ähnliche Ansichten wie Sie.</p></details>"
                    + "<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Schritt 3:</strong> 'Kollegin'</summary><p>Platzieren Sie <strong>Kollegin</strong> weiter entfernt, da sie oft anderer Meinung als Sie ist – aber näher bei <strong>Ich</strong> als bei <strong>Freund</strong>, weil Sie zwischen der Kollegin und dem Freund einen noch größeren politischen Unterschied wahrnehmen.</p></p></details>"
                    + "<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Schritt 4:</strong> 'Verwandter'</summary><p>Der <strong>Verwandte</strong> denkt politisch ganz anders – setzen Sie ihn weit weg von <strong>Ich</strong>, aber etwas näher an <strong>Freund</strong> und <strong>Kollegin</strong>, da Sie finden, dass der Verwandte in manchen Punkten deren Ansichten teilt.</p></details>"
                )
            ),
            "all_dots_instr": (
                "All dots must be within the square boundary to proceed. You can re-position any dot at any time until you are satisfied with the arrangement."
                if lan == 'en'
                else "Um fortzufahren müssen alle Punkte im Rechteck platziert werden. Sie können jeden Punkt verschieben bis Sie mit der Anordnung zufrieden sind."
            ),
            "latest_error_msg": (
                "<p><strong>Error(s) in your previous attempt:</strong></p>"
                if lan == 'en'
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
        if lan == 'en':
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
            "nslide": 3 + len(C.LABELLED) + C.NCONTACTS + 2,
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
                if lan == 'en'
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
                if lan == 'en'
                else f"Versuch {player.attemptPractice} von {C.N_MAX_PRACTICE_RUNS}"
            ),
            "page_title": (
                "Political Mapping – Practice – Results"
                if lan == 'en'
                else "Politisches Mapping – Training – Ergebnis"
            ),
            "success_msg": (
                "<strong>Well done!</strong> Your arrangement fulfills all criteria."
                if lan == 'en'
                else "<strong>Gut gemacht!</strong> Ihre Anordnung der Punkte erfüllt alle Kriterien."
            ),
            "error_msg": (
                f"<strong>Your arrangement does not meet all steps of the instructions:</strong></p><p style='white-space: pre-line;'>{errors}</p><p>Please repeat the training and try to arrange the dots so that all criteria are fulfilled.</p>"
                if lan == 'en'
                else f"<strong>Ihre Anordnung erfüllt nicht alle Schritte der Anleitung:</strong></p><p style='white-space: pre-line;'>{errors}</p><p>Bitte wiederholen Sie das Training und versuchen Sie, die Punkte so anzuordnen, dass alle Kriterien erfüllt sind.</p>"
            ),
            "img_help": not (player.attemptPractice <= 1 or player.isTrainingPassed),
            "img_help_text": "<p>"
            + (
                "Below you can find one possible arrangement of the dots that fulfills all criteria:"
                if lan == 'en'
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


#################################
#####  Spatial Arrangement Mapping   #####
#################################
class slide06_SPaM(Page):
    form_model = "player"
    form_fields = ["positions"]

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.t_on_toc3 = int(time.time())

    @staticmethod
    def is_displayed(player: Player):
        return player.consent & player.isTrainingPassed

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        displ_names = (
            ["Self" if lan == 'en' else "Ich"]
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
                "x": 530 + 60 * (dottype == "labelledPerson"),
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
            "nslide": 3 + len(C.LABELLED) + C.NCONTACTS + 2 + 1,
            "lan_en": lan == "en",
            "dots": init_dots,
            "page_title": (
                "Political Mapping – Part 1"
                if lan == 'en'
                else "Politisches Mapping – Teil 1"
            ),
            "instru1": (
                "We now continue to the main task in this survey."
                if lan == 'en'
                else "Wir beginnen nun mit dem Hauptteil dieser Umfrage."
            ),
            "instruRoom": (
                "Imagine you, your social contacts, and typical voters of the German parties are in a room (the rectangle below)."
                if lan == 'en'
                else "Stellen Sie sich vor, Sie sind zusammen mit Ihren Kontakten und mit jeweils den typischen Wählern oder Wählerinnen der vorher genannten Parteien in einem Raum (das Rechteck unten)."
            ),
            "instru_main": (
                "<p>Arrange the people in the room based on how <em>you</em> see their political views about questions regarding climate change, migration, inequality and diversity:</p><ul><li><strong>Place individuals closer together if you perceive them as politically similar.</strong></li><li><strong>Place individuals farther apart if you perceive them as politically different.</strong></li></ul>"
                if lan == 'en'
                else "<p>Ordnen Sie die Personen im Raum so an, wie <em>Sie</em> deren politische Ansichten zu Fragen über Klimawandel, Migration, Ungleichheit und Vielfalt wahrnehmen:</p><ul> <li>Platzieren Sie Personen <strong>näher beieinander</strong>, wenn Sie diese als <strong>politisch ähnlich</strong> wahrnehmen.</li><li>Platzieren Sie Personen <strong>weiter auseinander</strong>, wenn Sie diese als <strong>politisch unterschiedlich</strong> wahrnehmen.</li></ul>"
            ),
            "no_wrong_answers": (
                f"<p>There are NO right or wrong answers — we are interested in your personal perception.</p>"
                if lan == 'en'
                else "<p>Es gibt weder falsche noch richtige Antworten – wir sind an Ihrer persönliche Einschätzung interessiert.</p>"
            ),
            # "instru_click": (
            #     "<summary style='white-space: nowrap;'><strong>Helping lines</strong></summary>If you want you can activate helping lines. When you click on one of the dots, circles will appear that might help you evaluate how well your arrangement reflects your sense of political similarity. You can scale the circles by moving the small arrows <strong><></strong>."
            #     if lan == 'en'
            #     else "<summary style='white-space: nowrap;'><strong>Hilfslinien</strong></summary>Wenn Sie möchten, können Sie unten Hilfslinien aktivieren: Beim Klicken auf einen Punkt erscheinen Kreis, die Ihnen dabei helfen könnten einzuschätzen, wie gut Ihre Anordnung Ihre Wahrnehmung politischer Ähnlichkeit widerspiegelt. Die Kreise lassen sich über die kleinen Pfeile <strong><></strong> skalieren."
            # ),
            "all_dots_instr": (
                "All dots must be within the square boundary to proceed. You can re-position any dot at any time until you are satisfied with the arrangement."
                if lan == 'en'
                else "Um fortzufahren müssen alle Punkte im Rechteck platziert werden. Sie können jeden Punkt verschieben bis Sie mit der Anordnung zufrieden sind."
            ),
            # "labelClose": "similar" if lan == 'en' else "ähnlich",
            # "labelFar": "different" if lan == 'en' else "unterschiedlich",
            # "helping_lines": (
            #     "Show helping lines" if lan == 'en' else "Hilfslinien anzeigen"
            # ),
        }


# #################################
# #####  Spatial Arrangement Mapping – Personas   #####
# #################################
# class slide07_SPaM_personas(Page):
#     form_model = "player"
#     form_fields = ["positions"]

#     @staticmethod
#     def vars_for_template(player: Player):
#         lan = player.language
#         questions = [C.QUS[i] for i in json.loads(player.question_sorting)]

#         def get_ops(prefix, questions):
#             return {q: getattr(player, f"{prefix}{q}", "NA") or "NA" for q in questions}

#         def format_ops(ops_dict, lan):
#             return "; ".join(
#                 f"{C.QUESTIONSHORTTEXT[lan][q]}: {val if lan=='en' else C.LIKERT5_transde[val] }"
#                 for q, val in ops_dict.items()
#             )

#         P = f"P{player.ps_placed + 1}"
#         p_ops = json.loads(player.ps)
#         n_ps = len(p_ops.keys())
#         P_op = [p_ops[P][q] for q in questions]
#         P_op = ["" if str(op) == "nan" else op for op in P_op]
#         pos = json.loads(player.positions) if player.positions else []

#         P_text_short = "; ".join(
#             [
#                 f"{C.QUESTIONSHORTTEXT[lan][q]}: {P_op[i] if lan=='en' else C.LIKERT5_transde[P_op[i]]}"
#                 for i, q in enumerate(questions)
#             ]
#         )

#         # Write dot descriptions of Self, Contacts, Labelled, and past Personas
#         dot_descrs = {
#             "self": format_ops(
#                 get_ops(
#                     "own_", [C.QUS[i] for i in json.loads(player.question_sorting)]
#                 ),
#                 lan,
#             )
#         }
#         for f in range(1, C.NCONTACTS + 1):
#             dot_descrs[f"contact{f}"] = format_ops(
#                 get_ops(f"contact{f}_", questions), lan
#             )
#         for v in C.LABELLED:
#             dot_descrs[f"{v}"] = format_ops(
#                 get_ops(f"{v.replace(" ", "")}_", questions), lan
#             )
#         for p in range(1, player.ps_placed + 1):
#             currP = f"P{p}"
#             currP_op = [p_ops[currP][q] for q in questions]
#             currP_op = ["" if str(op) == "nan" else op for op in currP_op]
#             dot_descrs[currP] = "; ".join(
#                 [
#                     f"{C.QUESTIONSHORTTEXT[lan][q]}: {op if lan=='en' else C.LIKERT5_transde[op]}"
#                     for q, op in zip(questions, currP_op)
#                 ]
#             )

#         # Prepare initial dot data
#         init_dots = [
#             {
#                 "varname": p["varname"],
#                 "name_disp": p["name_disp"],
#                 "x": p["x"],
#                 "y": p["y"],
#                 "dottype": p["dottype"],
#                 "descr": dot_descrs.get(p["varname"], ""),
#                 "t_first_moved": p["t_first_moved"],
#                 "t_last_moved": p["t_last_moved"],
#             }
#             for p in pos
#         ]
#         init_dots.append(
#             {
#                 "varname": P,
#                 "name_disp": P,
#                 "x": 530,
#                 "y": 350,
#                 "dottype": "P",
#                 "descr": P_text_short,
#                 "t_first_moved": -1,
#                 "t_last_moved": -1,
#             }
#         )

#         return {
#             "maxslides": C.MAXSLIDES,
#             "nslide": 3 + len(C.LABELLED) + C.NCONTACTS + 2 + 2,
#             "lan_en": lan == "en",
#             "P": P,
#             "P_text_short": P_text_short,
#             "dots": init_dots,
#             "n_ps": n_ps,
#             "ps_placed": player.ps_placed + 1,
#             "page_title": (
#                 "Political Mapping – Part 2"
#                 if lan == 'en'
#                 else "Politisches Mapping – Teil 2"
#             ),
#             "heading": (
#                 f"Person {player.ps_placed+1} of { n_ps} "
#                 if lan == 'en'
#                 else f"Person {player.ps_placed+1} von {n_ps}"
#             ),
#             "instru_main": (
#                 "<details><summary style='margin-bottom:0.5em;'><strong>Instructions (as before)</strong></summary><p>Arrange the people in the room based on how <em>you</em> see their political views on questions regarding climate change, migration, inequality and diversity:</p><ul><li><strong>Place individuals closer together if you perceive them as politically similar.</strong></li><li><strong>Place individuals farther apart if you perceive them as politically different.</strong></li></ul></details>"
#                 if lan == 'en'
#                 else "<details><summary style='margin-bottom:0.5em;'><strong>Anleitung (wie zuvor)</strong></summary><p>Ordnen Sie die Personen im Raum so an, wie <em>Sie</em> deren politische Ansichten zu Fragen über Klimawandel, Migration, Ungleichheit und Vielfalt wahrnehmen:</p><ul><li><strong>Platzieren Sie Personen näher beieinander, wenn Sie diese als politisch ähnlich wahrnehmen.</strong></li><li><strong>Platzieren Sie Personen weiter auseinander, wenn Sie diese als politisch unterschiedlich wahrnehmen.</strong></li></ul></details>"
#             ),
#             "no_wrong_answers": (
#                 f"<p>There are NO right or wrong answers — we are interested in your personal perception.</p>"
#                 if lan == 'en'
#                 else "<p>Es gibt weder falsche noch richtige Antworten – wir sind an Ihrer persönliche Einschätzung interessiert.</p>"
#             ),
#             "instru_p1": (
#                 f"<p>In the next part of this survey, you will be introduced to a hypothetical person along with a brief description of their political views.</p><p> Try to imagine this person as clearly as possible based on the information provided. How politically similar or different do you think this person is — compared to yourself, your social contacts, and the typical voters in the room?<p>"
#                 if lan == 'en'
#                 else f"<p>Im nächsten Teil dieser Umfrage stellen wir Ihnen eine hypothetische Person vor und geben einen kurzen Überblick über deren politische Ansichten.</p><p>Versuchen Sie, sich diese Person so gut wie möglich auf Grundlage dieser Informationen vorzustellen. Wie politisch ähnlich oder unterscheidlich erscheint Ihnen diese Person – im Vergleich zu Ihnen selbst, Ihren sozialen Kontakten und den typischen Wähler oder Wählerinnen im Raum?</p>"
#             ),
#             "instru_p2": (
#                 f"Here are the responses of the person <strong>{P}</strong> to the previous questions:"
#                 if lan == 'en'
#                 else f"Hier sind die Antworten der Person <strong>{P}</strong> auf die vorherigen Fragen:"
#             ),
#             "instru_click": (
#                 "<strong>Tip</strong>: If you click on a dot, a box with the individual's opinions will appear on the right side."
#                 if lan == 'en'
#                 else "<strong>Tipp</strong>: Wenn Sie auf einen Punkt klicken, erscheint auf der rechten Seite eine Info-Box mit den Meinungen der Person."
#             ),
#             "all_dots_instr": (
#                 "All dots must be within the square boundary to proceed. You can re-position any dot, <strong>including the dots from the previous mapping exercise</strong>, at any time until you are satisfied with the arrangement."
#                 if lan == 'en'
#                 else "Um fortzufahren müssen alle Punkte im Rechteck platziert werden. Sie können jeden Punkt, <strong>inklusive der Punkte aus der vorherigen Aufgabe</strong>, verschieben bis Sie mit der Anordnung zufrieden sind."
#             ),
#             "reminder": (
#                 "Remember, there are no right or wrong answers. We are most interested in your own political perceptions!"
#                 if lan == 'en'
#                 else "Denken Sie daran: Es gibt keine richtigen oder falschen Antworten. Wir sind vor allem an Ihrer eigenen politischen Wahrnehmung interessiert!"
#             ),
#             "labelClose": "similar" if lan == 'en' else "ähnlich",
#             "labelFar": "different" if lan == 'en' else "unterschiedlich",
#             "helping_lines": (
#                 "Show helping circles" if lan == 'en' else "Hilfslinien anzeigen"
#             ),
#         }

#     @staticmethod
#     def before_next_page(player: Player, timeout_happened):
#         player.ps_placed += 1
#         p_points = list(json.loads(player.ps).keys())
#         if player.ps_placed == len(p_points):
#             player.t_on_check_page = int(time.time())

#     @staticmethod
#     def is_displayed(player):
#         return (
#             player.consent
#             #and (player.ps_placed <= C.NPS_MAX)
#             and (player.ps_placed < len(json.loads(player.ps)))
#         )


#################################
#####  Pairwise similiarty ratings   #####
#################################
class slide08_PlausibilityCheck_Pairs(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        return (player.consent) and (player.n_check <= (player.n_checks)) and player.isTrainingPassed

    @staticmethod
    def get_form_fields(player: Player):
        i = player.n_check
        return [f"checkPair{i}"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        valid_pairs = json.loads(getattr(player, "valid_pairs"))
        pair = [
            getattr(player, f"checkPair{player.n_check}_dot1"),
            getattr(player, f"checkPair{player.n_check}_dot2"),
        ]
        valid_pairs.remove(pair)
        player.valid_pairs = json.dumps(valid_pairs)

        if player.n_check == 1:
            player.t_after_first_check = int(time.time())
        player.t_after_last_check = int(time.time())
        player.t_on_importance = int(time.time())

        player.n_check += 1

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        valid_pairs = json.loads(player.valid_pairs)
        p1, p2 = random.choice(valid_pairs)
        setattr(player, f"checkPair{player.n_check}_dot1", p1)
        setattr(player, f"checkPair{player.n_check}_dot2", p2)

        def get_descr(p):
            if "contact" in p:
                plabel = (
                    f"Your contact <span class='pill' style='background-color: {C.FRIENDCOLOR}; color: white;'><strong>"
                    if lan == 'en'
                    else f"Ihr Kontakt <span class='pill' style='background-color: {C.FRIENDCOLOR}; color: white;'><strong>"
                )
                plabel += f"{getattr(player, p)}</strong></span>"
            if p == "self":
                plabel = (
                    f"<span class='pill' style='background-color: #808080; color: white;'><strong>Yourself</strong></span>"
                    if lan == 'en'
                    else f"<span class='pill' style='background-color: #808080; color: white;'><strong>Sie selbst</strong></span>"
                )
            if p in C.LABELLED:
                plabel = (
                    f"A typical <span class='pill' style='background-color: {C.LABELLEDCOLORS[p]}; color: {'white' if not p=='FDP' else '#424949'};'><strong>{p} voter</strong></span>"
                    if lan == 'en'
                    else f"typische Person, die <span class='pill' style='background-color: {C.LABELLEDCOLORS[p]}; color: {'white' if not p=='FDP' else '#424949'};'>{'die ' if p=='Green Party' or p=='Left Party' else ''} <strong>{C.LABELLED_de[p]} wählt</strong></span>"
                )
            return plabel


        return {
            "maxslides": C.MAXSLIDES,
            "nslide": 3 + len(C.LABELLED) + C.NCONTACTS + 2 + 2 + 1,
            "lan_en": lan == "en",
            "p1": p1,
            "p2": p2,
            # "p1_dot": p1_dot,
            # "p2_dot": p2_dot,
            "current_check": f"checkPair{player.n_check}",
            "page_title": (
                f"Pairwise comparison of political views – {player.n_check} of {player.n_checks}"
                if lan == 'en'
                else f"Paarweiser Vergleich politischer Meinungen {player.n_check} von {player.n_checks}"
            ),
            "instru1": (
                f"<p>Now consider the following two individuals:</p><ol><li style='font-size:18px;'>{get_descr(p1)}</li><li style='font-size:18px;'>{get_descr(p2)}</li></ol>"
                if lan == 'en'
                else f"<p>Denken Sie nun an die folgenden beiden Personen:</p><ol><li style='font-size:18px;'>{get_descr(p1)}</li><li style='font-size:18px;'>{get_descr(p2)}</li></ol>"
            ),
            "question": (
                "<p>In <em>your</em> opinion, how similar are these two individuals overall in their political views on migration, climate change, inequality and diversity?</p>"
                if lan == 'en'
                else "<p>Wie ähnlich sind sich diese beiden Personen <em>Ihrer Meinung nach</em> insgesamt in ihren politischen Ansichten zu Migration, Klimawandel, Ungleichheit und Vielfalt?</p>"
            ),
            "Ithink": "",  # "Your estimate:" if lan == 'en' else "Ihre Einschätzung:",
            # "img1": p1_dot["dottype"] == "P",
            # "img2": p2_dot["dottype"] == "P",
            "choices": list(range(0, 11)),
            "similarity_min": 0,
            "similarity_max": 10,
            "similarity_min_label": (
                "Not at all similar" if lan == 'en' else "Überhaupt nicht ähnlich"
            ),
            "similarity_max_label": (
                "Extremely similar" if lan == 'en' else "Extrem ähnlich"
            ),
        }


class slide09_Importance(Page):
    form_model = "player"
    form_fields = [f"importance_{q}" for q in C.QUS]+["importance_comments"]

    @staticmethod 
    def before_next_page(player: Player, timeout_happened):
        player.t_on_satisfaction = int(time.time())
        
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
                    "first_label": "not important at all" if lan=='en' else "überhaupt nicht wichtig",  # Strongly Disagree
                    "last_label": "extremely important"  if lan=='en' else "extrem wichtig",  # Strongly Agree
                    "choices": dict(
                        zip(np.arange(0, 101), np.arange(0, 101))
                    ),  # dict(zip(range(1, 8), labels)),  # 1-7 mapping
                }
            )            
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": 3 + len(C.LABELLED) + C.NCONTACTS + 2 + 2 + 2,
            "lan_en": lan == "en",
            "field_question_pairs": field_question_pairs,
            "page_title": (
                "Key Topics Influencing Your Arrangement"
                if lan == 'en'
                else "Wichtige Themen für Ihre Anordnung"
            ),
            "question": (
                "Please rate the importance of each of the four political topics for your Arrangement (0–100):"
                if lan == 'en'
                else "Bitte bewerten Sie die Wichtigkeit jedes der vier politischen Themen für Ihre Anordnung (0–100):"
            ),
            "explain_text": (
                "You can add further comments or explanations here (optional):"
                if lan == 'en'
                else "Sie können hier weitere Anmerkungen oder Erklärungen hinzufügen (optional):"
            ),
        }


#################################
#####  Overall Satisfaction with Map   #####
#################################
class slide10_Satisfaction(Page):
    form_model = "player"
    form_fields = ["satisfaction_text", "satisfaction"]

    @staticmethod
    def is_displayed(player: Player):
        return player.consent  and player.isTrainingPassed

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
        p_ops = json.loads(player.ps)
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
        for currP in json.loads(player.ps).keys():
            currP_op = [p_ops[currP][q] for q in questions]
            currP_op = ["" if str(op) == "nan" else op for op in currP_op]
            dot_descrs[currP] = "; ".join(
                [
                    f"{C.QUESTIONSHORTTEXT[lan][q]}: {op if lan=='en' else op}"
                    for q, op in zip(questions, currP_op)
                ]
            )

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
            "nslide": 3 + len(C.LABELLED) + C.NCONTACTS + 2 + 2 + 3,
            "lan_en": lan == "en",
            "dots": init_dots,
            "page_title": (
                "Overall satisfaction with your map"
                if lan == 'en'
                else "Zufriedenheit mit Ihrer Anordnung"
            ),
            "instru1": (
                "Below we show the political map you created."
                if lan == 'en'
                else "Im Folgenden finden Sie die von Ihnen erstellte politische Karte."
            ),
            "question": (
                "<p>How satisfied are you with your arrangement? Does the arrangement overall reflect your perception of the political similarities and differences between the individuals?</p>"
                if lan == 'en'
                else "<p>Wie zufrieden sind Sie mit Ihrer Anordnung? Entspricht die Gesamtanordnung Ihrer Wahrnehmung der politischen Ähnlichkeiten und Unterschiede zwischen den einzelnen Personen?</p>"
            ),
            "explain_text": (
                "If you would like, you can add further comments or explanations here (optional):"
                if lan == 'en'
                else "Falls Sie möchten, können Sie hier weitere Anmerkungen oder Erklärungen hinzufügen (optional):"
            ),
            "choices": list(range(0, 11)),
            "satisfaction_min": 0,
            "satisfaction_max": 10,
            "satisfaction_min_label": (
                "Not accurate at all" if lan == 'en' else "Trifft überhaupt nicht zu"
            ),
            "satisfaction_max_label": (
                "Completely accurate" if lan == 'en' else "Trifft voll und ganz zu"
            ),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.t_on_relationships = int(time.time())


#################################
#####  Social Relationships   #####
#################################
class slide11_Relationships(Page):
    form_model = "player"
    form_fields = [f"contact{n}_socialCloseness" for n in range(1, C.NCONTACTS + 1)]

    @staticmethod
    def is_displayed(player: Player):
        return player.consent  and player.isTrainingPassed

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        field_question_pairs = []
        fields = [f"contact{n}_socialCloseness" for n in range(1, C.NCONTACTS + 1)]

        for field, n in zip(fields, range(1, C.NCONTACTS + 1)):
            choices = dict(
                zip(
                    C.OPTIONS_CONTACTS_CLOSE,
                    (
                        C.OPTIONS_CONTACTS_CLOSE
                        if lan == 'en'
                        else [
                            "Nicht besonders nah",
                            "Etwas nah",
                            "Sehr nah",
                            "Extrem nah",
                            "Keine Angabe",
                        ]
                    ),
                )
            )
            field_question_pairs.append(
                {
                    "field_name": field,
                    "question_text": (
                        f"Your relation with <span class='pill' style='background-color: {C.FRIENDCOLOR}; color: white;'><strong>{getattr(player, f'contact{n}')}</strong></span>"
                        if lan == 'en'
                        else f"Ihre Beziehung zu <span class='pill' style='background-color: {C.FRIENDCOLOR}; color: white;'><strong>{getattr(player, f'contact{n}')}</strong></span>"
                    ),
                    "choices": choices,
                }
            )
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": 3 + len(C.LABELLED) + C.NCONTACTS + 2 + 2 + 4,
            "lan_en": lan == "en",
            "page_title": (
                "<em>Social</em> Closeness to the Contacts"
                if lan == 'en'
                else "<em>Soziale</em> Nähe zu den Kontakten"
            ),
            "field_question_pairs": field_question_pairs,
            "qu_closeness": (
                "How would you rate in general the social closeness to your contacts mentioned – regardless of political views?"
                if lan == 'en'
                else "Wie würden Sie allgemein die soziale Nähe zwischen Ihnen und den genannten Kontakten einschätzen – unabhängig von politischen Ansichten?"
            ),
            "disclaimer": (
                "All your responses are linked to generic names <em>Contact 1</em>, <em>Contact 2</em>, etc. To protect privacy, we do <strong>not store</strong> the actual names or initials of your social contacts."
                if lan == 'en'
                else "Alle Ihre Antworten werden generischen Bezeichnungen wie <em>Kontakt 1</em>, <em>Kontakt 2</em> usw. zugeordnet. Zum Schutz der Privatsphäre werden die von Ihnen angegebenen Namen oder Initialen <strong>nicht gespeichert</strong>.."
            ),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.t_on_demographics = int(time.time())


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
        return player.consent  and player.isTrainingPassed


    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": 3 + len(C.LABELLED) + C.NCONTACTS + 2 + 2 + 5,
            "lan_en": lan == "en",
            "page_title": (
                "Final questions"
                if lan == 'en'
                else "Abschließende Fragen"
            ),
            "qu_age": "How old are you?" if lan == 'en' else "Wie alt sind Sie?",
            "qu_interest": (
                "How interested would you say you are in politics – are you..."
                if lan == 'en'
                else "Wie sehr sind Sie persönlich an Politik interessiert? Sind Sie ...?"
            ),
            "choices_interest": dict(
                zip(
                    C.CHOICES_INTEREST,
                    (
                        C.CHOICES_INTEREST
                        if lan == 'en'
                        else [
                            "Überhaupt nicht interessiert",
                            "Kaum interessiert",
                            "Ziemlich interessiert",
                            "Sehr interesiert",
                        ]
                    ),
                )
            ),
            "qu_identity": (
                "Do you feel closer to one of the political parties in Germany than the others? If so, which one?"
                if lan == 'en'
                else "Gibt es eine bestimmte politische Partei in Deutschland, der Sie sich politisch näher fühlen als allen anderen Parteien? Welcher?"
            ),
            "choices_identity": dict(
                zip(
                    C.CHOICES_IDENTITY,
                    (
                        C.CHOICES_IDENTITY
                        if lan == 'en'
                        else [
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
                    ),
                )
            ),
            "qu_party_comment": (
                "Would you like to add anything to the question above? (optional):"
                if lan == 'en'
                else "Möchten Sie etwas dazu ergänzen zu dieser Frage? (optional)"
            ),
            "qu_polarization": (
                "What do you think: How politically divided are the people in your country these days?"
                if lan == 'en'
                else "Was denken Sie: Wie politisch gespalten sind die Menschen in Ihrem Land heutzutage?"
            ),
            "choices_pol": dict(
                zip(
                    C.CHOICES_POLARISED,
                    (
                        C.CHOICES_POLARISED
                        if lan == 'en'
                        else [
                            "Überhaupt nicht gespalten",
                            "Etwas gespalten",
                            "Sehr gespalten",
                            "Extrem gespalten",
                        ]
                    ),
                )
            ),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.t_on_success = int(time.time())


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
            "maxslides": C.MAXSLIDES,
            "nslide": 3 + len(C.LABELLED) + C.NCONTACTS + 2 + 2 + 6,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.completed = True

    def is_displayed(player: Player):
        return player.consent  and player.isTrainingPassed



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
    + [slide04_PersonOpinion] * (C.NCONTACTS + len(C.LABELLED))
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
