from dataclasses import dataclass

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
@dataclass
class technology_setup:
    name: str
    description : str
    research_time : int
    tech_id : int
    location : int
    button : int
    player : int
    enabled : bool
    cost_type : tuple
    cost_quantity : tuple
    icon_id : int
@dataclass
class object_setup:
    name: str
    description : str
    object : int
    building : int
    button : int
    player : int
    enabled_object : bool
    cost_type : tuple
    cost_quantity : tuple

def John_Galverb(scenario,trigger_manager):
    player = PlayerId.ONE
    set_up_blue_tech = [
    technology_setup(
        name="Dispatch the management",
        description="Research dispatch the management : allow you to create two extra expedition manager per research",
        tech_id =TechInfo.BLANK_TECHNOLOGY_0.ID,
        location=BuildingInfo.TENT_C.ID,
        button=1,
        enabled=True,
        player=player,
        research_time=10,
        cost_type=(Attribute.UNUSED_RESOURCE_498, None),
        cost_quantity=(1, None),
        icon_id = 19,
    ),
    technology_setup(
        name="Economie direction",
        description="Research economy direction : The workrate aura granted by the Expedition Manager is increased by 5%.",
        tech_id=TechInfo.BLANK_TECHNOLOGY_1.ID,
        location=BuildingInfo.TENT_C.ID,
        button=2,
        enabled=True,
        player=player,
        research_time=10,
        cost_type=(Attribute.UNUSED_RESOURCE_498, None),
        cost_quantity=(1, None),
        icon_id=114,
    ),
    technology_setup(
        name="Troop management",
        description="Research troop management : Healing aura effect of the expedition manager for military unit is increased by 5%, attack speed of military unit arround the expedition manager is increased by 4%",
        tech_id=TechInfo.BLANK_TECHNOLOGY_2.ID,
        location=BuildingInfo.TENT_C.ID,
        button=3,
        enabled=True,
        player=player,
        research_time=10,
        cost_type=(Attribute.UNUSED_RESOURCE_498, None),
        cost_quantity=(1, None),
        icon_id=44,
    ),
    technology_setup(
        name="extend the peremiters of action",
        description="Research extend the peremiters of action : expedition manager aura range is increased by 2 tiles ",
        tech_id=TechInfo.BLANK_TECHNOLOGY_3.ID,
        location=BuildingInfo.TENT_C.ID,
        button=4,
        enabled=True,
        player=player,
        research_time=10,
        cost_type=(Attribute.UNUSED_RESOURCE_498,None),
        cost_quantity=(1, None),
        icon_id=164,
    )
    ]
    set_up_blue_object = [
        object_setup(
            object=UnitInfo.KING.ID,
            name="Expedition manager",
            description="Create expedition manager <cost> : Certified manager by john itself, there aura effect make your villagers work faster, heal your military and make then attack faster",
            building=BuildingInfo.TENT_C.ID,
            button=6,
            enabled_object=True,
            player=player,
            cost_type =(Attribute.FOOD_STORAGE,Attribute.GOLD_STORAGE),
            cost_quantity=(250,100),
        ),
        object_setup(
            object=BuildingInfo.TENT_C .ID,
            name="Expedition tent",
            description="Create expedition tent <cost> : John Galverb expedition tent, John is able to create expedition manager from is tent and upgrade then with skill point",
            building=UnitInfo.VILLAGER_MALE.ID,
            button=8,
            enabled_object=True,
            player=player,
            cost_type=(Attribute.WOOD_STORAGE, Attribute.STONE_STORAGE),
            cost_quantity=(200, 75),
        ),
    ]
    shared_trigger = None
    for cfg in set_up_blue_tech:
        shared_trigger = tech_define(
            scenario,
            trigger_manager,
            name=cfg.name,
            description=cfg.description,
            tech_id=cfg.tech_id,
            player=cfg.player,
            location=cfg.location,
            button=cfg.button,
            enabled=cfg.enabled,
            research_time=cfg.research_time,
            cost_quantity=cfg.cost_quantity,
            cost_type=cfg.cost_type,
            trigger=shared_trigger,
            icon_id= cfg.icon_id,
        )
    for cfg in set_up_blue_object:
        shared_trigger = object_define(
            scenario,
            trigger_manager,
            name=cfg.name,
            description=cfg.description,
            object=cfg.object,
            player=cfg.player,
            building=cfg.building,
            button=cfg.button,
            enabled_object=cfg.enabled_object,
            cost_quantity=cfg.cost_quantity,
            cost_type=cfg.cost_type,
            trigger=shared_trigger,
        )
    john_galverg_XS()
    shared_trigger.new_effect.script_call(
        message="setup_aura_blue();"
    )
    joh_tech_list = [(TechInfo.BLANK_TECHNOLOGY_0.ID,"dispatch_management();"),(TechInfo.BLANK_TECHNOLOGY_1.ID,"economy_direction();"),
                     (TechInfo.BLANK_TECHNOLOGY_2.ID,"troop_management();"),(TechInfo.BLANK_TECHNOLOGY_3.ID,"extend_peremiters();")]
    for i in range (len(joh_tech_list)):
        tech,xs = joh_tech_list[i]
        technology_bonus_john = trigger_manager.add_trigger(
            name=f"John tech {tech}",
            enabled=True,
            looping=True,
            execute_on_load=True,
        )
        technology_bonus_john.new_condition.research_technology(
            source_player=player,
            technology=tech,
        )
        technology_bonus_john.new_effect.script_call(
            message=xs,
        )
        technology_bonus_john.new_effect.enable_disable_technology(
            technology=tech,
            enabled=False,
            source_player=player,
        )
        technology_bonus_john.new_effect.enable_disable_technology(
            technology=tech,
            enabled=True,
            source_player=player,
        )

