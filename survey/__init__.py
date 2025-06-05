from otree.api import *
import json




doc = """
Your app description
"""




personas = [
  {
    "name": "Green Progressive / Social Justice Activist",
    "description": "Young, urban, left-leaning, pro-equality and environmentalist.",  # Alternative: "Strongly leftist, fights for equality and systemic change.", 
    "responses": {"climate_concern": "Strongly agree", 
                  "gay_adoption": "Strongly agree",
                  "migration_enriches_culture": "Strongly agree",
                  "govt_reduce_inequ": "Strongly agree",
                  "free_elect": "Strongly agree",
                  "politician_salaries": "Strongly disagree"
                  }
  },
  {
    "name": "Centrist Pragmatist",
    "description": "Moderate, politically balanced, avoids extremes, skeptical of migration.",
    "responses": {"climate_concern": "Neutral", 
                  "gay_adoption": "Neutral",
                  "migration_enriches_culture": "Strongly disagree",
                  "govt_reduce_inequ": "Neutral",
                  "free_elect": "Strongly agree",
                  "politician_salaries": "Neutral"
                  }
  },
  {
    "name": "Economic Liberal",
    "description": "Pro-market, fiscally conservative, socially moderate.",
    "responses": {"climate_concern": "Neutral", 
                  "gay_adoption": "Neutral",
                  "migration_enriches_culture": "Neutral",
                  "govt_reduce_inequ": "Strongly disagree",
                  "free_elect": "Strongly agree",
                  "politician_salaries": "Strongly agree"
                  }
  },
  {
    "name": "National Populist",
    "description": "Anti-elite, nationalist, anti-immigration, skeptical of climate action.",
    "responses": {"climate_concern": "Strongly disagree", 
                  "gay_adoption": "Strongly disagree",
                  "migration_enriches_culture": "Strongly disagree",
                  "govt_reduce_inequ": "Strongly disagree",
                  "free_elect": "Neutral",
                  "politician_salaries": "Neutral"
                  }
  },
  {
    "name": "Left-Conservative Dissenter",
    "description": "Economically leftist, culturally traditional, skeptical of globalization and political elites.",
    "responses": {"climate_concern": "Strongly agree", 
                  "gay_adoption": "Strongly disagree",
                  "migration_enriches_culture": "Strongly disagree",
                  "govt_reduce_inequ": "Strongly agree",
                  "free_elect": "Strongly agree",
                  "politician_salaries": "Strongly disagree"
                  }
    }, 
{
  "name": "Old-School Unionist",
  "description": "Economically Marxist, pro-worker, culturally moderate, skeptical of elites and identity politics.",
  "responses": {"climate_concern": "Neutral", 
                  "gay_adoption": "Neutral",
                  "migration_enriches_culture": "Neutral",
                  "govt_reduce_inequ": "Strongly agree",
                  "free_elect": "Strongly agree",
                  "politician_salaries": "Strongly disagree"
                  }
},
{
    "name": "Moderate Christian Democrat",
    "description": "Center-right, values tradition, stability, social market economy, and democratic institutions.",
    "responses": {"climate_concern": "Strongly agree", 
                  "gay_adoption": "Neutral",
                  "migration_enriches_culture": "Neutral",
                  "govt_reduce_inequ": "Neutral",
                  "free_elect": "Strongly agree",
                  "politician_salaries": "Strongly agree"
                  }
    }, 
 {
  "name": "Tech Libertarian",
  "description": "Hyper-individualist, pro-market, socially liberal, anti-redistribution and skeptical of government regulation.",
  "responses": {"climate_concern": "Strongly disagree", 
                  "gay_adoption": "Strongly agree",
                  "migration_enriches_culture": "Strongly agree",
                  "govt_reduce_inequ": "Strongly disagree",
                  "free_elect": "Strongly agree",
                  "politician_salaries": "Neutral"
                  }
}
]


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
    QUESTIONS_SC =["climate_concern", 
                   "gay_adoption", 
                    "migration_enriches_culture",
                   "govt_reduce_inequ",
                   "free_elect", 
                   "politician_salaries"]
    questiontext = [
        'I am very concerned about climate change.', 
        'Gay and lesbian couples should have the same rights to adopt children as couples consisting of a man and a woman.', 
        'It is enriching for cultural life in Germany when migrants come here.', 
        'The state should take measures to reduce income differences more than before.',
        'That national elections are free and fair is extremely important for democracy.',
        'Politicians should receive a higher salary during their term of office.'
        ]
    questionshorttext =[
        "concerned about climate", 
        "equal adoption rights for gay couples", 
        "migration enriches culture",
        "state should act to reduce income differences", 
        "free & fair elections important", 
        "higher politician salaries"]
    QUESTIONS =questiontext# [f"{q} (1 agree strongly - 7 disagree strongly)" for q in  questions]
    CHECKTEXT = lambda which: f"To what extent does this actually reflect your perception of political similarity?"
    REASONTEXT ="Please briefly describe why (in two to three sentences)" 
    NFRIENDS = 3
    P_OPS =  {f"P{n+1}": P["responses"]  for n, P in enumerate(personas)}
    NPS = len(P_OPS.keys())
    c = "worried about climate change."
    g = "equal rights to adopt children for gay/lesbian couples."
    m = "migration enriches cultural life in Germany."
    i = "more state measures to reduce income differences."
    ps = "higher salaries for politicians."
    P_OP_RESPONSE = {"climate_concern": 
                     {"Strongly disagree": "is not at all "+c, "Neutral":"is somewhat "+c, "Strongly agree":"is extremely "+c},"gay_adoption": 
                     {"Strongly disagree": "strongly disapproves "+g, "Neutral":"is neutral about "+g, "Strongly agree":"strongly approves "+g}, 
                     "migration_enriches_culture":
                     {"Strongly disagree": "strongly disagrees that "+m, "Neutral":"has a neutral position on whether "+m, "Strongly agree":"strongly agrees that "+m}, 
                     "govt_reduce_inequ": 
                     {"Strongly disagree": "strongly opposes "+i, "Neutral":"is neutral about "+i, "Strongly agree":"strongly supports "+i},
                     "free_elect":
                     {"Strongly disagree": "thinks free and fair elections are not at all important for democracy.", 
                      "Neutral": "is doubtful whether free and fair elections are important for democracy.", 
                      "Strongly agree":"thinks free and fair elections are extremely important for democracy."
                      }, 
                      "politician_salaries":{
                          "Strongly disagree":"strongly supports "+ps, "Neutral":"is neutral about "+ps, "Strongly agree":"strongly supports "+ps
                      }
                    }
    
    VOTERS = ["Green", "AfD"]


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

