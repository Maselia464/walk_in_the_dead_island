from dataclasses import dataclass
from dis import Instruction
from email.headerregistry import UniqueUnstructuredHeader
from importlib.metadata import requires

from AoE2ScenarioParser.datasets.effects import attributes
from AoE2ScenarioParser.objects.support import area


from logging import disable
from AoE2ScenarioParser.datasets.trigger_lists import *
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from pyexpat.errors import messages

# Information of unit/building/hero and tech IDs
from AoE2ScenarioParser.datasets.projectiles import ProjectileInfo
from AoE2ScenarioParser.datasets.object_support import Civilization, StartingAge
from AoE2ScenarioParser.datasets.object_support import *
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.techs import TechInfo
# Information about player IDs
from AoE2ScenarioParser.datasets.players import PlayerId, PlayerColorId, ColorId
from AoE2ScenarioParser import scenarios
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
# Information about terrain IDs
from AoE2ScenarioParser.datasets.terrains import TerrainId

from AoE2ScenarioParser.datasets.trigger_lists import \
    DiplomacyState, Operation, ButtonLocation, PanelLocation, \
    TimeUnit, VisibilityState, DifficultyLevel, TechnologyState, \
    Comparison, ObjectAttribute, Attribute, UnitAIAction, \
    AttackStance, ObjectType, ObjectClass, DamageClass, \
    HeroStatusFlag, Hotkey, BlastLevel, TerrainRestrictions, \
    ColorMood, ObjectState, SecondaryGameMode, ChargeType, \
    ChargeEvent, CombatAbility, FogVisibility, GarrisonType, \
    OcclusionMode, ProjectileHitMode, ProjectileVanishMode, \
    UnitTrait, ProjectileSmartMode, Age, ActionType, VictoryTimerType

from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.data_objects.unit import Unit
from AoE2ScenarioParser.objects.support import area
from AoE2ScenarioParser.objects.managers.unit_manager import UnitManager
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.objects.managers.map_manager import MapManager
from AoE2ScenarioParser.objects.managers.player_manager import PlayerManager
from AoE2ScenarioParser.objects.managers.message_manager import MessageManager

from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers

from AoE2ScenarioParser.objects.managers.option_manager import OptionManager
from XS import john_galverg_XS
from AoE2ScenarioParser.datasets.support.info_dataset_base import InfoDatasetBase
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from data_tool import tech_define, object_define

from unicodedata import category
# Dictionnaire pour le script
from AoE2ScenarioParser.objects.support.area import Area




