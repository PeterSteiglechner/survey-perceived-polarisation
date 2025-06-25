from otree.api import *
import json
import pandas as pd
import random
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
    LIKERT5_string_noNA_de = ['Stimme voll zu', 'Stimme eher zu', 'Teils/teils', 'Stimme eher nicht zu', 'Stimme gar nicht zu']
    LIKERT5_transde = dict(zip(LIKERT5_string_noNA, LIKERT5_string_noNA_de))
    LIKERT5_transde["NA"] = "NA"
    QUESTIONS = ["climate_concern", "gay_marriage", "rights_for_integration", "econ_inequality"]
    QUESTIONTEXT = {
        "en":
        dict(zip(QUESTIONS, [
        "I am very concerned about climate change.",
        "It is good that marriages between two women or two men are allowed.",
        "Only migrants who make an effort and integrate should be given the same rights as natives.",
        "The differences in income and wealth in Germany are too high.",
    ])), "de":
      dict(zip(QUESTIONS, [
        "Ich bin sehr besorgt über den Klimawandel.",
        "Es ist gut, dass Ehen zwischen zwei Frauen bzw. zwischen zwei Männern erlaubt sind.",
        "Nur Migranten, die sich anstrengen und integrieren, sollten die gleichen Rechte bekommen wie Einheimische.",
        "Die Einkommens- und Vermögensunterschiede in Deutschland sind zu groß.",
    ]))
    }
    QUESTIONSHORTTEXT =  {
        "en":
        dict(zip( QUESTIONS, [
         "extreme concern about climate change", 
         "support same-sex marriage",
         "equal rights only for migrants who integrate",
         "economic differences too high"
    ])), 
        "de":
                dict(zip( QUESTIONS, [
         "Extreme Besorgnis über Klimawandel", 
         "Unterstützung für gleichgeschlechtliche Ehe",
         "Gleiche Rechte nur für Migranten/-innen, die sich integrieren",
         "Ökonomische Unterschiede sind zu groß"
    ])),}

    QUESTIONNAMES = {
        "en":
        dict(zip( QUESTIONS, [
        "Opinion about climate change.", 
        "Opinion about same-sex marriage.", 
        "Opinion about equal rights for migrants only when they integrate.",
        "Opinion about economic inequality.",
        ])), 
        "de":
                dict(zip( QUESTIONS, [
        "Die Meinung der Person zum Klimawandel.", 
        "Die Meinung der Person zu gleichgeschlechtlicher Ehe.", 
        "Die Meinung der Person ob die Rechte von Migrant/-innen von deren Integration abhängen.",
        "Die Meinung der Person zu ökonomischer Ungleichheit.",
        ]))}
    
    NCONTACTS = 3

    LABELLED = ["Green voter", "AfD voter", "FDP voter"]
    LABELLED_de = dict(zip(LABELLED, ["Grünen Wähler", "AfD Wähler", "FDP Wähler"]))
    LABELLEDCOLORS = dict(zip(LABELLED, ["#46962b", "#009ee0", "#ffed00"]))

    PERSONAS = pd.read_csv("_static/personas.csv")[QUESTIONS]
    P_OPS =  {f"P{n+1}": row.to_dict()  for n, row in PERSONAS.iterrows()}
    NPS = len(P_OPS.keys())

    NR_P_CHECKS = 4
    OPTIONS_P_CHECKS = ['No','Somewhat','Yes']
    NR_OTHER_CHECKS = 5 
    OPTIONS_OTHER_CHECKS = ["Very different", "Quite different",  "Neither", "Quite similar", "Very similar"]

    CHOICES_TOPICS= [qname+"." for q,qname in QUESTIONNAMES["en"].items()]+["Different opinion(s) or topic(s).", "I don't know."]

    CHOICES_INTEREST = ["Not at all interested.", "Hardly interested.", "Quite interested.", "Very interested."]

    CHOICES_IDENTITY = ["CDU/CSU", "AfD", "SPD", "Green Party", "Left Party", "BSW", "FDP", "Other party", "No party", "Refuse to say/No answer"]

    CHOICES_POLARISED = ["Not at all divided.", "Somewhat divided.", "Very divided.", "Extremely divided."]

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
    return  models.LongStringField(label=label, blank=False) 