def define_friend(label, n):
    return  models.LongStringField(label=label, initial=f"contact {n}")


class Player(BasePlayer):
    age = models.IntegerField(label='How old are you?', min=18, max=100)
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
    for toCheck in ["f1f2", "P1P2"]:
        exec(f"check_self_{toCheck} = models.StringField(        choices=['not at all','somewhat','very much'],label=C.CHECKTEXT('your friends'),widget=widgets.RadioSelectHorizontal,blank=True)")
        exec(f"reason_{toCheck} =  models.LongStringField(label=C.REASONTEXT)")
    del toCheck

    isTrainingPassed = models.BooleanField(initial=False)#
    isTrainingCondFvC = models.BooleanField(initial=False)#
    isTrainingCondSelfvFC = models.BooleanField(initial=False)#
    isTrainingCondSvFC = models.BooleanField(initial=False)#
    trainingMessageConfirmed = models.BooleanField(initial=False)#
    isTrainingCondSvF = models.BooleanField(initial=False)#
    current_friend = models.IntegerField(initial=1) 
    evaluated_voter = models.IntegerField(initial=0) 
    ps_placed = models.IntegerField(initial=0)  

    

#################################
#####  OWN POLITICAL OPINIONS   #####
#################################
for q in C.QUESTIONS_SC:
    setattr(Player, f"own_{q}", make_field(''))  
