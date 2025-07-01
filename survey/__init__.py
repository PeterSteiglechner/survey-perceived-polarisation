from otree.api import *
import json
import pandas as pd
import random
import numpy  as np
from itertools import combinations

doc = """
Your app description
"""


def distance(a,b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5


class C(BaseConstants): 
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    N_MAX_PRACTICE_RUNS = 5
    
    # CONSTANTS 
    #LIKERT5 = [1,2,3,4,5] 
    LIKERT5_string_noNA = ['Strongly agree','Agree', 'Neutral','Disagree', 'Strongly disagree']
    LIKERT5_string_noNA_de = ['Stimme voll und ganz zu', 'Stimme eher zu', 'Teils/teils', 'Stimme eher nicht zu', 'Stimme überhaupt nicht zu']
    LIKERT5_transde = dict(zip(LIKERT5_string_noNA, LIKERT5_string_noNA_de))
    LIKERT5_transde["NA"] = "NA"
    LIKERT5_transde[""] = ""
    
    QUS = ["climate_concern", "gay_marriage", "rights_indep_integration", "econ_inequality"]

    QU_SORTS = [[0,1,2,3], [1,3,0,2], [2,0,3,1], [3,2,1,0]]

    QUESTIONTEXT = {
        "en":
        dict(zip(QUS, [
        "I am very concerned about climate change.",
        "It is good that marriages between two women or two men are allowed.",
        "Migrants should be given the same rights as natives, regardless of whether they make an effort and integrate.", # Only migrants who make an effort and integrate should be given the same rights as natives.
        "The differences in income and in wealth in Germany are too high.",
    ])), "de":
      dict(zip(QUS, [
        "Ich bin sehr besorgt über den Klimawandel.",
        "Es ist gut, dass Ehen zwischen zwei Frauen bzw. zwischen zwei Männern erlaubt sind.",
        "Migranten und Migrantinnen sollten die gleichen Rechte bekommen wie Einheimische unabhängig davon, ob sie sich anstrengen und integrieren.", #"Nur Migranten, die sich anstrengen und integrieren, sollten die gleichen Rechte bekommen wie Einheimische.",
        "Die Einkommens- und Vermögensunterschiede in Deutschland sind zu groß.",
    ]))
    }
    QUESTIONSHORTTEXT =  {
        "en":
        dict(zip( QUS, [
         "extreme concern about climate change", 
         "support same-sex marriage",
         "equal rights for migrants regardless of integration",  #"equal rights only for migrants who integrate",
         "income and wealth differences too high"
    ])), 
        "de":
                dict(zip( QUS, [
         "Extreme Besorgnis über Klimawandel", 
         "Unterstützung für gleichgeschlechtliche Ehe",
         "Gleiche Rechte für Migranten/-innen unabhängig von deren Integration",
         "Einkommens- und Vermögensunterschiede zu groß"
    ])),}

    QUESTIONNAMES = {
        "en":
        dict(zip( QUS, [
        "Opinion about climate change", 
        "Opinion about same-sex marriage", 
        "Opinion about whether equal rights for migrants should be given regardless of their integration efforts",
        "Opinion about economic inequality",
        ])), 
        "de":
                dict(zip( QUS, [
        "Die Meinung der Person zum Klimawandel", 
        "Die Meinung der Person zu gleichgeschlechtlicher Ehe", 
        "Die Meinung der Person ob Migranten oder Migrantinnen gleiche Rechte wie Einheimische bekommen sollten unabhängig von deren Integrationsbemühungen",
        "Die Meinung der Person zu ökonomischer Ungleichheit",
        ]))}
    
    NCONTACTS = 3

    LABELLED = ["Green Party", "AfD", "FDP", "Left Party"]
    LABELLED_de = dict(zip(LABELLED, ["Grünen", "AfD", "FDP", "Linken"]))
    LABELLEDCOLORS = dict(zip(LABELLED, ["#46962b", "#009ee0", "#ffed00", "#ff0000"]))
    LABELLED = list(np.random.choice(LABELLED, replace=False, size = len(LABELLED)))

    PERSONAS = pd.read_csv("_static/personas.csv")[QUS]
    P_OPS =  {f"P{n+1}": row.to_dict()  for n, row in PERSONAS.iterrows()}
    NPS = len(P_OPS.keys())

    NR_P_CHECKS = 4
    OPTIONS_P_CHECKS = ['No','Somewhat','Yes']
    NR_OTHER_CHECKS = 5 
    OPTIONS_OTHER_CHECKS = ["Very different", "Quite different",  "Neither", "Quite similar", "Very similar"]

    CHOICES_TOPICS= [qname for q,qname in QUESTIONNAMES["en"].items()]+["Different opinion(s) or topic(s)", "I don't know"]

    CHOICES_INTEREST = ["Not at all interested", "Hardly interested", "Quite interested", "Very interested"]

    CHOICES_IDENTITY = ["CDU/CSU", "AfD", "SPD", "Green Party", "Left Party", "BSW", "FDP", "Other party", "No party", "Refuse to say/No answer"]

    CHOICES_POLARISED = ["Not at all divided", "Somewhat divided", "Very divided", "Extremely divided"]

    OPTIONS_CONTACTS_CLOSE = ["Not particularly close", "Somewhat close", "Close", "Very close", "No answer"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

def make_field(label, language="en"):
    return models.StringField(
        choices= C.LIKERT5_string_noNA+["NA"],
        label=label,
        widget=widgets.RadioSelect,
    )

def define_contact(label, n):
    return  models.LongStringField(label=label, blank=False, max_length=20) 

class Player(BasePlayer):

    completed = models.BooleanField(blank=False)

    consent = models.BooleanField(blank=False)
    
    question_sorting = models.LongStringField(initial=json.dumps(C.QU_SORTS[np.random.choice(range(4))]))

    language = models.StringField(
        choices=[['en', 'English'], ['de', 'Deutsch']],
        widget=widgets.RadioSelect,
        label="Language / Sprache"
    )

    #################################
    #####  DEMOGRAPHICS   #####
    #################################

    age = models.IntegerField(label='', min=18, max=100)

    political_interest = models.StringField(
        label='', 
        choices= C.CHOICES_INTEREST,
        blank=False, 
        widget=widgets.RadioSelect
        )

    feel_closest_party = models.StringField(
        label='',  
        choices=C.CHOICES_IDENTITY,
        blank=False, 
        widget=widgets.RadioSelect
        )
    
    party_comment = models.LongStringField(label="", blank=True)

    how_polarised = models.StringField(
        label='',
        choices=C.CHOICES_POLARISED,
        blank=False,
        widget=widgets.RadioSelect
        )
   
    topic_importance = models.LongStringField(
        label='',
        blank=True,
    )

    importance_comments = models.LongStringField(blank=True, label="", initial="", null=True)  
    
    #################################
    #####  MAP POSITIONS   #####
    #################################

    # JSON data of positions
    positionsTest = models.LongStringField(blank=True)  
    positions_preP = models.LongStringField(blank=True)
    positions = models.LongStringField(blank=True)  

    #################################
    #####  Plausibility checks   #####
    #################################

    # triples with self
    valid_p1p2self_triples = models.LongStringField(blank=True)
    check = models.IntegerField(initial=1) 
    
    # pairwise
    checkPair = models.IntegerField(initial=1) 


    #################################
    #####  PRACTICE RUN   #####
    #################################

    isTrainingPassed = models.BooleanField(initial=False)#
    isTrainingCondFvC = models.BooleanField(initial=False)#
    isTrainingCondSelfvFC = models.BooleanField(initial=False)#
    isTrainingCondSvFC = models.BooleanField(initial=False)#
    isTrainingCondSvF = models.BooleanField(initial=False)#
    attemptPractice = models.IntegerField(initial=0) 

    #################################
    #####  RUNNING VARIABLES   #####
    #################################

    current_contact = models.IntegerField(initial=1) 
    evaluated_labelledPerson = models.IntegerField(initial=0) 
    ps_placed = models.IntegerField(initial=0)  
    which_contact_type = models.StringField(initial="contact")  # 'contact' or 'labelledPerson'


#################################
#####  Plausibility checks   #####
#################################
for n in range(1, C.NR_P_CHECKS+1):
    setattr(Player, f"check{n}_p1", models.LongStringField(blank=True))  
    setattr(Player, f"check{n}_p2", models.LongStringField(blank=True))  
    setattr(Player, f"check{n}", models.StringField(choices=C.OPTIONS_P_CHECKS,label="", widget=widgets.RadioSelect,blank=False))  
    setattr(Player, f"check{n}_explain", models.LongStringField(label="",blank=True))  

for n in range(1, C.NR_OTHER_CHECKS+1):
    setattr(Player, f"checkPair{n}_dot1", models.LongStringField(blank=True))  
    setattr(Player, f"checkPair{n}_dot2", models.LongStringField(blank=True))  
    setattr(Player, f"checkPair{n}", models.StringField(choices=C.OPTIONS_OTHER_CHECKS,label="", widget=widgets.RadioSelect,blank=False))  



#################################
#####  OWN POLITICAL OPINIONS   #####
#################################
for q in C.QUS:
    setattr(Player, f"own_{q}", make_field(''))  

#################################
#####  CONTACTS & CONTACTS' POLITICAL OPINIONS   #####
#################################
for n in range(1,C.NCONTACTS+1):
    setattr(Player, f"contact{n}", define_contact(f"Contact {n}: ", n))
    setattr(Player, f"contact{n}_generalCloseness",  models.StringField(choices=C.OPTIONS_CONTACTS_CLOSE,label="", widget=widgets.RadioSelect,blank=False))
    for q in C.QUS:
        setattr(Player, f"contact{n}_{q}", make_field(''))

#################################
#####  LABELLED INDIVIDS' POLITICAL OPINIONS   #####
#################################
for name in C.LABELLED:
    for q in C.QUS:
        setattr(Player, f"{name.replace(" ", "")}_{q}", make_field(''))




#################################

#################################

#################################


#################################
#####       PAGES           #####
#################################

class slide01_Introduction(Page):
    form_model = 'player'
    form_fields = ['consent', 'language']



class slide02_Opinions(Page):
    form_model = 'player'
    form_fields = [f"own_{q}" for q in C.QUS]
    @staticmethod
    def is_displayed(player: Player):
        return player.consent
    @staticmethod
    def vars_for_template(player: Player): 
        lan = player.language
        questions = [C.QUS[i] for i in json.loads(player.question_sorting)]
        
        fields =  [f"own_{q}" for q in questions]
        questions = [C.QUESTIONTEXT[player.language][q] for q in questions]
        field_question_pairs = []
        for field, question in zip(fields, questions):
            choices = dict(zip(C.LIKERT5_string_noNA[::-1], (C.LIKERT5_string_noNA[::-1] if lan=="en" else C.LIKERT5_string_noNA_de[::-1])))  
            field_question_pairs.append({
                'field_name': field,
                'question_text': question,
                'choices': choices,
            })
        return {
            'lan_en':lan=="en",
            'field_question_pairs': field_question_pairs, 
            'page_title': 'Your political views' if player.language == 'en' else 'Ihre politischen Ansichten',
            'instruction_text': '<p style="margin-bottom: 0.5em;" >At the beginning of this survey, we are interested in your own political opinions. </p><p style="margin-bottom: 0.5em;" >Please indicate to what extent you agree or disagree with the following statements.</p><p style="margin-bottom: 0.5em;" > There are no right or wrong answers; we are most interested in which response option is most aligned with your views.</p>' if player.language == 'en' else '<p style="margin-bottom: 0.5em;">Zum Start dieser Umfrage interessieren wir uns für Ihre eigenen politischen Ansichten.</p><p style="margin-bottom: 0.5em;" > Bitte geben Sie an, inwieweit Sie den folgenden Aussagen zustimmen oder nicht zustimmen.</p><p style="margin-bottom: 0.5em;" >Es gibt keine richtigen oder falschen Antworten. Wir interessieren uns dafür welche Antwortmöglichkeit am ehestn Ihren Ansichten entspricht.</p>',
            'table_head':"Your responses" if player.language =="en" else 'Ihre Antworten'
            }
    
class slide03_Contacts(Page):
    form_model = 'player'
    form_fields = [f"contact{n}" for n in range(1, C.NCONTACTS+1)]
    @staticmethod
    def is_displayed(player: Player):
        return player.consent
    @staticmethod
    def vars_for_template(player:Player):
        lan = player.language
        contact_fields = []
        for n in range(1, C.NCONTACTS+1):
            contact_fields.append({
                'name': f'contact{n}',
                'label': f"Contact {n}:" if lan == "en" else f"Kontakt {n}:"
            })
        return {
            'lan_en':lan=="en",
            "ncontacts": C.NCONTACTS,
            "contact_fields": contact_fields,
            'page_title': "Social Contacts" if lan=="en" else "Soziale Kontakte", 
            'instruction_text': f"<p style='margin-bottom:0.5em;'>Think about <strong>{C.NCONTACTS} social contacts</strong> that you know well. This can include friends, family members, colleagues, ....</p><p style='margin-bottom:0.5em;'>Please write down their names or initials so that you are later able to recognise them (we will not use/store that information).</p>" if lan=="en" else f"<p style='margin-bottom:0.5em;'>Denken Sie an <strong>{C.NCONTACTS} soziale Kontakte</strong>, die Sie gut kennen. Das können Freunde, Freundinnen, Familienmitglieder, Kollegen, etc. sein.</p><p style='margin-bottom:0.5em;'>Bitte notieren Sie die Namen oder Initialen dieser Kontakte in den Feldern unten, so dass Sie diese später wiedererkennen (wir werden diese Informationen nicht speichern oder verwenden).</p>", 
              }
    @staticmethod
    def error_message(player: Player, values):
        contacts = [v.strip() for v in values.values() if v.strip()]
        if len(contacts) < C.NCONTACTS:
            return "Please fill in all contact fields!" if player.language=="en" else "Bitte füllen Sie alle Felder aus!"
        if len(set(contacts)) < len(contacts):
            return "Each contact must be unique. Please correct duplicates. You can use nicknames, initials, or anything that you will later recognise." if player.language=="en" else "Jeder Kontakt muss einen eindeutigen Namen haben. Bitte korrigieren Sie Duplikate. Sie können Spitznamen, Initialien oder alles benutzen, was Sie später wiedererkennen."

class slide04_PersonOpinion(Page):
    form_model = "player"
    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.which_contact_type == 'contact':
            idx = player.current_contact
            name = getattr(player, f"contact{idx}")
            prefix = f"contact{idx}_"
            displName = f"{name}"
            displName1 = f"Ihren Kontakt <strong>{name}</strong>"
            displName3 = f"<strong>{name}</strong>"
            displName4 = f"<strong>{name}</strong>"
            #displName4 = f"{name}"
            color = "#00ff80"  # contact color
        else:  # mode == 'labelledPerson'
            idx = player.evaluated_labelledPerson
            name = C.LABELLED[idx]
            prefix = f"{name.replace(" ","")}_"
            displName = f"a typical {name} voter" if lan=="en" else f"{C.LABELLED_de[name]} Wähler/-in"
            displName4 = "The person"
            color = C.LABELLEDCOLORS[name]
            if lan=="de":
                displName1 = f"eine typische Wählerin oder einen typischen Wähler der <strong>{C.LABELLED_de[name]}</strong>"
                displName3 = f"Wähler/Wählerin der {C.LABELLED_de[name]}"
                displName4 = f"Die Person"
        fields = [f"{prefix}{q}" for q in [C.QUS[i] for i in json.loads(player.question_sorting)]]
        questions = [C.QUESTIONTEXT[lan][q] for q in [C.QUS[i] for i in json.loads(player.question_sorting)]]
        field_question_pairs = []
        for field, question in zip(fields, questions):
            choices = dict(zip(C.LIKERT5_string_noNA[::-1], (C.LIKERT5_string_noNA[::-1] if lan=="en" else C.LIKERT5_string_noNA_de[::-1])))   # convert list of tuples to dict
            field_question_pairs.append({
                'field_name': field,
                'question_text': question,
                'choices': choices,
            })
        return {
            'lan_en':lan=="en",
            "nslide":3+idx+(1+C.NCONTACTS if player.which_contact_type=="labelledPerson" else 0) ,
            "name": name,
            "color": color,
            "person_type": player.which_contact_type,
            "fields": fields,
            "questions": questions,
            "would_respond": f"<p style='margin-top: 0.5em;'>{displName4} would probably respond with:</p>" if lan=="en" else f"<p style='margin-top: 0.5em;'>{displName4} würde vermutlich antworten:</p>",
            "field_question_pairs": field_question_pairs,            
            'page_title': 'Political Opinions of Others' if lan == 'en' else 'Politische Meinungen von anderen Menschen',
            'instruction_text': f'Thinking about <strong>{displName}</strong>, how do you think <strong>{displName}</strong> would respond to those same political questions?' if lan == 'en' else f'Denken Sie nun an {displName1}. Wie würde diese Person die selben politischen Fragen beantworten?',
            'table_head':f"<strong>{displName}</strong>'s responses" if lan =="en" else f"Antworten von <strong>{displName3}</strong>"
        }

    @staticmethod
    def get_form_fields(player: Player):
        if player.which_contact_type == 'contact':
            prefix = f"contact{player.current_contact}_"
        else:
            name = C.LABELLED[player.evaluated_labelledPerson]
            prefix = f"{name.replace(" ", "")}_"
        return [f"{prefix}{q}" for q in [C.QUS[i] for i in json.loads(player.question_sorting)]]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.which_contact_type == 'contact':
            player.current_contact += 1
        else:
            player.evaluated_labelledPerson += 1
        if player.current_contact > C.NCONTACTS:
            player.which_contact_type = "labelledPerson"

    @staticmethod
    def is_displayed(player: Player):
        if not player.consent:
            return False
        if player.which_contact_type == 'contact':
            return player.current_contact <= C.NCONTACTS
        else:
            return player.evaluated_labelledPerson <= len(C.LABELLED)
        


class slide05a_MapTest(Page):
    form_model = 'player'
    form_fields = ['positionsTest'] 

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.positionsTest = player.positionsTest
        player.attemptPractice += 1

    @staticmethod
    def is_displayed(player):
        return player.consent and (not player.isTrainingPassed)
    
    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        if player.attemptPractice==0:
            init_dots = [{"dottype": "self", "varname": "self", "name_disp": "Self" if lan=="en" else "Ich", "x": 330, "y": 50, "color":"grey"}, 
            {"dottype": "friend", "varname": "friend", "name_disp": "Friend" if lan=="en" else "Freund", "x": 330, "y": 100, "color":"blue"}, 
            {"dottype": "coworker", "varname": "coworker", "name_disp": "Co-Worker" if lan=="en" else "Kollegin", "x": 330, "y": 150, "color":"blue"}, 
            {"dottype": "sister", "varname": "sister", "name_disp": "Sister" if lan=="en" else "Schwester", "x": 330, "y": 200, "color":"blue"}, 
            ]
        else:
            init_dots = json.loads(getattr(player, "positionsTest", []))
        return {
            "nslide":3+len(C.LABELLED)+C.NCONTACTS+1,
            'lan_en':lan=="en",
            "dots": init_dots,
    'page_title': "Political Mapping – Practice" if lan=="en" else "Politisches Mapping – Training",
    'lan':lan,
    'instruction_text1': 
    "In the following part, we will ask you to place people on a political map based on how distant or similar you perceive their political views to be. To prepare for this main task, we will begin with a short <strong>practice round</strong>." if lan=="en" else "Im folgenden Teil werden wir Sie bitten, Personen auf einer politischen Landkarte einzuordnen, je nachdem, wie ähnlich oder unterschiedlich Sie deren politischen Ansichten wahrnehmen. Zur Vorbereitung auf die eigentliche Aufgabe beginnen wir mit einer kurzen <strong>Übungsrunde</strong>.", 
    'instruction_text2': "Imagine you, a friend, a co-worker, and your sister are placed in a room (represented by the rectangle below)." if lan=="en" else "Stellen Sie sich vor, dass Sie sich zusammen mit einem Freund, einer Arbeitskollegin und Ihrer Schwester in einem Raum befinden (das Rechteck unten).",
    'instruction_text3': 
        "<p style='margin-bottom:0.5em;'><strong>Arrange the people in the room based on how <em>you</em> see their political views:</strong></p><ul style='margin-bottom:0.5em;'><li><strong>Place individuals closer together if you perceive them as politically similar.</strong></li><li><strong>Place individuals farther apart if  you perceive them as politically different.</strong></li></ul>" if lan=="en" else "<p style='margin-bottom:0.5em;'><strong>Ordnen Sie die Personen im Raum so an, wie <em>Sie</em> deren politischen Ansichten wahrnehmen:</strong></p><ul style='margin-bottom:0.5em;'> <li><strong>Platzieren Sie Personen näher beieinander, wenn Sie diese als politisch ähnlich wahrnehmen.</strong></li><li><strong>Platzieren Sie Personen weiter auseinander, wenn Sie diese als politisch unterschiedlich wahrnehmen.</strong></li></ul>",
    'disclaimer': "<p style='margin-bottom:0.5em;>This is a practice round – some arrangements match the instructions below, others do not. When you click <em>Next</em>, we will show you whether your arrangement meets all the instructions.</p><p style='margin-bottom:0.5em;'><strong>In the main task on the next slide, there will be NO right or wrong answers — only your personal perception will matter.</strong></p>" if lan=="en" else "<p style='margin-bottom:0.5em;'>Dies ist eine Übungsrunde – einige Anordnungen entsprechen den untenstehenden Anweisungen, andere nicht. Wenn Sie auf <em>Weiter</em> klicken, erfahren Sie, ob Ihre Anordnung alle Vorgaben erfüllt.</p><p style='margin-bottom:0.5em;'><strong>In dem Hauptteil auf der nächsten Seite wird es KEINE richtigen oder falschen Antworten geben – nur Ihre persönliche Wahrnehmung wird relevant sein.</strong></p>",
    'detailed_instructions_1': "<h3>Step-by-Step Instructions</h4><p style='margin-bottom: 0.5em; color: black;'>You will start with several points on the right side. Drag these one by one into the rectangle as described in the following instructions:</p>" if lan=="en" else
    "<h3>Schritt-für-Schritt Anleitung</h4><p style='margin-bottom: 0.5em; color: black;'>Sie beginnen mit mehreren Punkten auf der rechten Seite. Ziehen Sie diese nacheinander in das Rechteck, wie in der folgenden Anleitung beschrieben:</p>", 
    'detailed_instructions_2': "<details style='margin-bottom: 0em;'><summary style='white-space: nowrap;'><strong>Step 1</strong></summary>Place the point <em>Self</em> somewhere inside the rectangle. This point represents your own political views.</details> <details style='margin-bottom: 0em;'><summary style='white-space: nowrap;'><strong>Step 2</strong></summary>Place the point <em>Friend</em> near you. The friend has similar views to yours.</details> <details style='margin-bottom: 0em;'><summary style='white-space: nowrap;'><strong>Step 3</strong></summary>Add your <em>Co-worker</em>. Since you often disagree with them, place the point <em>Co-worker</em> farther away from <em>Self</em>.</details> <details style='margin-bottom: 0em;'><summary style='white-space: nowrap;'><strong>Step 4</strong></summary>You also believe that your co-worker's views are even more different from your friend's than from yours. Therefore, place the point so that <em>Co-worker</em> is farther from <em>Friend</em> than from <em>Self</em>.</details> <details style='margin-bottom: 0em;'><summary style='white-space: nowrap;'><strong>Step 5</strong></summary>Add your <em>Sister</em>. You feel that your sister thinks quite differently politically than you do. So place the point <em>Sister</em> far away from the point <em>Self</em>.</details> <details style='margin-bottom: 0em;'><summary style='white-space: nowrap;'><strong>Step 6</strong></summary>You think your sister's political views align somewhat more with your friend and co-worker than with yourself. Therefore, place the point <em>Sister</em> closer to the points <em>Co-worker</em> and <em>Friend</em> than to the point <em>Self</em>.</details>" if lan == "en" else "<details style='margin-bottom: 0em;'><summary style='white-space: nowrap;'><strong>Schritt 1</strong></summary>Platzieren Sie den Punkt <em>Ich</em> irgendwo im Rechteck. Dieser Punkt steht für Ihre eigenen politischen Ansichten.</details><details style='margin-bottom: 0em;'><summary style='white-space: nowrap;'><strong>Schritt 2</strong></summary> Platzieren Sie den Punkt <em>Freund</em> in Ihrer Nähe. Der Freund hat ähnliche Ansichten wie Sie.</details><details style='margin-bottom: 0em;'><summary style='white-space: nowrap;'><strong>Schritt 3</strong></summary>Fügen Sie Ihre <em>Kollegin</em> hinzu. Da sie oft anderer Meinung sind als sie, platzieren Sie den Punkt <em>Kollegin</em> weiter entfernt von <em>Ich</em>.</details><details style='margin-bottom: 0em;'><summary style='white-space: nowrap;'><strong>Schritt 4</strong></summary>Sie glauben außerdem, dass die Ansichten Ihrer Kollegin dem Freund noch fremder sind als Ihnen. Platzieren Sie daher den Punkt so, dass <em>Kollegin</em> weiter von <em>Freund</em> entfernt ist als von <em>Ich</em>.</details><details style='margin-bottom: 0em;'><summary style='white-space: nowrap;'><strong>Schritt 5</strong></summary>Fügen Sie nun Ihre <em>Schwester</em> hinzu. Sie haben das Gefühl, dass Ihre Schwester politisch ganz anders denkt als Sie. Platzieren Sie also den Punkt <em>Schwester</em> weit weg von dem Punkt <em>Ich</em>.</details><details style='margin-bottom: 0em;'><summary style='white-space: nowrap;'><strong>Schritt 6</strong></summary>Sie denken, dass Ihre Schwester politisch etwas mehr mit Ihrem Freund und Ihrer Kollegin übereinstimmt als mit Ihnen selbst. Platzieren Sie also den Punkt <em>Schwester</em> näher bei den Punkten <em>Kollegin</em> und <em>Freund</em> als bei dem Punkt <em>Ich</em>.</details>",
    'all_dots_instr': "All dots must be within the square boundary to proceed. You can re-position any dot at any time until you are satisfied with the arrangement." if lan=="en" else "Um fortzufahren müssen alle Punkte im Rechteck platziert werden. Sie können jeden Punkt verschieben bis Sie mit der Anordnung zufrieden sind."
  }
    

class slide05b_MapTestResult(Page):
    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language

        pos = json.loads(player.positionsTest)
        pos = {p["varname"]: [p["x"], p["y"]] for p in pos}
        #calculate distances
        dF = distance(pos["self"], pos["friend"])
        dC = distance(pos["self"], pos["coworker"])
        dS = distance(pos["self"], pos["sister"])
        dFS = distance(pos["friend"], pos["sister"])
        dFC = distance(pos["friend"], pos["coworker"])
        dCS = distance(pos["coworker"], pos["sister"])
        # check conditions
        player.isTrainingCondFvC = bool(dF<dC)  # Rule 2/3
        player.isTrainingCondSelfvFC = bool(dFC>dC)  # Rule 4
        player.isTrainingCondSvF = bool(dS>dF) # Rule 5
        player.isTrainingCondSvFC = bool((dFS<dS) and (dCS<dS)) # Rule 6.
        isTrainingPassed = player.isTrainingCondFvC & player.isTrainingCondSelfvFC & player.isTrainingCondSvFC & player.isTrainingCondSvF
        player.isTrainingPassed = isTrainingPassed

        errors = ""
        if lan=="en":
            errors += r"- <em>Instructions 2/3: </em> The distance between 'Self' and 'Co-worker' should be larger than the distance between 'Self' and 'Friend'. <br>" if player.isTrainingCondFvC==0 else ""
            errors += r"- <em>Instruction 4: </em> The distance between 'Friend' and 'Co-worker' should be larger than the distance between 'Self' and 'Co-worker'. <br>" if player.isTrainingCondSelfvFC==0 else ""
            errors += r"- <em>Instruction 5: </em> The distance between 'Self' and 'Sister' should be larger than the distance between 'Self' and 'Friend'. <br>" if player.isTrainingCondSvF==0 else ""
            errors += r"- <em>Instruction 6: </em> The distance between 'Self' and 'Sister' should be larger than the distances between 'Friend' and 'Sister' and between 'Co-worker' and 'Sister'. <br>" if player.isTrainingCondSvFC==0 else ""
        else:
            errors += r"- <em>Schritt 2/3: </em> Die Distanz zwischen 'Ich' und 'Kollegin' sollte größer sein als die Distanz zwischen 'Ich' und 'Freund'. <br>" if player.isTrainingCondFvC == 0 else ""
            errors += r"- <em>Schritt 4: </em>Die Distanz zwischen 'Freund' und 'Kollegin' sollte größer sein als die Distanz zwischen 'Ich' und 'Kollegin'. <br>" if player.isTrainingCondSelfvFC == 0 else ""
            errors += r"- <em>Schritt 5: </em> Die Distanz zwischen 'Ich' und 'Schwester' sollte größer sein als die Distanz zwischen 'Ich' und 'Freund'. <br>" if player.isTrainingCondSvF == 0 else ""
            errors += r"- <em>Schritt 6: </em> Die Distanz zwischen 'Ich' und 'Schwester' sollte größer sein als die Distanzen zwischen 'Freund' und 'Schwester' sowie 'Kollegin' und 'Schwester'. <br>" if player.isTrainingCondSvFC == 0 else ""

        return {
            "nslide":3+len(C.LABELLED)+C.NCONTACTS+2,
            "lan_en": lan=="en",
            "passed": player.isTrainingPassed, 
            "button_msg": ("Continue" if player.isTrainingPassed else ("Continue Anyway" if player.attemptPractice == C.N_MAX_PRACTICE_RUNS else "Repeat Training")) if lan=="en" else  ("Weiter" if player.isTrainingPassed else ("Trotzdem weiter" if player.attemptPractice == C.N_MAX_PRACTICE_RUNS else "Wiederhole Training")),
            "attempt_msg": f"Attempt {player.attemptPractice} of {C.N_MAX_PRACTICE_RUNS}" if lan=="en" else f"Versuch {player.attemptPractice} von {C.N_MAX_PRACTICE_RUNS}",
            "page_title": "Political Mapping – Practice – Results" if lan=="en" else "Politisches Mapping – Training – Ergebnis", 
            'success_msg': "<strong>Well done!</strong> Your arrangement fulfills all criteria." if lan=="en" else "<strong>Gut gemacht!</strong> Ihre Anordnung der Punkte erfüllt alle Kriterien.",
            'error_msg': f"<strong>Your arrangement does not meet all steps of the instructions:</strong></p><p style='margin: 0 0 1em 0; white-space: pre-line;'>{errors}</p><p style='margin-bottom: 0.5em;'>Please repeat the training and try to arrange the dots so that all criteria are fulfilled.</p>" if lan=="en" else f"<strong>Ihre Anordnung erfüllt nicht alle Schritte der Anleitung:</strong></p><p style='margin: 0 0 1em 0; white-space: pre-line;'>{errors}</p><p style='margin-bottom: 0.5em;'>Bitte wiederholen Sie das Training und versuchen Sie, die Punkte so anzuordnen, dass alle Teile der Anleitung erfüllt sind.</p>",
            "img_help": not (player.attemptPractice<=2 or player.isTrainingPassed),
            "img_help_text": "<p style='margin-bottom: 0.5em;'>"+("Below you can find one possible arrangement of the dots that fulfills all criteria" if lan == "en" else "Unten sehen Sie eine mögliche Anordnung der Punkte, die alle Kriterien erfüllt")+":</p>",
             "img_source":  f"correctTraining_{lan}.png",
            } 
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consent and (player.attemptPractice<=C.N_MAX_PRACTICE_RUNS) and ((not player.isTrainingPassed) or (player.isTrainingPassed and player.attemptPractice==0))



class slide06_SPaM(Page):
    form_model = 'player'
    form_fields = ['positions_preP','positions']
    @staticmethod
    def is_displayed(player: Player):
        return player.consent
    @staticmethod
    def vars_for_template(player:Player):
        lan = player.language
        displ_names =  ["Self" if lan=="en" else "Ich"]+[getattr(player, f"contact{f}") for f in range(1,C.NCONTACTS+1)]+[f"{v+" voter" if lan=="en" else C.LABELLED_de[v]+' Wähler/Wählerin'}" for v in C.LABELLED]
        types = ["self"]+["contact"]*C.NCONTACTS + ["labelledPerson"]*len(C.LABELLED)
        varnames = ["self"]+[f"contact{f}" for f in range(1,C.NCONTACTS+1)]+[f"{v}" for v in C.LABELLED] 
        init_dots = [{"dottype": dottype, "varname": varname, 
        "name_disp": name, "x": 530, "y": 40 + i * 60, "descr": ""} for i, (dottype, varname, name) in enumerate(zip(types, varnames, displ_names))]
        return {
            "nslide":3+len(C.LABELLED)+C.NCONTACTS+2+1,
            'lan_en':lan=="en",
            "dots":init_dots,
            "page_title": "Political Mapping – Part 1" if lan=="en" else "Politisches Mapping – Teil 1",
            "instru1": "We now continue to the main task in this survey." if lan=="en" else "Wir beginnen nun mit dem Hauptteil dieser Umfrage.",
            "instruRoom": "Imagine you, your three social contacts, a typical Green Party voter, FDP voter, AfD voter, and Left Party voter are in a room (represented by the rectangle below)." if lan=="en" else "Stellen Sie sich vor, dass Sie sich zusammen mit Ihren drei Kontakten und mit jeweils einem typischen Wähler oder einer typischen Wählerin der Grünen, der AfD, der FDP und der Linken in einem Raum befinden (repräsentiert durch das Rechteck unten).",
            'instru_main': "<p style='margin-bottom:0.5em;'>Arrange the people in the room based on how <em>you</em> see their political views about questions regarding climate change, migration, inequality and minorities:</p><ul style='margin-bottom:0.5em;'><li><strong>Place individuals closer together if you perceive them as politically similar.</strong></li><li><strong>Place individuals farther apart if  you perceive them as politically different.</strong></li></ul><p style='margin-bottom:0.5em;'>There are NO right or wrong answers — we are interested in your personal perception.</p>" if lan=="en" else "<p style='margin-bottom:0.5em;'>Ordnen Sie die Personen im Raum so an, wie <em>Sie</em> deren politischen Ansichten zu Fragen über Klimawandel, Migration, Ungleichheit und Minderheiten wahrnehmen:</p><ul style='margin-bottom:0.5em;'> <li><strong>Platzieren Sie Personen näher beieinander, wenn Sie diese als politisch ähnlich wahrnehmen.</strong></li><li><strong>Platzieren Sie Personen weiter auseinander, wenn Sie diese als politisch unterschiedlich wahrnehmen.</strong></li></ul><p style='margin-bottom:0.5em;'>Es gibt KEINE richtigen oder falschen Antworten – wir sind an Ihrer persönliche Einschätzung interessiert.</p>", 
            'instru_click': "<summary style='white-space: nowrap;'><strong>Helping lines</strong></summary> If you enable this function and click on one of the dots, circles will appear that might help you evaluate how well your arrangement matches with how you roughly perceive political similarity. You can scale the circles by moving the small arrows <strong><></strong>." if lan=="en" else "<summary style='white-space: nowrap;'><strong>Hilfslinien</strong></summary> Wenn Sie diese Funktion aktivieren und auf einen der Punkte klicken, erscheinen Kreise, die Ihnen dabei helfen können einzuschätzen wie gut Ihre Anordnung widerspiegelt, wie Sie politische Nähe wahrnehmen. Sie können die Kreise durch Verschieben der kleinen Pfeile skalieren <strong><></strong>.", 
            'all_dots_instr': "All dots must be within the square boundary to proceed. You can re-position any dot at any time until you are satisfied with the arrangement." if lan=="en" else "Um fortzufahren müssen alle Punkte im Rechteck platziert werden. Sie können jeden Punkt verschieben bis Sie mit der Anordnung zufrieden sind.", 
            "labelClose": "close" if lan=="en" else "ähnlich",
            "labelFar": "distant" if lan=="en" else "unterschiedlich",
            "helping_lines": "Show helping lines" if lan=="en" else "Hilfslinien anzeigen", 
            # "button_to_disable_helping_lines":
}

class slide07_SPaM_personas(Page):
    form_model = 'player'
    form_fields = ['positions']  
    
    @staticmethod
    def vars_for_template(player:Player):
        lan = player.language
        questions = [C.QUS[i] for i in json.loads(player.question_sorting)]
        def get_ops(prefix, questions):
            return {
                q: getattr(player, f"{prefix}{q}", "NA") or "NA"
                for q in questions
            }
        def format_ops(ops_dict, lan):
            return "; ".join(
                f"{C.QUESTIONSHORTTEXT[lan][q]}: {val if lan=="en" else C.LIKERT5_transde[val] }"
                for q, val in ops_dict.items()
            )
        
        P = f"P{player.ps_placed + 1}"
        P_op = [C.P_OPS[P][q] for q in questions]
        P_op = ["" if str(op)=="nan" else op for op in P_op]
        pos = json.loads(player.positions) if player.positions else []

        P_text_short = "; ".join([
            f"{C.QUESTIONSHORTTEXT[lan][q]}: {P_op[i] if lan=='en' else C.LIKERT5_transde[P_op[i]]}"
            for i, q in enumerate(questions) 
        ])

        # Write dot descriptions of Self, Contacts, Labelled, and past Personas
        dot_descrs = {"self": format_ops(get_ops("own_", [C.QUS[i] for i in json.loads(player.question_sorting)]), lan)}
        for f in range(1, C.NCONTACTS + 1):
            dot_descrs[f"contact{f}"] = format_ops(get_ops(f"contact{f}_", questions), lan)
        for v in C.LABELLED:
            dot_descrs[f"{v}"] = format_ops(get_ops(f"{v.replace(" ", "")}_", questions), lan)
        for p in range(1, player.ps_placed + 1):
            currP = f"P{p}"
            currP_op = [C.P_OPS[currP][q] for q in questions]
            currP_op = ["" if str(op)=="nan" else op for op in currP_op]
            dot_descrs[currP] = "; ".join([
                f"{C.QUESTIONSHORTTEXT[lan][q]}: {op if lan=="en" else C.LIKERT5_transde[op]}"
                for q, op in zip(questions, currP_op) 
            ])

        # Prepare initial dot data
        init_dots = [
                    {"varname": p["varname"],
                    "name_disp": p["name_disp"],
                    "x": p["x"],
                    "y": p["y"],
                    "dottype": p["dottype"],
                    "descr": dot_descrs.get(p["varname"], "")}
                for p in pos
            ]
        init_dots.append({"varname": P, "name_disp": P, "x": 530, "y": 350, "dottype": "P", "descr": P_text_short})

        return {
            "nslide":3+len(C.LABELLED)+C.NCONTACTS+2+2,
            'lan_en':lan=="en",
            "P": P,
            "P_text_short": P_text_short,
            "dots": init_dots, 
            "img_source": f"{P}_op_{lan}_sort{''.join([f"{n}" for n in json.loads(player.question_sorting)])}.png",
            "n_ps": C.NPS,
            "ps_placed": player.ps_placed+1,
            "page_title": "Political Mapping – Part 2" if lan=="en" else "Politisches Mapping – Teil 2", 
            "heading": f"Person {player.ps_placed+1} of { C.NPS} " if lan=="en" else f"Person {player.ps_placed+1} von {C.NPS}",
            'instru_main': "<p style='margin-bottom:0.5em;'>Arrange the people in the room based on how <em>you</em> see their political views on questions regarding climate change, migration, inequality and minorities:</p><ul style='margin-bottom:0.5em;'><li><strong>Place individuals closer together if you perceive them as politically similar.</strong></li><li><strong>Place individuals farther apart if  you perceive them as politically different.</strong></li></ul><p style='margin-bottom:0.5em;'>There are NO right or wrong answers — we are interested in your personal perception.</p>" if lan=="en" else "<p style='margin-bottom:0.5em;'>Ordnen Sie die Personen im Raum so an, wie <em>Sie</em> deren politischen Ansichten zu Fragen über Klimawandel, Migration, Ungleichheit und Minderheiten wahrnehmen:</p><ul style='margin-bottom:0.5em;'><li><strong>Platzieren Sie Personen näher beieinander, wenn Sie diese als politisch ähnlich wahrnehmen.</strong></li><li><strong>Platzieren Sie Personen weiter auseinander, wenn Sie diese als politisch unterschiedlich wahrnehmen.</strong></li></ul><p style='margin-bottom:0.5em;'>Es gibt KEINE richtigen oder falschen Antworten – wir sind an Ihrer persönliche Einschätzung interessiert.</p>", 
            'instru_p1': f"<p style='margin-bottom:1em;'>In the next part of this survey, you will be introduced to a hypothetical person along with a brief description of their political views.</p><p style='margin-bottom:1em;'> Try to imagine this person as clearly as possible based on the information provided. How politically similar or different do you think this person is — compared to yourself, your social contacts, and the typical voters in the room?<p>" if lan=="en" else f"<p style='margin-bottom:1em;'>Im nächsten Teil dieser Umfrage stellen wir Ihnen eine hypothetische Person vor und geben einen kurzen Überblick über deren politische Ansichten.</p><p style='margin-bottom:1em;'>Versuchen Sie, sich diese Person so gut wie möglich auf Grundlage dieser Informationen vorzustellen. Wie politisch ähnlich oder unterscheidlich erscheint Ihnen diese Person – im Vergleich zu Ihnen selbst, Ihren sozialen Kontakten und den typischen Wähler oder Wählerinnen im Raum?</p>", #<p style='margin-bottom:1em;'>Now consider the person <strong>{P}</strong>. Place the pink dot within the rectangle according to their political closeness or distance to the other individuals.<p>" if lan =="en" else "<p style='margin-bottom:1em;'>Betrachten Sie die Person <strong>{P}</strong>. Platzieren Sie den pinken Punkt im Rechteck entsprechend der politischen Nähe oder Distanz zu den anderen Personen.</p>"
            'instru_p2': f"Here are the responses of the person <strong>{P}</strong> to (some of) the questions from the previous slides :" if lan=="en" else f"Hier sind die Antworten von der Person <strong>{P}</strong> auf (ein paar) Fragen der vorherigen Seiten:",
            'instru_click': "<strong>Pop-up</strong>: If you click on a dot, a box with the individual's opinions will appear on the right side." if lan=="en" else "<strong>Pop-up</strong>: Wenn Sie auf einen Punkt klicken, erscheint auf der rechten Seite eine Info-Box mit den Meinungen der Person.",
            'all_dots_instr': "All dots must be within the square boundary to proceed. You can re-position any dot, <strong>including the dots from the previous mapping exercise</strong>, at any time until you are satisfied with the arrangement." if lan=="en" else "Um fortzufahren müssen alle Punkte im Rechteck platziert werden. Sie können jeden Punkt, <strong>inklusive der Punkte aus der vorherigen Aufgabe</strong>, verschieben bis Sie mit der Anordnung zufrieden sind.", 
            'reminder': "Remember, there are no right or wrong answers. We are most interested in your own political perceptions!" if lan=="en" else "Denken Sie daran: Es gibt keine richtigen oder falschen Antworten. Wir sind vor allem an Ihrer eigenen politischen Wahrnehmung interessiert!",
            "labelClose": "close" if lan=="en" else "ähnlich",
            "labelFar": "distant" if lan=="en" else "unterschiedlich",
            "helping_lines": "Show helping circles" if lan=="en" else "Hilfslinien anzeigen", 
        }
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.ps_placed += 1

        if player.ps_placed==C.NPS:
            # Find NR_P_CHECKS triples for which the distance self-p is >= 1.5 times the self-q; fill the rest with random triples self-p-q.
            positions = json.loads(getattr(player, "positions"))
            pos = {p["varname"]: [p["x"], p["y"]] for p in positions}
            p_points = [f"P{i}" for i in range(1, C.NPS+1)]
            distances = {p: distance(pos["self"], pos[p]) for p in p_points}
            valid_pairs = []
            for i, p1 in enumerate(p_points):
                for p2 in p_points[i+1:]:
                    d1 = distances[p1]
                    d2 = distances[p2]
                    if d1 >= 2 * d2 or d2 >= 2 * d1:
                        valid_pairs.append((p1, p2))
            while len(valid_pairs)<C.NR_P_CHECKS:
                p1, p2 = random.choice(list(combinations(p_points, 2)))
                if not (p1, p2) in valid_pairs and not (p2, p1) in valid_pairs:
                    valid_pairs.append((p1,p2))
            player.valid_p1p2self_triples = json.dumps(valid_pairs)
    
    @staticmethod
    def is_displayed(player):
        return player.consent and (player.ps_placed <= C.NPS)



class slide08a_PlausibilityCheck_Ps(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.consent
    
    @staticmethod
    def get_form_fields(player: Player):
        i = player.check
        return [f'check{i}', f'check{i}_explain']
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        valid_pairs = json.loads(getattr(player, "valid_p1p2self_triples"))
        pair = [getattr(player, f'check{player.check}_p1'),  getattr(player, f'check{player.check}_p2')]
        valid_pairs.remove(pair)
        player.valid_p1p2self_triples = json.dumps(valid_pairs)

        player.check += 1

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        questions = [C.QUS[i] for i in json.loads(player.question_sorting)]
        positions = json.loads(getattr(player, "positions"))
        pos = {p["varname"]: [p["x"], p["y"]] for p in positions}
        p_points = [f"P{i}" for i in range(1, C.NPS+1)]
        focal_point = "self" 
        #focal_point_label= "yourself"
        distances = {p: distance(pos[focal_point], pos[p]) for p in p_points}
        valid_pairs = json.loads(player.valid_p1p2self_triples)
        p1,p2 = random.choice(valid_pairs)

        positions = {dot["varname"]: dot for dot in positions if dot["varname"] in ["self", p1, p2]}

        dist_p1 = distances[p1]
        dist_p2 = distances[p2]
        significant = ((dist_p1 >= 1.5 * dist_p2) or (dist_p2 >= 1.5 * dist_p1))
        setattr(player, f'check{player.check}_p1', p1)
        setattr(player, f'check{player.check}_p2', p2)
        distantP = p1 if dist_p1 > dist_p2 else p2
        similarP = p2 if dist_p1 > dist_p2 else p1
        
        dot_descrs= {}
        for p in [p1, p2]:
            currP = f"{p}"
            currP_op = [C.P_OPS[currP][q] for q in questions]
            currP_op = ["" if str(op)=="nan" else op for op in currP_op]
            dot_descrs[currP] = "; ".join([
                f"{C.QUESTIONSHORTTEXT[lan][q]}: {op if lan=="en" else C.LIKERT5_transde[op]}"
                for q, op in zip(questions, currP_op)])
        
        dots = [{
            "varname": p["varname"],
            "name_disp": p["name_disp"],
            "x": p["x"]*300/500,
            "y": p["y"]*300/500,
            "dottype": p["dottype"],
            "descr": dot_descrs.get(p["varname"], "")}
            for pname, p in positions.items()]
        
        return {
            "nslide":3+len(C.LABELLED)+C.NCONTACTS+2+2,
            'lan_en':lan=="en",
            'p0_coords': pos[focal_point],
            'p1_coords': pos[p1],
            'p2_coords': pos[p2],
            'dots': dots,
            'p1': p1,
            'p2': p2,
            'ncheck': player.check,
            'nr_tot_checks': C.NR_P_CHECKS + C.NR_OTHER_CHECKS,
            'current_check': f'check{player.check}',
            'current_check_explain': f'check{player.check}_explain',
            'page_title': f"Direct comparion of political views – {player.check} of {C.NR_P_CHECKS + C.NR_OTHER_CHECKS}" if lan=="en" else f"Direktvergleich politischer Meinungen – {player.check} von {C.NR_P_CHECKS + C.NR_OTHER_CHECKS}" , 
            'instru1': "Below we show a subset of the political map you created." if lan=="en" else "Im Folgenden finden Sie einen kleinen Ausschnitt der von Ihnen erstellten politischen Landkarte.", 
            'relation': f"Your arrangement indicates that you perceive a <strong>{'much' if significant else ''} greater political distance to {distantP} than to {similarP}</strong>." if lan=="en" else f"Ihre Anordnung deutet darauf hin, dass Sie eine <strong>{'viel' if significant else ''} größere politische Distanz zu {distantP} empfinden als zu {similarP}</strong>.", 
            'question': "Is this correct?" if lan=="en" else "Ist das korrekt?", 
            'choices': dict(zip(C.OPTIONS_P_CHECKS, C.OPTIONS_P_CHECKS if lan=="en" else ["Nein", "Teils/teils", "Ja"])), 
            "explain_text": "If you believe this is incorrect, feel free to use the textbox below to explain why (optional):" if lan == "en" else "Falls Sie glauben, dass dies nicht korrekt ist, benutzen Sie gerne das untenstehende Textfeld, um zu beschreiben, warum (optional):"
            }


class slide08b_PlausibilityCheck_Pairs(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.consent
    
    @staticmethod
    def get_form_fields(player: Player):
        i = player.checkPair
        return [f'checkPair{i}']
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.checkPair += 1

    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        points = [
            ["contact2", C.LABELLED[2]],
            ["self", C.LABELLED[1]],
            ["contact1", C.LABELLED[2]],
            [C.LABELLED[2], C.LABELLED[1]],
            ["contact3", C.LABELLED[0]],
            ]
        p1, p2 = points[player.checkPair-1]
        setattr(player, f'checkPair{player.checkPair}_dot1', p1)
        setattr(player, f'checkPair{player.checkPair}_dot2', p2)

        p1label = (
                ("<strong>your contact "  if lan=="en" else "<strong>Ihr Kontakt ")+f"{getattr(player, p1)}</strong>" 
            )  if "contact" in p1 else (
                ("<strong>yourself</strong>" if lan=="en" else "<strong>Sie selbst</strong>")
            )  if p1=="self" else (
                (f"a typical <strong>{p1} voter</strong> " if lan=="en" else f"ein <strong>typischer Wähler oder eine Wählerin der {C.LABELLED_de[p1]}</strong>") if p1 in C.LABELLED else p1
            )
        p2label = (
                ("your contact " if lan=="en" else "Ihr Kontakt ")+f"{getattr(player, p2)}" 
            ) if "contact" in p2 else (
                ("yourself" if lan=="en" else "Sie selbst")  
            ) if p2=="self" else (
                (f"a typical <strong>{p2}</strong> voter" if lan=="en" else f"einen <strong>typischen Wähler oder eine Wählerin der {C.LABELLED_de[p2]}</strong>") if p2 in C.LABELLED else p2
            )
        return {
            "nslide":3+len(C.LABELLED)+C.NCONTACTS+2+3,
            'lan_en': lan=="en", 
            'p1': p1,
            'p2': p2,
            'current_check': f'checkPair{player.checkPair}',
            'page_title': f"Direct comparion of political views – {player.check+player.checkPair-1} of {C.NR_P_CHECKS + C.NR_OTHER_CHECKS}" if lan=="en" else f"Direktvergleich politischer Meinungen {player.check+player.checkPair-1} von {C.NR_P_CHECKS + C.NR_OTHER_CHECKS}", 
            'instru1': f"<p style='margin-bottom: 1.5em;'>Consider now the following two individuals:</p><p style='margin-bottom: 1.5em;'>{p1label} and {p2label}</p>" if lan=="en" else f"<p style='margin-bottom: 1.5em;'>Denken Sie nun an die beiden folgenden Personen:</p> <p style='margin-bottom: 1.5em;'>{p1label} und {p2label}</p>",
            'question': "<p style='margin-bottom: 1.5em;'>How different or similar do you consider their political views?</p>" if lan=="en" else "<p style='margin-bottom: 1.5em;'>Wie unterschiedlich oder ähnlich schätzen Sie die politischen Ansichten dieser beiden Personen ein?</p>",
            'choices': dict(zip(C.OPTIONS_OTHER_CHECKS, (C.OPTIONS_OTHER_CHECKS if lan=="en" else ["Sehr unterschiedlich", "Eher unterschiedlich",  "Weder noch", "Eher ähnlich", "Sehr ähnlich"]))),
        }


class slide09_Importance(Page):
    form_model = 'player'
    form_fields = ['topic_importance', 'importance_comments']
    @staticmethod
    def is_displayed(player: Player):
        return player.consent
     
    @staticmethod
    def vars_for_template(player):
        lan = player.language
        return {
            "nslide":3+len(C.LABELLED)+C.NCONTACTS+2+4,
            'lan_en':lan=="en",
            'topic_choices': dict(zip(C.CHOICES_TOPICS, C.CHOICES_TOPICS if lan == "en" else [qname for q,qname in C.QUESTIONNAMES["de"].items()]+["Andere Meinungen oder Themen", "Ich weiß nicht"])), 
            'page_title': "Key Topics Influencing Your Arrangement" if lan=="en" else "Wichtige Themen für Ihre Anordnung",
            'question': "Which topics influenced how you arranged the dots in the previous political mapping tasks? You may select multiple ones." if lan=="en" else " Welche Themen haben Ihre Anordnung der Punkte in dem vorherigen politischen Mapping beeinflusst? Sie können auch mehrere auswählen.",
            'explain_text': "If you would like, you can add further comments or explanations here (optional):" if lan == "en" else " Falls Sie möchten, können Sie hier weitere Anmerkungen oder Erklärungen hinzufügen (optional):"
        }
    @staticmethod
    def error_message(player, values):
        lan = player.language
        if values['topic_importance']:
            selected_choices = values['topic_importance'].split(',')
            valid_choices = C.CHOICES_TOPICS
            for choice in selected_choices:
                if choice.strip() not in valid_choices:
                    return "Invalid selection detected." if lan=="en" else "Ungültige Eingabe."
        return None


class slide10_Relationships(Page):
    form_model = "player"
    form_fields = [f"contact{n}_generalCloseness" for n in range(1, C.NCONTACTS+1)]

    @staticmethod
    def is_displayed(player: Player):
        return player.consent
    @staticmethod 
    def vars_for_template(player: Player):
        lan = player.language
        field_question_pairs = []
        fields =  [f"contact{n}_generalCloseness" for n in range(1, C.NCONTACTS+1)]

        for field, n in zip(fields, range(1, C.NCONTACTS+1)):
            choices = dict(zip(C.OPTIONS_CONTACTS_CLOSE, C.OPTIONS_CONTACTS_CLOSE if lan=="en" else ["Nicht besonders nah", "Etwas nah", "Sehr nah", "Extrem nah", "Keine Angabe"]))
            field_question_pairs.append({
                'field_name': field,
                'question_text': f"How close are you generally with <strong>{getattr(player, f'contact{n}')}</strong>?" if lan=="en" else f"Wie nah würden Sie Ihre Bezieung zu <strong>{getattr(player, f'contact{n}')}</strong> generell beschreiben?",
                'choices': choices,
            })
        return {
        "nslide":3+len(C.LABELLED)+C.NCONTACTS+2+5,
        'lan_en':lan=="en",
        'page_title': "<em>Social</em> Closeness to the Contacts" if lan=="en" else "<em>Soziale</em> Nähe zu den Kontakten", 
        "field_question_pairs": field_question_pairs,
        'qu_closeness': 'How close would you describe your relation in general with the three previously mentioned social contacts? This question is independent of whether you feel political similar or not; we aim to capture the emotional/social nature of your relationship with those contacts.' if lan=="en" else "Wie nah würden Sie Ihre Beziehungen generall zu den drei zuvor genannten sozialen Kontakten beschreiben? Diese Frage ist unabhängig davon ob Sie sich politisch ähnlich sind oder nicht; wir würden gerne Ihre emotionale/soziale Nähe zu diesen Personen erfassen.", 
        'disclaimer': "All your responses are linked to generic names <em>Contact 1</em>, <em>Contact 2</em>, etc. To protect privacy, we do <strong>not</strong> store the actual names or initials of your social contacts." if lan=="en" else "Alle Ihre Antworten werden generischen Namen <em>Kontakt 1</em>, <em>Kontakt 2</em> usw. zugeordnet. Zum Schutz der Privatsphäre speichern wir <strong>nicht</strong> die tatsächlichen Namen Ihrer sozialen Kontakte."
        }


class slide11_Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'political_interest', 'feel_closest_party', "party_comment", "how_polarised"]
    @staticmethod
    def is_displayed(player: Player):
        return player.consent
    @staticmethod 
    def vars_for_template(player: Player):
        lan = player.language
        return {
            "nslide":3+len(C.LABELLED)+C.NCONTACTS+2+6,
            'lan_en':lan=="en",
            'page_title': "Final questions about you" if lan=="en" else "Abschließende Fragen über Sie", 
            'qu_age': "How old are you?"if lan=="en" else "Wie alt sind Sie?",
            'qu_interest': 'How interested would you say you are in politics – are you...' if lan=="en" else "Wie sehr sind Sie persönlich an Politik interessiert? Sind Sie ...?", 
            'choices_interest': dict(zip(C.CHOICES_INTEREST, C.CHOICES_INTEREST if lan=="en" else ["Überhaupt nicht interessiert", "Kaum interessiert", "Ziemlich interessiert", "Sehr interesiert"])),
            'qu_identity': 'Do you feel closer to one of the political parties in Germany than the others? If so, which one?' if lan=="en" else "Gibt es eine bestimmte politische Partei in Deutschland, der Sie sich mehr verbunden fühlen als allen anderen Parteien? Welcher?", 
            'choices_identity': dict(zip(C.CHOICES_IDENTITY, C.CHOICES_IDENTITY if lan=="en" else ["CDU/CSU", "AfD", "SPD", "Bündnis 90/Die Grünen", "Die Linke", "BSW", "FDP", "Andere Partei", "Keiner Partei", "Keine Antwort"])),
            "qu_party_comment": "Would you like to add anything to the question above? (optional):" if lan=="en" else "Möchten Sie etwas dazu ergänzen zu dieser Frage? (optional)",
            'qu_polarization': "What do you think: How politically divided are the people in your country these days?" if lan=="en" else "Was denken Sie: Wie politisch gespalten sind die Menschen in Ihrem Land heutzutage?",
            'choices_pol':  dict(zip(C.CHOICES_POLARISED, C.CHOICES_POLARISED if lan=="en" else ["Überhaupt nicht gespalten", "Etwas gespalten", "Sehr gespalten", "Extrem gespalten"])) 
        }


class slideSuccess(Page):
    form_model = 'player'
    form_fields = ['completed']
    @staticmethod
    def vars_for_template(player: Player):
        return {"lan_en": player.language=="en", "nslide":3+len(C.LABELLED)+C.NCONTACTS+2+3}
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.completed = True
    def is_displayed(player: Player):
        return player.consent

class slideFail(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return ~player.consent or ~player.completed


    @staticmethod
    def vars_for_template(player: Player):
        return {"lan_en": player.language=="en"}




page_sequence = [slide01_Introduction,    slide02_Opinions, 
    slide03_Contacts] + \
    [slide04_PersonOpinion] * (C.NCONTACTS + len(C.LABELLED)) + \
    [slide05a_MapTest, slide05b_MapTestResult] * C.N_MAX_PRACTICE_RUNS +\
    [slide06_SPaM] +\
    [slide07_SPaM_personas] * C.NPS +\
    [slide08a_PlausibilityCheck_Ps] * C.NR_P_CHECKS +\
    [slide08b_PlausibilityCheck_Pairs] * C.NR_OTHER_CHECKS +\
    [slide09_Importance, slide10_Relationships, slide11_Demographics, 
     slideSuccess, slideFail]

#print("Total slides: ", len(page_sequence), 3+C.NCONTACTS+len(C.LABELLED)+2+1+1+1+1+4)