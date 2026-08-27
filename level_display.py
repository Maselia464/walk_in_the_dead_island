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

from AoE2ScenarioParser.datasets.support.info_dataset_base import InfoDatasetBase
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario



from unicodedata import category
# Dictionnaire pour le script
from AoE2ScenarioParser.objects.support.area import Area
def level_display(scenario,trigger_manager):
    level_display_trigger = trigger_manager.add_trigger(
        name=f"list player level",
        enabled=True,
        looping=False,
        execute_on_load=True,
        short_description=f"---Player level---",
        description_order=50,
        display_on_screen=True,
        description=f"---Player level---",
        display_as_objective=True
    )
    level_display_trigger.new_condition.accumulate_attribute(
        source_player=PlayerId.EIGHT,
        attribute=Attribute.UNUSED_RESOURCE_200,
        quantity=10000,
    )
    for p in range (1,8):
        description_order = 50 - p
        if p == PlayerId.ONE:
            variable_1 = 1
            variable_2 = 2
            variable_3 = 3
            color = "Blue"
        elif p == PlayerId.TWO:
            variable_1 = 4
            variable_2 = 5
            variable_3 = 6
            color = "Red"
        elif p == PlayerId.THREE:
            variable_1 = 7
            variable_2 = 8
            variable_3 = 9
            color = "Green"
        elif p == PlayerId.FOUR:
            variable_1 = 10
            variable_2 = 11
            variable_3 = 12
            color = "Yellow"
        elif p == PlayerId.FIVE:
            variable_1 = 13
            variable_2 = 14
            variable_3 = 15
            color = "Aqua"
        elif p == PlayerId.SIX:
            variable_1 = 16
            variable_2 = 17
            variable_3 = 18
            color = "Purple"
        elif p == PlayerId.SEVEN:
            variable_1 = 19
            variable_2 = 20
            variable_3 = 21
            color = "Grey"
        else :
            variable_1 = 0
            variable_2 = 0
            variable_3 = 0
            color = "Fuck you"
        level_display_trigger = trigger_manager.add_trigger(
            name=f"Level display for p{p}",
            enabled=True,
            looping=False,
            execute_on_load=True,
            short_description=f"{color} current level : <Variable {variable_1}>\nRequired XP for next level <Variable {variable_3}>\ <Variable {variable_2}> ",
            description_order=description_order,
            display_on_screen=True,
            description=f"{color} current level : <Variable {variable_1}>\nNext level in : <Variable {variable_3}>\ <Variable {variable_2}> ",
            display_as_objective=True
        )
        level_display_trigger.new_condition.accumulate_attribute(
            source_player=PlayerId.EIGHT,
            attribute=Attribute.UNUSED_RESOURCE_200,
            quantity=10000,
        )