class Player(BasePlayer):

    consent = models.BooleanField(blank=False)

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
    # check1_p1 =  models.LongStringField(blank=True)
    # check1_p2 =  models.LongStringField(blank=True)
    # check2_p1 =  models.LongStringField(blank=True)
    # check2_p2 =  models.LongStringField(blank=True)
    # check3_p1 =  models.LongStringField(blank=True)
    # check3_p2 =  models.LongStringField(blank=True)
    # check4_p1 =  models.LongStringField(blank=True)
    # check4_p2 =  models.LongStringField(blank=True)
    # check1 = models.StringField(choices=C.OPTIONS_P_CHECKS, label="", widget=widgets.RadioSelect,blank=False)
    # check1_explain = models.LongStringField(label="",blank=True)
    # check2 = models.StringField(choices=C.OPTIONS_P_CHECKS, label="", widget=widgets.RadioSelect,blank=False)
    # check2_explain = models.LongStringField(label="",blank=True)
    # check3 = models.StringField(choices=C.OPTIONS_P_CHECKS,label="", widget=widgets.RadioSelect,blank=False)
    # check3_explain = models.LongStringField(label="",blank=True)
    # check4 = models.StringField(choices=C.OPTIONS_P_CHECKS,label="", widget=widgets.RadioSelect,blank=False)
    # check4_explain = models.LongStringField(label="",blank=True)
    
    # pairwise
    checkPair = models.IntegerField(initial=1) 
    # checkPair1_dot1 =  models.LongStringField(blank=True)
    # checkPair1_dot2 =  models.LongStringField(blank=True)
    # checkPair2_dot1 =  models.LongStringField(blank=True)
    # checkPair2_dot2 =  models.LongStringField(blank=True)
    # checkPair3_dot1 =  models.LongStringField(blank=True)
    # checkPair3_dot2 =  models.LongStringField(blank=True)
    # checkPair4_dot1 =  models.LongStringField(blank=True)
    # checkPair4_dot2 =  models.LongStringField(blank=True)
    # checkPair5_dot1 =  models.LongStringField(blank=True)
    # checkPair5_dot2 =  models.LongStringField(blank=True)
    # checkPair1 = models.StringField(choices=C.OPTIONS_OTHER_CHECKS,label="", widget=widgets.RadioSelect,blank=False)
    # checkPair2 = models.StringField(choices=C.OPTIONS_OTHER_CHECKS,label="", widget=widgets.RadioSelect,blank=False)
    # checkPair3 = models.StringField(choices=C.OPTIONS_OTHER_CHECKS,label="", widget=widgets.RadioSelect,blank=False)
    # checkPair4 = models.StringField(choices=C.OPTIONS_OTHER_CHECKS,label="", widget=widgets.RadioSelect,blank=False)
    # checkPair5 = models.StringField(choices=C.OPTIONS_OTHER_CHECKS,label="", widget=widgets.RadioSelect,blank=False)

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
for q in C.QUESTIONS:
    setattr(Player, f"own_{q}", make_field(''))  

#################################
#####  CONTACTS & CONTACTS' POLITICAL OPINIONS   #####
#################################
for n in range(1,C.NCONTACTS+1):
    setattr(Player, f"contact{n}", define_contact(f"Contact {n}: ", n))
    for q in C.QUESTIONS:
        setattr(Player, f"contact{n}_{q}", make_field(''))

