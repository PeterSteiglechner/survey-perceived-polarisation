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
        "regulate_internet",
        "east_germans",
    ]

    # QU_SORTS = [[0, 1, 2, 3], [1, 3, 0, 2], [2, 0, 3, 1], [3, 2, 1, 0]]
    # QU_SORTS = list(
    #     np.random.choice(range(len(QUS)), replace=False, size=len(QUS))
    # )  # [[0, 1, 2, 3], [1, 3, 0, 2], [2, 0, 3, 1], [3, 2, 1, 0]]

    QUESTIONTEXT = {
        "en": dict(
            zip(
                QUS,
                [
                    "I am very concerned about climate change.",
                    "It is good that same-sex marriages are allowed.",  # between two women or two men
                    "Migrants should have the same rights as natives – regardless of whether they make an effort and integrate.",  # Only migrants who make an effort and integrate should be given the same rights as natives.
                    "Income and wealth inequality in Germany is too high.",
                    "Digital technologies, including the internet and social media, should be more strongly regulated.",
                    "The lifetime achievements of East Germans should be recognized more.",
                ],
            )
        ),
        "de": dict(
            zip(
                QUS,
                [
                    "Ich bin sehr besorgt über den Klimawandel.",
                    "Es ist gut, dass gleichgeschlechtliche Ehen erlaubt sind.",  #  zwei Frauen bzw. zwischen zwei Männern
                    "Migranten und Migrantinnen sollten die gleichen Rechte wie Einheimische haben – unabhängig davon, ob sie sich anstrengen und integrieren.",
                    # Nur Migranten, die sich anstrengen und integrieren, sollten die gleichen Rechte bekommen wie Einheimische.
                    "Die Einkommens- und Vermögensunterschiede in Deutschland sind zu groß.",
                    "Digitale Technologien, insbesondere das Internet und soziale Medien, sollten stärker reguliert werden.",
                    "Die Lebensleistungen der Ostdeutschen sollten stärker anerkannt werden.",
                ],
            )
        ),
    }
    QUESTIONSHORTTEXT = {
        "en": dict(
            zip(
                QUS,
                [
                    "Strong concern about climate change",
                    "Strong same-sex marriage support",
                    "Equal rights for migrants, independent of integration efforts",
                    "Income and wealth inequalities are too high",
                    "Stronger regulation of Internet and social media",
                    "More recognition for East Germans",
                ],
            )
        ),
        "de": dict(
            zip(
                QUS,
                [
                    "Extreme Besorgnis wegen des Klimawandels",
                    "Unterstützung für gleichgeschlechtliche Ehen",
                    "Gleiche Rechte für Migranten/-innen, unabhängig vom Integrationsgrad",
                    "Einkommens- und Vermögens-unterschiede zu groß",
                    "Stärkere Regulierung von Internet und sozialen Medien",
                    "Mehr Anerkennung für Ostdeutsche",
                ],
            )
        ),
    }

    QUESTIONNAMES = {
        "en": dict(
            zip(
                QUS,
                [
                    "...are concerned about climate change?",  # "on climate change concerns",
                    "...approve that same-sex marriages are allowed?",  # "on same-sex marriage",
                    "...believe that equal rights for migrants should be independent of their integration?",  # "on migrants' rights",  # "Opinion about whether equal rights for migrants should be given regardless of their integration efforts",
                    "...think that economic inequalities are too high?",  # "on economic inequalities",
                    "...support stronger regulation of the internet and social media?",
                    "...think there should be more recognition of East Germans' lifetime achievements?",
                ],
            )
        ),
        "de": dict(
            zip(
                QUS,
                [
                    "...wegen des Klimawandels besorgt sind?",  # "beim Thema Besorgnis über den Klimawandel",
                    "...es gut finden, dass gleichgeschlechtliche Ehen erlaubt sind?",  # "beim Thema gleichgeschlechtliche Ehen",
                    "...finden, dass Migrantinnen und Migranten gleiche Rechte haben sollten, unabhängig von deren Integration?",  # "beim Thema Rechte für Migranten und Migrantinnen",  # "Die Meinung der Person ob Migranten oder Migrantinnen unabhängig von Integrationsbemühungen die gleichen Rechte wie Einheimische bekommen sollten",
                    "...denken, dass ökonomische Ungleichheiten zu groß sind?",  # "beim Thema ökonomische Ungleichheiten",
                    "...finden, dass das Internet und soziale Medien stärker reguliert werden sollten?",
                    "...finden, dass die Lebensleistungen der Ostdeutschen stärker anerkannt werden sollten?",
                ],
            )
        ),
    }

    QUESTIONNAMESPOL = {
        "en": dict(
            zip(
                QUS,
                [
                    "on concern about climate change",  # "on climate change concerns",
                    "on same-sex marriage support",  # "on same-sex marriage",
                    "on whether equal rights for migrants should depend on integration",  # "on migrants' rights",  # "Opinion about whether equal rights for migrants should be given regardless of their integration efforts",
                    "on the evaluation economic inequalities",  # "on economic inequalities",
                    "on internet and social media regulation",
                    "on the recognition of east german achievements",
                ],
            )
        ),
        "de": dict(
            zip(
                QUS,
                [
                    "über die Besorgnis wegen des Klimawandels",  # "beim Thema Besorgnis über den Klimawandel",
                    "zum Thema gleichgeschlechtliche Ehen",  # "beim Thema gleichgeschlechtliche Ehen",
                    "darüber ob gleiche Rechte für Migrantinnen und Migranten von deren Integration abhängen sollten",  # "beim Thema Rechte für Migranten und Migrantinnen",  # "Die Meinung der Person ob Migranten oder Migrantinnen unabhängig von Integrationsbemühungen die gleichen Rechte wie Einheimische bekommen sollten",
                    "über Einschätzungen zu ökonomischen Ungleichheiten",  # "beim Thema ökonomische Ungleichheiten",
                    "über die Regulierung von Internet und sozialen Medien",
                    "über die Anerkennung von Ostdeutschen Lebensleistungen",
                ],
            )
        ),
    }

    # QUS_OTHERS = [
    #     "regulate_internet",
    #     # "monitor_health",
    #     "social_housing",
    #     "gmo_safe",
    #     "east_germans",
    #     "voluntary_work",
    #     "wages_politicians",
    # ]
    # QUESTIONS_OTHERS = {
    #     "en": dict(
    #         zip(
    #             QUS_OTHERS,
    #             [
    #                 "The internet should be regulated much more strongly.",  # # Source GESIS GLES https://search.gesis.org/research_data/ZA5722  #es sollte überhaupt keine Kontrolle des Internets geben
    #                 # "In a public health crisis, such as during a pandemic, it is more important to monitor and track the population than to protect individuals' privacy.",  # Source: ESS 10SC Is it more important for governments to onitor and track the public or to maintain public privacy when fighting a pandemic?
    #                 "There is a serious shortage of social housing in Germany.",
    #                 "The production and consumption of genetically modified foods is a societal risk.",  # based on ESS
    #                 "The lifetime achievements of East Germans should be recognized more.",  # Triggerpunkte
    #                 "Voluntary work should be credited towards future pensions.",
    #                 "Politicians should receive lower remuneration for their public service.",  # https://www.ifo.de/DocDL/cesifo1_wp11778.pdf"
    #             ],
    #         )
    #     ),
    #     "de": dict(
    #         zip(
    #             QUS_OTHERS,
    #             [
    #                 "Das Internet sollte viel stärker kontrolliert werden.",
    #                 # "In einer öffentlichen Gesundheitskrise, wie z.B. einer Pandemie, ist es wichtiger, die Bevölkerung zu überwachen und nachzuverfolgen, als die Privatsphäre von Personen zu schützen.",
    #                 "In Deutschland herrscht ein gravierender Mangel an Sozialwohnungen.",
    #                 "Die Herstellung und der Verzehr gentechnisch veränderter Lebensmittel stellen ein gesellschaftliches Risiko dar.",
    #                 "Die Lebensleistungen der Ostdeutschen sollten stärker gewürdigt werden.",
    #                 "Ehrenamtliche Tätigkeiten sollten auf die zukünftige Rente angerechnet werden.",
    #                 "Politiker und Politikerinnen sollten für ihren öffentlichen Dienst eine geringere Vergütung erhalten.",
    #             ],
    #         )
    #     ),
    #     # The lifetime achievements of East Germans should be recognized more.  TRIGGERPUNKTE
    #     # Significantly more wind turbines should be erected, even if this has to be done close to towns and villages.
    # }
    N_PERSONS = 10
    N_PAIRWISE_FIX = True
    MIN_REFERENCES = 7
    MAX_REFERENCE_LEN = 10  # characters

    # N_BATCHES = 2
    REFPERSONCOLOR = "#FF8C42"
    SELFCOLOR = "#BC9CE0FF"  # "#9B7EBD"
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
                " (<em>Bündnis Sahra Wagenknecht</em>)",
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

    # NLABELLED = 7  # len(LABELLED)
    MAXSLIDES = 17
    #  op
    #  id + toc
    #  references
    #  person Op
    # 5 voter Op + toc
    #  MapGame
    #  MapTest
    #  Map + toc
    #  Satis
    # 10 Pairiwse
    #  + toc
    #  compare Task
    #  importance
    #  relationships
    # 15 identity Identities
    #  demographics
    #  end

    FORCED_PAIRS = (
        []
    )  # ("Green Party", "AfD"), ("self", "AfD"), ("self", "Green Party")]

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
        "Keine Angabe",
    ]

    CHOICES_GENDER = ["Female", "Male", "Diverse", "Refuse to say/No answer"]
    CHOICES_GENDER_DE = ["Weiblich", "Männlich", "Divers", "Keine Angabe"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def slider(min, max, label="", blank=False, nan=False):
    return models.IntegerField(
        choices=list(range(min, max + 1)) + ([-999] if nan else []),
        label=label,
        widget=widgets.RadioSelect,
        blank=blank,
    )


def define_reference(label, n, blank=False):
    return models.LongStringField(label=label, blank=blank, max_length=20)


class Player(BasePlayer):

    completed = models.BooleanField(inital=False)

    consent = models.BooleanField(blank=False)

    recontact = models.BooleanField(blank=False)

    question_sorting = models.LongStringField(initial="")
    voter_sorting = models.LongStringField(initial="")

    language = models.StringField(
        choices=[["en", "English"], ["de", "Deutsch"]],
        widget=widgets.RadioSelect,
        label="Language / Sprache",
    )

    overall_comments = models.LongStringField(label="", blank=True)

    age = models.IntegerField(label="", min=18, max=100)

    gender = models.StringField(
        label="", blank=False, widget=widgets.RadioSelect, choices=C.CHOICES_GENDER
    )

    political_discussion = slider(0, 100)

    political_interest = slider(0, 100)

    feel_closest_party = models.StringField(
        label="", choices=C.CHOICES_IDENTITY, blank=False, widget=widgets.RadioSelect
    )

    lrscale = slider(-50, +50, label="lrscale")

    party_comment = models.LongStringField(label="", blank=True)

    how_polarised = slider(0, 100)

    how_polarised_comments = models.LongStringField(label="", blank=True)

    importance_comments = models.LongStringField(
        blank=True, label="", initial="", null=True
    )
    # importance_other_comments = models.LongStringField(
    #     blank=True, label="", initial="", null=True
    # )

    n_references = models.IntegerField(blank=True)

    nudged_for_variation = models.BooleanField(initial=False)

    #################################
    #####  TIME   #####
    #################################
    visited_toc = models.IntegerField(blank=False, initial=0)

    t_on_consent = models.IntegerField(blank=True)
    t_on_ownOpinion = models.IntegerField(blank=True)
    t_on_identity = models.IntegerField(blank=True)
    t_on_toc1 = models.IntegerField(blank=True)
    t_on_nameRefPeople = models.IntegerField(blank=True)
    t_on_referencesOpinions = models.IntegerField(blank=True)
    t_on_voterOpinions = models.IntegerField(blank=True)
    t_on_ownOpinion2 = models.IntegerField(blank=True)
    t_on_toc2 = models.IntegerField(blank=True)
    t_on_practiceGame = models.IntegerField(blank=True)
    t_on_practice = models.IntegerField(blank=True)
    t_practicesSubmitted = models.LongStringField(blank=True, initial="{}")
    t_on_practiceResult_first = models.IntegerField(blank=True)
    t_on_map = models.IntegerField(blank=True)
    t_firstDotMoved = models.IntegerField(blank=True)
    t_on_satisfaction = models.IntegerField(blank=True)
    # t_on_mapP = models.IntegerField(blank=True)
    t_on_toc3 = models.IntegerField(blank=True)
    t_on_pairwise = models.IntegerField(blank=True)
    t_after_first_pair = models.IntegerField(blank=True)
    t_submittedPairs = models.LongStringField(blank=True, initial="{}")
    t_on_toc4 = models.IntegerField(blank=True)
    t_on_taskCompare = models.IntegerField(blank=True)
    t_on_importance = models.IntegerField(blank=True)
    # t_on_importance_other = models.IntegerField(blank=True)
    t_on_polarisation = models.IntegerField(blank=True)
    t_on_relationships = models.IntegerField(blank=True)
    t_on_contactIdentities = models.IntegerField(blank=True)
    t_on_politicalinterest = models.IntegerField(blank=True)
    t_on_success = models.IntegerField(blank=True)
    t_on_fail = models.IntegerField(blank=True)

    #################################
    #####  MAP POSITIONS   #####
    #################################

    # JSON data of positions
    positionsGame = models.LongStringField(blank=True)
    positionsTest = models.LongStringField(blank=True)
    positions = models.LongStringField(blank=True)
    min_pair = models.LongStringField(blank=True)
    max_pair = models.LongStringField(blank=True)

    #################################
    #####  Similarity ratings   #####
    #################################

    valid_pairs = models.LongStringField(blank=True, initial="")
    pairSequence = models.LongStringField(blank=True, initial="")

    n_check = models.IntegerField(initial=1)
    n_checks = models.IntegerField(initial=0)
    n_dots = models.IntegerField(initial=0)

    satisfaction = slider(0, 100)
    # accurateMapping = slider(0, 100)
    mappingEnjoy = slider(-50, 50)
    mappingEasier = slider(-50, 50)
    satisfaction_text = models.LongStringField(label="", blank=True)
    task_text = models.LongStringField(label="", blank=True)

    #################################
    #####  PRACTICE RUN   #####
    #################################

    isTrainingPassed = models.BooleanField(initial=False)  #
    is_distS2F_gt_distS2C = models.BooleanField(initial=False)  #
    is_distF2C_gt_distS2C = models.BooleanField(initial=False)  #
    is_distS2R_gt_distS2F = models.BooleanField(initial=False)  #
    # is_distS2R_gt_distF2RanddistC2R = models.BooleanField(initial=False)  #
    is_distsRCS_similar = models.BooleanField(initial=False)
    is_FR_gt_SR = models.BooleanField(blank=True)
    practice_sanity_check_answer = models.StringField(blank=True)
    practice_sanity_check_correct = models.BooleanField(initial=False)
    attempts_sanity_check = models.IntegerField(initial=1)
    attemptPractice = models.IntegerField(initial=0)
    latest_error_msg = models.LongStringField(blank=True, initial="")

    #################################
    #####  RUNNING VARIABLES   #####
    #################################

    # current_reference = models.IntegerField(initial=1)
    # evaluated_labelledPerson = models.IntegerField(initial=0)
    # current_batch = models.IntegerField(initial=1)
    current_page = models.IntegerField(initial=0)


#################################
#####  OWN POLITICAL OPINIONS   #####
#################################
for q in C.QUS:
    setattr(Player, f"own__{q}", slider(-100, 100, nan=True))
    setattr(Player, f"own2__{q}", slider(-100, 100, nan=True))
    setattr(Player, f"how_polarised_{q}", slider(0, 100))

#################################
#####  PERSONS & PERSONS' POLITICAL OPINIONS   #####
#################################
for n in range(1, C.N_PERSONS + 1):
    setattr(
        Player,
        f"reference{n}",
        define_reference(f"Person {n}: ", n, blank=True),  # (n > C.MIN_REFERENCES)),
    )
    setattr(
        Player,
        f"reference{n}_socialCloseness",
        slider(0, 100, blank=(n > C.MIN_REFERENCES)),
    )
    setattr(
        Player,
        f"reference{n}_PartyFeelClosest",
        models.StringField(
            label="",
            choices=C.CHOICES_IDENTITY + ["I don't know"],
            blank=(n > C.MIN_REFERENCES),
            widget=widgets.RadioSelect,
        ),
    )
    for q in C.QUS:
        setattr(
            Player,
            f"reference{n}__{q}",
            slider(-100, 100, blank=(n > C.MIN_REFERENCES)),
        )

#################################
#####  LABELLED INDIVIDS' POLITICAL OPINIONS   #####
#################################
for name in C.LABELLED:
    for q in C.QUS:
        setattr(Player, f"{name.replace(' ', '')}__{q}", slider(-100, 100))


#################################
#####  PAIRWISE SIMILARITY RATING   #####
#################################
for n in range(1, 1 + C.N_PERSONS + len(C.LABELLED) + 1):
    # setattr(Player, f"checkPair{n}_dot1", models.LongStringField(blank=True))
    # setattr(Player, f"checkPair{n}_dot2", models.LongStringField(blank=True))
    setattr(Player, f"similarityPair{n}", slider(0, 100))

###########################
####  Importance
###########################
for q in C.QUS:
    setattr(Player, f"importance_{q}", slider(0, 100))
# for q in C.QUS_OTHERS:
#     setattr(Player, f"importance_{q}", slider(0, 100))


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
    form_fields = ["consent"]  # , "language"]

    @staticmethod
    def vars_for_template(player: Player):
        player.language = "de"
        if player.field_maybe_none(f"t_on_consent") is None:
            player.t_on_consent = int(time.time())

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.question_sorting = json.dumps(
            np.random.choice(range(len(C.QUS)), replace=False, size=len(C.QUS)).tolist()
            # C.QU_SORTS[np.random.choice(range(len(C.QU_SORTS)))]
        )
        voters = list(np.random.choice(C.LABELLED, replace=False, size=len(C.LABELLED)))
        player.voter_sorting = json.dumps(voters)
        player.current_page += 1


#################################
#####  Overview   #####
#################################
class slide00_toc(Page):
    form_model = "player"
    form_fields = []

    @staticmethod
    def is_displayed(player):
        # trainingPassed = player.isTrainingPassed
        return player.consent  # and (player.visited_toc < 3 or trainingPassed)

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.visited_toc == 0 and player.field_maybe_none(f"t_on_toc1") is None:
            player.t_on_toc1 = int(time.time())
        elif player.visited_toc == 1 and player.field_maybe_none(f"t_on_toc2") is None:
            player.t_on_toc2 = int(time.time())
        if player.visited_toc == 2 and player.field_maybe_none(f"t_on_toc3") is None:
            player.t_on_toc3 = int(time.time())
        if player.visited_toc == 3 and player.field_maybe_none(f"t_on_toc4") is None:
            player.t_on_toc4 = int(time.time())

        n_checks = {0: 1, 1: 3, 2: 4, 3: 5}[player.visited_toc]
        checks = ["<span saclass='checkmark'>✅</span>  "] * n_checks + [
            "<span saclass='checkmark upcoming'>⬜</span>  "
        ] * 6
        hl = {
            0: [0, 0, 0, 0, 0, 0],
            1: [0, 0, 0, 0, 0, 0],
            2: [0, 0, 0, 0, 0, 0],
            3: [0] * 6,
        }[player.visited_toc]
        hls = ["" if not hl_li else " class='upcoming'" for hl_li in hl]
        if lan == "en":
            items = f"<ul><li{hls[0]}>{checks[0]}Your own political opinions</li><li{hls[1]}>{checks[1]}Political opinions of other people</li><li{hls[3]}>{checks[3]}Creating your own political map <em>(with two short practice tasks)</em></li><li{hls[4]}>{checks[4]}Pairwise comparison of the political views of individuals</li><li{hls[5]}>{checks[5]}Short concluding questions</li></ul>"
            if player.visited_toc == 0:
                i1 = "Thank you very much for your responses so far!<br>Below you can find an overview of the remaining tasks."  # in this survey. On the next pages, we will continute with the ones highlighted in <span class='upcoming'>yellow</span>."
                i2 = ""
            if player.visited_toc == 1:
                i1 = "Thank you very much for your evaluations of the political views of other individuals!"  # ➡️ In the following part, we will ask you to place people on a political map based on how similar or different you perceive their political views to be."
                i2 = "➡️ In the following, we ask you to place individuals on a self-created, political map. To prepare you for this task, we ask you to complete <strong>two short practice tasks</strong>."
            if player.visited_toc == 2:
                i1 = "Thank you very much for creating your own personal political map!"
                i2 = "➡️ To help us better understand your political map, we ask you to again evaluate the political similarity between a few (randomly selected) pairs of individuals."
            if player.visited_toc == 3:
                i1 = "Thank you! This was the main part of the survey."
                i2 = "➡️ We will close the survey with a few short questions about the previous tasks."
        else:
            items = f"<ul><li{hls[0]}>{checks[0]}Ihre eigenen politischen Ansichten</li><li{hls[1]}>{checks[1]}Die politischen Ansichten anderer Personen</li><li{hls[3]}>{checks[3]}Ihre persönliche politische Karte <em>(plus zwei kurze Übungsaufgaben)</em></li> <li{hls[4]}>{checks[4]}Paarweiser Vergleich der politischen Ansichten von einzelnen Personen</li><li{hls[5]}>{checks[5]}Kurze Abschlussfragen </li></ul>"
            # (Menschen in Ihrem sozialen Umfeld und typische Wählerinnen und Wähler)
            # items = f"<ul><li{hls[0]}>{checks[0]}Ihre eigenen politischen Ansichten und Identität</li><li{hls[1]}>{checks[1]}Ihre Einschätzungen über die politischen Ansichten von Personen oder Kontakten, die Sie gut kennen und deren Meinungen Ihnen vertraut sind.</li> <li{hls[2]}>{checks[2]}Ihre Einschätzungen über die politischen Ansichten typischer Wählerinnen und Wähler der politischen Parteien in Deutschland</li>  <li{hls[3]}>{checks[3]}Die genannten Personen auf einer persönlichen politischen Karte verorten<br>(inklusive zwei kurzer Übungsaufgaben)</li> <li{hls[4]}>{checks[4]}Ihre Einschätzungen über die politische Ähnlichkeit einzelner Personen zueinander</li>  <li{hls[5]}>{checks[5]}Abschlussfragen zur Umfrage, über Ihre sozialen Beziehungen zu den genannten Personen oder Kontakten und über Ihre Person</li></ul>"
            if player.visited_toc == 0:
                i1 = "Vielen Dank für Ihre Antworten bisher!<br>Unten finden Sie eine Übersicht der noch anstehenden Aufgaben."  # Auf den nächsten Seiten werden wir mit den <span class='upcoming'>gelb</span> markierten beginnen.# ➡️ In den folgenden Seiten geht es um Ihre Einschätzungen zu den politischen Ansichten von Ihren sozialen Kontakten und von typischen Wählern oder Wählerinnen."
                i2 = ""
            if player.visited_toc == 1:
                i1 = "Vielen Dank für Ihre Einschätzungen über die politischen Ansichten von anderen Personen!"  # ➡️ Im folgenden Teil werden wir Sie bitten, Personen auf einer politischen Karte zu platzieren, je nachdem, wie ähnlich oder unterschiedlich Sie deren politische Ansichten wahrnehmen."
                i2 = "➡️ Im Folgenden werden wir Sie bitten, die Personen auf einer von Ihnen erstellten politischen Karte zu platzieren. Zur Vorbereitung auf diese Aufgabe, bitten wir Sie <strong>zwei kurze Übungsaufgaben</strong> zu bearbeiten."
            if player.visited_toc == 2:
                i1 = "Vielen Dank für das Erstellen Ihrer persönlichen politischen Karte!"
                i2 = "➡️ Um uns dabei zu helfen, Ihre Antworten besser zu verstehen, bitten wir Sie zunächst nochmals die Ähnlichkeit der politischen Ansichten einiger (zufällig ausgewählter) Paare einzuschätzen."
            if player.visited_toc == 3:
                i1 = "Vielen Dank! Das Erstellen der politischen Karte und die paarweisen Vergleiche waren der Hauptteil dieser Umfrage."
                i2 = "➡️ Wir werden die Umfrage nun mit einigen kurzen Fragen zu den vorangegangenen Aufgaben abschließen."
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


#################################
#####  Own opinions   #####
#################################
# class slide02_Opinions(Page):
class slide02_OpinionsWithNan(Page):
    form_model = "player"
    form_fields = [f"own__{q}" for q in C.QUS]

    @staticmethod
    def is_displayed(player: Player):
        return player.consent

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_ownOpinion") is None:
            player.t_on_ownOpinion = int(time.time())
        questions = [C.QUS[i] for i in json.loads(player.question_sorting)]

        fields = [f"own__{q}" for q in questions]
        questions = []
        for q in [C.QUS[i] for i in json.loads(player.question_sorting)]:
            questions.append(
                {
                    "prefix": f"{q}",
                    "text": C.QUESTIONTEXT[lan][q],
                }
            )
        field_question_pairs = []
        for field, question in zip(fields, questions):
            field_question_pairs.append(
                {
                    "field_name": field,
                    "question_text": question,
                }
            )
        pillname = (
            lambda name: f"<span class='pill' style='background-color: {C.SELFCOLOR}; color: white;'>{name}</span>"
        )
        return {
            "lan_en": lan == "en",
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "questions": questions,
            "color": C.SELFCOLOR,
            "field_question_pairs": field_question_pairs,
            "page_title": (
                "Your Political Views"
                if player.language == "en"
                else "Ihre Politischen Ansichten"
            ),
            "first_label": C.LIKERT7[0] if lan == "en" else C.LIKERT7_de[0],
            "neutral_label": C.LIKERT7[3] if lan == "en" else C.LIKERT7_de[3],
            "last_label": C.LIKERT7[6] if lan == "en" else C.LIKERT7_de[6],
            "instruction_text": (
                "<p>We are interested in this survey in your own political opinions among other things. </p><p>Please indicate to what extent you agree or disagree with the following statements.</p><p>There are no right or wrong answers! Please select the response option that is most aligned with your own views.</p>"
                if player.language == "en"
                else "<p>Wir interessieren uns in dieser Umfrage unter Anderem für Ihre eigenen politischen Ansichten.</p><p> Bitte geben Sie an, inwieweit Sie den folgenden Aussagen zustimmen oder nicht zustimmen.</p><p>Es gibt keine richtigen oder falschen Antworten! Wählen Sie bitte die Antwortmöglichkeit, die am ehesten Ihren Ansichten entspricht.</p>"
            ),
            "overallquestion": (
                f"To what extent do {pillname('you')} agree with the statement?"
                if player.language == "en"
                else f"Inwieweit stimmen {pillname('Sie')} der Aussage oben zu?"
            ),
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.current_page += 1


#################################
#####  IDENTITY   #####
#################################
class slide02a_Identity(Page):
    form_model = "player"
    form_fields = [
        "feel_closest_party",
        "lrscale",
        "party_comment",
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.consent

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_identity") is None:
            player.t_on_identity = int(time.time())
        question = (
            "In politics, people sometimes talk of 'left' and 'right'. Where would you place yourself on this scale, if -5 means 'left' and 5 means 'right'?"
            if lan == "en"
            else "In der Politik spricht man manchmal von 'links' und 'rechts'. Wo auf der Skala von -5 bis 5 würden Sie sich selbst einstufen, wenn -5 für 'links' und 5 für 'rechts' steht?"
        )
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "page_title": (
                "Your Political Identity"
                if lan == "en"
                else "Ihre Politische Identität"
            ),
            "qu_identity": (
                "In Germany, many people tend to lean toward a particular political party for long periods of time, even though they occasionally vote for another party. How about you: do you generally lean toward a particular party? And if so, which one?"  # "Do you feel closer to one of the political parties in Germany than the others? If so, which one?"
                if lan == "en"
                else "In Deutschland neigen viele Leute längere Zeit einer bestimmten politischen Partei zu, obwohl sie auch ab und zu eine andere Partei wählen. Wie ist das bei Ihnen: Neigen Sie - ganz allgemein - einer bestimmten Partei zu? Und wenn ja, welcher?"  # "Gibt es eine bestimmte politische Partei in Deutschland, der Sie sich politisch näher fühlen als allen anderen Parteien? Welcher?"  # In Deutschland neigen viele Leute längere Zeit einer bestimmten politischen Partei zu, obwohl sie auch ab und zu eine andere Partei wählen. Wie ist das bei Ihnen: Neigen Sie - ganz allgemein - einer bestimmten Partei zu? Und wenn ja, welcher?
            ),
            "choices_identity": dict(
                zip(
                    C.CHOICES_IDENTITY,
                    (C.CHOICES_IDENTITY if lan == "en" else C.CHOICES_IDENTITY_DE),
                )
            ),
            "qu_party_comment": (
                "Would you like to add anything to the question above? <em>(optional)</em>:"
                if lan == "en"
                else "Möchten Sie etwas zu dieser Frage ergänzen? <em>(optional)</em>"
            ),
            "lr_question": question,
            "lr_first_label": (
                "left <em>(-5)</em>" if lan == "en" else "links <em>(-5)</em>"
            ),
            "lr_last_label": (
                "right <em>(5)</em>" if lan == "en" else "rechts <em>(5)</em>"
            ),
            # "lr_choices": dict(zip(np.arange(0, 10.1, 1), np.arange(0, 10.1, 1))),
            "partytext": (
                "In the following, we will use<ul style='font-size: 8pt; color: grey'><li><em>Green party</em> for the party Bündnis 90/Die Grünen and</li><li><em>Left party</em> for the party Die Linke.</li><li>Note: <em>BSW</em> for Bündnis Sahra Wagenknecht.</li></ul>"
                if lan == "en"
                else "Im Folgenden benutzen wir<ul style='font-size: 8pt; color: grey'><li><em>Grüne</em> für die Partei Bündnis 90/Die Grünen und</li><li><em>Linke</em> für die Partei Die Linke.</li><li><em>BSW</em> steht für Bündnis Sahra Wagenknecht.</li></ul>"
            ),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.current_page += 1


#################################
#####  Contacts   #####
#################################
class slide03_References(Page):
    form_model = "player"
    form_fields = [f"reference{n}" for n in range(1, C.N_PERSONS + 1)]

    @staticmethod
    def is_displayed(player: Player):
        return player.consent

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_nameRefPeople") is None:
            player.t_on_nameRefPeople = int(time.time())
        references_fields = []
        for n in range(1, C.N_PERSONS + 1):
            field_value = player.field_maybe_none(f"reference{n}")
            references_fields.append(
                {
                    "name": f"reference{n}",
                    "label": f"Person {n}:" if lan == "en" else f"Person {n}:",
                    "value": field_value if field_value is not None else "",
                    "max_length": C.MAX_REFERENCE_LEN,
                }
            )
        return {
            "lan_en": lan == "en",
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "nreferences": C.N_PERSONS,
            "references_fields": references_fields,
            "page_title": (
                "Your Social Circle" if lan == "en" else "Ihr Soziales Umfeld"
            ),
            "instruction_text0": (
                "Next to your own political opinions, we are also interested in the opinions in your social circle."
                if lan == "en"
                else "Neben Ihren eigenen politischen Meinungen interessieren wir uns auch für die Meinungen in Ihrem sozialen Umfeld."
            ),
            "instruction_text1": (
                f"Please think about <strong>{C.N_PERSONS} people</strong> who you would count to your social circle. This may include friends, family members, colleagues (who you value), or other people <ul style='margin-top:-1em;'><li>whose opinions matter to you personally, </li><li>who have a substantial influence on you, or </li><li>with whom you talk about politics or world events in person or otherwise.</li></ul>"
                if lan == "en"
                else f"Denken Sie bitte an <strong>{C.N_PERSONS} Personen</strong>, die Sie zu Ihrem sozialen Umfeld zählen würden. Dazu können zum Beispiel, Freunde, Familienmitglieder, Kolleginnen (die Sie wertschätzen), oder andere Personen gehören, <ul style='margin-top:-1em;'><li>deren Meinungen für Sie persönlich wichtig sind, </li><li>die einen großen Einfluss auf Sie haben, oder</li><li>mit denen Sie sich persönlich oder anderweitig über Politik und Weltgeschehen austauschen.</li></ul>"
            ),
            "disclaimer2": (
                f"It can be difficult to come up with {C.N_PERSONS} such contacts. However, since this is a critical part of our study, we ask you to name <em>at least {C.MIN_REFERENCES}</em> contacts. You may leave the last {C.N_PERSONS - C.MIN_REFERENCES} text boxes empty, but we would highly appreciate it if you can fill all {C.N_PERSONS}."
                if lan == "en"
                else f"Es kann schwer sein, {C.N_PERSONS} solche Kontakte zu nennen. Da dies aber ein wichtiger Teil unserer Umfrage ist, bitten wir Sie <em>zumindest {C.MIN_REFERENCES}</em> Kontakte zu nennen. Sie können die letzten {C.N_PERSONS - C.MIN_REFERENCES} Textfelder leer lassen; wir wären allerdings sehr dankbar, wenn Sie tatsächlich alle {C.N_PERSONS} ausfüllen."
            ),
            "instruction_text3": (
                "Please write down names or initials of the contacts below such that you can recognize them later (we will not use or store this information)."
                if lan == "en"
                else "Bitte notieren Sie unten die Namen oder Initialen dieser Personen, so dass Sie diese später wiedererkennen (wir werden diese Informationen weder verwenden noch speichern)."
            ),
            "reminder": (
                f"You will estimate on the next page how these {C.N_PERSONS} contacts would probably respond to the political questions from the first page. We recommend to choose people that you know relatively well."
                if lan == "en"
                else f"Sie werden auf der nächsten Seite einschätzen, wie diese {C.N_PERSONS} Kontakte wahrscheinlich auf die politischen Fragen auf der ersten Seite antworten würden. Wir empfehlen, Kontakte zu wählen, die Sie relativ gut kennen."
            ),
            # "instruction2": (
            #     "➡️ In the next slides, we will ask you what you think these people would respond to the political questions from the previous slide."
            #     if lan == "en"
            #     else "➡️ In den folgenden Seiten, fragen wir Sie was diese Personen Ihrer Meinung nach auf die politischen Fragen antworten würden."
            # ),
        }

    @staticmethod
    def error_message(player: Player, values):
        for field_name, value in values.items():
            if field_name.startswith("reference"):
                setattr(player, field_name, value)

        # Then check for minimum references
        references = [v.strip() for v in values.values() if v and v.strip()]
        if len(references) < C.MIN_REFERENCES:
            return (
                f"Please fill in at least the first {C.MIN_REFERENCES} fields!"
                if player.language == "en"
                else f"Bitte füllen Sie zumindest die ersten {C.MIN_REFERENCES} Felder aus!"
            )

        # Finally check for duplicates
        if len(set(references)) < len(references):
            return (
                "Each person must have a unique name. Please correct duplicates. You can use nicknames, initials, or anything that will later allow you to recognise the people."
                if player.language == "en"
                else "Jede Person muss einen eindeutigen Namen haben. Bitte korrigieren Sie Duplikate. Sie können Spitznamen, Initialien oder alles benutzen, was es Ihnen ermöglicht die Personen später wiedererkennen."
            )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.n_references = int(
            np.sum(
                [
                    len(getattr(player, f"reference{n}")) > 0
                    for n in range(1, C.N_PERSONS + 1)
                ]
            )
        )
        valid_pairs = list(
            combinations(
                ["self"]
                + [f"reference{c}" for c in range(1, player.n_references + 1)]
                + C.LABELLED,
                2,
            )
        )
        valid_pairs = [tuple(v) for v in valid_pairs if not v in C.FORCED_PAIRS]
        player.valid_pairs = json.dumps(valid_pairs)
        player.n_checks = (
            (1 + C.N_PERSONS + len(C.LABELLED))
            if C.N_PAIRWISE_FIX
            else (1 + player.n_references + len(C.LABELLED))
        )
        player.n_dots = 1 + player.n_references + len(C.LABELLED)
        player.current_page += 1


#################################
#####  Person Opinions   #####
#################################


class slide04_ReferencesOpinions(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_referencesOpinions") is None:
            player.t_on_referencesOpinions = int(time.time())
        # start = 1 if player.current_batch == 1 else 6
        # end = 5 if player.current_batch == 1 else 10

        pillname = (
            lambda name: f"<span class='pill' style='background-color: {C.REFPERSONCOLOR}; color: white;'>{name}</span>"
        )

        questions = []
        for q in [C.QUS[i] for i in json.loads(player.question_sorting)]:
            questions.append(
                {
                    "prefix": f"{q}",
                    "text": C.QUESTIONTEXT[lan][q],
                }
            )

        references = [
            {
                "id": f"reference{i}",
                "name": (
                    f"{pillname(getattr(player, f'reference{i}'))} would most likely respond with:"
                    if lan == "en"
                    else f"{pillname(getattr(player, f'reference{i}'))} würde am ehesten so antworten:"
                ),
            }
            for i in range(1, player.n_references + 1)
        ]

        # Build a flat list of all question-reference combinations with values
        question_reference_pairs = []
        for q in [C.QUS[i] for i in json.loads(player.question_sorting)]:
            for i in range(1, player.n_references + 1):
                field_name = f"reference{i}__{q}"
                value = player.field_maybe_none(field_name)
                question_reference_pairs.append(
                    {
                        "ref_id": f"reference{i}",
                        "question_prefix": q,
                        "field_name": field_name,
                        "value": value if value is not None else "",
                    }
                )

        return dict(
            lan_en=(lan == "en"),
            maxslides=C.MAXSLIDES,
            nslide=player.current_page,  # (f"{player.current_page}{'a' if player.current_batch==1 else 'b'} "),
            page_title=(
                f"Political Opinions in your Social Circle"
                if lan == "en"
                else "Politische Meinungen in Ihrem Sozialen Umfeld"
            ),  # + ("I" if player.current_batch == 1 else "II"),
            # instruction_text_batch=(
            #     "Please note: On the next page, we will ask you about your evaluations of the other five references."
            #     if lan == "en"
            #     else "Hinweis: Auf der nächsten Seite bitten wir Sie um Ihre Einschätzung der fünf weiteren Kontakte."
            # ),
            instruction_bestguess=(
                "It can be difficult to estimate how someone else might respond. Please move the slider to the point that <em>you belief</em> best reflects the position of each person."
                if lan == "en"
                else "Es kann schwierig sein, einzuschätzen, wie jemand anderes antwortet. Bitte bewegen Sie den Schieberegler auf den Punkt, der <em>Ihrer Meinung nach</em> am besten die Position der jeweiligen Person widerspiegelt."
            ),
            nudge_variation=(
                "The slider is smooth, so that you can indicate nuances among your contact opinions. Your contacts might for example generally agree on an issue, but some might still have stronger views than others."
                if lan == "en"
                else "Der Schieberegler ist stufenlos, damit Sie auch feine Unterschiede zwischen Ihren Kontakten angeben können. Ihre Kontakte sind sich vielleicht generell über ein Thema einig, aber einige könnten dennoch etwas stärkere Ansichten haben als andere."
            ),
            instruction_text=(
                f"How do you think each of these {pillname(f'{player.n_references} contacts')} would respond to the political statements? To what extent would they agree or disagree with the statements?"
                if lan == "en"
                else f"Wie würden Ihrer Meinung nach diese {pillname(f'{player.n_references} Kontakte')} auf die politischen Aussagen antworten? Inwieweit würden sie wohl den Aussagen zustimmen oder nicht zustimmen?"
            ),
            references=references,
            question_reference_pairs=question_reference_pairs,
            questions=questions,
            color=C.REFPERSONCOLOR,
            textcolor="white",
            # would_respond=(
            #     f"To what extent would these {pillname('individuals')} agree or disagree with the following statements?"
            #     if lan == "en"
            #     else f"Inwieweit würden diese {pillname('Personen')} wohl den folgenden Aussagen zustimmen oder nicht zustimmen?"
            # ),
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
            for i in range(1, player.n_references + 1):
                fields.append(f"reference{i}__{q}")
        return fields

    @staticmethod
    def error_message(player, values):
        lan = player.language
        if not player.nudged_for_variation and player.n_references > 0:
            errormsg = (
                "<h4>Note</h4>You have indicated that your social contacts all have the exact same opinion on the following statements: "
                if lan == "en"
                else "<h4>Hinweis</h4>Sie haben angegeben, dass Ihre Kontakte alle exakt gleiche Ansichten zu folgenden Aussagen haben: "
            ) + "<ul style='margin-top:0.5em;margin-bottom:0.5em;'>"
            nudges = 0
            for q in [C.QUS[i] for i in json.loads(player.question_sorting)]:
                variance = np.std(
                    [
                        values[f"reference{i}__{q}"]
                        for i in range(1, player.n_references + 1)
                    ]
                )
                if variance == 0:
                    nudges += 1
                    errormsg += f"<li>{C.QUESTIONTEXT[lan][q]}</li>"
            errormsg += "</ul>" + (
                "Please consider if some of the contacts might feel a bit stronger or weaker about their views. If so, please indicate those nuances by adjusting the sliders slightly. Thank you!"
                if lan == "en"
                else "Bitte überlegen Sie noch einmal, ob nicht einige Ihrer Kontakte etwas stärkere Ansichten haben als andere. Falls ja, drücken Sie diese Abstufung bitte aus indem Sie die jeweiligen Schieberegler leicht anpassen. Vielen Dank!"
            )
            if nudges > 0:
                player.nudged_for_variation = True
                # Store the values temporarily so they can be restored
                for field_name, value in values.items():
                    setattr(player, field_name, value)
                return errormsg
                return errormsg

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.current_page += 1

    @staticmethod
    def is_displayed(player: Player):
        return player.consent  # & (player.current_batch < (C.N_BATCHES + 1))


class slide04b_VotersOpinions(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_voterOpinions") is None:
            player.t_on_voterOpinions = int(time.time())
        pillname = (
            lambda x, color: f"<span class='pill' style='background-color: {color}; color: {'#424949' if x=='FDP' or color==C.LABELLEDCOLORS['FDP'] or color=='#dddddd' else 'white'};'><strong>{x}</strong></span>"
        )
        player.voter_sorting = json.dumps(C.LABELLED)
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
                else "Politische Meinungen Typischer Wählerinnen/Wähler"
            ),
            instruction_text=(
                f"Now think of seven people who are each representative of a typical voter for the political parties in Germany: {partylist}."
                if lan == "en"
                else f"Denken Sie nun an sieben Personen, die jeweils repräsentativ für einen typischen Wähler oder eine typische Wählerin der politischen Parteien in Deutschland stehen: {partylist}."
            ),
            references=voters,
            questions=questions,
            would_respond=(
                f"To what extent would {pillname('each of these voters', 'grey')} agree or disagree with the following statements?"
                if lan == "en"
                else f"Inwieweit würden {pillname('diese Wählerinnen/Wähler', '#dddddd')} wohl jeweils den folgenden Aussagen zustimmen oder nicht zustimmen?"
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
                fields.append(f"{p.replace(' ', '')}__{q}")
        return fields

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.current_page += 1

    @staticmethod
    def is_displayed(player: Player):
        return player.consent


class slide02_OpinionsWithNanRevisited(Page):
    form_model = "player"
    form_fields = [f"own2__{q}" for q in C.QUS]

    @staticmethod
    def is_displayed(player: Player):
        return player.consent

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_ownOpinion2") is None:
            player.t_on_ownOpinion2 = int(time.time())
        questions = [C.QUS[i] for i in json.loads(player.question_sorting)]
        opinions = dict(
            zip(questions, [getattr(player, f"own__{q}") for q in questions])
        )

        fields = [f"own2__{q}" for q in questions]
        questions = []
        for q in [C.QUS[i] for i in json.loads(player.question_sorting)]:
            questions.append(
                {
                    "prefix": f"{q}",
                    "text": C.QUESTIONTEXT[lan][q],
                    "initial_value": opinions[q],
                }
            )
        field_question_pairs = []
        for field, question, opinion in zip(fields, questions, opinions):
            field_question_pairs.append(
                {
                    "field_name": field,
                    "question_text": question,
                }
            )
        pillname = (
            lambda name: f"<span class='pill' style='background-color: {C.SELFCOLOR}; color: white;'>{name}</span>"
        )
        return {
            "lan_en": lan == "en",
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "questions": questions,
            "color": C.SELFCOLOR,
            "field_question_pairs": field_question_pairs,
            "page_title": (
                "Your Political Views – Review"
                if player.language == "en"
                else "Ihre Politischen Ansichten – Überprüfung"
            ),
            "first_label": C.LIKERT7[0] if lan == "en" else C.LIKERT7_de[0],
            "neutral_label": C.LIKERT7[3] if lan == "en" else C.LIKERT7_de[3],
            "last_label": C.LIKERT7[6] if lan == "en" else C.LIKERT7_de[6],
            "instruction_text": (
                "<p><b>Please check and confirm your previous answers about your own political views.</b></p><p>After reflecting on how others might see these political topics, you may now understand the questions a bit differently.</p>"
                if player.language == "en"
                else "<p><b>Bitte überprüfen und bestätigen Sie Ihre vorherigen Antworten zu Ihren eigenen politischen Ansichten.</b></p><p>Nachdem Sie darüber nachgedacht haben, wie andere diese politischen Themen sehen, verstehen Sie die Fragen möglicherweise etwas anders.</p>"
            ),
            "instruction_text2": (
                "If your responses still reflect your views well, just click <em>Continue</em>. If not, feel free to adjust them before proceeding."
                if player.language == "en"
                else "Wenn Ihre Antworten immer noch Ihre Ansichten gut widerspiegeln, klicken Sie einfach auf <em>Weiter</em>. Wenn nicht, können Sie Ihre Antworten hier anpassen."
            ),
            "overallquestion": (
                f"To what extent do {pillname('you')} agree or disagree with the statement?"
                if player.language == "en"
                else f"Inwieweit stimmen {pillname('Sie')} der Aussage oben zu oder nicht zu?"
            ),
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.current_page += 1


#################################
#####  Play Practice Run   #####
#################################
class slide05a_MapGame(Page):
    form_model = "player"
    form_fields = ["positionsGame"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.positionsGame = player.positionsGame
        player.current_page += 1

    @staticmethod
    def is_displayed(player):
        return player.consent

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_practiceGame") is None:
            player.t_on_practiceGame = int(time.time())
        init_dots = [
            {
                "dottype": "food",
                "varname": "tomatosalad",
                "name_disp": ("Tomato Salad" if lan == "en" else "Tomatensalat"),
                "x": 360,
                "y": 50,
                "color": "#d97565   ",
            },
            {
                "dottype": "food",
                "varname": "pizza",
                "name_disp": "Pizza Margherita" if lan == "en" else "Pizza Margherita",
                "x": 360,
                "y": 100,
                "color": "#d97565",
            },
            {
                "dottype": "food",
                "varname": "spaghetticarbo",
                "name_disp": (
                    "Spaghetti Carbonara" if lan == "en" else "Spaghetti Carbonara"
                ),
                "x": 360,
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
                "Political Mapping – Warm-up (Practice)"
                if lan == "en"
                else "Politische Karte – Aufwärmen (Übung)"
            ),
            "lan": lan,
            "instruction_text2": (
                "Imagine you have to arrange the following meals – Tomato Salad, Spaghetti Carbonara, and Pizza Margherita – in a rectangle."
                if lan == "en"
                else "Stellen Sie sich vor, Sie müssten die folgenden Gerichte – Tomatensalat, Spaghetti Carbonara und Pizza Margherita – in einem Rechteck platzieren."
            ),
            "instruction_text3": (
                "<ul><li><strong>Place meals closer together if you perceive them as similar.</strong></li><li><strong>Place meals farther apart if you perceive them as different.</strong></li></ul>"
                if lan == "en"
                else "<ul><li>Platzieren Sie Gerichte <strong>näher beieinander</strong>, wenn Sie diese als <strong>ähnlich</strong> wahrnehmen.</li><li>Platzieren Sie Gerichte <strong>weiter auseinander</strong>, wenn Sie diese als <strong>unterschiedlich</strong> wahrnehmen.</li></ul>"
            ),
            "detailed_instructions_1": (
                "<details><summary>Technical Instructions (click if needed)</summary><ul><li>You will start with several points on the right side.</li><li>Drag these one by one into the rectangle and place them as described above.</li><li>You can re-position any dot at any time until you are satisfied with the arrangement.</li></ul></details>"
                if lan == "en"
                else "<details><summary>Technische Anleitung (falls benötigt, hier klicken)</summary><ul><li>Sie beginnen mit mehreren Punkten auf der rechten Seite.</li><li>Ziehen Sie diese nacheinander in das Rechteck und ordnen Sie die Punkte wie oben beschrieben an.</li><li>Sie können jeden Punkt verschieben, bis Sie mit der Anordnung zufrieden sind.</li></ul></details>"
            ),
            "tomato": (
                "<em>Example:</em> A participant, who dislikes tomatoes, might arrange the dishes quite differently compared to a participant, who does not eat meat."
                if lan == "en"
                else "<em>Beispiel:</em> Eine Teilnehmerin, die Tomaten nicht mag, würde die Gerichte vermutlich ganz anders platzieren als ein Teilnehmer, der kein Fleisch isst."
            ),
            "no_wrong_answers": (
                f"This dot arrangement – as the arrangements in the following tasks – is of course subjective:"
                if lan == "en"
                else "Diese Anordnung – wie auch die Anordnungen in den folgenden Aufgaben – ist natürlich individuell:"
            ),
            "all_dots_instr": (
                "All dots must be within the square boundary to proceed."
                if lan == "en"
                else "Um fortzufahren, müssen alle Punkte im Rechteck platziert werden."
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
        player.positionsTest = player.field_maybe_none("positionsTest")

        t_submitted = json.loads(player.t_practicesSubmitted)
        assert type(t_submitted) == dict
        t_submitted[player.attemptPractice] = int(time.time())
        player.t_practicesSubmitted = json.dumps(t_submitted)

        player.attemptPractice += 1

    @staticmethod
    def is_displayed(player):
        trainingPassed = player.isTrainingPassed
        return player.consent and (not trainingPassed)

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_practice") is None:
            player.t_on_practice = int(time.time())
        colors = {
            "self": C.SELFCOLOR,
            "friend": "#4DA8DA",
            "coworker": "#2E8B57",
            "relative": "#D64545",
        }
        if player.attemptPractice == 0:
            init_dots = [
                {
                    "dottype": "self",
                    "varname": "self",
                    "name_disp": "Self" if lan == "en" else "Ich",
                    "x": 330,
                    "y": 50,
                    "color": C.SELFCOLOR,
                },
                {
                    "dottype": "friend",
                    "varname": "friend",
                    "name_disp": "Friend" if lan == "en" else "Freund",
                    "x": 330,
                    "y": 100,
                    "color": colors["friend"],
                },
                {
                    "dottype": "coworker",
                    "varname": "coworker",
                    "name_disp": "Co-Worker" if lan == "en" else "Kollegin",
                    "x": 330,
                    "y": 150,
                    "color": colors["coworker"],
                },
                {
                    "dottype": "relative",
                    "varname": "relative",
                    "name_disp": "Relative" if lan == "en" else "Verwandter",
                    "x": 330,
                    "y": 200,
                    "color": colors["relative"],
                },
            ]
        else:
            init_dots = json.loads(getattr(player, "positionsTest", []))
        pill = (
            lambda x, c: f"<span class='pill' style='background-color: {colors[c]}; color: white;'>{x}</span>"
        )
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "dots": init_dots,
            "page_title": (
                "Political Mapping – Practice 2"
                if lan == "en"
                else "Politische Karte – Übung 2"
            ),
            "lan": lan,
            "instruction_text1": (
                "In the <strong>second Practice</strong> we now focus on the perception of political differences."
                if lan == "en"
                else "In der <strong>zweiten Übung</strong> geht es nun um die Wahrnehmung von politischen Unterschieden."
            ),
            "instruction_text2": (
                "Imagine you, a friend, a co-worker, and a relative of yours are in a room together."
                if lan == "en"
                else "Stellen Sie sich vor, Sie sind zusammen mit einem Freund, einer Arbeitskollegin und einem Verwandten in einem Raum."
            ),
            "instruction_text3": (
                "Arrange the people in the room based on how <em>you</em> see their political views:<ul><li><strong>Place individuals closer together if you perceive them as <em>politically</em> similar.</strong></li><li><strong>Place individuals farther apart if you perceive them as <em>politically</em> different.</strong></li></ul>"
                if lan == "en"
                else "Ordnen Sie die Personen im Raum so an, wie <em>Sie</em> deren politische Ansichten wahrnehmen:<ul> <li>Platzieren Sie Personen <strong>näher beieinander</strong>, wenn Sie diese als <strong><em>politisch</em> ähnlich</strong> wahrnehmen.</li><li>Platzieren Sie Personen <strong>weiter auseinander</strong>, wenn Sie diese als <strong><em>politisch</em> unterschiedlich</strong> wahrnehmen.</li></ul>"
            ),
            "disclaimer": (
                "This is a practice task! When you click on <em>Next</em>, you will see whether your arrangement meets all the aspects of the instructions. You have 5 attempts."
                if lan == "en"
                else "Dies ist eine Übungsaufgabe! Wenn Sie auf <em>Weiter</em> klicken, erfahren Sie, ob Ihre Anordnung alle Aspekte der Anweisungen erfüllt. Sie haben 5 Versuche."
            ),  # In the main task on the next slide, there will be NO right or wrong answers — only your personal perception will matter.</p> #  Im Hauptteil auf der nächsten Seite wird es dagegegen KEINE richtigen oder falschen Antworten geben – nur Ihre persönliche Wahrnehmung wird relevant sein.
            "detailed_instructions_1": (
                "<h3>Step-by-Step Instructions</h4><p>Arrange the dots in the room (the rectangle below) as described in the step-by-step instructions.</p><p>You can collapse/expand each instruction by clicking for example on <b>Step 1</b>.</p>"
                if lan == "en"
                else "<h3>Schritt-für-Schritt Anweisungen</h4><p>Platzieren Sie die Punkte in dem Raum (das Rechteck unten) wie in den Schritt-für-Schritt Anweisungen beschrieben.</p><p>Sie können die einzelnen Anweisungen ein-/ausklappen indem Sie z.B. auf <b>Schritt 1</b> klicken.</p>"
            ),
            "detailed_instructions_2": (
                (
                    f"<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Step 1:</strong> {pill('Self', 'self')}</summary><p>Place the dot {pill('Self', 'self')} somewhere within the rectangle – this dot represents your own political views.</p></details>"
                    + f"<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Step 2:</strong> {pill('Friend', 'friend')}</summary><p>Place the dot {pill('Friend', 'friend')} near you – they share similar views.</p></details>"
                    + f"<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Step 3:</strong> {pill('Co-worker', 'coworker')}</summary><p>Place {pill('Co-worker', 'coworker')} farther away, because, although you value her, you often disagree with her opinions. Position {pill('Co-worker', 'coworker')} closer to {pill('Self', 'self')} than to {pill('Friend', 'friend')}, because you perceive an even greater political difference between Co-worker and Friend.</p></details>"
                    # + f"<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Step 4:</strong> {pill('Relative', 'relative')}</summary><p>Your relative has very different political views to you – place {pill('Relative', 'relative')} far from {pill('Self', 'self')}. At the same time, the relative shares some opinions with your friend and your co-worker – place {pill('Relative', 'relative')} somewhat closer to {pill('Friend', 'friend')} and {pill('Co-worker', 'coworker')} than to {pill('Self', 'self')}.</p></details>"
                    + f"<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Step 4:</strong> {pill('Relative', 'relative')}</summary><p>Your relative has very different political views compared to you. But also compared to your co-worker. Place the dot {pill('Relative', 'relative')} in a triangle with {pill('Co-worker', 'coworker')}, and {pill('Ich', 'self')} such that the distances between the three dots are similar.</p></details>"
                )
                if lan == "en"
                else (
                    f"<details  open style='margin-bottom: 0em;'> <summary  style='white-space: nowrap;'><strong>Schritt 1:</strong> {pill('Ich', 'self')}</summary> <p>Platzieren Sie den Punkt {pill('Ich', 'self')} irgendwo im Rechteck – dieser Punkt steht für Ihre politischen Ansichten.</p></details>"
                    + f"<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Schritt 2:</strong> {pill('Freund', 'friend')}</summary><p>Setzen Sie den Punkt {pill('Freund', 'friend')} in Ihre Nähe – er teilt ähnliche Ansichten wie Sie.</p></details>"
                    + f"<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Schritt 3:</strong> {pill('Kollegin', 'coworker')}</summary><p>Platzieren Sie {pill('Kollegin', 'coworker')} weiter entfernt, da Sie die Kollegin zwar schätzen aber oft anderer Meinung sind. Platzieren Sie {pill('Kollegin', 'coworker')} etwas näher zu {pill('Ich', 'self')} als zu {pill('Freund', 'friend')}, weil Sie zwischen der Kollegin und dem Freund eine noch größere politische Differenz wahrnehmen.</p></p></details>"
                    # + f"<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Schritt 4:</strong> {pill('Verwandter', 'relative')}</summary><p>Der Verwandte denkt politisch ganz anders als Sie – setzen Sie {pill('Verwandter', 'relative')} weit weg von {pill('Ich', 'self')}. Gleichzeitig teilt der Verwandte aber einige Ansichten sowohl mit dem Freund als auch mit der Kollegin – platzieren Sie {pill('Verwandter', 'relative')} daher näher an {pill('Freund', 'friend')} und {pill('Kollegin', 'coworker')} als an {pill('Ich', 'self')}.</p></details>"
                    + f"<details  open style='margin-bottom: 0em;'><summary  style='white-space: nowrap;'><strong>Schritt 4:</strong> {pill('Verwandter', 'relative')}</summary><p>Ihr Verwandter denkt politisch ganz anders als Sie. Aber auch ganz anders als Ihre Kollegin. Platzieren Sie den Punkt {pill('Verwandter', 'relative')} in einem Dreieck mit {pill('Kollegin', 'coworker')} und {pill('Ich', 'self')} so dass die Distanzen zwischen den drei Punkten ähnlich groß sind.</p></details>"
                )
            ),
            "all_dots_instr": (
                "All dots must be within the square boundary to proceed. You can re-position any dot at any time until you are satisfied with the arrangement."
                if lan == "en"
                else "Um fortzufahren, müssen alle Punkte im Rechteck platziert werden. Sie können jeden Punkt verschieben, bis Sie mit der Anordnung zufrieden sind."
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
    form_model = "player"
    form_fields = ["practice_sanity_check_answer"]

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_practiceResult_first") is None:
            player.t_on_practiceResult_first = int(time.time())
        dots = json.loads(player.positionsTest)
        pos = {p["varname"]: [p["x"], p["y"]] for p in dots}

        # calculate distances
        dF = distance(pos["self"], pos["friend"])
        dC = distance(pos["self"], pos["coworker"])
        dR = distance(pos["self"], pos["relative"])
        dFR = distance(pos["friend"], pos["relative"])
        dFC = distance(pos["friend"], pos["coworker"])
        dCR = distance(pos["coworker"], pos["relative"])
        # check conditions
        player.is_distS2F_gt_distS2C = bool(
            dF < dC
        )  # Rule: co-worker is quite different.
        player.is_distF2C_gt_distS2C = bool(
            dFC > dC
        )  # Rule: colleague is closer to self than to friend.
        player.is_distS2R_gt_distS2F = bool(dR > dF)  # Rule: relative is very different
        # player.is_distS2R_gt_distF2RanddistC2R = bool(
        #     (dR > dFR) and (dR > dCR)
        # )  # Rule 6.
        player.is_distsRCS_similar = (
            max(dR, dC, dCR) / min(dR, dC, dCR) < 1.67
        )  # is R roughly equally far from S, F, and C?

        isTrainingPassed = (
            player.is_distS2F_gt_distS2C
            & player.is_distF2C_gt_distS2C
            & player.is_distS2R_gt_distS2F
            & player.is_distsRCS_similar
        )
        player.isTrainingPassed = isTrainingPassed
        colors = {
            "self": C.SELFCOLOR,
            "friend": "#4DA8DA",
            "coworker": "#2E8B57",
            "relative": "#D64545",
        }
        pill = (
            lambda x, c: f"<span class='pill' style='background-color: {colors[c]}; color: white;'>{x}</span>"
        )
        errors = "<ul>"
        if lan == "en":
            errors += (
                rf"<li>The distance between {pill('Self', 'self')} and {pill('Co-worker', 'coworker')} should be larger than the distance between {pill('Self', 'self')} and {pill('Friend', 'friend')}.</li>"
                if player.is_distS2F_gt_distS2C == 0
                else ""
            )
            errors += (
                rf"<li>The distance between {pill('Friend', 'friend')} and {pill('Co-worker', 'coworker')} should be larger than the distance between {pill('Self', 'self')} and {pill('Co-worker', 'coworker')}. </li>"
                if player.is_distF2C_gt_distS2C == 0
                else ""
            )
            errors += (
                rf"<li>The distance between {pill('Self', 'self')} and {pill('Relative', 'relative')} should be larger than the distance between {pill('Self', 'self')} and {pill('Friend', 'friend')}. </li>"
                if player.is_distS2R_gt_distS2F == 0
                else ""
            )
            # errors += (
            #     rf"<li>The distance between {pill('Self', 'self')} and {pill('Relative', 'relative')} should be larger than the distance between {pill('Friend', 'friend')} and {pill('Relative', 'relative')} and larger than the distance between {pill('Co-worker', 'coworker')} and {pill('Relative', 'relative')}. <br>"
            #     if player.is_distS2R_gt_distF2RanddistC2R == 0
            #     else ""
            # )
            maxDistR = max(dR, dC, dCR) / min(dR, dC, dCR)
            whichmaxDistR = (
                [
                    ("Relative", "Self"),
                    ("Co-worker", "Self"),
                    ("Relative", "Co-worker"),
                ][np.argmax([dR, dC, dCR])],
                [("relative", "self"), ("coworker", "self"), ("relative", "coworker")][
                    np.argmax([dR, dC, dCR])
                ],
            )
            whichminDistR = (
                [
                    ("Relative", "Self"),
                    ("Co-worker", "Self"),
                    ("Relative", "Co-worker"),
                ][np.argmin([dR, dC, dCR])],
                [("relative", "self"), ("coworker", "self"), ("relative", "coworker")][
                    np.argmin([dR, dC, dCR])
                ],
            )
            errors += (
                rf"<li>The distances between {pill('Relative', 'relative')}, {pill('Self', 'self')}, and {pill('Co-worker', 'coworker')} should be similar. In your arrangement, however, {pill(whichmaxDistR[0][0], whichmaxDistR[1][0])}–{pill(whichmaxDistR[0][1], whichmaxDistR[1][1])} is substantially larger than {pill(whichminDistR[0][0], whichminDistR[1][0])}–{pill(whichminDistR[0][1], whichminDistR[1][1])}.</li>"
                if player.is_distsRCS_similar == 0
                else ""
            )
        else:
            errors += (
                rf"<li>Die Distanz zwischen {pill('Freund', 'friend')} und {pill('Kollegin', 'coworker')} sollte größer sein als die Distanz zwischen {pill('Ich', 'self')} und {pill('Friend', 'friend')}. </li>"
                if player.is_distS2F_gt_distS2C == 0
                else ""
            )
            errors += (
                rf"<li>Die Distanz zwischen {pill('Freund', 'friend')} und {pill('Kollegin', 'coworker')} sollte größer sein als die Distanz zwischen {pill('Ich', 'self')} und {pill('Kollegin', 'coworker')}. </li>"
                if player.is_distF2C_gt_distS2C == 0
                else ""
            )
            errors += (
                rf"<li>Die Distanz zwischen {pill('Ich', 'self')} und {pill('Verwandte', 'relative')} sollte größer sein als die Distanz zwischen {pill('Ich', 'self')} und {pill('Freund', 'friend')}. </li>"
                if player.is_distS2R_gt_distS2F == 0
                else ""
            )
            # errors += (
            #     rf"<li>Die Distanz zwischen {pill('Ich', 'self')} und {pill('Verwandte', 'relative')} sollte größer sein als die Distanz zwischen {pill('Freund', 'friend')} und {pill('Verwandte', 'relative')} und größer als die Distanz zwischen {pill('Kollegin', 'coworker')} und {pill('Verwandte', 'relative')}. </li>"
            #     if player.is_distS2R_gt_distF2RanddistC2R == 0
            #     else ""
            # )
            maxDistR = max(dR, dFR, dCR) / min(dR, dFR, dCR)
            whichmaxDistR = (
                [
                    ("Verwandter", "Ich"),
                    ("Kollegin", "Ich"),
                    ("Verwandter", "Kollegin"),
                ][np.argmax([dR, dC, dCR])],
                [("relative", "self"), ("coworker", "self"), ("relative", "coworker")][
                    np.argmax([dR, dC, dCR])
                ],
            )
            whichminDistR = (
                [
                    ("Verwandter", "Ich"),
                    ("Kollegin", "Ich"),
                    ("Verwandter", "Kollegin"),
                ][np.argmin([dR, dC, dCR])],
                [("relative", "self"), ("coworker", "self"), ("relative", "coworker")][
                    np.argmin([dR, dC, dCR])
                ],
            )
            errors += (
                rf"<li>Die Distanzen zwischen {pill('Verwandter', 'relative')}, {pill('Ich', 'self')} und {pill('Kollegin', 'coworker')} sollten ähnlich sein. In Ihrer Anordnung ist allerdings {pill(whichmaxDistR[0][0], whichmaxDistR[1][0])}–{pill(whichmaxDistR[0][1], whichmaxDistR[1][1])} deutlich größer als {pill(whichminDistR[0][0], whichminDistR[1][0])}–{pill(whichminDistR[0][1], whichminDistR[1][1])}</li>"
                if player.is_distsRCS_similar == 0
                else ""
            )
        errors += "</ul>"

        player.latest_error_msg = errors

        if player.isTrainingPassed:
            player.is_FR_gt_SR = bool(dFR > dR)
        player.practice_sanity_check_correct = False

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
                        else "Repeat Practice"
                    )
                )
                if lan == "en"
                else (
                    "Weiter"
                    if player.isTrainingPassed
                    else (
                        "Trotzdem weiter"
                        if player.attemptPractice == C.N_MAX_PRACTICE_RUNS
                        else "Wiederhole Übung"
                    )
                )
            ),
            "attempt_msg": (
                f"Attempt {player.attemptPractice} of {C.N_MAX_PRACTICE_RUNS}"
                if lan == "en"
                else f"Versuch {player.attemptPractice} von {C.N_MAX_PRACTICE_RUNS}"
            ),
            "page_title": (
                "Political Mapping – Practice 2 – Results"
                if lan == "en"
                else "Politische Karte – Übung 2 – Ergebnisse"
            ),
            "success_msg": (
                "<strong>Well done!</strong> Your arrangement fulfills all aspects of the instructions."
                if lan == "en"
                else "<strong>Sehr gut!</strong> Ihre Anordnung erfüllt alle Aspekte der Anleitung."
            ),
            "error_msg": (
                f"<strong>Your arrangement does not meet all aspects of the instructions:</strong></p><p style='white-space: pre-line;'>{errors}</p><p>Please repeat the practice task and try to arrange the dots such that all criteria are met.</p>"
                if lan == "en"
                else f"<strong>Ihre Anordnung stimmt nicht mit allen Aspekten der Anleitung überein:</strong></p><p style='white-space: pre-line;'>{errors}</p><p>Bitte wiederholen Sie die Übungsaufgabe und versuchen Sie, die Punkte so anzuordnen, dass alle Kriterien erfüllt sind.</p>"
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
            "show_canvas": player.isTrainingPassed,
            "dots": pos if player.isTrainingPassed else [],
            "sanity_check_error": (player.practice_sanity_check_correct),
            "sanity_question": (
                f"According to <em>your</em> map of this practice scenario, which individual is politically closer to the {pill('Relative', 'relative')}?"
                if lan == "en"
                else f"In Ihrer Anordnung oben, wer ist dem {pill('Verwandten', 'relative')} politisch näher: Sie selbst oder Ihr Freund?"
            ),
            "option_a": (
                f"{pill('Self', 'self')} is politically closer to the relative"
                if lan == "en"
                else f"{pill('Ich', 'self')} ist dem Verwandten politisch näher"
            ),
            "option_b": (
                f"{pill('Friend', 'friend')} is politically closer to the relative"
                if lan == "en"
                else f"{pill('Freund', 'friend')} ist dem Verwandten politisch näher"
            ),
        }

    @staticmethod
    def is_displayed(player: Player):
        return (
            player.consent
            and (not player.practice_sanity_check_correct)
            and (player.attemptPractice <= C.N_MAX_PRACTICE_RUNS)
            and (
                (not player.isTrainingPassed)
                or (player.isTrainingPassed and player.attemptPractice == 0)
            )
        )

    @staticmethod
    def error_message(player, values):
        if player.isTrainingPassed:
            if values.get("practice_sanity_check_answer") != (
                "Self" if player.is_FR_gt_SR else "Friend"
            ):
                player.practice_sanity_check_correct = False
                player.attempts_sanity_check += 1
                if player.language == "en":
                    return "Your answer is unfortunately incorrect. Please try again."
                else:
                    return "Ihre Antwort ist leider nicht korrekt. Bitte versuchen Sie es erneut."
            else:
                player.practice_sanity_check_correct = True

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.isTrainingPassed and player.practice_sanity_check_correct:
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
        pairSequence = fixedPairs + valid_pairs[: (player.n_checks - len(fixedPairs))]
        random.shuffle(pairSequence)
        player.pairSequence = json.dumps(pairSequence)

        dots_t_first_moved = [d["t_first_moved"] for d in dots]
        player.t_firstDotMoved = min(dots_t_first_moved)
        player.current_page += 1

    @staticmethod
    def is_displayed(player: Player):
        # trainingPassed = player.isTrainingPassed
        return player.consent  # and trainingPassed

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_map") is None:
            player.t_on_map = int(time.time())
        displ_names = (
            ["Self" if lan == "en" else "Ich"]
            + [
                getattr(player, f"reference{f}")
                for f in range(1, player.n_references + 1)
            ]
            + [
                f"{v+' voter' if lan=='en' else C.LABELLED_de[v]+' W.'}"  # Wähler/Wählerin
                for v in C.LABELLED
            ]
        )
        types = (
            ["self"]
            + ["reference"] * player.n_references
            + ["labelledPerson"] * len(C.LABELLED)
        )
        varnames = (
            ["self"]
            + [f"reference{f}" for f in range(1, player.n_references + 1)]
            + [f"{v}" for v in C.LABELLED]
        )
        init_dots = [
            {
                "dottype": dottype,
                "varname": varname,
                "name_disp": name,
                "x": 576 + 80 * (dottype == "labelledPerson"),
                "y": 32
                + (i - (dottype == "labelledPerson") * (player.n_references + 0.45))
                * 42,
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
                else "Wir beginnen nun mit der Hauptaufgabe dieser Umfrage."
            ),
            "instruRoom": (
                f"Imagine you, the {player.n_references} people representing your social circle, and typical voters of the German parties are in a room (the rectangle below)."
                if lan == "en"
                else f"Stellen Sie sich vor, Sie sind zusammen mit den {player.n_references} Personen, die Ihr soziales Umfeld repräsentieren, und mit den typischen Wählern oder Wählerinnen der vorher genannten Parteien in einem Raum (das Rechteck unten)."
            ),
            "instru_main": (
                "<p>Arrange the people in the room based on how <em>you</em> see their views on the political questions from the beginning of this survey:</p><ul><li><strong>Place individuals closer together if you perceive them as politically similar.</strong></li><li><strong>Place individuals farther apart if you perceive them as politically different.</strong></li></ul>"  # regarding climate change, migration, inequality and diversity
                if lan == "en"
                else "<p>Ordnen Sie die Personen im Raum so an, wie <em>Sie</em> deren Ansichten zu den politischen Fragen vom Beginn der Umfrage wahrnehmen:</p><ul> <li>Platzieren Sie Personen <strong>näher beieinander</strong>, wenn Sie diese als <strong>politisch ähnlich</strong> wahrnehmen.</li><li>Platzieren Sie Personen <strong>weiter auseinander</strong>, wenn Sie diese als <strong>politisch unterschiedlich</strong> wahrnehmen.</li></ul>"  # über Klimawandel, Migration, Ungleichheit und Vielfalt
            ),
            "no_wrong_answers": (
                f"<p>There are NO right or wrong answers — we are interested in your personal perception.</p>"
                if lan == "en"
                else "<p>Es gibt weder falsche noch richtige Antworten – wir sind an Ihrer persönlichen Einschätzung interessiert.</p>"
            ),
            "gender": (
                "" if lan == "en" else "<b>W.</b> steht für Wählerinnen und Wähler."
            ),
            # "instru_click": (
            #     "<summary style='white-space: nowrap;'><strong>Helping lines</strong></summary>If you want you can activate helping lines. When you click on one of the dots, circles will appear that might help you evaluate how well your arrangement reflects your sense of political similarity. You can scale the circles by moving the small arrows <strong><></strong>."
            #     if lan == 'en'
            #     else "<summary style='white-space: nowrap;'><strong>Hilfslinien</strong></summary>Wenn Sie möchten, können Sie unten Hilfslinien aktivieren: Beim Klicken auf einen Punkt erscheinen Kreis, die Ihnen dabei helfen könnten einzuschätzen, wie gut Ihre Anordnung Ihre Wahrnehmung politischer Ähnlichkeit widerspiegelt. Die Kreise lassen sich über die kleinen Pfeile <strong><></strong> skalieren."
            # ),
            "all_dots_instr": (
                "All dots must be within the square boundary to proceed. You can re-position any dot at any time until you are satisfied with the arrangement."
                if lan == "en"
                else "Um fortzufahren, müssen alle Punkte im Rechteck platziert werden. Sie können jeden Punkt verschieben, bis Sie mit der Anordnung zufrieden sind."
            ),
            # "labelClose": "similar" if lan == 'en' else "ähnlich",
            # "labelFar": "different" if lan == 'en' else "unterschiedlich",
            # "helping_lines": (
            #     "Show helping lines" if lan == 'en' else "Hilfslinien anzeigen"
            # ),
        }


#################################
#####  SATISFACTION   #####
#################################
class slide07_Satisfaction(Page):
    form_model = "player"
    form_fields = [
        "satisfaction_text",
        "satisfaction",
    ]

    @staticmethod
    def is_displayed(player: Player):
        # trainingPassed = player.isTrainingPassed
        return player.consent  # and trainingPassed

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_satisfaction") is None:
            player.t_on_satisfaction = int(time.time())
        questions = [C.QUS[i] for i in json.loads(player.question_sorting)]

        def get_ops(prefix, questions):
            return {q: player.field_maybe_none(f"{prefix}{q}") for q in questions}

        def format_ops(ops_dict, lan):
            return "; ".join(
                f"{C.QUESTIONSHORTTEXT[lan][q]}: {val if lan=='en' else val }"
                for q, val in ops_dict.items()
            )

        pos = json.loads(player.positions) if player.positions else []

        dot_descrs = {
            "self": format_ops(
                get_ops(
                    "own2__", [C.QUS[i] for i in json.loads(player.question_sorting)]
                ),
                lan,
            )
        }
        for f in range(1, player.n_references + 1):
            dot_descrs[f"reference{f}"] = format_ops(
                get_ops(f"reference{f}__", questions), lan
            )
        for v in C.LABELLED:
            dot_descrs[f"{v}"] = format_ops(
                get_ops(f"{v.replace(' ','')}__", questions), lan
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
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "dots": init_dots,
            "page_title": (
                "Satisfaction with your political map"
                if lan == "en"
                else "Zufriedenheit mit Ihrer politischen Karte"
            ),
            "instru1": (
                "Below we show the political map you created."
                if lan == "en"
                else "Unten finden Sie die von Ihnen erstellte persönliche politische Karte."
            ),
            "instru2": (
                "Tipp: If you click on one of the dots in the square, a popup will appear showing your responses for that particular person."
                if lan == "en"
                else "Tipp: Wenn Sie auf einen der Punkte im Rechteck klicken, erscheint ein Fenster, das Ihre Antworten für die jeweilige Person zeigt."
            ),
            "question": (
                "<p>How <em>satisfied</em> are you with your political map? Does this arrangement of dots reflect more or less accurately how you perceive differences between the political opinions of the individuals?</p>"
                if lan == "en"
                else "<p>Wie <em>zufrieden</em> sind Sie mit Ihrer politischen Karte? Spiegelt diese Anordnung der Punkte mehr oder weniger <em>akkurat</em> wider, wie Sie die Differenzen zwischen den politischen Meinungen der Personen wahrnehmen?</p>"
            ),
            "explain_text": (
                "If you like, you can add any thoughts, comments, or explanations here <em>(optional)</em>:"
                if lan == "en"
                else "Wenn Sie möchten, können Sie hier Ihre Gedanken, Bemerkungen oder Erklärungen hinzufügen <em>(optional)</em>:"
            ),
            # "choices": list(range(0, 11)),
            "satisfaction_canvas_width": 400,
            "canvas_width": C.CANVAS_WIDTH,
            "satisfaction_min": 0,
            "satisfaction_max": 100,
            "satisfaction_min_label": (
                "Not satisfied at all / Not accurate at all <em>(0)</em>"
                if lan == "en"
                else "Gar nicht zufrieden / Gar nicht akkurat <em>(0)</em>"
            ),
            "satisfaction_max_label": (
                "Very satisfied / Very accurate <em>(10)</em>"
                if lan == "en"
                else "Sehr zufrieden / Sehr akkurat <em>(10)</em>"
            ),
            "more_later": (
                "Later, we will ask you a few additional short questions about this political mapping task and your approach to arranging the dots."
                if lan == "en"
                else "Wir werden Ihnen später noch ein paar zusätzliche Fragen zu dieser Aufgabe – der Erstellung Ihrer politische Karte — sowie zu Ihrem Vorgehen bei der Anordnung der Punkte stellen."
            ),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.current_page += 1


#################################
#####  Pairwise similiarty ratings   #####
#################################
class slide08_PlausibilityCheck_Pairs(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):
        # trainingPassed = player.isTrainingPassed
        return (
            (player.consent)
            and (player.n_check <= (player.n_checks))
            # and trainingPassed
        )

    @staticmethod
    def get_form_fields(player: Player):
        i = player.n_check
        return [f"similarityPair{i}"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.n_check == 1:
            player.t_after_first_pair = int(time.time())
        player.n_check += 1
        if player.n_check == player.n_checks:
            player.current_page += 1

        # x = player.field_maybe_none(f"t_submittedPairs")
        # print(x)
        # t_submitted = json.loads(player.t_submittedPairs)
        # assert type(t_submitted) == dict
        # t_submitted[player.n_check] = int(time.time())
        # player.t_submittedPairs = json.dumps(t_submitted)

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_pairwise") is None:
            player.t_on_pairwise = int(time.time())

        def get_descr(p):
            if "reference" in p:
                plabel = (
                    f"your contact <span class='pill' style='background-color: {C.REFPERSONCOLOR}; color: white;'><strong>"
                    if lan == "en"
                    else f"Ihr Kontakt <span class='pill' style='background-color: {C.REFPERSONCOLOR}; color: white;'><strong>"
                )
                plabel += f"{getattr(player, p)}</strong></span>"
            elif p == "self":
                plabel = (
                    f"<span class='pill' style='background-color: {C.SELFCOLOR}; color: white;'><strong>yourself</strong></span>"
                    if lan == "en"
                    else f"<span class='pill' style='background-color: {C.SELFCOLOR}; color: white;'><strong>Sie selbst</strong></span>"
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
                f"Similarity of Pairs – {player.n_check} of {player.n_checks}"
                if lan == "en"
                else f"Ähnlichkeit von Paaren – {player.n_check} von {player.n_checks}"
            ),
            "instru1": (
                f"<p>Now consider the following two individuals:</p>"
                if lan == "en"
                else f"<p>Denken Sie nun an die folgenden beiden Personen:</p>"
            ),
            "instru2": (
                f"<ul><li style='font-size:18px;'>{get_descr(p1)}</li><li style='font-size:18px;'>{get_descr(p2)}</li></ul>"
                if lan == "en"
                else f"<ul><li style='font-size:18px;'>{get_descr(p1)}</li><li style='font-size:18px;'>{get_descr(p2)}</li></ul>"
            ),
            "question": (
                "<p>In your view, how similar are these two individuals in their views on the political questions from the beginning of this survey?</p>"  # concerning climate change, migration, inequality, and diversity
                if lan == "en"
                else "<p>Wie ähnlich sind sich diese beiden Personen Ihrer Meinung nach in ihren Ansichten über die politischen Fragen vom Beginn dieser Umfrage?</p>"  # zu Klimawandel, Migration, Ungleichheit und Diversität
            ),
            "similarity_min": 0,
            "similarity_max": 100,
            "similarity_min_label": (
                "Not at all similar" if lan == "en" else "Überhaupt nicht ähnlich"
            ),
            "similarity_max_label": (
                "Extremely similar" if lan == "en" else "Extrem ähnlich"
            ),
            "completedPairs": player.n_check,
            "final": player.n_check == player.n_checks,
            "pairs": pairSequence,
            "pair_indices": list(range(player.n_checks)),
        }


#################################
#####  Tasks   #####
#################################
class slide09_Tasks(Page):
    form_model = "player"
    form_fields = [
        "mappingEnjoy",
        "mappingEasier",
        "task_text",
    ]

    @staticmethod
    def is_displayed(player: Player):
        # trainingPassed = player.isTrainingPassed
        return player.consent  # and trainingPassed

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_taskCompare") is None:
            player.t_on_taskCompare = int(time.time())
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "page_title": (
                "Political mapping task vs. Pairwise comparison Task"
                if lan == "en"
                else "Politischen Karte vs. Paarweiser Vergleich"
            ),
            "questioneasierMapping": (
                "<p>Which task did you find <b>easier</b> to provide your evaluation of the political similarity/differences between people?</p>"  #  Arranging the 18 dots on the square <em>or</em> or evaluating the similarity of 18 pairs of individuals?
                if lan == "en"
                else "<p>Welche Aufgabe hat sich <b>einfacher</b> angefühlt, um Ihre Wahrnehmung von politischen Unterschieden oder Ähnlichkeit auszudrücken? </p>"  # Die 18 Punkte auf der Karte anzuordnen <em>oder</em> Die politische Ähnlichkeit von 18 Paaren zu bewerten?
            ),
            "easier_min": -50,
            "easier_max": 50,
            "easier_min_label": (
                f"Evaluation of {player.n_checks} <b>pairs</b> was much easier for me <em>(-5)</em>"
                if lan == "en"
                else f"Bewerten der {player.n_checks} <b>Paare</b> war viel einfacher für mich <em>(-5)</em>"
            ),
            "easier_neutral_label": (
                "Similarly easy or hard <em>(0)</em>"
                if lan == "en"
                else "Ähnlich einfach bzw. schwer <em>(0)</em>"
            ),
            "easier_max_label": (
                f"Arranging {player.n_dots} <b>dots</b> was much easier for me <em>(5)</em>"
                if lan == "en"
                else f"Anordnen der {player.n_dots} <b>Punkte</b> war viel einfacher für mich <em>(5)</em>"
            ),
            "questionenjoyMapping": (
                "<p>Which task did you find <em>more enjoyable</em>? </p>"  # Arranging 18 dots in the square <em>or</em> Evaluating the similarity of 18 pairs?
                if lan == "en"
                else "<p>Welche Aufgabe hat Ihnen <b>besser gefallen</b>? </p>"  # Die 18 Punkte auf der Karte anzuordnen <em>oder</em> Die politische Ähnlichkeit von 18 Paaren zu bewerten?
            ),
            "enjoy_min": -50,
            "enjoy_max": 50,
            "enjoy_min_label": (
                f"I enjoyed much more to evaluate {player.n_checks} <b>pairs</b> <em>(-5)</em>"
                if lan == "en"
                else f"Mir hat es viel besser gefallen, {player.n_checks} <b>Paare</b> zu bewerten <em>(-5)</em>"
            ),
            "enjoy_neutral_label": (
                "Similarly enjoyable <em>(0)</em>"
                if lan == "en"
                else "Ähnlich gut bzw. schlecht <em>(0)</em>"
            ),
            "enjoy_max_label": (
                f"I enjoyed much more to arrange {player.n_dots} <b>dots</b> <em>(5)</em>"
                if lan == "en"
                else f"Mir hat es viel besser gefallen, {player.n_dots} <b>Punkte</b> anzuordnen <em>(5)</em>"
            ),
            "explain_text": (
                "If you would like, you can add further thoughts, comments, or explanations here <em>(optional)</em>:"
                if lan == "en"
                else "Falls Sie möchten, können Sie hier weitere Gedanken, Anmerkungen oder Erklärungen hinzufügen <em>(optional)</em>:"
            ),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.current_page += 1


#################################
#####  IMPORTANCE QUESTIONS   #####
#################################
class slide10_Importance(Page):
    form_model = "player"
    form_fields = [f"importance_{q}" for q in C.QUS] + ["importance_comments"]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.current_page += 1

    @staticmethod
    def is_displayed(player: Player):
        # trainingPassed = player.isTrainingPassed
        return player.consent  # and trainingPassed

    @staticmethod
    def vars_for_template(player):
        lan = player.language
        if player.field_maybe_none(f"t_on_importance") is None:
            player.t_on_importance = int(time.time())
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
                    ),
                    "last_label": (
                        "extremely important" if lan == "en" else "extrem wichtig"
                    ),
                }
            )
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "field_question_pairs": field_question_pairs,
            "page_title": (
                "Issue Importance" if lan == "en" else "Wichtigkeit von Themen"
            ),
            "table_head": (
                "For your perception of political differences or similarities, how important was the extent to which the people..."
                if lan == "en"
                else "Für Ihre Wahrnehmung politischer Unterschiede oder Gemeinsamkeiten, wie wichtig war es, inwieweit die Personen..."
            ),
            "question": (
                "Please rate <b>how important</b> each of the issues were to you in the last two tasks (creating the political map and evaluating the pairs of individuals)!"
                if lan == "en"
                else "Bitte schätzen Sie ein, <b>wie wichtig</b> die politischen Themen jeweils für Sie in den letzten beiden Aufgaben waren (die politische Karte zu erstellen bzw. einzelne Paare zu bewerten)!"
            ),
            "explain_text": (
                "If you want, you can explain here in more detail how these issues have influenced you or not influenced you in the previous tasks <em>(optional)</em>:"
                if lan == "en"
                else "Wenn Sie wollen, können Sie hier näher erklären, inwiefern die Fragen Sie in den letzten Aufgaben beeinflusst oder nicht beeinflusst haben <em>(optional)</em>:"
            ),
        }


#################################
#####  POLARISATION   #####
#################################
class slide11_PolarisationTopics(Page):
    form_model = "player"
    form_fields = [f"how_polarised_{q}" for q in C.QUS] + [
        "how_polarised",
        "how_polarised_comments",
    ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.current_page += 1

    @staticmethod
    def is_displayed(player: Player):
        # trainingPassed = player.isTrainingPassed
        return player.consent  # and trainingPassed

    @staticmethod
    def vars_for_template(player):
        lan = player.language
        if player.field_maybe_none(f"t_on_polarisation") is None:
            player.t_on_polarisation = int(time.time())
        questions = [C.QUS[i] for i in json.loads(player.question_sorting)]
        fields = [f"how_polarised_{q}" for q in questions]
        questions = [
            ("..." if lan == "en" else "...")
            + C.QUESTIONNAMESPOL[player.language][q]
            + "?"
            for q in questions
        ]

        first_label = (
            "Not at all divided" if lan == "en" else "Überhaupt nicht gespalten"
        )
        last_label = "Extremely divided" if lan == "en" else "Extrem gespalten"
        field_question_pairs = []
        for field, question in zip(fields, questions):
            field_question_pairs.append(
                {
                    "field_name": field,
                    "question_text": question,
                }
            )

        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "field_question_pairs": field_question_pairs,
            "how_polarised_question_text": (
                "...on political issues in general?"
                if lan == "en"
                else "...bei politischen Themen insgesamt?"
            ),
            "first_label": first_label,
            "last_label": last_label,
            "page_title": (
                "Your Perception of Polarisation"
                if lan == "en"
                else "Ihre Wahrnehmung von Polarisierung"
            ),
            "question": (
                "Please rate below how <b>politically divided</b> you perceive the opinions in Germany to be these days, first for the opinions on each of the political topics separately and then for political opinions in general."
                if lan == "en"
                else "Bitte schätzen Sie unten, wie <b>gespalten</b> Sie die politischen Meinungen heutzutage in Deutschland wahrnehmen, zuerst zu den politischen Themen separat und dann in politischen Fragen generell."
            ),
            "qu_polarization": (
                "What do you think: How divided are the opinions of people in Germany..."
                if lan == "en"
                else "Was denken Sie: Wie gespalten sind die Meinungen der Menschen in Deutschland..."
            ),
            "explain_text": (
                "If you want, you can describe how you perceive political division and polarisation in more detail <em>(optional)</em>:"
                if lan == "en"
                else "Wenn Sie wollen, können Sie hier Ihre Wahrnehmung von Spaltung und Polarisierung näher beschreiben <em>(optional)</em>:"
            ),
        }


#################################
#####  Social Relationships   #####
#################################
class slide12_Relationships(Page):
    form_model = "player"
    form_fields = [f"reference{n}_socialCloseness" for n in range(1, C.N_PERSONS + 1)]

    @staticmethod
    def is_displayed(player: Player):
        # trainingPassed = player.isTrainingPassed
        return player.consent  # and trainingPassed

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_relationships") is None:
            player.t_on_relationships = int(time.time())
        references = [
            {
                "id": f"reference{i}",
                "name": (
                    f"Your relation with <span class='pill' style='background-color: {C.REFPERSONCOLOR}; color: white;'><strong>{getattr(player, f'reference{i}')}</strong></span>"
                    if lan == "en"
                    else f"Ihre Beziehung zu <span class='pill' style='background-color: {C.REFPERSONCOLOR}; color: white;'><strong>{getattr(player, f'reference{i}')}</strong></span>"
                ),
            }
            for i in range(1, player.n_references + 1)
        ]

        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "color": C.REFPERSONCOLOR,
            "page_title": (
                "<em>Social</em> Closeness to Your Contacts"
                if lan == "en"
                else "<em>Soziale</em> Nähe zu Ihren Kontakten"
            ),
            "references": references,
            "qu_closeness": (
                "How would you rate in general the type of relation between you and the people or contacts you mentioned previously – regardless of political views?"
                if lan == "en"
                else "Wie würden Sie im Allgemeinen die Art der Beziehung zwischen Ihnen und den Personen in Ihrem sozialen Umfeld – unabhängig von politischen Ansichten? "
            ),
            "disclaimer": (
                "All your responses are linked to generic names <em>Person 1</em>, <em>Person 2</em>, etc. To protect privacy, we do <strong>not store</strong> the names or initials you provided."
                if lan == "en"
                else "Ihren Kontakten werden generischen Bezeichnungen wie <em>Person 1</em>, <em>Person 2</em> usw. zugeordnet. Zum Schutz der Privatsphäre werden die von Ihnen angegebenen Namen oder Initialen <strong>nicht gespeichert</strong>."
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
        player.current_page += 1


#################################
#####  SOCIAL CONTACTS POLITICAL IDENTITY   #####
#################################


class slide13_ContactIdentities(Page):
    form_model = "player"
    form_fields = [f"reference{n}_PartyFeelClosest" for n in range(1, C.N_PERSONS + 1)]

    @staticmethod
    def is_displayed(player: Player):
        # trainingPassed = player.isTrainingPassed
        return player.consent  # and trainingPassed

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_contactIdentities") is None:
            player.t_on_contactIdentities = int(time.time())
        references = [
            {
                "id": f"reference{i}",
                "name": (
                    f"Your contact <span class='pill' style='background-color: {C.REFPERSONCOLOR}; color: white;'><strong>{getattr(player, f'reference{i}')}</strong></span> is probably most leaning towards this party:"
                    if lan == "en"
                    else f"Ihr Kontakt <span class='pill' style='background-color: {C.REFPERSONCOLOR}; color: white;'><strong>{getattr(player, f'reference{i}')}</strong></span> neigt vermutlich am ehesten zu dieser Partei:"
                ),
            }
            for i in range(1, player.n_references + 1)
        ]

        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "color": C.REFPERSONCOLOR,
            "page_title": (
                "Political Identities of Your Contacts"
                if lan == "en"
                else "Politische Identitäten Ihrer Kontakte"
            ),
            "references": references,
            "qu_identities": (
                "Do <em>you</em> think, that your social contacts generally lean towards particular political parties in Germany?"  # "Do <em>you</em> think, there are political parties in Germany, that your social contacts respectively feel politically closer to than to all others? If so, which ones?"  # In Germany, many people tend to lean toward a particular political party for long periods of time, even though they occasionally vote for another party. How about you: do you generally lean toward a particular party? And if so, which one?
                if lan == "en"
                else "Glauben <em>Sie</em>, dass Ihre sozialen Kontakte – ganz allgemein – zu bestimmten politischen Parteien in Deutschland neigen?"  # "Glauben <em>Sie</em>, dass es bestimmte politische Parteien in Deutschland gibt, denen Ihre Kontakte sich jeweils politisch näher fühlen als allen anderen Parteien? Welchen? "   # Neigen Sie - ganz allgemein - einer bestimmten Partei zu? Und wenn ja, welcher?"
            ),
            "disclaimerDontKnow": (
                "If you are very unsure, you can always select <em>No answer</em>."
                if lan == "en"
                else "Wenn Sie sehr unsicher sind, können Sie immer die Option <em>Keine Angabe</em> auswählen."
            ),
            "choices_identity": dict(
                zip(
                    C.CHOICES_IDENTITY,
                    (
                        C.CHOICES_IDENTITY  # +
                        if lan == "en"
                        else C.CHOICES_IDENTITY_DE  #
                    ),
                )
            ),
            "disclaimer": (
                "All your responses are linked to generic names <em>Person 1</em>, <em>Person 2</em>, etc. To protect privacy, we do <strong>not store</strong> the names or initials you provided."
                if lan == "en"
                else "Ihren Kontakten werden generischen Bezeichnungen wie <em>Person 1</em>, <em>Person 2</em> usw. zugeordnet. Zum Schutz der Privatsphäre werden die von Ihnen angegebenen Namen oder Initialen <strong>nicht gespeichert</strong>."
            ),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.current_page += 1


#################################
#####  PoliticalInterest   #####
#################################
class slide14_PoliticalInterest(Page):
    form_model = "player"
    form_fields = [
        # "age",
        # "gender",
        "political_interest",
        "political_discussion",
        "overall_comments",
        "recontact",
    ]

    @staticmethod
    def is_displayed(player: Player):
        # trainingPassed = player.isTrainingPassed
        return player.consent  # and trainingPassed

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.field_maybe_none(f"t_on_politicalinterest") is None:
            player.t_on_politicalinterest = int(time.time())
        return {
            "maxslides": C.MAXSLIDES,
            "nslide": player.current_page,
            "lan_en": lan == "en",
            "page_title": (
                "Political Interest" if lan == "en" else "Politisches Interesse"
            ),
            # "qu_age": "How old are you?" if lan == "en" else "Wie alt sind Sie?",
            # "qu_gender": (
            #     "Which gender do you have?"
            #     if lan == "en"
            #     else "Welches Geschlecht haben Sie?"
            # ),
            # "choices_gender": dict(
            #     zip(
            #         C.CHOICES_GENDER,
            #         (C.CHOICES_GENDER if lan == "en" else C.CHOICES_GENDER_DE),
            #     )
            # ),
            "qu_discussion": (
                "How often, if ever, do you talk about politics or current events with your family, friends, or acquaintances?"
                if lan == "en"
                else "Wie oft, wenn überhaupt, sprechen Sie mit Ihrer Familie, Ihren Freunden oder Bekannten über Politik oder aktuelle Ereignisse?"
            ),
            "discussion_min": 0,
            "discussion_max": 100,
            "discussion_min_label": ("Never" if lan == "en" else "Nie"),
            "discussion_max_label": ("Very often" if lan == "en" else "Sehr oft"),
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
            "recontact_options": dict(
                zip(
                    [True, False],
                    (
                        [
                            "Yes. I want to be invited.",
                            "No. I do not want to be invited.",
                        ]
                        if lan == "en"
                        else [
                            "Ja. Ich möchte eingeladen werden.",
                            "Nein. Ich möchte nicht eingeladen werden.",
                        ]
                    ),
                )
            ),
            "recontact_question": (
                "We would like to invite you to participate in a similar survey for a follow-up study in a few weeks. Would you like to be invited by Bilendi for this follow-up survey? And if you participate in the second survey, can we link your responses from both surveys?"
                if lan == "en"
                else "Wir würden Sie gerne in einigen Wochen einladen, an einer ähnlichen Umfrage für eine Folgestudie teilzunehmen. Möchten Sie von Bilendi für diese Umfrage eingeladen werden? Und wenn Sie an der zweiten Umfrage teilnehmen, können wir dann Ihre Antworten aus beiden Umfragen miteinander verknüpfen?"
            ),  # <em>Your decision is entirely voluntary and will not affect your participation or the use of your data in any way.</em> <em> Ihre Entscheidung ist vollkommen freiwillig und hat keinerlei Auswirkungen auf Ihre Teilnahme oder die Verwendung Ihrer Daten.</em>
            "overall_comments_qu": (
                "Before you exit the survey by clicking on <em>Complete Survey</em>, feel free to add any final thoughts or comments. Is there anything you would like to share? We value your feedback."
                if lan == "en"
                else "Bevor Sie die Umfrage durch Klicken auf <em>Umfrage Abschließen</em> beenden, können Sie gerne noch abschließende Gedanken oder Kommentare hinzufügen. Gibt es etwas, das Sie uns mitteilen möchten? Wir freuen uns über Ihr Feedback."
            ),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
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
        if player.field_maybe_none(f"t_on_success") is None:
            player.t_on_success = int(time.time())
        return {
            "lan_en": player.language == "en",
        }

    def is_displayed(player: Player):
        # trainingPassed = player.isTrainingPassed
        return player.consent and player.completed  # and trainingPassed


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
        if player.field_maybe_none(f"t_on_fail") is None:
            player.t_on_fail = int(time.time())
        return {"lan_en": player.language == "en"}


#################################
#####  SEQUENCE   #####
#################################
page_sequence = (
    [
        slide01_Introduction,
        slide02_OpinionsWithNan,
        slide02a_Identity,
        slide00_toc,
        slide03_References,
    ]
    + [slide04_ReferencesOpinions]
    + [slide04b_VotersOpinions]
    + [slide02_OpinionsWithNanRevisited]
    + [slide00_toc]
    + [slide05a_MapGame]
    + [slide05a_MapTest, slide05b_MapTestResult] * C.N_MAX_PRACTICE_RUNS
    + [slide06_SPaM]
    + [slide07_Satisfaction]
    + [slide00_toc]
    + [slide08_PlausibilityCheck_Pairs] * (1 + C.N_PERSONS + len(C.LABELLED))
    + [slide00_toc]
    + [
        slide09_Tasks,
        slide10_Importance,
        # slide10b_ImportanceOther,
        slide11_PolarisationTopics,
        slide12_Relationships,
        slide13_ContactIdentities,
        slide14_PoliticalInterest,
        slideSuccess,
        slideFail,
    ]
)
