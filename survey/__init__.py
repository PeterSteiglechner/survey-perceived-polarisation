from otree.api import *
import json
import pandas as pd
import random

doc = """
Your app description
"""


def distance(a,b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5


class C(BaseConstants): 
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    LIKERT11 = list(range(0,11)) + [-999]
    LIKERT5_string = ["Strongly\nAgree","Agree","Neutral","Disagree","Strongly\nDisagree"] #+ ["Refuse/Don't know"]
    LIKERT5_string = [
        (1, 'Strongly agree'),
        (2, 'Agree'),
        (3, 'Neutral'),
        (4, 'Disagree'),
        (5, 'Strongly disagree'),
        (-999, "----NA----"),
    ]
    LIKERT5_string_noNA = [
        (1, 'Strongly agree'),
        (2, 'Agree'),
        (3, 'Neutral'),
        (4, 'Disagree'),
        (5, 'Strongly disagree')
    ]
    LIKERT_NUM2TEX = {num:tex for num, tex in LIKERT5_string}
    LIKERT_TEX2NUM = {tex:num for num, tex in LIKERT5_string}
    
    LIKERT5 = [1,2,3,4,5] + [-999]
    SLIDER = list(range(0,101)) +  [-999]
    QUESTIONS = ["climate_concern", 
                   "gay_adoption", 
                    "migration_enriches_culture",
                   "govt_reduce_inequ",
                   "free_elect", 
                   "politician_salaries"]
    QUESTIONTEXT = dict(zip( QUESTIONS, [
        'I am very concerned about climate change.', 
        'Gay and lesbian couples should have the same rights to adopt children as couples consisting of a man and a woman.', 
        'It is enriching for cultural life in Germany when migrants come here.', 
        'The state should take measures to reduce income differences more than before.',
        'That national elections are free and fair is extremely important for democracy.',
        'Politicians should receive a higher salary during their term of office.'
        ]))
    QUESTIONSHORTTEXT = dict(zip( QUESTIONS, [
        "concerned about climate", 
        "equal adoption rights for gay couples", 
        "migration enriches culture",
        "state should act to reduce income differences", 
        "free & fair elections important", 
        "higher politician salaries"
        ]))
    PERSONAS = pd.read_csv("_static/personas.csv")[QUESTIONS]
    P_OPS =  {f"P{n+1}": row.to_dict()  for n, row in PERSONAS.iterrows()}

    #CHECKTEXT = lambda which: f"To what extent does this actually reflect your perception of political similarity?"
    REASONTEXT ="Please briefly describe why (in two to three sentences)" 
    NCONTACTS = 3
    LABELLED = ["Green voter", "AfD voter"]
    LABELLEDCOLORS = dict(zip(LABELLED, ["#46962b", "#009ee0"]))
    NPS = len(P_OPS.keys())
    NR_CHECKS = 4

    N_MAX_PRACTICE_RUNS = 5

    # c = "worried about climate change."
    # g = "equal rights to adopt children for gay/lesbian couples."
    # m = "migration enriches cultural life in Germany."
    # i = "more state measures to reduce income differences."
    # ps = "higher salaries for politicians."
    # P_OP_RESPONSE = {"climate_concern": 
    #                  {"Strongly disagree": "is not at all "+c, "Neutral":"is somewhat "+c, "Strongly agree":"is extremely "+c},"gay_adoption": 
    #                  {"Strongly disagree": "strongly disapproves "+g, "Neutral":"is neutral about "+g, "Strongly agree":"strongly approves "+g}, 
    #                  "migration_enriches_culture":
    #                  {"Strongly disagree": "strongly disagrees that "+m, "Neutral":"has a neutral position on whether "+m, "Strongly agree":"strongly agrees that "+m}, 
    #                  "govt_reduce_inequ": 
    #                  {"Strongly disagree": "strongly opposes "+i, "Neutral":"is neutral about "+i, "Strongly agree":"strongly supports "+i},
    #                  "free_elect":
    #                  {"Strongly disagree": "thinks free and fair elections are not at all important for democracy.", 
    #                   "Neutral": "is doubtful whether free and fair elections are important for democracy.", 
    #                   "Strongly agree":"thinks free and fair elections are extremely important for democracy."
    #                   }, 
    #                   "politician_salaries":{
    #                       "Strongly disagree":"strongly supports "+ps, "Neutral":"is neutral about "+ps, "Strongly agree":"strongly supports "+ps
    #                   }
    #                 }

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

def make_field(label):
    return models.StringField(
        choices=C.LIKERT5_string_noNA,
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
    age = models.IntegerField(label='How old are you?', min=18, max=100)
    political_interest = models.StringField(label='How interested would you say you are in politics - are you...',
                                     choices=["Very interested", "Quite interested", "Hardly interested", "Not at all interested"],
                                     widget=widgets.RadioSelectHorizontal)

    feel_closest = models.StringField(label='Do you feel yourself closer to one of the political parties than the others?',
                                     choices=["yes", "no", "refuse to say"],
                                     widget=widgets.RadioSelectHorizontal)
    feel_closest_party = models.StringField(label='Which party do you feel closest to?',
                                     choices=["CDU/CSU", "AfD", "SPD", "Grüne", "Linke", "BSW", "FDP", "other", "refuse to say"],
                                     widget=widgets.RadioSelectHorizontal, 
                                     blank=True)
    how_polarised = models.StringField(label='People sometimes say that the public polarises on political issues. Would you agree?',
                                     choices=["Strongly Agree", "Somewhat Agree", "Somewhat Disagree", "Strongly Disagree"],
                                     widget=widgets.RadioSelect)
    
    
    #################################
    #####  MAP POSITIONS   #####
    #################################
    positionsTest = models.LongStringField()  # Stores JSON data of positions
    positions_preP = models.LongStringField(blank=True)
    positions = models.LongStringField(blank=True)  # Stores JSON data of positions

    #################################
    #####  CHecks   #####
    #################################
    check = models.IntegerField(initial=1) 
    check1_p1 =  models.LongStringField(blank=True)
    check1_p2 =  models.LongStringField(blank=True)
    check2_p1 =  models.LongStringField(blank=True)
    check2_p2 =  models.LongStringField(blank=True)
    check3_p1 =  models.LongStringField(blank=True)
    check3_p2 =  models.LongStringField(blank=True)
    check4_p1 =  models.LongStringField(blank=True)
    check4_p2 =  models.LongStringField(blank=True)
    check1 = models.StringField(choices=['not at all','somewhat','very much'], label="", widget=widgets.RadioSelectHorizontal,blank=False)
    check2 = models.StringField(        choices=['not at all','somewhat','very much'], label="", widget=widgets.RadioSelectHorizontal,blank=False)
    check3 = models.StringField(        choices=['not at all','somewhat','very much'],label="", widget=widgets.RadioSelectHorizontal,blank=False)
    check4 = models.StringField(        choices=['not at all','somewhat','very much'],label="", widget=widgets.RadioSelectHorizontal,blank=False)
    
    
    # for toCheck in ["f1f2", "P1P2"]:
    #     exec(f"check_self_{toCheck} = models.StringField(        choices=['not at all','somewhat','very much'],label=C.CHECKTEXT('your contacts'),widget=widgets.RadioSelectHorizontal,blank=False)")
    #     exec(f"reason_{toCheck} =  models.LongStringField(label=C.REASONTEXT)")
    # del toCheck

    isTrainingPassed = models.BooleanField(initial=False)#
    isTrainingCondFvC = models.BooleanField(initial=False)#
    isTrainingCondSelfvFC = models.BooleanField(initial=False)#
    isTrainingCondSvFC = models.BooleanField(initial=False)#
    #trainingMessageConfirmed = models.BooleanField(initial=False)#
    isTrainingCondSvF = models.BooleanField(initial=False)#
    attemptPractice = models.IntegerField(initial=0) 


    current_contact = models.IntegerField(initial=1) 
    evaluated_labelledPerson = models.IntegerField(initial=0) 
    ps_placed = models.IntegerField(initial=0)  
    mode = models.StringField(initial="contact")  # 'contact' or 'labelledPerson'
    

#################################
#####  OWN POLITICAL OPINIONS   #####
#################################
for q in C.QUESTIONS:
    setattr(Player, f"own_{q}", make_field(''))  
#################################
#####  CONTACTS' POLITICAL OPINIONS   #####
#################################
for n in range(1,C.NCONTACTS+1):
    setattr(Player, f"contact{n}", define_contact(f"Contact {n}: ", n))
    for q in C.QUESTIONS:
        setattr(Player, f"contact{n}_{q}", make_field(''))

for name in C.LABELLED:
    for q in C.QUESTIONS:
        setattr(Player, f"{name.replace(" ", "")}_{q}", make_field(''))

# PAGES
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
            choices = dict(C.LIKERT5_string_noNA)  # convert list of tuples to dict
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


class slide04_PersonOpinion(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):
        if player.mode == 'contact':
            idx = player.current_contact
            name = getattr(player, f"contact{idx}")
            prefix = f"contact{idx}_"
            heading = f"{name}"
            color = "#ff9600"  # Optional: generic or specific contact color
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
            choices = dict(C.LIKERT5_string_noNA)  # convert list of tuples to dict
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
        if player.mode == 'contact':
            prefix = f"contact{player.current_contact}_"
        else:
            name = C.LABELLED[player.evaluated_labelledPerson]
            prefix = f"{name.replace(" ", "")}_"
        return [f"{prefix}{q}" for q in C.QUESTIONS]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.mode == 'contact':
            player.current_contact += 1
        else:
            player.evaluated_labelledPerson += 1
        if player.current_contact > C.NCONTACTS:
            player.mode = "labelledPerson"
    @staticmethod
    def is_displayed(player: Player):
        if player.mode == 'contact':
            return player.current_contact <= C.NCONTACTS
        else:
            return player.evaluated_labelledPerson <= len(C.LABELLED)
        


class slide05a_MapTest(Page):
    form_model = 'player'
    form_fields = ['positionsTest']  # Store the final positions

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.attemptPractice += 1
        player.positionsTest = player.positionsTest
        pos = json.loads(player.positionsTest)
        pos = {p["label"]: [p["x"], p["y"]] for p in pos}
        #calculate distances
        dF = distance(pos["self"], pos["F"])
        dC = distance(pos["self"], pos["C"])
        dS = distance(pos["self"], pos["S"])
        dFS = distance(pos["F"], pos["S"])
        dFC = distance(pos["F"], pos["C"])
        dCS = distance(pos["C"], pos["S"])
        # check conditions
        player.isTrainingCondFvC = bool(dF<dC)  # Rule 2/3
        player.isTrainingCondSelfvFC = bool(dFC>dC)  # Rule 4
        player.isTrainingCondSvF = bool(dS>dF) # Rule 5
        player.isTrainingCondSvFC = bool((dFS<dS) and (dCS<dS)) # Rule 6.
        isTrainingPassed = player.isTrainingCondFvC & player.isTrainingCondSelfvFC & player.isTrainingCondSvFC & player.isTrainingCondSvF
        #print("isTrainingPassed", isTrainingPassed, dF, dS, dFS, dCS)
        player.isTrainingPassed = isTrainingPassed
    
    @staticmethod
    def is_displayed(player):
        return not player.isTrainingPassed 
    

class slide05b_MapTestResult(Page):
    @staticmethod
    def vars_for_template(player: Player):
        errors = ""
        errors += r"- The distance between self and C should be larger than the distance between self and F (bullet points 2/3). <br>" if player.isTrainingCondFvC==0 else ""
        errors += r"- The distance between F and C should be larger than the distance between self and C (bullet point 4). <br>" if player.isTrainingCondSelfvFC==0 else ""
        errors += r"- The distance between self and S should be larger than the distance between self and F (bullet point 5). <br>" if player.isTrainingCondSvF==0 else ""
        errors += r"- The distances between F and S and between C and S should be smaller than the distance between self and S (bullet point 6). <br>" if player.isTrainingCondSvFC==0 else ""
        
        return {"passed": player.isTrainingPassed, "errors":errors, "attempt":player.attemptPractice, "max_attempts": C.N_MAX_PRACTICE_RUNS} 
    
    @staticmethod
    def is_displayed(player: Player):
        return player.attemptPractice<=C.N_MAX_PRACTICE_RUNS or not player.isTrainingPassed



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
    form_fields = ['positions']  # Store the final positions
    
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
        
        # Determine current profile
        P = f"P{player.ps_placed + 1}"
        P_op = [C.LIKERT_TEX2NUM[op] for q, op in C.P_OPS[P].items()]

        # Parse positions
        pos = json.loads(player.positions) if player.positions else []

        # Full and short textual representations
        # P_text = f"{P} " + f" {P} ".join([
        #     C.P_OP_RESPONSE[q][C.LIKERT_NUM2TEX[P_op[n]]] for n, q in enumerate(C.QUESTIONS)
        # ])
        P_text_short = "; ".join([
            f"{C.QUESTIONSHORTTEXT[q]}: {C.LIKERT_NUM2TEX[P_op[i]]}"
            for i, q in enumerate(C.QUESTIONS)
        ])

        # Initialize dot descriptions of Contacts, Labelled, and Past Personas
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
            {
                "label": p["label"],
                "name": p["name"],
                "x": p["x"],
                "y": p["y"],
                "dottype": p["dottype"],
                "descr": dot_descrs.get(p["name"], "")
            }
            for p in pos
        ]
        init_dots.append({
            "label": P,
            "name": P,
            "x": 530,
            "y": 100,
            "dottype": "P",
            "descr": P_text_short
        })

        return {
            "P": P,
            #"P_text": P_text,
            "P_text_short": P_text_short,
            "dots": init_dots, 
            "img_source": f"{P}_op.png"
        }
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.ps_placed += 1

    @staticmethod
    def is_displayed(player):
        return player.ps_placed <= C.NPS  


class slide08_plausibilityCheck(Page):
    form_model = 'player'
    
    @staticmethod
    def get_form_fields(player: Player):
        # get the current iteration number
        i = player.check
        return [f'check{i}']
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
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

        p_points = [f"P{i}" for i in range(1, C.NPS)]
        focal_point = "self" #if random.random() < 0.5 else (f"contact{int(random.random()*C.NCONTACTS)+1}")
        focal_point_label= "yourself"

        # Calculate all distances from 'self' to P points
        distances = {p: distance(pos[focal_point], pos[p]) for p in p_points}

        # Find pairs where one distance is >= 1.5 times the other
        valid_pairs = []
        for i, p1 in enumerate(p_points):
            for p2 in p_points[i+1:]:
                d1 = distances[p1]
                d2 = distances[p2]
                if d1 >= 1.5 * d2 or d2 >= 1.5 * d1:
                    valid_pairs.append((p1, p2))
        if valid_pairs:
            p1, p2 = random.choice(valid_pairs)
            significant = True
        else:
            print("no significant differences in P distances")
            p1, p2 = random.sample(p_points, 2)
            significant = False
        # Save to participant.vars so accessible in before_next_page
        player.participant.vars[f'check{player.check}_p1'] = p1
        player.participant.vars[f'check{player.check}_p2'] = p2
        

        dist_p1 = distances[p1]
        dist_p2 = distances[p2]

        distantP = p1 if dist_p1 > dist_p2 else p2
        similarP = p2 if dist_p1 > dist_p2 else p1

        isDistF1LargerDistF2 = distance(pos["self"], pos[player.contact1]) > distance(pos["self"], pos[player.contact2])
        distantFriend = player.contact1 if isDistF1LargerDistF2 else player.contact2
        similarFriend = player.contact2 if isDistF1LargerDistF2 else player.contact1

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
            'distantP': distantP,
            'similarP': similarP,
            'current_check': f'check{player.check}',
            'significant': "much larger" if significant else "larger"
        }
    