#################################
#####  LABELLED INDIVIDS' POLITICAL OPINIONS   #####
#################################
for name in C.LABELLED:
    for q in C.QUESTIONS:
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
    form_fields = [f"own_{q}" for q in C.QUESTIONS]
    @staticmethod
    def is_displayed(player: Player):
        return player.consent
    @staticmethod
    def vars_for_template(player: Player): 
        lan = player.language
        fields =  [f"own_{q}" for q in C.QUESTIONS]
        questions = [C.QUESTIONTEXT[player.language][q] for q in C.QUESTIONS]
        field_question_pairs = []
        for field, question in zip(fields, questions):
            choices = dict(zip(C.LIKERT5_string_noNA[::-1], (C.LIKERT5_string_noNA[::-1] if lan=="en" else C.LIKERT5_string_noNA_de[::-1])))  
            field_question_pairs.append({
                'field_name': field,
                'question_text': question,
                'choices': choices,
            })
        return {
            'field_question_pairs': field_question_pairs, 
            'page_title': 'Your political views' if player.language == 'en' else 'Ihre politischen Ansichten',
            'instruction_text': '<p style="margin-bottom: 0.5em;" >At the beginning of this survey, we are interested in your own political opinions. </p><p style="margin-bottom: 0.5em;" >Please indicate to what extent you agree or disagree with the following statements. There are no right or wrong answers; we are most interested in which response option is most aligned with your views.</p>' if player.language == 'en' else '<p style="margin-bottom: 0.5em;">Zum Start dieser Umfrage interessieren wir uns für Ihre politischen Ansichten.</p><p style="margin-bottom: 0.5em;" > Bitte geben Sie an, inwieweit Sie den folgenden Aussagen zustimmen oder nicht zustimmen. Es gibt keine richtigen oder falschen Antworten; wir interessieren uns dafür welche Antwortmöglichkeiten am Ehesten ihren Ansichten entspricht.</p>',
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
            "ncontacts": C.NCONTACTS,
            "contact_fields": contact_fields,
            'page_title': "Social Contacts" if lan=="en" else "Soziale Kontakte", 
            'instruction_text': f"Think about <strong>{C.NCONTACTS} social contacts</strong> that you know well. This can include friends, family members, colleagues, .... Please write down their names or initials so that you are later able to recognise them (we will not use that information)." if lan=="en" else f"Denken Sie an <strong>{C.NCONTACTS} soziale Kontakte</strong>, die Sie gut kennen. Das können Freunde, Freundinnen, Familienmitglieder, Kollegen, etc. sein. Bitte notieren Sie die Namen oder Initialen dieser Kontakte in den Feldern unten, damit Sie sie später wiedererkennen (wir werden diese Informationen nicht verwenden).", 
              }
    @staticmethod
    def error_message(player: Player, values):
        contacts = [v.strip() for v in values.values() if v.strip()]
        if len(contacts) < C.NCONTACTS:
            return "Please fill in all contact fields." if player.language=="en" else "Bitte füllen Sie alle Felder aus."
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
            displName1 = f"ihren Kontakt <strong>{name}</strong>"
            displName2 = f"<strong>{name}</strong>"
            displName3 = f"<strong>{name}</strong>"
            color = "#ff9600"  # contact color
        else:  # mode == 'labelledPerson'
            idx = player.evaluated_labelledPerson
            name = C.LABELLED[idx]
            prefix = f"{name.replace(" ","")}_"
            displName = f"a typical {name}" if lan=="en" else f"{C.LABELLED_de[name]}"
            color = C.LABELLEDCOLORS[name]
            if lan=="de":
                displName1 = f"eine <strong>typische {C.LABELLED_de[name]}in</strong>/<strong>typischen {C.LABELLED_de[name]}</strong>"
                displName2 = "diese Person" 
                displName3 = f"<strong>{C.LABELLED_de[name]}/-in</strong>"
        fields = [f"{prefix}{q}" for q in C.QUESTIONS]
        questions = [C.QUESTIONTEXT[lan][q] for q in C.QUESTIONS]
        field_question_pairs = []
        for field, question in zip(fields, questions):
            choices = dict(zip(C.LIKERT5_string_noNA[::-1], (C.LIKERT5_string_noNA[::-1] if lan=="en" else C.LIKERT5_string_noNA_de[::-1])))   # convert list of tuples to dict
            field_question_pairs.append({
                'field_name': field,
                'question_text': question,
                'choices': choices,
            })
        return {
            "name": name,
            "color": color,
            "fields": fields,
            "questions": questions,
            "field_question_pairs": field_question_pairs,            
            'page_title': 'Political Opinions of Others' if lan == 'en' else 'Politischen Meinungen von Anderen Menschen',
            'instruction_text': f'Thinking about <strong>{displName}</strong>, how do you think <strong>{displName}</strong> would respond to those same political questions?' if lan == 'en' else f'Denken Sie nun an {displName1}. Wie würde {displName2} die selben politischen Fragen beantworten?',
            'table_head':f"<strong>{displName}</strong>'s responses" if lan =="en" else f"Antworten: {displName3}"
        }

    @staticmethod
    def get_form_fields(player: Player):
        if player.which_contact_type == 'contact':
            prefix = f"contact{player.current_contact}_"
        else:
            name = C.LABELLED[player.evaluated_labelledPerson]
            prefix = f"{name.replace(" ", "")}_"
        return [f"{prefix}{q}" for q in C.QUESTIONS]

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
    
    @staticmethod
    def is_displayed(player):
        return player.consent and (not player.isTrainingPassed)
    
    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language
        return {
    'page_title': "Political Mapping – Practice" if lan=="en" else "Politisches Mapping – Training",
    'lan':lan,
    'instruction_text1': 
    "In the following part, we will ask you to place people on a political map based on how distant or similar their political views are. To prepare for the main task, we will begin with a short <strong>practice round</strong>." if lan=="en" else "Im folgenden Teil werden wir Sie bitten, Personen auf einer politischen Landkarte einzuordnen, je nachdem, wie ähnlich oder unterschiedlich die politischen Ansichten dieser Personen sind. Zur Vorbereitung auf die eigentliche Aufgabe beginnen wir mit einer kurzen <strong>Übungsrunde</strong>.", 
    'instruction_text2': "Imagine you, a friend, a co-worker, and your sister are placed in a room (represented by the rectangle below)." if lan=="en" else "Stellen Sie sich vor, dass Sie, ein Freund, eine Arbeitskollegin und Ihre Schwester sich in einem Raum befinden (das Rechteck unten).",
    'instruction_text3': "<p>Your task is to arrange everyone's position in the room based on their political views:</p><ul><li><strong>Place individuals with similar political views close to each other.</strong></li><li><strong>Place individuals with differing political views farther apart.</strong></li></ul><p>Use the space within the rectangle to show these relationships.</p>" if lan=="en" else ""
    "<p>Ihre Aufgabe ist es, die Positionen aller Personen im Raum basierend auf ihren politischen Ansichten anzuordnen:</p><ul><li><strong>Platzieren Sie Personen mit ähnlichen politischen Ansichten nahe beieinander.</strong></li><li><strong>Platzieren Sie Personen mit unterschiedlichen politischen Ansichten weiter auseinander.</strong></li></ul><p>Nutzen Sie den Raum im Rechteck, um diese Beziehungen darzustellen.</p>",
    'detailed_instructions': "<h4>Step-by-Step Instructions</h4><p style='margin-bottom: 0.5em; color: black;'>You will start with several points on the right side. Drag these one by one into the rectangle as described in the following instructions:</p><ol><li>First, place the point <em>Me</em> somewhere inside the rectangle. This point represents your own political views.</li><li>Next, place the point <em>Friend</em> near you. The friend has similar views to yours.</li><li>Then add your <em>Co-worker</em>. Since you often disagree with them, place the point <em>Co-worker</em> farther away from <em>Me</em>.</li><li>You also believe that your co-worker's views are even more different from your friend's than from yours. Therefore, place the point so that <em>Co-worker</em> is farther from <em>Friend</em> than from <em>Me</em>.</li><li>Now add your <em>Sister</em>. You feel that your sister thinks quite differently politically than you do. So place the point <em>Sister</em> far away from the point <em>Me</em>.</li><li>You think your sister's political views align somewhat more with your friend and co-worker than with yourself. Therefore, place the point <em>Sister</em> closer to the points <em>Co-worker</em> and <em>Friend</em> than to the point <em>Me</em>.</li></ol>" if lan=="en" else
    "<h4>Schritt-für-Schritt Anleitung</h4><p style='margin-bottom: 0.5em; color: black;'>Sie beginnen mit mehreren Punkten auf der rechten Seite. Ziehen Sie diese nacheinander in das Rechteck, wie in der folgenden Anleitung beschrieben:</p><ol><li>Zunächst platzieren Sie den Punkt <em>Ich</em> irgendwo im Rechteck. Dieser Punkt steht für Ihre eigenen politischen Ansichten.</li><li>Nun platzieren Sie den Punkt <em>Freund</em> in Ihrer Nähe. Der Freund hat ähnliche Ansichten wie Sie.</li> <li>Als nächstes fügen Sie Ihre <em>Kollegin</em> hinzu. Da sie oft anderer Meinung sind als sie, platzieren Sie den Punkt <em>Kollegin</em> weiter entfernt von <em>Ich</em>.</li> <li>Sie glauben außerdem, dass die Ansichten Ihrer Kollegin dem Freund noch fremder sind als Ihnen. Platzieren Sie daher den Punkt so, dass <em>Kollegin</em> weiter von <em>Freund</em> entfernt ist als von <em>Ich</em>.</li> <li>Fügen Sie nun Ihre <em>Schwester</em> hinzu. Sie haben das Gefühl, dass Ihre Schwester politisch ganz anders denkt als Sie. Platzieren Sie also den Punkt <em>Schwester</em> weit weg von dem Punkt <em>Ich</em>.</li> <li>Sie denken, dass Ihre Schwester politisch etwas mehr mit Ihrem Freund und Ihrer Kollegin übereinstimmt als mit Ihnen selbst. Platzieren Sie also den Punkt <em>Schwester</em> näher bei den Punkten <em>Kollegin</em> und <em>Freund</em> als bei dem Punkt <em>Ich</em>.</li> </ol>", 
    'all_dots_instr': "All dots must be within the square boundary to proceed. You can re-position any dot at any time until you are satisfied with the arrangement." if lan=="en" else "Um fortzufahren müssen alle Punkte im Rechteck platziert werden. Sie können jeden Punkt verschieben bis Sie mit der Anordnung zufrieden sind."
  }
    

