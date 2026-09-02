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

def Markus_skoliose (scenario,trigger_manager):
    player = PlayerId.THREE
    shared_trigger = None
    set_up_green_tech = [
        technology_setup(
            name="Soil science",
            description="Research soil science : building cost is reduce by 5%, the reduction rate increase by 5% for each tehc you took before this one in the expedition tent",
            tech_id=TechInfo.BLANK_TECHNOLOGY_0.ID,
            location=BuildingInfo.TENT_C.ID,
            button=1,
            enabled=True,
            player=player,
            research_time=20,
            cost_type=(Attribute.UNUSED_RESOURCE_498, None),
            cost_quantity=(1, None),
            icon_id=5,
        ),
        technology_setup(
            name="Identify the vintage point",
            description="Identify the vintage point : towers bombard towers and donjon get +1 range and +1 attacks, you get +1 extra range and attack for every tech you took before this one on the expedition tent",
            tech_id=TechInfo.BLANK_TECHNOLOGY_1.ID,
            location=BuildingInfo.TENT_C.ID,
            button=2,
            enabled=True,
            player=player,
            research_time=20,
            cost_type=(Attribute.UNUSED_RESOURCE_498, None),
            cost_quantity=(1, None),
            icon_id=69,
        ),
        technology_setup(
            name="Cartograph defensive gear",
            description="Research cartograph defensive gear : Archer and infantry units gain +1 armor and piercing armor, +1 extra armor point for each tech you took before this one",
            tech_id=TechInfo.BLANK_TECHNOLOGY_2.ID,
            location=BuildingInfo.TENT_C.ID,
            button=3,
            enabled=True,
            player=player,
            research_time=20,
            cost_type=(Attribute.UNUSED_RESOURCE_498, None),
            cost_quantity=(1, None),
            icon_id=170,
        ),
        technology_setup(
            name="Drawing the median line",
            description="Drawing the median line : you get 2 extra skill points to spend on other temple and plus 2 extra one for each tech you took before this one in the expedition tent",
            tech_id=TechInfo.BLANK_TECHNOLOGY_3.ID,
            location=BuildingInfo.TENT_C.ID,
            button=4,
            enabled=True,
            player=player,
            research_time=20,
            cost_type=(Attribute.UNUSED_RESOURCE_498, None),
            cost_quantity=(1, None),
            icon_id=4,
        ),
        technology_setup(
            name="Establish commercial road",
            description="Establish commercial road : trade cart workrate bring 10% more gold and extra 10% per tech you research before this one in the expedition tent",
            tech_id=TechInfo.BLANK_TECHNOLOGY_4.ID,
            location=BuildingInfo.TENT_C.ID,
            button=5,
            enabled=True,
            player=player,
            research_time=20,
            cost_type=(Attribute.UNUSED_RESOURCE_498, None),
            cost_quantity=(1, None),
            icon_id=113,
        ),
        technology_setup(
            name="Clearing the path",
            description="Clearing the path : You received 1 saboteur capable to removing rocks to clear a path and one extra saboteur for each tech you search in the expedition tent before this one",
            tech_id=TechInfo.BLANK_TECHNOLOGY_5.ID,
            location=BuildingInfo.TENT_C.ID,
            button=6,
            enabled=True,
            player=player,
            research_time=20,
            cost_type=(Attribute.UNUSED_RESOURCE_498, None),
            cost_quantity=(1, None),
            icon_id=312,
        ),
        technology_setup(
            name="Know your environnement",
            description="Know your environnement : Military units (expect siege) received +2 attacks and +2 extra attacks per tech your researched before this one in the expedition tent",
            tech_id=TechInfo.BLANK_TECHNOLOGY_6.ID,
            location=BuildingInfo.TENT_C.ID,
            button=7,
            enabled=True,
            player=player,
            research_time=20,
            cost_type=(Attribute.UNUSED_RESOURCE_498, None),
            cost_quantity=(1, None),
            icon_id=269,
        )
        ]
    set_up_green_object = [
        object_setup(
            object=BuildingInfo.TENT_C.ID,
            name="Expedition tent",
            description="Build the expedition tent <cost> : Markus Skoliose expedition tent, allow you to search 7 different technologies that get betters every time you search one.",
            building=UnitInfo.VILLAGER_MALE.ID,
            button=8,
            enabled_object=True,
            player=player,
            cost_type=(Attribute.WOOD_STORAGE, Attribute.STONE_STORAGE),
            cost_quantity=(200, 75),
        ),
    ]
    for cfg in set_up_green_tech:
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
    for cfg in set_up_green_object:
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
    tech_list=[(TechInfo.BLANK_TECHNOLOGY_0.ID,"soil_science();"),(TechInfo.BLANK_TECHNOLOGY_1.ID,"vintage_point();"),(TechInfo.BLANK_TECHNOLOGY_2.ID,"catograph_defensive_gear();")
               ,(TechInfo.BLANK_TECHNOLOGY_3.ID,"draw_the_mediant_line();"),(TechInfo.BLANK_TECHNOLOGY_4.ID,"commercial_road();"),(TechInfo.BLANK_TECHNOLOGY_5.ID,"clear_the_path();")
               ,(TechInfo.BLANK_TECHNOLOGY_6.ID,"know_the_environnement();")]
    #green_gimmick()
    for i in range(len(tech_list)):
        tech_id = tech_list[i][0]
        xs_script = tech_list[i][1]
        search_tech = trigger_manager.add_trigger(
            name=f"Tech for markus {tech_id}",
            enabled=True,
            looping=False,
            execute_on_load=True,
        )
        search_tech.new_condition.research_technology(
            source_player=player,
            technology=tech_id,
        )
        search_tech.new_effect.script_call(
            message=xs_script,
        )
        search_tech.new_effect.script_call(
            message="green_gimmick();"
        )
        search_tech.new_effect.deactivate_trigger(
            trigger_id=search_tech.trigger_id,
        )