#################################
#####  FRIENDS' POLITICAL OPINIONS   #####
#################################
for f in range(1,C.NFRIENDS+1):
    setattr(Player, f"friend{f}", define_friend(f"Contact {f}", f))
    for q in C.QUESTIONS_SC:
        setattr(Player, f"f{f}_{q}", make_field(''))

for f in ["GreenVoter", "AfDVoter"]:
    for q in C.QUESTIONS_SC:
        setattr(Player, f"{f}_{q}", make_field(''))

# PAGES
class Introduction(Page):
    pass

class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'feel_closest', 'feel_closest_party', "how_polarised"]


class Friends(Page):
    form_model = 'player'
    form_fields = [f"friend{n}" for n in range(1, C.NFRIENDS+1)]
    @staticmethod
    def vars_for_template(player:Player):
        return {"nfriends":C.NFRIENDS}

class FriendOpinions(Page):
    form_model = "player"
    @staticmethod
    def get_form_fields(player):
        return [f"f{player.current_friend}_{q}" for q in C.QUESTIONS_SC]
        
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.current_friend +=1

    @staticmethod
    def vars_for_template(player):
        # d = {f'question_{q_sc}': q for q_sc, q in zip(C.QUESTIONS_SC, C.QUESTIONS)}
        d = {"friend_name": getattr(player, f"friend{player.current_friend}")}
        d["fields"] = [f"f{player.current_friend}_{q}" for q in C.QUESTIONS_SC]
        d["questions"] = C.questiontext
        d["field_question_pairs"] = list(zip(d["fields"], d["questions"]))
        return d

    @staticmethod
    def is_displayed(player):
        return player.current_friend <= C.NFRIENDS  

class Voter_Opinions(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player):
        return [f"{C.VOTERS[player.evaluated_voter]}Voter_{q}" for q in C.QUESTIONS_SC]
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.evaluated_voter +=1
    @staticmethod
    def vars_for_template(player: Player): 
        voter = C.VOTERS[player.evaluated_voter]
        d = {
            "name": voter,
            "fields": [f"{voter}Voter_{q}" for q in C.QUESTIONS_SC], 
            "questions": C.questiontext
            }
        d["field_question_pairs"] = list(zip(d["fields"], d["questions"]))
        return d
    @staticmethod
    def is_displayed(player):
        return player.evaluated_voter <= len(C.VOTERS)  
    
class AfD_Opinions(Page):
    form_model = 'player'
    #form_fields = [f"AfDVoter_{q}" for q in C.QUESTIONS_SC]
    @staticmethod
    def get_form_fields(player):
        return [f"GreenVoter_{q}" for q in C.QUESTIONS_SC]
    @staticmethod
    def vars_for_template(player: Player): 
        d = {"fields": [f"AfDVoter_{q}" for q in C.QUESTIONS_SC],
        "questions": C.questiontext}
        d["field_question_pairs"] = list(zip(d["fields"], d["questions"]))
        return d

class Opinions(Page):
    form_model = 'player'
    form_fields = [f"own_{q}" for q in C.QUESTIONS_SC]
    @staticmethod
    def vars_for_template(player: Player): 
        d = {"fields": [f"own_{q}" for q in C.QUESTIONS_SC],
        "questions": C.questiontext}
        d["field_question_pairs"] = list(zip(d["fields"], d["questions"]))
        return d

class MapTest(Page):
    form_model = 'player'
    form_fields = ['positionsTest']  # Store the final positions
   
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
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
    

