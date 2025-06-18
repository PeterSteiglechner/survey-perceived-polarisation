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
    LIKERT5 = [1,2,3,4,5] 
    LIKERT5_string_noNA = [
        (1, 'Strongly agree'),
        (2, 'Agree'),
        (3, 'Neutral'),
        (4, 'Disagree'),
        (5, 'Strongly disagree')
        ]
    LIKERT_NUM2TEX = {num:tex for num, tex in LIKERT5_string_noNA}
    LIKERT_NUM2TEX[-999] = "NA"
    LIKERT_TEX2NUM = {tex:num for num, tex in LIKERT5_string_noNA}
    QUESTIONS = ["climate_concern", "gay_marriage", "rights_for_integration", "econ_inequality"]
    QUESTIONTEXT = dict(zip(QUESTIONS, [
        "I am very concerned about climate change.",
        "It is good that marriages between two women or two men are allowed.",
        "Only migrants who make an effort and integrate should be given the same rights as natives.",
        "The differences in income and wealth in Germany are too high.",
    ]))
    QUESTIONSHORTTEXT = dict(zip( QUESTIONS, [
         "concerned about climate change", 
         "support same-sex marriage",
         "equal rights only for migrants who integrate",
         "economic differences too high"
    ])) 
    QUESTIONNAMES = dict(zip( QUESTIONS, [
        "Opinion about climate change", 
        "Opinion about same-sex marriage", 
        "Opinion about migrants' rights and integration",
        "Opinion about economic inequality",
        ]))
    
    NCONTACTS = 3

    LABELLED = ["Green voter", "AfD voter"]
    LABELLEDCOLORS = dict(zip(LABELLED, ["#46962b", "#009ee0"]))

    PERSONAS = pd.read_csv("_static/personas.csv")[QUESTIONS]
    P_OPS =  {f"P{n+1}": row.to_dict()  for n, row in PERSONAS.iterrows()}
    NPS = len(P_OPS.keys())

    NR_P_CHECKS = 3

    NR_OTHER_CHECKS = 5

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

def make_field(label):
    return models.StringField(
        choices=C.LIKERT5_string_noNA[::-1],
        label=label,
        widget=widgets.RadioSelect,
    )

def make_slider(label):
    return models.IntegerField(
        choices=C.SLIDER,
        label=label,
        widget=widgets.RadioSelectHorizontal,
    )

def define_contact(label, n):
    return  models.LongStringField(label=label, blank=False) # , initial=f"contact {n}",


class Player(BasePlayer):

    #################################
    #####  DEMOGRAPHICS   #####
    #################################

    age = models.IntegerField(label='', min=18, max=100)

    political_interest = models.StringField(
        label='', 
        choices=["not at all interested.", "hardly interested.", "quite interested.", "very interested."], 
        blank=False, 
        widget=widgets.RadioSelect
        )

    feel_closest_party = models.StringField(
        label='', 
        choices=["CDU/CSU", "AfD", "SPD", "Grüne", "Linke", "BSW", "FDP", "other", "no party", "refuse to say"], 
        blank=False, 
        widget=widgets.RadioSelect
        )

    how_polarised = models.StringField(
        label='',
        choices=["Not at all divided.", "Somewhat divided.", "Very divided.", "Extremely divided."],
        blank=False,
        widget=widgets.RadioSelect
        )
   
    topic_importance = models.StringField(
        label='',
        blank=True
    )

    importance_comments = models.LongStringField(label="Do you have any thoughts or reflections on which topics are most relevant for how you perceive political similarity or distance between individuals?", blank=True)

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
    check1_p1 =  models.LongStringField(blank=True)
    check1_p2 =  models.LongStringField(blank=True)
    check2_p1 =  models.LongStringField(blank=True)
    check2_p2 =  models.LongStringField(blank=True)
    check3_p1 =  models.LongStringField(blank=True)
    check3_p2 =  models.LongStringField(blank=True)
    check1 = models.StringField(choices=['No','Somewhat','Yes'], label="", widget=widgets.RadioSelect,blank=False)
    check1_explain = models.LongStringField(label="If you think this is not correct, you can use this textbox to explain why:",blank=True)
    check2 = models.StringField(choices=['No','Somewhat','Yes'], label="", widget=widgets.RadioSelect,blank=False)
    check2_explain = models.LongStringField(label="If you think this is not correct, you can use this textbox to explain why:",blank=True)
    check3 = models.StringField(choices=['No','Somewhat','Yes'],label="", widget=widgets.RadioSelect,blank=False)
    check3_explain = models.LongStringField(label="If you think this is not correct, you can use this textbox to explain why:",blank=True)
    
    # pairwise
    checkPair = models.IntegerField(initial=1) 
    checkPair1_dot1 =  models.LongStringField(blank=True)
    checkPair1_dot2 =  models.LongStringField(blank=True)
    checkPair2_dot1 =  models.LongStringField(blank=True)
    checkPair2_dot2 =  models.LongStringField(blank=True)
    checkPair3_dot1 =  models.LongStringField(blank=True)
    checkPair3_dot2 =  models.LongStringField(blank=True)
    checkPair4_dot1 =  models.LongStringField(blank=True)
    checkPair4_dot2 =  models.LongStringField(blank=True)
    checkPair5_dot1 =  models.LongStringField(blank=True)
    checkPair5_dot2 =  models.LongStringField(blank=True)
    checkPair1 = models.StringField(choices=["Very distant", "More distant than similar",  "Neither distant nor similar", "More similar than distant", "Very similar"],label="", widget=widgets.RadioSelect,blank=False)
    checkPair2 = models.StringField(choices=["Very distant", "More distant than similar",  "Neither distant nor similar", "More similar than distant", "Very similar"],label="", widget=widgets.RadioSelect,blank=False)
    checkPair3 = models.StringField(choices=["Very distant", "More distant than similar",  "Neither distant nor similar", "More similar than distant", "Very similar"],label="", widget=widgets.RadioSelect,blank=False)
    checkPair4 = models.StringField(choices=["Very distant", "More distant than similar",  "Neither distant nor similar", "More similar than distant", "Very similar"],label="", widget=widgets.RadioSelect,blank=False)
    checkPair5 = models.StringField(choices=["Very distant", "More distant than similar",  "Neither distant nor similar", "More similar than distant", "Very similar"],label="", widget=widgets.RadioSelect,blank=False)

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
    pass