def Morange_legellan(scenario,trigger_manager):
    player = PlayerId.FOUR
    shared_trigger = None
    scenario_uuid = scenario.uuid
    area = Area.from_uuid(scenario_uuid)
    set_up_yellow_tech = [
        technology_setup(
            name="Armor from Poitier",
            description="Armor from blacksmith the of Poitier  : Mercenaries gain +2 armors and +2 piercing",
            tech_id=TechInfo.BLANK_TECHNOLOGY_0.ID,
            location=BuildingInfo.TENT_C.ID,
            button=6,
            enabled=True,
            player=player,
            research_time=20,
            cost_type=(Attribute.UNUSED_RESOURCE_498, None),
            cost_quantity=(1, None),
            icon_id=64,
        ),
        technology_setup(
            name="Sword from Toulouse",
            description="sword from Toulouse  : Mercenaries gain +2 attacks",
            tech_id=TechInfo.BLANK_TECHNOLOGY_1.ID,
            location=BuildingInfo.TENT_C.ID,
            button=7,
            enabled=True,
            player=player,
            research_time=20,
            cost_type=(Attribute.UNUSED_RESOURCE_498, None),
            cost_quantity=(1, None),
            icon_id=17,
        ),
        technology_setup(
            name="Projectile of Breizt",
            description="Sword from Toulouse : Ranged mercenaries (expect siege) gain +2 attacks ",
            tech_id=TechInfo.BLANK_TECHNOLOGY_2.ID,
            location=BuildingInfo.TENT_C.ID,
            button=8,
            enabled=True,
            player=player,
            research_time=20,
            cost_type=(Attribute.UNUSED_RESOURCE_498, None),
            cost_quantity=(1, None),
            icon_id=59,
        ),technology_setup(
            name="French charisma",
            description="French charisma : Mercenaires price is reduce by 10%",
            tech_id=TechInfo.BLANK_TECHNOLOGY_3.ID,
            location=BuildingInfo.TENT_C.ID,
            button=9,
            enabled=True,
            player=player,
            research_time=20,
            cost_type=(Attribute.UNUSED_RESOURCE_498, None),
            cost_quantity=(1, None),
            icon_id=219,
        ),

        ]
    set_up_yellow_object = [
        object_setup(
            object=BuildingInfo.TENT_C.ID,
            name="Expedition tent",
            description="Build the expedition tent <cost> : Morange Legellan expedition tent, allow you to upgrade your mercenaries ",
            building=UnitInfo.VILLAGER_MALE.ID,
            button=7,
            enabled_object=True,
            player=player,
            cost_type=(Attribute.WOOD_STORAGE, Attribute.STONE_STORAGE),
            cost_quantity=(200, 75),
        ),
        object_setup(
            object=BuildingInfo.TRADE_WORKSHOP.ID,
            name="Mercenary Tavern",
            description="Build the mercenaries tavern <cost> : Allow you hire mercenaries to do your dirty work, carefull hiring and losing mercenaries increase the cost.",
            building=UnitInfo.VILLAGER_MALE.ID,
            button=9,
            enabled_object=True,
            player=player,
            cost_type=(Attribute.WOOD_STORAGE, None),
            cost_quantity=(175, None),
        ),
        object_setup(
            object=HeroInfo.ZHOU_YU.ID,
            name="hire local mercenaries",
            description="Hire local mercenaries <cost> : Hire nine warrior from different tribe of this continent, cheap and reliable agains light enemy.",
            building=BuildingInfo.TRADE_WORKSHOP.ID,
            button=1,
            enabled_object=True,
            player=player,
            cost_type=(Attribute.GOLD_STORAGE, None),
            cost_quantity=(150, None),
        ),
        object_setup(
            object=HeroInfo.ZHAO_YUN.ID,
            name="hire french mercenaries",
            description="Hire french mercenaries <cost> : Hire twelve french mercenaires composed of heavy infantry, cavalry and axe trownman that can destroy armor, costly but efficient",
            building=BuildingInfo.TRADE_WORKSHOP.ID,
            button=2,
            enabled_object=True,
            player=player,
            cost_type=(Attribute.GOLD_STORAGE, None),
            cost_quantity=(500, None),
        ),
        object_setup(
            object=HeroInfo.ZAKARE.ID,
            name="hire mercenaries from the east",
            description="Hire mercenaries from the east <cost> : Hire twelve mercenaries from the east, mostly infantry with elephant archer and two fast light cav, Their cost increase very fast",
            building=BuildingInfo.TRADE_WORKSHOP.ID,
            button=3,
            enabled_object=True,
            player=player,
            cost_type=(Attribute.GOLD_STORAGE, None),
            cost_quantity=(450, None),
        ),
        object_setup(
            object=HeroInfo.ZHANG_FEI.ID,
            name="hire the italians mercenaries",
            description="Hire mercenaries from the east <cost> : High cost mercenaries, come with strong swordman, arbalester and bombard canon to siege the enemy",
            building=BuildingInfo.TRADE_WORKSHOP.ID,
            button=4,
            enabled_object=True,
            player=player,
            cost_type=(Attribute.GOLD_STORAGE, None),
            cost_quantity=(1050, None),
        ),
    ]
    for cfg in set_up_yellow_tech:
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
    for cfg in set_up_yellow_object:
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
        message="setup_morrange();"
    )
    list_merc = [(HeroInfo.ZHOU_YU.ID,"local_merc();"),(HeroInfo.ZHAO_YUN.ID,"french_merc();"),(HeroInfo.ZAKARE.ID,"east_merc();"),(HeroInfo.ZHANG_FEI.ID,"italian_merc();")]
    list_tech = [(TechInfo.BLANK_TECHNOLOGY_0.ID,"armor_from_poitier();"),(TechInfo.BLANK_TECHNOLOGY_1.ID,"toulouse_sword();"),
    (TechInfo.BLANK_TECHNOLOGY_2.ID,"projectile_from_brezt();"),(TechInfo.BLANK_TECHNOLOGY_3.ID,"french_charisma();")]
    for i in range(len(list_merc)):
        setup_void_morrange = trigger_manager.add_trigger(
            name=f"Mercenaries function {list_merc[i][0]}",
            enabled=True,
            looping=True,
            execute_on_load=True,
        )
        setup_void_morrange.new_condition.objects_in_area(
            source_player=player,
            object_list=list_merc[i][0],
            quantity=1,
            **area.select_entire_map().to_dict(),
        )
        setup_void_morrange.new_effect.script_call(
            message=list_merc[i][1],
        )
        setup_void_morrange.new_effect.remove_object(
            source_player=player,
            object_list_unit_id=list_merc[i][0],
            max_units_affected=1,
            **area.select_entire_map().to_dict(),
        )
    for i in range(len(list_tech)):
        upgrade_merc = trigger_manager.add_trigger(
            name=f"Upgrade merc tech {list_tech[i][0]}",
            enabled=True,
            looping=True,
            execute_on_load=True,
        )
        upgrade_merc.new_condition.research_technology(
            source_player=player,
            technology=list_tech[i][0],
        )
        upgrade_merc.new_effect.script_call(
            message=list_tech[i][1],
        )
        upgrade_merc.new_effect.enable_disable_technology(
            source_player=player,
            enabled=False,
            technology=list_tech[i][0],
        )
        upgrade_merc.new_effect.enable_disable_technology(
            source_player=player,
            enabled=True,
            technology=list_tech[i][0],
        )
    dead_merc_count = trigger_manager.add_trigger(
        name=f"Dead merc function",
        enabled=True,
        looping=True,
        execute_on_load=True,
    )
    dead_merc_count.new_condition.objects_in_area(
        source_player=player,
        object_list=UnitInfo.INVISIBLE_OBJECT_A.ID,
        quantity=1,
        **area.select_entire_map().to_dict(),
    )
    dead_merc_count.new_effect.script_call(
        message="dead_merc_count();"
    )
    dead_merc_count.new_effect.remove_object(
        source_player=player,
        object_list_unit_id=UnitInfo.INVISIBLE_OBJECT_A.ID,
        max_units_affected=1,
        **area.select_entire_map().to_dict(),
    )