class MapTestResult(Page):
    @staticmethod
    def vars_for_template(player: Player):
        passedMsg = "Well done! Your arrangement fulfills all the criteria. Below we show another possible example of an arrangement that accurately describes the scenario."
        errors = ""
        errors += r"The distance between self and C should be larger than the distance between self and F (bullet points 2/3). <br>" if player.isTrainingCondFvC==0 else ""
        errors += r"The distance between F and C should be larger than the distance between self and C (bullet point 4). <br>" if player.isTrainingCondSelfvFC==0 else ""
        errors += r"The distance between self and S should be larger than the distance between self and F (bullet point 5). <br>" if player.isTrainingCondSvF==0 else ""
        errors += r"The distances between F and S and between C and S should be smaller than the distance between self and S (bullet point 6). <br>" if player.isTrainingCondSvFC==0 else ""
        
        failedMsg=fr"Your arrangement does not meet all parts of the description: <br>  <br> {errors} <br>"+\
        "Please repeat the training and try to arrange the dots so that all criteria are fulfilled. You can see one possible arrangement that fulfills all the criteria below."
        if player.isTrainingPassed:
            player.trainingMessageConfirmed = True
        return {"isTrainingPassedMsg": passedMsg if player.isTrainingPassed else failedMsg} 
    @staticmethod
    def is_displayed(player: Player):
        return not player.trainingMessageConfirmed or not player.isTrainingPassed

class Map(Page):
    form_model = 'player'
    form_fields = ['positions_preP','positions']
    
    @staticmethod
    def vars_for_template(player:Player):
        names =  ["self"]+[getattr(player, f"friend{f}") for f in range(1,C.NFRIENDS+1)]+[f"{v}Voter" for v in C.VOTERS] 
        types = ["self"]+["friend"]*C.NFRIENDS + ["voter"]*len(C.VOTERS)
        dotnames = ["self"]+[f"friend{f}" for f in range(1,C.NFRIENDS+1)]+[f"{v}Voter" for v in C.VOTERS] 
        init_dots = [{"dottype": dottype, "label": name, 
        "name":dotname, "x": 530, "y": 40 + i * 60, "descr": ""} for i, (dottype, name, dotname) in enumerate(zip(types, names, dotnames))]
        return dict(dots=init_dots)
    
    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #     if player.positions_preP:
    #         player.positions = player.positions_preP

# class Map(Page):
#     form_model = 'player'
#     form_fields = ['positions']  # Store the final positions
    
#     @staticmethod
#     def vars_for_template(player: Player):
#         return {f"friend{f}": getattr(player, f"friend{f}") for f in range(1, C.NFRIENDS+1)}
#     @staticmethod
#     def before_next_page(player: Player, timeout_happened):
#         player.positions = player.positions_preP