# class slide08_CheckDistance(Page):
#     form_model = 'player'
#     form_fields = ['check_self_f1f2', "reason_f1f2", "check_self_P1P2", "reason_P1P2"]
    
#     @staticmethod
#     def vars_for_template(player: Player):
#         pos = json.loads(getattr(player, f"positions"))
#         pos = {p["label"]: [p["x"], p["y"]] for p in pos}
#         isDistF1LargerDistF2 = distance(pos["self"], pos[player.contact1]) > distance(pos["self"], pos[player.contact2])
#         isDistP1LargerDistP2 = distance(pos["self"], pos["P1"]) > distance(pos["self"], pos["P2"])
#         distantFriend = player.contact1 if isDistF1LargerDistF2 else player.contact2
#         similarFriend = player.contact2 if isDistF1LargerDistF2 else player.contact1
#         distantP = "P1" if isDistP1LargerDistP2 else "P2"
#         similarP = "P2" if isDistP1LargerDistP2 else "P1"
#         return {
#             'distantFriend': distantFriend,
#             'similarFriend': similarFriend,
#             'distantP': distantP,
#             'similarP': similarP,
#         }
    

# class ResultsWaitPage(WaitPage):
#     pass
class slide09_Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'political_interest', 'feel_closest', 'feel_closest_party', "how_polarised"]

class slide10_Results(Page):
    pass


# 
#page_sequence = [Introduction, Opinions, Friends]+[FriendOpinions]*C.NCONTACTS+[Green_Opinions, AfD_Opinions]+[MapTest, MapTestResult] * 5 + [Map]+[MapP]*C.NPS+[CheckDistance, Demographics, Results]

#[FriendOpinions]*C.NCONTACTS+[Voter_Opinions] * len(C.LABELLED)
page_sequence = [slide01_Introduction, 
    slide02_Opinions, 
    slide03_Contacts] + \
    [slide04_PersonOpinion] * (C.NCONTACTS + len(C.LABELLED)) + \
    [slide05a_MapTest, slide05b_MapTestResult] * 5+\
    [slide06_SPaM] +\
    [slide07_SPaM_personas] * C.NPS +\
    [slide08_plausibilityCheck] * C.NR_CHECKS +\
    [slide09_Demographics, 
     slide10_Results]

    #+[slide05a_MapTest, slide05b_MapTestResult] * 5