class slide02_Opinions(Page):
    form_model = 'player'
    form_fields = [f"own_{q}" for q in C.QUESTIONS]
    @staticmethod
    def vars_for_template(player: Player): 
        fields =  [f"own_{q}" for q in C.QUESTIONS]
        questions = [C.QUESTIONTEXT[q] for q in C.QUESTIONS]
        #d["field_question_pairs"] = list(zip(d["fields"], d["questions"]))

        field_question_pairs = []
        for field, question in zip(fields, questions):
            choices = dict(C.LIKERT5_string_noNA[::-1])  # convert list of tuples to dict
            field_question_pairs.append({
                'field_name': field,
                'question_text': question,
                'choices': choices.items(),
            })
        return {'field_question_pairs': field_question_pairs}
    
class slide03_Contacts(Page):
    form_model = 'player'
    form_fields = [f"contact{n}" for n in range(1, C.NCONTACTS+1)]
    @staticmethod
    def vars_for_template(player:Player):
        return {"ncontacts": C.NCONTACTS}
    @staticmethod
    def error_message(player: Player, values):
        contacts = [v.strip() for v in values.values() if v.strip()]
        if len(contacts) < C.NCONTACTS:
            return "Please fill in all contact fields."
        if len(set(contacts)) < len(contacts):
            return "Each contact must be unique. Please avoid duplicates. You can use nicknames, initials, or anything that you will later recognise."