class MapP(Page):
    form_model = 'player'
    form_fields = ['positions']  # Store the final positions
    
    @staticmethod
    def vars_for_template(player:Player):
        P = f"P{player.ps_placed+1}"
        P_op = [C.LIKERT_TEX2NUM[op] for q, op in C.P_OPS[P].items()]
        pos_raw = getattr(player, "positions")
        if pos_raw:
            pos = json.loads(pos_raw)
        else:
            pos = []
        P_text = f"{P} "+f" {P} ".join([C.P_OP_RESPONSE[q][C.LIKERT_NUM2TEX[P_op[n]]] for n, q in enumerate(C.QUESTIONS_SC)])
        P_text_short = "; ".join([f"{q}: {C.LIKERT_NUM2TEX[op]}" for q, op in zip(C.questionshorttext, P_op)]) 
        
        own_ops = {qsc: (getattr(player, "own_"+qsc) if  getattr(player, "own_"+qsc)!="" else -999) for qsc in C.QUESTIONS_SC}
        dot_descrs = {"self": "; ".join([f"{q}: {C.LIKERT_NUM2TEX[int(own_ops[qsc])]}" for q, qsc in zip(C.questionshorttext, C.QUESTIONS_SC)])}
        for f in range(1, C.NFRIENDS+1):
            f_ops = {qsc:  (getattr(player, f"f{f}_"+qsc) if  getattr(player, f"f{f}_"+qsc)!="" else -999) for qsc in C.QUESTIONS_SC}
            dot_descrs[f"friend{f}"] = "; ".join([f"{q}: {C.LIKERT_NUM2TEX[int(f_ops[qsc])]}" for q, qsc in zip(C.questionshorttext, C.QUESTIONS_SC)])
        for v in C.VOTERS:
            v_ops = {qsc:  (getattr(player, f"{v}Voter_"+qsc) if  getattr(player, f"{v}Voter_"+qsc)!="" else -999) for qsc in C.QUESTIONS_SC}            
            dot_descrs[f"{v}Voter"] = "; ".join([f"{q}: {C.LIKERT_NUM2TEX[int(v_ops[qsc])]}" for q, qsc in zip(C.questionshorttext, C.QUESTIONS_SC)])
        for p in range(1, player.ps_placed+1):
            #print(f"looking at p={p}")
            currP = f"P{player.ps_placed+1}"
            currP_op = [C.LIKERT_TEX2NUM[op] for q, op in C.P_OPS[currP].items()]
            dot_descrs[f"P{p}"] =  "; ".join([f"{q}: {C.LIKERT_NUM2TEX[op]}" for q, op in zip(C.questionshorttext, currP_op)]) 

            #"; ".join([f"{q}: {op}" for q, (key, op) in zip(C.questionshorttext, C.P_OPS["P"+p]["responses"].items())]) 
        
        init_dots = [{"label": p["label"], "name":p["name"], "x":p["x"], "y":p["y"], "dottype": p["dottype"], "descr":dot_descrs[p["name"]]} for p in pos]
        init_dots.append(
            {"label": P, "name": P, "x": 530, "y": 400, "dottype": "P", "descr":P_text_short} 
        )

        return dict(dots=init_dots, 
                    currentP=P,
                    P_op_text = P_text,
                    P_op_text_short = P_text_short,
                    img_source=f"{P}_op.png")
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.ps_placed += 1

    @staticmethod
    def is_displayed(player):
        return player.ps_placed <= C.NPS  


class CheckDistance(Page):
    form_model = 'player'
    form_fields = ['check_self_f1f2', "reason_f1f2", "check_self_P1P2", "reason_P1P2"]
    
    @staticmethod
    def vars_for_template(player: Player):
        pos = json.loads(getattr(player, f"positions"))
        pos = {p["label"]: [p["x"], p["y"]] for p in pos}
        isDistF1LargerDistF2 = distance(pos["self"], pos[player.friend1]) > distance(pos["self"], pos[player.friend2])
        isDistP1LargerDistP2 = distance(pos["self"], pos["P1"]) > distance(pos["self"], pos["P2"])
        distantFriend = player.friend1 if isDistF1LargerDistF2 else player.friend2
        similarFriend = player.friend2 if isDistF1LargerDistF2 else player.friend1
        distantP = "P1" if isDistP1LargerDistP2 else "P2"
        similarP = "P2" if isDistP1LargerDistP2 else "P1"
        return {
            'distantFriend': distantFriend,
            'similarFriend': similarFriend,
            'distantP': distantP,
            'similarP': similarP,
        }
    

class ResultsWaitPage(WaitPage):
    pass

class Results(Page):
    pass


# 
#page_sequence = [Introduction, Opinions, Friends]+[FriendOpinions]*C.NFRIENDS+[Green_Opinions, AfD_Opinions]+[MapTest, MapTestResult] * 5 + [Map]+[MapP]*C.NPS+[CheckDistance, Demographics, Results]

#+[MapTest, MapTestResult] * 5
page_sequence = [Introduction, Opinions, Friends]+[FriendOpinions]*C.NFRIENDS+[Voter_Opinions] * len(C.VOTERS) +[Map]+[MapP]*C.NPS+[CheckDistance, Demographics, Results]