def start_of_the_game(scenario: AoE2DEScenario) :
    trigger_manager = scenario.trigger_manager
    # ------------------------------ SONS ------------------------------
    # hamish_1 = "Hamish_dial_1.wem"
    # hamish_2 = "Hamish_dial_2.wem"
    # Garry = "Galbert_1.wem"
    # Markus_1 = "Markus_1.wem"
    # Morange_1 = "Morange_1.wem"
    # Morange_2 = "Morange_2.wem"
    # Morange_3 = "Morange_3.wem"
    # Warmer_1 = "Warmer_1.wem"
    # Warmer_2 = "Warmer_2.wem"
    # Harris_1 = "Harris_1.wem"
    # Harris_2 = "Harris_2.wem"
    # John_1 = "John_1.wem"
    # John_2 = "John_2.wem"
    # John_3 = "John_3.wem"
    # John_4 = "John_4.wem"

    # ------------------------------ AVATARS (joueur, objet) ------------------------------
    JOHN = (PlayerId.ONE, UnitInfo.HAND_CANNONEER.ID)
    GARRY = (PlayerId.TWO, UnitInfo.MERCHANT.ID)
    MARKUS = (PlayerId.THREE, UnitInfo.SCOUT_CAVALRY.ID)
    MORRANGE = (PlayerId.FOUR, HeroInfo.CHARLEMAGNE.ID)
    HAMISH = (PlayerId.FIVE, HeroInfo.WILLIAM_WALLACE.ID)
    WARMER = (PlayerId.SIX, HeroInfo.SABOTEUR.ID)
    HARRIS = (PlayerId.SEVEN, HeroInfo.HARALD_HARDRADA.ID)

    SHORT = 15
    LONG = 30

    # ------------------------------ DIALOGUES ------------------------------
    dialogue_1 = "<AQUA> YOU PRINCESS MUT, COME HERE I SHOW YOU WHAT'S A REAL SWORD !"
    dialogue_2 = "<YELLOW>Morrange: Great idea to bring Maniacs to this mission John, someone hold him before he swing his sword at me"
    dialogue_3 = "<PURPLE>Warmer: Enough with your nonsense, the enemy is here, Harris stop looking at that rock and help us, you're pissing me off already !"
    dialogue_4 = "<GREY>Harris: Well you are never too sure.. Those kind of rock look friendly... THEN ! They murder you in your sleep."

    dialogue_5 = "<BLUE>John:  Gentlemen, Gentlemen, behave yourself ! If we want this exploration to be successful we have to be bounded and organize"
    dialogue_6 = "<YELLOW>Morrange: Say what you want John I'm not helping you scamming the resident of this place"
    dialogue_7 = "<BLUE>John: Morrange please... You should by now I'm just here to avenge my friend who die in this place... Markus status report, where are we ? What is the next path ?"
    dialogue_8 = "<GREEN>Markus: Hmmm... We... Well. If I take the median line and hmmm calibrate the position I... I think we are lost, I'm sorry I don't know where we are..."
    dialogue_9 = "<BLUE>John: What !? Do you mean you don't know where we are !? Markus ! I thought you were the man that could lead from point A to the Atlantic ocean"
    dialogue_10 = "<RED>Garry: Actually John I think this is quite expected. Ya. As we can observe this place is evolving as we speak and I believe the ruins is sensing something, So it's making this kind of protection YA ? Now you can see this rock and this palisade they weren't there before ! Oh I believe Markus' map are kinda outdated, so hmm what should we do boss ? I believe the best course of action is to dig it in right ?"
    dialogue_11 = "<BLUE>John: Well, that an information I wished to know sooner Garry... No matter *tick* if we want live we must act NOW ! Hamish Harris go forth and kill ! The rest do the same but with strategy. Warmer you got our back right ?"
    dialogue_12 = "<PURPLE>Warmer : Don't worry mister Galbert, my tower are ready to rain hell to these creatures ! HIN HIN HIN HAN! Just one thing, HARRIS ! You kill the creatures not the man next to you okay ? nah if you don't tell him he's gonna murder everyone because they speak too loud apparently"
    dialogue_13 = "<GREY>Harris : Don't worry cousin ! I already establish a very, very detail calculation to find what is not a monster and potential ally ! I got this right under the rug like we all say "
    dialogue_14 = "<YELLOW>Morrange: Uuuh is it too late to leave him here ? Like... I don't trust him."
    dialogue_15 = "<AQUA>Hamish : Lads ! You don't need to be worried. This one will jump in danger to save your arse ! He he, I am right Harris ? Harris... ? Where did he go ?"

    # ------------------------------ 1 : Hamish ------------------------------
    disable_targeting = [UnitInfo.MAN_AT_ARMS.ID,UnitInfo.LONG_SWORDSMAN.ID,UnitInfo.PIKEMAN.ID,UnitInfo.CROSSBOWMAN.ID,UnitInfo.SCORPION.ID,UnitInfo.SKIRMISHER.ID,UnitInfo.HAND_CANNONEER.ID,UnitInfo.KNIGHT.ID,UnitInfo.CAVALIER.ID,UnitInfo.MILITIA.ID,UnitInfo.SCOUT_CAVALRY.ID,UnitInfo.LIGHT_CAVALRY.ID,UnitInfo.VILLAGER_MALE.ID, UnitInfo.VILLAGER_FEMALE.ID]
    first_dialogue = trigger_manager.add_trigger(
        name="Harris is a crazy man",
        enabled=True,
        looping=False,
        execute_on_load=True,
    )
    for p in range (1,9):
        for y in range (len(disable_targeting)):
            first_dialogue.new_effect.disable_unit_targeting(
                source_player=p,
                object_list_unit_id=disable_targeting[y],
                area_x1 = 0,
                area_y1 = 0,
                area_y2 = 25,
                area_x2 = 36,
            )
            first_dialogue.new_effect.disable_unit_attackable(
                source_player=p,
                object_list_unit_id=disable_targeting[y],
                area_x1=0,
                area_y1=0,
                area_y2=25,
                area_x2=36,
            )
            first_dialogue.new_effect.disable_object_selection(
                source_player=p,
                object_list_unit_id=disable_targeting[y],
                area_x1=0,
                area_y1=0,
                area_y2=25,
                area_x2=36,
            )
    first_dialogue.new_effect.display_instructions(
        source_player=HAMISH[0],
        message=dialogue_1,
        # sound_name=hamish_1,
        object_list_unit_id=HAMISH[1],
        display_time=SHORT,
        instruction_panel_position=PanelLocation.TOP
    )

    # ------------------------------ 2 : Morrange ------------------------------
    second_dialogue = trigger_manager.add_trigger(
        name="french man from Bretagne ;)",
        enabled=True,
        looping=False,
        execute_on_load=False,
    )
    second_dialogue.new_condition.timer(
        timer=15,
    )
    second_dialogue.new_effect.display_instructions(
        source_player=MORRANGE[0],
        message=dialogue_2,
        # sound_name=Morange_1,
        display_time=SHORT,
        object_list_unit_id=MORRANGE[1],
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    # ------------------------------ 3 : Warmer ------------------------------
    third_dialogue = trigger_manager.add_trigger(
        name="Warmer is pissed off",
        enabled=True,
        looping=False,
        execute_on_load=False,
    )
    third_dialogue.new_condition.timer(
        timer=35,
    )
    third_dialogue.new_effect.display_instructions(
        source_player=WARMER[0],
        message=dialogue_3,
        # sound_name=Warmer_1,
        display_time=LONG,
        object_list_unit_id=WARMER[1],
        instruction_panel_position=PanelLocation.BOTTOM,
    )
    for p in range (1,9):
        for y in range (len(disable_targeting)):
            third_dialogue.new_effect.enable_unit_targeting(
                source_player=p,
                object_list_unit_id=disable_targeting[y],
                area_x1 = 0,
                area_y1 = 0,
                area_y2 = 25,
                area_x2 = 36,
            )
            third_dialogue.new_effect.enable_unit_attackable(
                source_player=p,
                object_list_unit_id=disable_targeting[y],
                area_x1=0,
                area_y1=0,
                area_y2=25,
                area_x2=36,
            )
            third_dialogue.new_effect.enable_object_selection(
                source_player=p,
                object_list_unit_id=disable_targeting[y],
                area_x1=0,
                area_y1=0,
                area_y2=25,
                area_x2=36,
            )
    for p in range (1,9):
        third_dialogue.new_effect.change_object_stance(
            source_player=p,
            area_x1=0,
            area_y1=0,
            area_y2=25,
            area_x2=36,
            attack_stance=AttackStance.AGGRESSIVE_STANCE,
        )
        third_dialogue.new_effect.change_diplomacy(
            source_player=PlayerId.EIGHT,
            target_player=p,
            diplomacy=DiplomacyState.ENEMY,
        )
        third_dialogue.new_effect.change_diplomacy(
            source_player=p,
            target_player=PlayerId.EIGHT,
            diplomacy=DiplomacyState.ENEMY,
        )
    third_dialogue.new_effect.remove_object(
        source_player=PlayerId.EIGHT,
        area_x1=0,
        area_y1=0,
        area_y2=25,
        area_x2=36,
        object_list_unit_id=UnitInfo.INVISIBLE_OBJECT_A.ID
    )

    # ------------------------------ 4 : Harris ------------------------------
    fourth_dialogue = trigger_manager.add_trigger(
        name="The rocks !",
        enabled=True,
        looping=False,
        execute_on_load=False,
    )
    fourth_dialogue.new_condition.timer(
        timer=70,
    )
    fourth_dialogue.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.MIDDLE
    )
    fourth_dialogue.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.TOP
    )
    fourth_dialogue.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.BOTTOM
    )
    fourth_dialogue.new_effect.display_instructions(
        source_player=HARRIS[0],
        message=dialogue_4,
        # sound_name=Harris_1,
        display_time=LONG,
        object_list_unit_id=HARRIS[1],
        instruction_panel_position=PanelLocation.TOP,
    )

    # ------------------------------ 5 : John ------------------------------
    fifth_dialogue = trigger_manager.add_trigger(
        name="John galber !",
        enabled=True,
        looping=False,
        execute_on_load=False,
    )
    fifth_dialogue.new_condition.timer(
        timer=85,
    )
    fifth_dialogue.new_effect.display_instructions(
        source_player=JOHN[0],
        message=dialogue_5,
        # sound_name=John_1,
        display_time=LONG,
        object_list_unit_id=JOHN[1],
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    # ------------------------------ 6 : Morrange ------------------------------
    six_dialogue = trigger_manager.add_trigger(
        name="Ok scammer",
        enabled=True,
        looping=False,
        execute_on_load=False,
    )
    six_dialogue.new_condition.timer(
        timer=100,
    )
    six_dialogue.new_effect.display_instructions(
        source_player=MORRANGE[0],
        message=dialogue_6,
        # sound_name=Morange_2,
        display_time=SHORT,
        object_list_unit_id=MORRANGE[1],
        instruction_panel_position=PanelLocation.BOTTOM,
    )

    # ------------------------------ 7 : John ------------------------------
    seven_dialogue = trigger_manager.add_trigger(
        name="Please Morrange",
        enabled=True,
        looping=False,
        execute_on_load=False,
    )
    seven_dialogue.new_condition.timer(
        timer=175,
    )
    seven_dialogue.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.MIDDLE
    )
    seven_dialogue.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.TOP
    )
    seven_dialogue.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.BOTTOM
    )
    seven_dialogue.new_effect.display_instructions(
        source_player=JOHN[0],
        message=dialogue_7,
        # sound_name=John_2,
        display_time=LONG,
        object_list_unit_id=JOHN[1],
        instruction_panel_position=PanelLocation.TOP,
    )

    # ------------------------------ 8 : Markus ------------------------------
    eight_dialogue = trigger_manager.add_trigger(
        name="Markus is lost",
        enabled=True,
        looping=False,
        execute_on_load=False,
    )
    eight_dialogue.new_condition.timer(
        timer=145,
    )
    eight_dialogue.new_effect.display_instructions(
        source_player=MARKUS[0],
        message=dialogue_8,
        # sound_name=Markus_1,
        display_time=LONG,
        object_list_unit_id=MARKUS[1],
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    # ------------------------------ 9 : John ------------------------------
    nine_dialogue = trigger_manager.add_trigger(
        name="John point A to Atlantic",
        enabled=True,
        looping=False,
        execute_on_load=False,
    )
    nine_dialogue.new_condition.timer(
        timer=175,
    )
    nine_dialogue.new_effect.display_instructions(
        source_player=JOHN[0],
        message=dialogue_9,
        # sound_name=John_3,
        display_time=LONG,
        object_list_unit_id=JOHN[1],
        instruction_panel_position=PanelLocation.BOTTOM,
    )

    # ------------------------------ 10 : Garry ------------------------------
    ten_dialogue = trigger_manager.add_trigger(
        name="Garry the ruins evolve",
        enabled=True,
        looping=False,
        execute_on_load=False,
    )
    ten_dialogue.new_condition.timer(
        timer=205,
    )
    ten_dialogue.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.MIDDLE
    )
    ten_dialogue.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.TOP
    )
    ten_dialogue.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.BOTTOM
    )
    ten_dialogue.new_effect.display_instructions(
        source_player=GARRY[0],
        message=dialogue_10,
        # sound_name=Garry,
        display_time=LONG,
        object_list_unit_id=GARRY[1],
        instruction_panel_position=PanelLocation.TOP,
    )

    # ------------------------------ 11 : John ------------------------------
    eleven_dialogue = trigger_manager.add_trigger(
        name="John act NOW",
        enabled=True,
        looping=False,
        execute_on_load=False,
    )
    eleven_dialogue.new_condition.timer(
        timer=235,
    )
    eleven_dialogue.new_effect.display_instructions(
        source_player=JOHN[0],
        message=dialogue_11,
        # sound_name=John_4,
        display_time=LONG,
        object_list_unit_id=JOHN[1],
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    # ------------------------------ 12 : Warmer ------------------------------
    twelve_dialogue = trigger_manager.add_trigger(
        name="Warmer towers ready",
        enabled=True,
        looping=False,
        execute_on_load=False,
    )
    twelve_dialogue.new_condition.timer(
        timer=265,
    )
    twelve_dialogue.new_effect.display_instructions(
        source_player=WARMER[0],
        message=dialogue_12,
        # sound_name=Warmer_2,
        display_time=LONG,
        object_list_unit_id=WARMER[1],
        instruction_panel_position=PanelLocation.BOTTOM,
    )

    # ------------------------------ 13 : Harris ------------------------------
    thirteen_dialogue = trigger_manager.add_trigger(
        name="Harris calculation",
        enabled=True,
        looping=False,
        execute_on_load=False,
    )
    thirteen_dialogue.new_condition.timer(
        timer=305,
    )
    thirteen_dialogue.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.MIDDLE
    )
    thirteen_dialogue.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.TOP
    )
    thirteen_dialogue.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.BOTTOM
    )
    thirteen_dialogue.new_effect.display_instructions(
        source_player=HARRIS[0],
        message=dialogue_13,
        # sound_name=Harris_2,
        display_time=LONG,
        object_list_unit_id=HARRIS[1],
        instruction_panel_position=PanelLocation.TOP,
    )

    # ------------------------------ 14 : Morrange ------------------------------
    fourteen_dialogue = trigger_manager.add_trigger(
        name="Morrange don't trust Harris",
        enabled=True,
        looping=False,
        execute_on_load=False,
    )
    fourteen_dialogue.new_condition.timer(
        timer=345,
    )
    fourteen_dialogue.new_effect.display_instructions(
        source_player=MORRANGE[0],
        message=dialogue_14,
        # sound_name=Morange_3,
        display_time=SHORT,
        object_list_unit_id=MORRANGE[1],
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    # ------------------------------ 15 : Hamish ------------------------------
    fifteen_dialogue = trigger_manager.add_trigger(
        name="Where is Harris ?",
        enabled=True,
        looping=False,
        execute_on_load=False,
    )
    fifteen_dialogue.new_condition.timer(
        timer=375,
    )
    fifteen_dialogue.new_effect.display_instructions(
        source_player=HAMISH[0],
        message=dialogue_15,
        # sound_name=hamish_2,
        display_time=LONG,
        object_list_unit_id=HAMISH[1],
        instruction_panel_position=PanelLocation.BOTTOM,
    )


def the_first_fortress(scenario: AoE2DEScenario):
    trigger_manager = scenario.trigger_manager
    SHORT = 15
    LONG = 30

    dial_1 = "<GREY>Harris: You cannot defeat me I am TWICE AS ANGRY AS YOU !! THAT BIG FORTRESS IS GOING DOWN !"
    dial_2 = "<YELLOW>Morrange : Woah Harris, hold yourself, maybe we should wait for the other to plan the assault first. That wasn't a question a Harris"

    fortress_1 = trigger_manager.add_trigger(
        name="The first fortress 1",
        enabled=False,
        looping=False,
    )
    fortress_1.new_effect.display_instructions(
        source_player=PlayerId.SEVEN,
        message=dial_1,
        display_time=SHORT,
        object_list_unit_id=HeroInfo.HARALD_HARDRADA.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    fortress_2 = trigger_manager.add_trigger(
        name="The first fortress 2",
        enabled=False,
        looping=False,
    )
    fortress_2.new_condition.timer(
        timer=15,
    )
    fortress_2.new_effect.display_instructions(
        source_player=PlayerId.FOUR,
        message=dial_2,
        display_time=LONG,
        object_list_unit_id=HeroInfo.CHARLEMAGNE.ID,
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    fortress_1.new_effect.activate_trigger(trigger_id=fortress_2.trigger_id)

    return fortress_1

def the_blackmist(scenario: AoE2DEScenario):
    trigger_manager = scenario.trigger_manager
    SHORT = 15
    LONG = 30

    dial_1 = "<BLUE>John : Markus ?"
    dial_2 = "<GREEN>Markus : I don't think that's the right path John ?"
    dial_3 = "<BLUE>John : Garry ?"
    dial_4 = "<RED>Garry : There seems to be a blacksmith ahead, maybe we can find some weapon"
    dial_5 = "<BLUE>John : Up to you just know that this place seems heavily protected !"

    arrival_1 = trigger_manager.add_trigger(
        name="Blackmist arrival 1",
        enabled=False,
        looping=False,
    )
    arrival_1.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=dial_1,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    arrival_2 = trigger_manager.add_trigger(
        name="Blackmist arrival 2",
        enabled=False,
        looping=False,
    )
    arrival_2.new_condition.timer(
        timer=15,
    )
    arrival_2.new_effect.display_instructions(
        source_player=PlayerId.THREE,
        message=dial_2,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.SCOUT_CAVALRY.ID,
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    arrival_3 = trigger_manager.add_trigger(
        name="Blackmist arrival 3",
        enabled=False,
        looping=False,
    )
    arrival_3.new_condition.timer(
        timer=30,
    )
    arrival_3.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=dial_3,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.BOTTOM,
    )

    arrival_4 = trigger_manager.add_trigger(
        name="Blackmist arrival 4",
        enabled=False,
        looping=False,
    )
    arrival_4.new_condition.timer(
        timer=45,
    )
    arrival_4.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.MIDDLE
    )
    arrival_4.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.TOP
    )
    arrival_4.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.BOTTOM
    )
    arrival_4.new_effect.display_instructions(
        source_player=PlayerId.TWO,
        message=dial_4,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.MERCHANT.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    arrival_5 = trigger_manager.add_trigger(
        name="Blackmist arrival 5",
        enabled=False,
        looping=False,
    )
    arrival_5.new_condition.timer(
        timer=60,
    )
    arrival_5.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=dial_5,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    arrival_1.new_effect.activate_trigger(trigger_id=arrival_2.trigger_id)
    arrival_1.new_effect.activate_trigger(trigger_id=arrival_3.trigger_id)
    arrival_1.new_effect.activate_trigger(trigger_id=arrival_4.trigger_id)
    arrival_1.new_effect.activate_trigger(trigger_id=arrival_5.trigger_id)

    after_dial_1 = "<GREEN>Garry would you look at that all sort of weapons and armor !"
    after_dial_2 = "<BLUE>John : Yeah this is good for the expedition we can use those and replace our rusty WHAAAAAAA !!!"
    after_dial_3 = "<ORANGE>Blacksmith : WE TA KE LE ME KO TO DO THI § KO LI KI ! HEH KO LI KI !"
    after_dial_4 = "<BLUE>John : WOAH WOAH WOAH CALM DOWN ! We don't want to fight you ! *someone shoot him please*"
    after_dial_5 = "<RED>Garry : No wait ! I think this person is the owner of this place, I can probably talk to him "
    after_dial_6 = "<RED>Garry : This is going to be rusty : Ko le kis te ke mos... hmmm... Ah tekerenos to ki lis ebekes ?"
    after_dial_7 = "<ORANGE>Blacksmith : ... Kemetos to kasatra ka me tekoros he ? Ko me tekeros "
    after_dial_8 = "<RED>Garry : He's wondering why aren't we affected by the curse and what are we doing here ?"
    after_dial_9 = "<BLUE>John : ask him about the damn direction !"
    after_dial_10 = "<RED>Garry : Kemounos del... how can I say direction.... hmmm... Kemetos ke takarata ke el kemetos ahbaj ke tonimiki ?"
    after_dial_11 = "<ORANGE>Blacksmith : KAMA ME TUKU SERA ! KEMETAKA MEH KO KAL KE ! Meteke te kesuros del ALEOHOP KEMETU ! Ko me ku ke soto !"
    after_dial_12 = "<RED>Garry : he said to continue through the jungle to the north , also he will forge us new weapon as long as we bring him those weird stone"
    after_dial_13 = "<BLUE>John : Every bit of help is welcome, thank him and let's go"
    after_dial_14 = "<RED>Garry : Komo del ka, Komo del ka"

    forge_1 = trigger_manager.add_trigger(
        name="Blackmist forge 1",
        enabled=False,
        looping=False,
    )
    forge_1.new_effect.display_instructions(
        source_player=PlayerId.THREE,
        message=after_dial_1,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.SCOUT_CAVALRY.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    forge_2 = trigger_manager.add_trigger(
        name="Blackmist forge 2",
        enabled=False,
        looping=False,
    )
    forge_2.new_condition.timer(
        timer=15,
    )
    forge_2.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=after_dial_2,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    forge_3 = trigger_manager.add_trigger(
        name="Blackmist forge 3",
        enabled=False,
        looping=False,
    )
    forge_3.new_condition.timer(
        timer=30,
    )
    forge_3.new_effect.display_instructions(
        source_player=PlayerId.EIGHT,
        message=after_dial_3,
        display_time=LONG,
        object_list_unit_id=UnitInfo.VILLAGER_MALE_BUILDER.ID,
        instruction_panel_position=PanelLocation.BOTTOM,
    )

    forge_4 = trigger_manager.add_trigger(
        name="Blackmist forge 4",
        enabled=False,
        looping=False,
    )
    forge_4.new_condition.timer(
        timer=60,
    )
    forge_4.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.MIDDLE
    )
    forge_4.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.TOP
    )
    forge_4.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.BOTTOM
    )
    forge_4.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=after_dial_4,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    forge_5 = trigger_manager.add_trigger(
        name="Blackmist forge 5",
        enabled=False,
        looping=False,
    )
    forge_5.new_condition.timer(
        timer=75,
    )
    forge_5.new_effect.display_instructions(
        source_player=PlayerId.TWO,
        message=after_dial_5,
        display_time=LONG,
        object_list_unit_id=UnitInfo.MERCHANT.ID,
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    forge_6 = trigger_manager.add_trigger(
        name="Blackmist forge 6",
        enabled=False,
        looping=False,
    )
    forge_6.new_condition.timer(
        timer=105,
    )
    forge_6.new_effect.display_instructions(
        source_player=PlayerId.TWO,
        message=after_dial_6,
        display_time=LONG,
        object_list_unit_id=UnitInfo.MERCHANT.ID,
        instruction_panel_position=PanelLocation.BOTTOM,
    )

    forge_7 = trigger_manager.add_trigger(
        name="Blackmist forge 7",
        enabled=False,
        looping=False,
    )
    forge_7.new_condition.timer(
        timer=135,
    )
    forge_7.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.MIDDLE
    )
    forge_7.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.TOP
    )
    forge_7.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.BOTTOM
    )
    forge_7.new_effect.display_instructions(
        source_player=PlayerId.EIGHT,
        message=after_dial_7,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.VILLAGER_MALE_BUILDER.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    forge_8 = trigger_manager.add_trigger(
        name="Blackmist forge 8",
        enabled=False,
        looping=False,
    )
    forge_8.new_condition.timer(
        timer=150,
    )
    forge_8.new_effect.display_instructions(
        source_player=PlayerId.TWO,
        message=after_dial_8,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.MERCHANT.ID,
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    forge_9 = trigger_manager.add_trigger(
        name="Blackmist forge 9",
        enabled=False,
        looping=False,
    )
    forge_9.new_condition.timer(
        timer=165,
    )
    forge_9.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=after_dial_9,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.BOTTOM,
    )

    forge_10 = trigger_manager.add_trigger(
        name="Blackmist forge 10",
        enabled=False,
        looping=False,
    )
    forge_10.new_condition.timer(
        timer=180,
    )
    forge_10.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.MIDDLE
    )
    forge_10.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.TOP
    )
    forge_10.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.BOTTOM
    )
    forge_10.new_effect.display_instructions(
        source_player=PlayerId.TWO,
        message=after_dial_10,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.MERCHANT.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    forge_11 = trigger_manager.add_trigger(
        name="Blackmist forge 11",
        enabled=False,
        looping=False,
    )
    forge_11.new_condition.timer(
        timer=195,
    )
    forge_11.new_effect.display_instructions(
        source_player=PlayerId.EIGHT,
        message=after_dial_11,
        display_time=LONG,
        object_list_unit_id=UnitInfo.VILLAGER_MALE_BUILDER.ID,
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    forge_12 = trigger_manager.add_trigger(
        name="Blackmist forge 12",
        enabled=False,
        looping=False,
    )
    forge_12.new_condition.timer(
        timer=225,
    )
    forge_12.new_effect.display_instructions(
        source_player=PlayerId.TWO,
        message=after_dial_12,
        display_time=LONG,
        object_list_unit_id=UnitInfo.MERCHANT.ID,
        instruction_panel_position=PanelLocation.BOTTOM,
    )

    forge_13 = trigger_manager.add_trigger(
        name="Blackmist forge 13",
        enabled=False,
        looping=False,
    )
    forge_13.new_condition.timer(
        timer=255,
    )
    forge_13.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.MIDDLE
    )
    forge_13.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.TOP
    )
    forge_13.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.BOTTOM
    )
    forge_13.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=after_dial_13,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    forge_14 = trigger_manager.add_trigger(
        name="Blackmist forge 14",
        enabled=False,
        looping=False,
    )
    forge_14.new_condition.timer(
        timer=270,
    )
    forge_14.new_effect.display_instructions(
        source_player=PlayerId.TWO,
        message=after_dial_14,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.MERCHANT.ID,
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    forge_1.new_effect.activate_trigger(trigger_id=forge_2.trigger_id)
    forge_1.new_effect.activate_trigger(trigger_id=forge_3.trigger_id)
    forge_1.new_effect.activate_trigger(trigger_id=forge_4.trigger_id)
    forge_1.new_effect.activate_trigger(trigger_id=forge_5.trigger_id)
    forge_1.new_effect.activate_trigger(trigger_id=forge_6.trigger_id)
    forge_1.new_effect.activate_trigger(trigger_id=forge_7.trigger_id)
    forge_1.new_effect.activate_trigger(trigger_id=forge_8.trigger_id)
    forge_1.new_effect.activate_trigger(trigger_id=forge_9.trigger_id)
    forge_1.new_effect.activate_trigger(trigger_id=forge_10.trigger_id)
    forge_1.new_effect.activate_trigger(trigger_id=forge_11.trigger_id)
    forge_1.new_effect.activate_trigger(trigger_id=forge_12.trigger_id)
    forge_1.new_effect.activate_trigger(trigger_id=forge_13.trigger_id)
    forge_1.new_effect.activate_trigger(trigger_id=forge_14.trigger_id)

    return arrival_1, forge_1


def middle_area(scenario: AoE2DEScenario):
    trigger_manager = scenario.trigger_manager
    SHORT = 15
    LONG = 30

    dial_1 = "<RED>Garry : Careful boys, this area is very dangerous ! As soon as we step in all those barracks will launch their monsters at us !"
    dial_2 = "<BLUE>John : Alright everyone time to plan this attack ! Get the siege and soldiers ready for a huge fight !"

    mid_1 = trigger_manager.add_trigger(
        name="Middle area 1",
        enabled=False,
        looping=False,
    )
    mid_1.new_effect.display_instructions(
        source_player=PlayerId.TWO,
        message=dial_1,
        display_time=LONG,
        object_list_unit_id=UnitInfo.MERCHANT.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    mid_2 = trigger_manager.add_trigger(
        name="Middle area 2",
        enabled=False,
        looping=False,
    )
    mid_2.new_condition.timer(
        timer=30,
    )
    mid_2.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=dial_2,
        display_time=LONG,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    mid_1.new_effect.activate_trigger(trigger_id=mid_2.trigger_id)

    return mid_1


def jungle_fortress(scenario: AoE2DEScenario):
    trigger_manager = scenario.trigger_manager
    SHORT = 15
    LONG = 30

    dial_1 = "<BLUE>John : Another fortress down, we are doing great so far !"
    dial_2 = "<WHITE>Old man : Do not get ahead of yourself mister Galbert !"
    dial_3 = "<AQUA>Hamish : ARF dying man !"
    dial_4 = "<BLUE>John : What the what ? Who are you ?"
    dial_5 = "<WHITE>Old man : I'm only a priest of this place John, the gods and I welcome you to our humble domain"
    dial_6 = "<BLUE>John : For a priest living here you sure know english !"
    dial_7 = "<WHITE>Old man : I've learned it from the gods, so I can speak to you John, you and your team are the last hope of this place"
    dial_8 = "<BLUE>John : Are we now ?"
    dial_9 = "<WHITE>Old man : Our king in the seek of power has created the curse and now the world is at risk, you have proven yourself capable of fixing it, although your motives aren't noble, you with your team can save us"
    dial_10 = "<BLUE>John : Ok and where do we go old man ?"
    dial_11 = "<WHITE>Old man : To the north, you must fight your way in, I can help you, come to my shop, some of my relics can help you but watch out for the consequences"
    dial_12 = "<BLUE>John : Yeaaaah... right..."
    dial_13 = "<RED>Garry : OH OH ! Cool history stuff please let me take a look"

    jungle_1 = trigger_manager.add_trigger(
        name="Jungle fortress dialogue 1",
        enabled=False,
        looping=False,
    )
    jungle_1.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=dial_1,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    jungle_2 = trigger_manager.add_trigger(
        name="Jungle fortress dialogue 2",
        enabled=False,
        looping=False,
    )
    jungle_2.new_condition.timer(
        timer=15,
    )
    jungle_2.new_effect.display_instructions(
        source_player=PlayerId.GAIA,
        message=dial_2,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.MONK.ID,
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    jungle_3 = trigger_manager.add_trigger(
        name="Jungle fortress dialogue 3",
        enabled=False,
        looping=False,
    )
    jungle_3.new_condition.timer(
        timer=30,
    )
    jungle_3.new_effect.display_instructions(
        source_player=PlayerId.FIVE,
        message=dial_3,
        display_time=SHORT,
        object_list_unit_id=HeroInfo.WILLIAM_WALLACE.ID,
        instruction_panel_position=PanelLocation.BOTTOM,
    )

    jungle_4 = trigger_manager.add_trigger(
        name="Jungle fortress dialogue 4",
        enabled=False,
        looping=False,
    )
    jungle_4.new_condition.timer(
        timer=45,
    )
    jungle_4.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.MIDDLE
    )
    jungle_4.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.TOP
    )
    jungle_4.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.BOTTOM
    )
    jungle_4.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=dial_4,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    jungle_5 = trigger_manager.add_trigger(
        name="Jungle fortress dialogue 5",
        enabled=False,
        looping=False,
    )
    jungle_5.new_condition.timer(
        timer=60,
    )
    jungle_5.new_effect.display_instructions(
        source_player=PlayerId.GAIA,
        message=dial_5,
        display_time=LONG,
        object_list_unit_id=UnitInfo.MONK.ID,
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    jungle_6 = trigger_manager.add_trigger(
        name="Jungle fortress dialogue 6",
        enabled=False,
        looping=False,
    )
    jungle_6.new_condition.timer(
        timer=90,
    )
    jungle_6.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=dial_6,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.BOTTOM,
    )

    jungle_7 = trigger_manager.add_trigger(
        name="Jungle fortress dialogue 7",
        enabled=False,
        looping=False,
    )
    jungle_7.new_condition.timer(
        timer=105,
    )
    jungle_7.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.MIDDLE
    )
    jungle_7.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.TOP
    )
    jungle_7.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.BOTTOM
    )
    jungle_7.new_effect.display_instructions(
        source_player=PlayerId.GAIA,
        message=dial_7,
        display_time=LONG,
        object_list_unit_id=UnitInfo.MONK.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    jungle_8 = trigger_manager.add_trigger(
        name="Jungle fortress dialogue 8",
        enabled=False,
        looping=False,
    )
    jungle_8.new_condition.timer(
        timer=135,
    )
    jungle_8.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=dial_8,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    jungle_9 = trigger_manager.add_trigger(
        name="Jungle fortress dialogue 9",
        enabled=False,
        looping=False,
    )
    jungle_9.new_condition.timer(
        timer=150,
    )
    jungle_9.new_effect.display_instructions(
        source_player=PlayerId.GAIA,
        message=dial_9,
        display_time=LONG,
        object_list_unit_id=UnitInfo.MONK.ID,
        instruction_panel_position=PanelLocation.BOTTOM,
    )

    jungle_10 = trigger_manager.add_trigger(
        name="Jungle fortress dialogue 10",
        enabled=False,
        looping=False,
    )
    jungle_10.new_condition.timer(
        timer=180,
    )
    jungle_10.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.MIDDLE
    )
    jungle_10.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.TOP
    )
    jungle_10.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.BOTTOM
    )
    jungle_10.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=dial_10,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    jungle_11 = trigger_manager.add_trigger(
        name="Jungle fortress dialogue 11",
        enabled=False,
        looping=False,
    )
    jungle_11.new_condition.timer(
        timer=195,
    )
    jungle_11.new_effect.display_instructions(
        source_player=PlayerId.GAIA,
        message=dial_11,
        display_time=LONG,
        object_list_unit_id=UnitInfo.MONK.ID,
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    jungle_12 = trigger_manager.add_trigger(
        name="Jungle fortress dialogue 12",
        enabled=False,
        looping=False,
    )
    jungle_12.new_condition.timer(
        timer=225,
    )
    jungle_12.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=dial_12,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.BOTTOM,
    )

    jungle_13 = trigger_manager.add_trigger(
        name="Jungle fortress dialogue 13",
        enabled=False,
        looping=False,
    )
    jungle_13.new_condition.timer(
        timer=240,
    )
    jungle_13.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.MIDDLE
    )
    jungle_13.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.TOP
    )
    jungle_13.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.BOTTOM
    )
    jungle_13.new_effect.display_instructions(
        source_player=PlayerId.TWO,
        message=dial_13,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.MERCHANT.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    jungle_1.new_effect.activate_trigger(trigger_id=jungle_2.trigger_id)
    jungle_1.new_effect.activate_trigger(trigger_id=jungle_3.trigger_id)
    jungle_1.new_effect.activate_trigger(trigger_id=jungle_4.trigger_id)
    jungle_1.new_effect.activate_trigger(trigger_id=jungle_5.trigger_id)
    jungle_1.new_effect.activate_trigger(trigger_id=jungle_6.trigger_id)
    jungle_1.new_effect.activate_trigger(trigger_id=jungle_7.trigger_id)
    jungle_1.new_effect.activate_trigger(trigger_id=jungle_8.trigger_id)
    jungle_1.new_effect.activate_trigger(trigger_id=jungle_9.trigger_id)
    jungle_1.new_effect.activate_trigger(trigger_id=jungle_10.trigger_id)
    jungle_1.new_effect.activate_trigger(trigger_id=jungle_11.trigger_id)
    jungle_1.new_effect.activate_trigger(trigger_id=jungle_12.trigger_id)
    jungle_1.new_effect.activate_trigger(trigger_id=jungle_13.trigger_id)

    return jungle_1


def last_area(scenario: AoE2DEScenario):
    trigger_manager = scenario.trigger_manager
    SHORT = 15
    LONG = 30

    dial_1 = "<GREEN>Markus : John this is it, the source of the curse"
    dial_2 = "<BLUE>John : Garry ! Analysis !"
    dial_3 = "<RED>Garry : Just destroy the huge building, the relic loses its base and the curse stops"
    dial_4 = "<GREY>Harris : Let's go ! I wanna break someone's skull"
    dial_5 = "<PURPLE>Warmer : Cousin's right, we can't delay too much !"
    dial_6 = "<BLUE>John : Time to finish this !"

    last_1 = trigger_manager.add_trigger(
        name="Last area 1",
        enabled=False,
        looping=False,
    )
    last_1.new_effect.display_instructions(
        source_player=PlayerId.THREE,
        message=dial_1,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.SCOUT_CAVALRY.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    last_2 = trigger_manager.add_trigger(
        name="Last area 2",
        enabled=False,
        looping=False,
    )
    last_2.new_condition.timer(
        timer=15,
    )
    last_2.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=dial_2,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    last_3 = trigger_manager.add_trigger(
        name="Last area 3",
        enabled=False,
        looping=False,
    )
    last_3.new_condition.timer(
        timer=30,
    )
    last_3.new_effect.display_instructions(
        source_player=PlayerId.TWO,
        message=dial_3,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.MERCHANT.ID,
        instruction_panel_position=PanelLocation.BOTTOM,
    )

    last_4 = trigger_manager.add_trigger(
        name="Last area 4",
        enabled=False,
        looping=False,
    )
    last_4.new_condition.timer(
        timer=45,
    )
    last_4.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.MIDDLE
    )
    last_4.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.TOP
    )
    last_4.new_effect.clear_instructions(
        instruction_panel_position=PanelLocation.BOTTOM
    )
    last_4.new_effect.display_instructions(
        source_player=PlayerId.SEVEN,
        message=dial_4,
        display_time=SHORT,
        object_list_unit_id=HeroInfo.HARALD_HARDRADA.ID,
        instruction_panel_position=PanelLocation.TOP,
    )

    last_5 = trigger_manager.add_trigger(
        name="Last area 5",
        enabled=False,
        looping=False,
    )
    last_5.new_condition.timer(
        timer=60,
    )
    last_5.new_effect.display_instructions(
        source_player=PlayerId.SIX,
        message=dial_5,
        display_time=SHORT,
        object_list_unit_id=HeroInfo.SABOTEUR.ID,
        instruction_panel_position=PanelLocation.MIDDLE,
    )

    last_6 = trigger_manager.add_trigger(
        name="Last area 6",
        enabled=False,
        looping=False,
    )
    last_6.new_condition.timer(
        timer=75,
    )
    last_6.new_effect.display_instructions(
        source_player=PlayerId.ONE,
        message=dial_6,
        display_time=SHORT,
        object_list_unit_id=UnitInfo.HAND_CANNONEER.ID,
        instruction_panel_position=PanelLocation.BOTTOM,
    )

    last_1.new_effect.activate_trigger(trigger_id=last_2.trigger_id)
    last_1.new_effect.activate_trigger(trigger_id=last_3.trigger_id)
    last_1.new_effect.activate_trigger(trigger_id=last_4.trigger_id)
    last_1.new_effect.activate_trigger(trigger_id=last_5.trigger_id)
    last_1.new_effect.activate_trigger(trigger_id=last_6.trigger_id)

    return last_1