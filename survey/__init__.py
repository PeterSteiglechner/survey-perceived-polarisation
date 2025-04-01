from otree.api import *
import numpy as np
import json

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    LIKERT11 = list(np.linspace(0,10,11).astype(int)) + [-999]
    LIKERT7 = list(np.linspace(1,7,7).astype(int)) + [-999]
    SLIDER = list(np.linspace(1,7,7).astype(int)) 
    QUESTIONS_SC =["climate_concern", 
                   "gay_adoption", 
                    "migration_enriches_culture",
                   "govt_reduce_inequ"]
    questiontext = [
        'I am very concerned about climate change.', 
        'Gay and lesbian couples should have the same rights to adopt children as couples consisting of a man and a woman.', 
        'It is enriching for cultural life in Germany when migrants come here.', 
        'The state should take measures to reduce income differences more than before.']
    QUESTIONS =questiontext# [f"{q} (1 agree strongly - 7 disagree strongly)" for q in  questions]
    CHECKTEXT = lambda which: f"To what extent does this actually reflect what you think about {which} political similarities to you?"
    REASONTEXT ="Briefly describe why you perceive distances in that way (in two to three sentences)" 
    NFRIENDS = 3
    NPS = 4


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass



def make_field(label):
    return models.IntegerField(
        choices=C.LIKERT7,
        label=label,
        widget=widgets.RadioSelectHorizontal,
    )

def make_slider(label):
    return models.IntegerField(
        choices=C.SLIDER,
        label=label,
        widget=widgets.RadioSelectHorizontal,
    )

def define_friend(label):
    return  models.LongStringField(label=label)


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
    #####  OWN POLITICAL OPINIONS   #####
    #################################
    climate_concern= make_slider(C.QUESTIONS[0])
    gay_adoption= make_slider(C.QUESTIONS[1])
    govt_reduce_inequ=  make_slider(C.QUESTIONS[2])
    migration_enriches_culture=  make_slider(C.QUESTIONS[3])

    
    
    #################################
    #####  MAP POSITIONS   #####
    #################################
    positionsTest = models.LongStringField()  # Stores JSON data of positions
    positions = models.LongStringField()  # Stores JSON data of positions

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
    ps_placed = models.IntegerField(initial=0)  



#################################
#####  FRIENDS' POLITICAL OPINIONS   #####
#################################
for f in range(1,C.NFRIENDS+1):
    setattr(Player, f"friend{f}", define_friend(f"Contact {f}"))
    for q in C.QUESTIONS_SC:
        setattr(Player, f"f{f}_{q}", make_field(''))

for f in ["Green_Voter", "AfD_Voter"]:
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

class Green_Opinions(Page):
    form_model = 'player'
    form_fields =  [f"Green_Voter_{q}" for q in C.QUESTIONS_SC]
    @staticmethod
    def vars_for_template(player: Player): 
        return {f'question_{q_sc}': q for q_sc, q in zip(C.QUESTIONS_SC, C.QUESTIONS)}
   
class AfD_Opinions(Page):
    form_model = 'player'
    form_fields = [f"AfD_Voter_{q}" for q in C.QUESTIONS_SC]
    @staticmethod
    def vars_for_template(player: Player): 
        return {f'question_{q_sc}': q for q_sc, q in zip(C.QUESTIONS_SC, C.QUESTIONS)}
   

class Opinions(Page):
    form_model = 'player'
    form_fields = C.QUESTIONS_SC
    @staticmethod
    def vars_for_template(player: Player): 
        return {f'question_{q_sc}': q for q_sc, q in zip(C.QUESTIONS_SC, C.QUESTIONS)}


class MapTest(Page):
    form_model = 'player'
    form_fields = ['positionsTest']  # Store the final positions
   
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.positionsTest = player.positionsTest
        pos = json.loads(player.positionsTest)
        pos = {p["label"]: np.array([p["x"], p["y"]]) for p in pos}
        #calculate distances
        dF = np.linalg.norm(pos["self"]-pos["F"])
        dC = np.linalg.norm(pos["self"]-pos["C"])
        dS = np.linalg.norm(pos["self"]-pos["S"])
        dFS = np.linalg.norm(pos["F"]-pos["S"])
        dFC = np.linalg.norm(pos["F"]-pos["C"])
        dCS = np.linalg.norm(pos["C"]-pos["S"])
        # check conditions
        player.isTrainingCondFvC = dF<dC  # Rule 2/3
        player.isTrainingCondSelfvFC = dFC>dC  # Rule 4
        player.isTrainingCondSvF = dS>dF # Rule 5
        player.isTrainingCondSvFC = (dFS<dS) & (dCS<dS) # Rule 6.
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
    form_fields = ['positions']  # Store the final positions
    
    @staticmethod
    def vars_for_template(player: Player):
        return {f"friend{f}": getattr(player, f"friend{f}") for f in range(1, C.NFRIENDS+1)}
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.positions = player.positions


class MapP(Page):
    form_model = 'player'
    form_fields = ['positions']  # Store the final positions
    
    @staticmethod
    def vars_for_template(player: Player):
        d = {f"friend{f}": getattr(player, f"friend{f}") for f in range(1, C.NFRIENDS+1)}
        d["currentP"] = player.ps_placed+1
        d["img_source"] = f"P{d['currentP']}.png"
        pos = json.loads(player.positions)
        pos = {p["label"]: [p["x"], p["y"]] for p in pos}
        for f in ["self"]+[f"friend{f}" for f in range(1, C.NFRIENDS+1)]+["Green_Voter", "AfD_Voter"]+[f"P{p}" for p in range(1,5)]:
            p = pos[f] if not "friend" in f else pos[getattr(player, f"friend{f[-1]}")]
            d[f"pos_{f}_x"] = p[0]
            d[f"pos_{f}_y"] = p[1]

            if f==f"P{d['currentP']}":
                d[f"pos_{f}_x"] = 0 + 10*int(f[-1])
                d[f"pos_{f}_y"] = 0+ 10*int(f[-1])
        return d
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.positions = player.positions
        player.ps_placed += 1

    @staticmethod
    def is_displayed(player):
        return player.ps_placed <= C.NFRIENDS  


class CheckDistance(Page):
    form_model = 'player'
    form_fields = ['check_self_f1f2', "reason_f1f2", "check_self_P1P2", "reason_P1P2"]
    
    @staticmethod
    def vars_for_template(player: Player):
        pos = json.loads(getattr(player, f"positions"))
        pos = {p["label"]: np.array([p["x"], p["y"]]) for p in pos}
        isDistF1LargerDistF2 = np.linalg.norm(pos["self"] - pos[player.friend1]) > np.linalg.norm(pos["self"] - pos[player.friend2])
        isDistP1LargerDistP2 = np.linalg.norm(pos["self"] - pos["P1"]) > np.linalg.norm(pos["self"] - pos["P2"])
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


#Demographics, Opinions,Friend3_Opinions, Friend4_Opinions,
# 
page_sequence = [Introduction, Opinions, Friends]+[FriendOpinions]*C.NFRIENDS+[Green_Opinions, AfD_Opinions]+[MapTest, MapTestResult] * 5 + [Map]+[MapP]*C.NPS+[CheckDistance, Demographics, Results]