class slide04_PersonOpinion(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        if player.which_contact_type == 'contact':
            idx = player.current_contact
            name = getattr(player, f"contact{idx}")
            prefix = f"contact{idx}_"
            heading = f"{name}"
            color = "#ff9600"  # contact color
        else:  # mode == 'labelledPerson'
            idx = player.evaluated_labelledPerson
            name = C.LABELLED[idx]
            prefix = f"{name.replace(" ","")}_"
            heading = f"a typical {name}"
            color = C.LABELLEDCOLORS[name]
        fields = [f"{prefix}{q}" for q in C.QUESTIONS]
        questions = [C.QUESTIONTEXT[q] for q in C.QUESTIONS]
        field_question_pairs = []
        for field, question in zip(fields, questions):
            choices = dict(C.LIKERT5_string_noNA[::-1])  # convert list of tuples to dict
            field_question_pairs.append({
                'field_name': field,
                'question_text': question,
                'choices': choices.items(),
            })
        return {
            "name": name,
            "color": color,
            "heading": heading,
            "fields": fields,
            "questions": questions,
            "field_question_pairs": field_question_pairs,
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
        return not player.isTrainingPassed 
    

class slide05b_MapTestResult(Page):
    @staticmethod
    def vars_for_template(player: Player):
        player.attemptPractice += 1
        pos = json.loads(player.positionsTest)
        pos = {p["label"]: [p["x"], p["y"]] for p in pos}
        #calculate distances
        dF = distance(pos["self"], pos["Friend"])
        dC = distance(pos["self"], pos["Co-worker"])
        dS = distance(pos["self"], pos["Sister"])
        dFS = distance(pos["Friend"], pos["Sister"])
        dFC = distance(pos["Friend"], pos["Co-worker"])
        dCS = distance(pos["Co-worker"], pos["Sister"])
        # check conditions
        player.isTrainingCondFvC = bool(dF<dC)  # Rule 2/3
        player.isTrainingCondSelfvFC = bool(dFC>dC)  # Rule 4
        player.isTrainingCondSvF = bool(dS>dF) # Rule 5
        player.isTrainingCondSvFC = bool((dFS<dS) and (dCS<dS)) # Rule 6.
        isTrainingPassed = player.isTrainingCondFvC & player.isTrainingCondSelfvFC & player.isTrainingCondSvFC & player.isTrainingCondSvF
        player.isTrainingPassed = isTrainingPassed

        errors = ""
        errors += r"- The distance between 'Self' and 'Co-worker' should be larger than the distance between 'Self' and 'Friend' (instructions 2/3). <br>" if player.isTrainingCondFvC==0 else ""
        errors += r"- The distance between 'Friend' and 'Co-worker' should be larger than the distance between 'Self' and 'Co-worker' (instruction 4). <br>" if player.isTrainingCondSelfvFC==0 else ""
        errors += r"- The distance between 'Self' and 'Sister' should be larger than the distance between 'Self' and 'Friend' (instruction 5). <br>" if player.isTrainingCondSvF==0 else ""
        errors += r"- The distance between 'Self' and 'Sister' should be larger than the distances between 'Friend' and 'Sister' and between 'Co-worker' and 'Sister' (instruction 6). <br>" if player.isTrainingCondSvFC==0 else ""

        return {"passed": player.isTrainingPassed, "errors":errors, "attempt": player.attemptPractice, "max_attempts": C.N_MAX_PRACTICE_RUNS} 
    
    @staticmethod
    def is_displayed(player: Player):
        return (player.attemptPractice<=C.N_MAX_PRACTICE_RUNS) and ((not player.isTrainingPassed) or (player.isTrainingPassed and player.attemptPractice==0))



class slide06_SPaM(Page):
    form_model = 'player'
    form_fields = ['positions_preP','positions']
    
    @staticmethod
    def vars_for_template(player:Player):
        names =  ["self"]+[getattr(player, f"contact{f}") for f in range(1,C.NCONTACTS+1)]+[f"{v}" for v in C.LABELLED] 
        types = ["self"]+["contact"]*C.NCONTACTS + ["labelledPerson"]*len(C.LABELLED)
        dotnames = ["self"]+[f"contact{f}" for f in range(1,C.NCONTACTS+1)]+[f"{v}" for v in C.LABELLED] 
        init_dots = [{"dottype": dottype, "label": name, 
        "name":dotname, "x": 530, "y": 40 + i * 60, "descr": ""} for i, (dottype, name, dotname) in enumerate(zip(types, names, dotnames))]
        return dict(dots=init_dots)

class slide07_SPaM_personas(Page):
    form_model = 'player'
    form_fields = ['positions']  
    
    @staticmethod
    def vars_for_template(player:Player):

        def get_ops(prefix, questions):
            return {
                q: getattr(player, f"{prefix}{q}", -999) or -999
                for q in questions
            }
        def format_ops(ops_dict):
            return "; ".join(
                f"{C.QUESTIONSHORTTEXT[q]}: {C.LIKERT_NUM2TEX[int(val)]}"
                for q, val in ops_dict.items()
            )
        
        P = f"P{player.ps_placed + 1}"
        P_op = [C.LIKERT_TEX2NUM[op] for q, op in C.P_OPS[P].items()]
        pos = json.loads(player.positions) if player.positions else []

        P_text_short = "; ".join([
            f"{C.QUESTIONSHORTTEXT[q]}: {C.LIKERT_NUM2TEX[P_op[i]]}"
            for i, q in enumerate(C.QUESTIONS)
        ])

        # Write dot descriptions of Self, Contacts, Labelled, and past Personas
        dot_descrs = {"self": format_ops(get_ops("own_", C.QUESTIONS))}
        for f in range(1, C.NCONTACTS + 1):
            dot_descrs[f"contact{f}"] = format_ops(get_ops(f"contact{f}_", C.QUESTIONS))
        for v in C.LABELLED:
            dot_descrs[f"{v}"] = format_ops(get_ops(f"{v.replace(" ", "")}_", C.QUESTIONS))
        for p in range(1, player.ps_placed + 1):
            currP = f"P{p}"
            currP_op = [C.LIKERT_TEX2NUM[op] for q, op in C.P_OPS[currP].items()]
            dot_descrs[currP] = "; ".join([
                f"{C.QUESTIONSHORTTEXT[q]}: {C.LIKERT_NUM2TEX[op]}"
                for q, op in zip(C.QUESTIONS, currP_op)
            ])

        # Prepare initial dot data
        init_dots = [
                    {"label": p["label"],
                    "name": p["name"],
                    "x": p["x"],
                    "y": p["y"],
                    "dottype": p["dottype"],
                    "descr": dot_descrs.get(p["name"], "")}
                for p in pos
            ]
        init_dots.append({"label": P, "name": P, "x": 530, "y": 300, "dottype": "P", "descr": P_text_short})

        return {
            "P": P,
            "P_text_short": P_text_short,
            "dots": init_dots, 
            "img_source": f"{P}_op.png",
            "n_ps": C.NPS,
            "ps_placed": player.ps_placed+1,
        }
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.ps_placed += 1

        if player.ps_placed==C.NPS:
            # Find NR_P_CHECKS triples for which the distance self-p is >= 1.5 times the self-q; fill the rest with random triples self-p-q.
            positions = json.loads(getattr(player, "positions"))
            pos = {p["label"]: [p["x"], p["y"]] for p in positions}
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
        return player.ps_placed <= C.NPS  



class slide08a_PlausibilityCheck_Ps(Page):
    form_model = 'player'
    
    @staticmethod
    def get_form_fields(player: Player):
        i = player.check
        return [f'check{i}', f'check{i}_explain']
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        valid_pairs = json.loads(getattr(player, "valid_p1p2self_triples"))
        pair = [player.participant.vars[f'check{player.check}_p1'], player.participant.vars[f'check{player.check}_p2']]
        valid_pairs.remove(pair)
        player.valid_p1p2self_triples = json.dumps(valid_pairs)

        p1_label = player.participant.vars.get(f'check{player.check}_p1')
        p2_label = player.participant.vars.get(f'check{player.check}_p2')
        if p1_label and p2_label:
            setattr(player, f'check{player.check}_p1', p1_label)
            setattr(player, f'check{player.check}_p2', p2_label)
        else:
            # fallback, just set empty string or default
            setattr(player, f'check{player.check}_p1', '')
            setattr(player, f'check{player.check}_p2', '')
        player.check += 1

    @staticmethod
    def vars_for_template(player: Player):
        positions = json.loads(getattr(player, "positions"))
        pos = {p["label"]: [p["x"], p["y"]] for p in positions}
        p_points = [f"P{i}" for i in range(1, C.NPS+1)]
        focal_point = "self" 
        focal_point_label= "yourself"
        distances = {p: distance(pos[focal_point], pos[p]) for p in p_points}
        valid_pairs = json.loads(player.valid_p1p2self_triples)
        p1,p2 = random.choice(valid_pairs)
        dist_p1 = distances[p1]
        dist_p2 = distances[p2]
        significant = ((dist_p1 >= 1.5 * dist_p2) or (dist_p2 >= 1.5 * dist_p1))
        player.participant.vars[f'check{player.check}_p1'] = p1
        player.participant.vars[f'check{player.check}_p2'] = p2
        distantP = p1 if dist_p1 > dist_p2 else p2
        similarP = p2 if dist_p1 > dist_p2 else p1
        dot_descrs= {}
        for p in [p1, p2]:
            currP = f"{p}"
            currP_op = [C.LIKERT_TEX2NUM[op] for q, op in C.P_OPS[currP].items()]
            dot_descrs[currP] = "; ".join([
                f"{C.QUESTIONSHORTTEXT[q]}: {C.LIKERT_NUM2TEX[op]}"
                for q, op in zip(C.QUESTIONS, currP_op)])
        return {
            'p0_coords': pos[focal_point],
            'p1_coords': pos[p1],
            'p2_coords': pos[p2],
            'p0': focal_point,
            'p0label': focal_point_label,
            'p1': p1,
            'p2': p2,
            'descr_p1': dot_descrs[p1],
            'descr_p2': dot_descrs[p2],
            'dist_p1': dist_p1,
            'dist_p2': dist_p2,
            'significant': "much larger" if significant else "larger",
            'distantP': distantP,
            'similarP': similarP,
            'ncheck': player.check,
            'nr_tot_checks': C.NR_P_CHECKS + C.NR_OTHER_CHECKS,
            'current_check': f'check{player.check}',
            'current_check_explain': f'check{player.check}_explain',
        }


class slide08b_PlausibilityCheck_Pairs(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        i = player.checkPair
        return [f'checkPair{i}']
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        p1_label = player.participant.vars.get(f'checkPair{player.check}_dot1')
        p2_label = player.participant.vars.get(f'checkPair{player.check}_dot2')
        if p1_label and p2_label:
            setattr(player, f'checkPair{player.checkPair}_dot1', p1_label)
            setattr(player, f'checkPair{player.checkPair}_dot2', p2_label)
        else:
            # fallback, just set empty string or default
            setattr(player, f'checkPair{player.checkPair}_dot1', '')
            setattr(player, f'checkPair{player.checkPair}_dot2', '')
        player.checkPair += 1

    @staticmethod
    def vars_for_template(player: Player):
        points = [
            ["contact2", C.LABELLED[0]],
            ["self", C.LABELLED[0]],
            ["contact1", C.LABELLED[0]],
            ["contact2", C.LABELLED[1]],
            ["self", C.LABELLED[1]],
            ]
        p1, p2 = points[player.checkPair-1]
        p1label = f"your contact {getattr(player, p1)}" if "contact" in p1 else ("yourself" if p1=="self" else (f"a typical {p1}" if p1 in C.LABELLED else p1))
        p2label = f"your contact {getattr(player, p2)}" if "contact" in p2 else ("yourself" if p2=="self" else(f"a typical {p2}" if p2 in C.LABELLED else p2))
        return {
            'p1': p1,
            'p1_label':p1label, 
            'p2': p2,
            'p2_label':p2label,
            'ncheck': player.checkPair,
            'nr_tot_checks': C.NR_P_CHECKS + C.NR_OTHER_CHECKS,
            'nr_total_checks':C.NR_P_CHECKS + player.checkPair,
            'current_check': f'checkPair{player.checkPair}',
        }


class slide09_Importance(Page):
    form_model = 'player'
    form_fields = ['topic_importance', 'importance_comments']
    
    @staticmethod
    def vars_for_template(player):
        return {
            'topic_choices': [qname+"." for q,qname in C.QUESTIONNAMES.items()]+["Different topic(s).", "I don't know."]
        }
    @staticmethod
    def error_message(player, values):
        if values['topic_importance']:
            selected_choices = values['topic_importance'].split(',')
            valid_choices = [qname+"." for q,qname in C.QUESTIONNAMES.items()]+["Different topic(s).", "I don't know."]
            for choice in selected_choices:
                if choice.strip() not in valid_choices:
                    return "Invalid selection detected."
        return None



class slide10_Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'political_interest', 'feel_closest_party', "how_polarised"]



class slide11_Results(Page):
    pass


# 
#page_sequence = [Introduction, Opinions, Friends]+[FriendOpinions]*C.NCONTACTS+[Green_Opinions, AfD_Opinions]+[MapTest, MapTestResult] * 5 + [Map]+[MapP]*C.NPS+[CheckDistance, Demographics, Results]

#[FriendOpinions]*C.NCONTACTS+[Voter_Opinions] * len(C.LABELLED)
page_sequence = [slide01_Introduction, 
    slide02_Opinions, 
    slide03_Contacts] + \
    [slide04_PersonOpinion] * (C.NCONTACTS + len(C.LABELLED)) + \
    [slide05a_MapTest, slide05b_MapTestResult] * C.N_MAX_PRACTICE_RUNS +\
    [slide06_SPaM] +\
    [slide07_SPaM_personas] * C.NPS +\
    [slide08a_PlausibilityCheck_Ps] * C.NR_P_CHECKS +\
    [slide08b_PlausibilityCheck_Pairs] * C.NR_OTHER_CHECKS +\
    [slide09_Importance, slide10_Demographics, 
     slide11_Results]

    #+[slide05a_MapTest, slide05b_MapTestResult] * 5