class slide05b_MapTestResult(Page):
    @staticmethod
    def vars_for_template(player: Player):
        lan = player.language

        player.attemptPractice += 1
        pos = json.loads(player.positionsTest)
        pos = {p["varname"]: [p["x"], p["y"]] for p in pos}
        #calculate distances
        dF = distance(pos["self"], pos["friend"])
        dC = distance(pos["self"], pos["co-worker"])
        dS = distance(pos["self"], pos["sister"])
        dFS = distance(pos["friend"], pos["sister"])
        dFC = distance(pos["friend"], pos["co-worker"])
        dCS = distance(pos["co-worker"], pos["sister"])
        # check conditions
        player.isTrainingCondFvC = bool(dF<dC)  # Rule 2/3
        player.isTrainingCondSelfvFC = bool(dFC>dC)  # Rule 4
        player.isTrainingCondSvF = bool(dS>dF) # Rule 5
        player.isTrainingCondSvFC = bool((dFS<dS) and (dCS<dS)) # Rule 6.
        isTrainingPassed = player.isTrainingCondFvC & player.isTrainingCondSelfvFC & player.isTrainingCondSvFC & player.isTrainingCondSvF
        player.isTrainingPassed = isTrainingPassed

        errors = ""
        if lan=="en":
            errors += r"- The distance between 'Self' and 'Co-worker' should be larger than the distance between 'Self' and 'Friend' (instructions 2/3). <br>" if player.isTrainingCondFvC==0 else ""
            errors += r"- The distance between 'Friend' and 'Co-worker' should be larger than the distance between 'Self' and 'Co-worker' (instruction 4). <br>" if player.isTrainingCondSelfvFC==0 else ""
            errors += r"- The distance between 'Self' and 'Sister' should be larger than the distance between 'Self' and 'Friend' (instruction 5). <br>" if player.isTrainingCondSvF==0 else ""
            errors += r"- The distance between 'Self' and 'Sister' should be larger than the distances between 'Friend' and 'Sister' and between 'Co-worker' and 'Sister' (instruction 6). <br>" if player.isTrainingCondSvFC==0 else ""
        else:
            errors += r"- Die Distanz zwischen 'Ich' und 'Kollegin' sollte größer sein als die Distanz zwischen 'Ich' und 'Freund' (Anweisungen 2/3). <br>" if player.isTrainingCondFvC == 0 else ""
            errors += r"- Die Distanz zwischen 'Freund' und 'Kollegin' sollte größer sein als die Distanz zwischen 'Ich' und 'Kollegin' (Anweisung 4). <br>" if player.isTrainingCondSelfvFC == 0 else ""
            errors += r"- Die Distanz zwischen 'Ich' und 'Schwester' sollte größer sein als die Distanz zwischen 'Ich' und 'Freund' (Anweisung 5). <br>" if player.isTrainingCondSvF == 0 else ""
            errors += r"- Die Distanz zwischen 'Ich' und 'Schwester' sollte größer sein als die Distanzen zwischen 'Freund' und 'Schwester' sowie 'Kollegin' und 'Schwester' (Anweisung 6). <br>" if player.isTrainingCondSvFC == 0 else ""

        return {
            "img_source": f"correctTraining_{lan}.png",
            "passed": player.isTrainingPassed, 
            "button_msg": ("Continue" if player.isTrainingPassed else ("Continue Anyway" if player.attemptPractice == C.N_MAX_PRACTICE_RUNS else "Repeat Training")) if lan=="en" else  ("Weiter" if player.isTrainingPassed else ("Trotzdem weiter" if player.attemptPractice == C.N_MAX_PRACTICE_RUNS else "Wiederhole Training")),
            "attempt_msg": f"Attempt {player.attemptPractice} of {C.N_MAX_PRACTICE_RUNS}" if lan=="en" else f"Versuch {player.attemptPractice} von {C.N_MAX_PRACTICE_RUNS}",
            "page_title": "Political Mapping – Practice – Results" if lan=="en" else "Politisches Mapping – Training – Ergebnis", 
            'success_msg': "<strong>Well done!</strong> Your arrangement fulfills all criteria." if lan=="en" else "<strong>Gut gemacht!</strong> Ihre Anordnung der Punkte erfüllt alle Kriterien.",
            'error_msg': f"<strong>Your arrangement does not meet all parts of the instructions:</strong></p><p style='margin: 0 0 1em 0; white-space: pre-line;'>{errors}</p><p style='margin: 0;'>Please repeat the training and try to arrange the dots so that all criteria are fulfilled. Below is one possible arrangement that meets all the criteria:</p>" if lan=="en" else f"<strong>Ihre Anordnung erfüllt nicht alle Teile der Anleitung:</strong></p><p style=‚margin: 0 0 1em 0; white-space: pre-line;‘>{errors}</p><p style=‚margin: 0;‘>Bitte wiederholen Sie das Training und versuchen Sie, die Punkte so anzuordnen, dass alle Teile der Anleitung erfüllt sind. Nachstehend sehen Sie eine mögliche Anordnung, die alle Kriterien erfüllt:</p>"
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
        displ_names =  ["Self" if lan=="en" else "Ich"]+[getattr(player, f"contact{f}") for f in range(1,C.NCONTACTS+1)]+[f"{v if lan=="en" else C.LABELLED_de[v]+'/-in'}" for v in C.LABELLED]
        types = ["self"]+["contact"]*C.NCONTACTS + ["labelledPerson"]*len(C.LABELLED)
        varnames = ["self"]+[f"contact{f}" for f in range(1,C.NCONTACTS+1)]+[f"{v}" for v in C.LABELLED] 
        init_dots = [{"dottype": dottype, "varname": varname, 
        "name_disp": name, "x": 530, "y": 40 + i * 60, "descr": ""} for i, (dottype, varname, name) in enumerate(zip(types, varnames, displ_names))]
        return {
            "dots":init_dots,
            "page_title": "Political Mapping – Part 1" if lan=="en" else "Politisches Mapping – Teil 1",
            "instru1": "We now continue to the main task in this survey." if lan=="en" else "Wir beginnen nun mit dem Hauptteil dieser Umfrage.",
            "instruRoom": "Imagine you, your three social contacts, a typical Green voter, a typical FDP voter, and a typical AfD voter are in a room (represented by the rectangle below)." if lan=="en" else "Stellen Sie sich vor, dass Sie sich zusammen mit Ihren drei Kontakten und mit jeweils einem typischen Wähler oder einer typischen Wählerin der Grünen, der AfD und der FDP in einem Raum befinden (repräsentiert durch das Rechteck unten).",
            'instru_main': "<p style='margin-bottom: 0.5em;'>Arrange everyone's position in the room based on their political views:</p><ul style='margin-bottom: 0.5em;'><li><strong>Place individuals with similar political views</strong> on questions regarding economic inequality, migration, minorities, and climate change <strong>close to each other.</strong></li><li><strong>Place individuals with differing political views on these topics farther apart.</strong></li></ul><p style='margin-bottom: 0.5em;'>Use the space within the rectangle to show these relationships.</p>" if lan=="en" else "<p style='margin-bottom: 0.5em;'>Ordnen Sie die Positionen aller Personen im Raum basierend auf ihren politischen Ansichten an:</p><ul style='margin-bottom: 0.5em;'><li><strong>Platzieren Sie Personen mit ähnlichen politischen Ansichten</strong> zu den Themen wirtschaftliche Ungleichheit, Migration, Minderheiten und Klimawandel <strong>nah beieinander.</strong></li>  <li><strong>Platzieren Sie Personen mit unterschiedlichen politischen Ansichten zu diesen Themen weiter auseinander.</strong></li></ul><p style='margin-bottom: 0.5em;'>Nutzen Sie den Raum im Rechteck, um diese Beziehungen darzustellen.</p>", 
            'all_dots_instr': "All dots must be within the square boundary to proceed. You can re-position any dot at any time until you are satisfied with the arrangement." if lan=="en" else "Um fortzufahren müssen alle Punkte im Rechteck platziert werden. Sie können jeden Punkt verschieben bis Sie mit der Anordnung zufrieden sind."
}

class slide07_SPaM_personas(Page):
    form_model = 'player'
    form_fields = ['positions']  
    
    @staticmethod
    def vars_for_template(player:Player):
        lan = player.language
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
        P_op = [op for q, op in C.P_OPS[P].items()]
        pos = json.loads(player.positions) if player.positions else []

        P_text_short = "; ".join([
            f"{C.QUESTIONSHORTTEXT[lan][q]}: {P_op[i] if lan=='en' else C.LIKERT5_transde[P_op[i]]}"
            for i, q in enumerate(C.QUESTIONS)
        ])

        # Write dot descriptions of Self, Contacts, Labelled, and past Personas
        dot_descrs = {"self": format_ops(get_ops("own_", C.QUESTIONS), lan)}
        for f in range(1, C.NCONTACTS + 1):
            dot_descrs[f"contact{f}"] = format_ops(get_ops(f"contact{f}_", C.QUESTIONS), lan)
        for v in C.LABELLED:
            dot_descrs[f"{v}"] = format_ops(get_ops(f"{v.replace(" ", "")}_", C.QUESTIONS), lan)
        for p in range(1, player.ps_placed + 1):
            currP = f"P{p}"
            currP_op = [op for q, op in C.P_OPS[currP].items()]
            dot_descrs[currP] = "; ".join([
                f"{C.QUESTIONSHORTTEXT[lan][q]}: {op if lan=="en" else C.LIKERT5_transde[op]}"
                for q, op in zip(C.QUESTIONS, currP_op)
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
        init_dots.append({"varname": P, "name_disp": P, "x": 530, "y": 300, "dottype": "P", "descr": P_text_short})

        return {
            "P": P,
            "P_text_short": P_text_short,
            "dots": init_dots, 
            "img_source": f"{P}_op_{lan}.png",
            "n_ps": C.NPS,
            "ps_placed": player.ps_placed+1,
            "page_title": "Political Mapping – Part 2" if lan=="en" else "Politisches Mapping – Teil 2", 
            "heading": f"Person {player.ps_placed+1} of { C.NPS} " if lan=="en" else f"Person {player.ps_placed+1} von {C.NPS}",
            'instru_main': "<p style='margin-bottom: 0.5em; color: grey;'>Arrange everyone's position in the room based on their political views:</p><ul style='margin-bottom: 0.5em; color: grey;'><li><strong>Place individuals with similar political views</strong> on questions regarding economic inequality, migration, minorities, and climate change <strong>close to each other.</strong></li><li><strong>Place individuals with differing political views on these topics farther apart.</strong></li></ul><p style='margin-bottom: 0.5em; color: grey;'>Use the space within the rectangle to show these relationships.</p>" if lan=="en" else
            "<p style='margin-bottom: 0.5em; color: grey;'>Ordnen Sie die Positionen aller Personen im Raum basierend auf ihren politischen Ansichten an:</p><ul style='margin-bottom: 0.5em; color: grey;'><li><strong>Platzieren Sie Personen mit ähnlichen politischen Ansichten</strong> zu den Themen wirtschaftliche Ungleichheit, Migration, Minderheiten und Klimawandel <strong>nah beieinander.</strong></li><li><strong>Platzieren Sie Personen mit unterschiedlichen politischen Ansichten zu diesen Themen weiter auseinander.</strong></li></ul><p style='margin-bottom: 0.5em; color: grey;'>Nutzen Sie den Raum im Rechteck, um diese Beziehungen darzustellen.</p>", 
            'instru_p1': f"Next, consider the individual <strong>{P}</strong> and place the red dot representing the political views of {P} in the rectangle according to their political similarity or distance relative to the other individuals." if lan=="en" else f"Betrachten Sie nun die Person <strong>{P}</strong> und platzieren Sie den roten Punkt, der <strong>{P}</strong>s Ansichten repräsentiert, im Rechteck. Achten Sie darauf, ihn entsprechend der politischen Nähe oder Distanz zu den anderen Personen zu positionieren.",
            'instru_p2': f"To get a flavour of {P}'s political views, here are <strong>{P}</strong>'s responses to the questions from the previous slides:" if lan=="en" else f"Um einen Eindruck von den politischen Ansichten von {P} zu bekommen, finden Sie hier <strong>{P}</strong>s Antworten auf die Fragen der vorherigen Folien:",
            'instru_click': "You can click on a dot to view detailed information about the individual's opinion." if lan=="en" else "Sie können auf einen Punkt klicken um detaillierte Informationen zu den Meinungen der Person zu sehen.",
            'all_dots_instr': "All dots must be within the square boundary to proceed. You can re-position any dot at any time until you are satisfied with the arrangement." if lan=="en" else "Um fortzufahren müssen alle Punkte im Rechteck platziert werden. Sie können jeden Punkt verschieben bis Sie mit der Anordnung zufrieden sind."
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
                    if d1 >= 1.5 * d2 or d2 >= 1.5 * d1:
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
            currP_op = [op for q, op in C.P_OPS[currP].items()]
            dot_descrs[currP] = "; ".join([
                f"{C.QUESTIONSHORTTEXT[lan][q]}: {op if lan=="en" else C.LIKERT5_transde[op]}"
                for q, op in zip(C.QUESTIONS, currP_op)])
        
        dots = [{
            "varname": p["varname"],
            "name_disp": p["name_disp"],
            "x": p["x"],
            "y": p["y"],
            "dottype": p["dottype"],
            "descr": dot_descrs.get(p["varname"], "")}
            for pname, p in positions.items()]
        
        return {
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
            'choices': dict(zip(["No", "Somewhat", "Yes"], ["No", "Somewhat", "Yes"] if lan=="en" else ["Nein", "Teils/teils", "Ja"])), 
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

        p1label = ("your contact "  if lan=="en" else "Ihr Kontakt ")+f"{getattr(player, p1)}" if "contact" in p1 else (("yourself" if lan=="en" else "Sie selbst")  if p1=="self" else (f"a typical {p1}" if lan=="en" else f"ein typischer {C.LABELLED_de[p1]}/eine typische {C.LABELLED_de[p1]}in" if p1 in C.LABELLED else p1))
        p2label = ("your contact "  if lan=="en" else "Ihr Kontakt ")+f"{getattr(player, p2)}" if "contact" in p2 else (("yourself" if lan=="en" else "Sie selbst")  if p2=="self" else (f"a typical {p2}" if lan=="en" else f"ein typischer {C.LABELLED_de[p2]}/eine typische {C.LABELLED_de[p2]}in" if p2 in C.LABELLED else p2))
        return {
            'p1': p1,
            'p2': p2,
            'current_check': f'checkPair{player.checkPair}',
            'page_title': f"Direct comparion of political views – {player.check+player.checkPair-1} of {C.NR_P_CHECKS + C.NR_OTHER_CHECKS}" if lan=="en" else f"Direktvergleich politischer Meinungen {player.check+player.checkPair-1} von {C.NR_P_CHECKS + C.NR_OTHER_CHECKS}", 
            'instru1': f"<p style='margin-bottom: 1.5em;'>Consider now the following two individuals:</p><p style='margin-bottom: 1.5em;'><strong>{p1label}</strong> and <strong>{p2label}</strong></p>" if lan=="en" else f"<p style='margin-bottom: 1.5em;'>Denken Sie nun an die beiden folgenden Personen:</p> <p style='margin-bottom: 1.5em;'><strong>{p1label}</strong> und <strong>{p2label}</strong></p>",
            'question': "<p style='margin-bottom: 1.5em;'>How different or similar do you consider their political views?</p>" if lan=="en" else "<p style='margin-bottom: 1.5em;'>Wie unterschiedlich oder ähnlich schätzen Sie die politischen Ansichten dieser beiden Personen ein?</p>",
            'choices': dict(zip(C.OPTIONS_OTHER_CHECKS, (C.OPTIONS_OTHER_CHECKS if lan=="en" else ["Sehr unterschiedlich.", "Eher unterschiedlich.",  "Weder noch.", "Eher ähnlich.", "Sehr ähnlich."]))),
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
            'topic_choices': dict(zip(C.CHOICES_TOPICS, C.CHOICES_TOPICS if lan == "en" else [qname+"." for q,qname in C.QUESTIONNAMES["de"].items()]+["Andere Meinungen oder Themen.", "Ich weiß nicht."])), 
            'page_title': "Key Topics Influencing Your Arrangement" if lan=="en" else "Wichtige Themen für Ihre Anordnung",
            'question': "Which topics influenced how you arranged the dots in the previous political mapping tasks? Please select one or more that apply." if lan=="en" else " Welche Themen haben Ihre Anordnung der Punkte in dem vorherigen politischen Mapping beeinflusst? Bitte wählen Sie ein oder mehrere aus.",
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



class slide10_Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'political_interest', 'feel_closest_party', "how_polarised"]
    @staticmethod
    def is_displayed(player: Player):
        return player.consent
    @staticmethod 
    def vars_for_template(player: Player):
        lan = player.language
        return {
            'page_title': "Final questions about you" if lan=="en" else "Abschließende Fragen über Sie", 
            'qu_age': "How old are you?"if lan=="en" else "Wie alt sind Sie?",
            'qu_interest': 'How interested would you say you are in politics – are you...' if lan=="en" else "Wie sehr sind Sie persönlich an Politik interessiert? Sind Sie ...?", 
            'choices_interest': dict(zip(C.CHOICES_INTEREST, C.CHOICES_INTEREST if lan=="en" else ["Überhaupt nicht interessiert.", "Kaum interessiert.", "Ziemlich interessiert.", "Sehr interesiert."])),
            'qu_identity': 'Do you feel closer to one of the political parties in Germany than the others? If so, which one?' if lan=="en" else "Gibt es eine bestimmte politische Partei in Deutschland, der Sie sich mehr verbunden fühlen als allen anderen Parteien? Welcher?", 
            'choices_identity': dict(zip(C.CHOICES_IDENTITY, C.CHOICES_IDENTITY if lan=="en" else ["CDU/CSU", "AfD", "SPD", "Bündnis 90/Die Grünen", "Die Linke", "BSW", "FDP", "Andere Partei", "Keiner Partei", "Keine Antwort"])),
            'qu_polarization': "What do you think: How politically divided are the people in your country these days?" if lan=="en" else "Was denken Sie: Wie politisch gespalten sind die Menschen in Ihrem Land heutzutage?",
            'choices_pol':  dict(zip(C.CHOICES_POLARISED, C.CHOICES_POLARISED if lan=="en" else ["Überhaupt nicht gespalten.", "Etwas gespalten.", "Sehr gespalten.", "Extrem gespalten."])) 
        }


class slide11_Results(Page):
    pass




page_sequence = [slide01_Introduction,    slide02_Opinions, 
    slide03_Contacts] + \
    [slide04_PersonOpinion] * (C.NCONTACTS + len(C.LABELLED)) + \
    [slide05a_MapTest, slide05b_MapTestResult] * C.N_MAX_PRACTICE_RUNS +\
    [slide06_SPaM] +\
    [slide07_SPaM_personas] * C.NPS +\
    [slide08a_PlausibilityCheck_Ps] * C.NR_P_CHECKS +\
    [slide08b_PlausibilityCheck_Pairs] * C.NR_OTHER_CHECKS +\
    [slide09_Importance, slide10_Demographics, 
     slide11_Results]