def Gary_buerg(scenario,trigger_manager):
    player = PlayerId.TWO
    set_up_red_tech = [
        technology_setup(
            name="Digging for treasure",
            description="Start digging for treasure <cost> : Once this tech is finished you get a relic, side note : note that there is a fix cycle of digging that allow you to get more relic with this tech, cycle repeat itself",
            tech_id=TechInfo.LOOM.ID,
            location=BuildingInfo.TENT_C.ID,
            button=1,
            enabled=True,
            player=player,
            research_time=10,
            cost_type=(Attribute.GOLD_STORAGE, None),
            cost_quantity=(2500, None),
            icon_id=19,
        ),
    ]
    set_up_red_object = [
        object_setup(
            object=BuildingInfo.TENT_C.ID,
            name="Expedition tent",
            description="Create expedition tent <cost> : Gary Buerg expedition tent, Gary tent is equiped with a 7800 powermax drill that will drill for relic on any soil",
            building=UnitInfo.VILLAGER_MALE.ID,
            button=8,
            enabled_object=True,
            player=player,
            cost_type=(Attribute.WOOD_STORAGE, Attribute.STONE_STORAGE),
            cost_quantity=(200, 75),
        ),
    ]
    shared_trigger = None
    for cfg in set_up_red_tech:
        shared_trigger = tech_define(
            scenario,
            trigger_manager,
            name=cfg.name,
            description=cfg.description,
            tech_id=cfg.tech_id,
            player=cfg.player,
            location=cfg.location,
            button=cfg.button,
            enabled=cfg.enabled,
            research_time=cfg.research_time,
            cost_quantity=cfg.cost_quantity,
            cost_type=cfg.cost_type,
            trigger=shared_trigger,
            icon_id=cfg.icon_id,
        )
    for cfg in set_up_red_object:
        shared_trigger = object_define(
            scenario,
            trigger_manager,
            name=cfg.name,
            description=cfg.description,
            object=cfg.object,
            player=cfg.player,
            building=cfg.building,
            button=cfg.button,
            enabled_object=cfg.enabled_object,
            cost_quantity=cfg.cost_quantity,
            cost_type=cfg.cost_type,
            trigger=shared_trigger,
        )
    shared_trigger.new_effect.script_call(
        message="setup_gary();"
    )
    drill_cycle = trigger_manager.add_trigger(
        name="drill cycle count",
        enabled=True,
        looping=True,
        execute_on_load=True,
    )
    drill_cycle.new_condition.research_technology(
        technology=TechInfo.BLANK_TECHNOLOGY_0.ID,
        source_player=player,
    )
    drill_cycle.new_effect.enable_disable_technology(
        source_player=player,
        technology=TechInfo.BLANK_TECHNOLOGY_0.ID,
        enabled=False,
    )
    drill_cycle.new_effect.enable_disable_technology(
        source_player=player,
        technology=TechInfo.BLANK_TECHNOLOGY_0.ID,
        enabled=True,
    )
    drill_cycle.new_effect.script_call(
        message="drill_reward();"
    )
