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

from AoE2ScenarioParser.datasets.support.info_dataset_base import InfoDatasetBase
@dataclass
class extension_setup:
    area_x: float
    area_y: float
    area_x2: float
    area_y2: float
    scenario : any
    trigger_manager : any
    trigger_edit : any
@dataclass
class SpawnZone:
    script: str
    rectangles: list[tuple[int, int, int, int]]
def extension_area_detector(scenario,trigger_manager, area_x, area_y,area_x2,area_y2,trigger_edit):
    scenario_uuid = scenario.uuid
    for p in range(1, 8):
        if p == 1:
            trigger_edit.new_condition.or_()
        trigger_edit.new_condition.objects_in_area(
            source_player=p,
            quantity=1,
            area_x1=area_x,
            area_y1=area_y,
            area_x2=area_x2,
            area_y2=area_y2,
        )
        if p != PlayerId.SEVEN:
            trigger_edit.new_condition.or_()
def special_area_function (scenario,trigger_manager,X_area, Y_area,trigger):
    scenario_uuid = scenario.uuid
    if X_area == 76.5 and Y_area == 6.5:
       data_extension = [ extension_setup(
            area_x=95,
            area_y=0,
            area_x2=34,
            area_y2=4,
           scenario=scenario,
           trigger_manager=trigger_manager,
           trigger_edit = trigger,
        )
       ]
       for i in data_extension:
           extension_area_detector(
               i.scenario,
               i.trigger_manager,
               area_x=i.area_x,
               area_y=i.area_y,
               area_x2=i.area_x2,
               area_y2=i.area_y2,
               trigger_edit=i.trigger_edit,
           )
       trigger.new_effect.script_call(
           message="dry_spawn_knight_A_function();"
       )
       trigger.new_effect.script_call(
           message="dry_spawn_knight_B_function();"
       )
    elif X_area == 222.5 and Y_area == 33.5:
        data_extension = [
            extension_setup(
                area_x=231,
                area_y=24,
                area_x2=238,
                area_y2=49,
                scenario=scenario,
                trigger_manager=trigger_manager,
                trigger_edit=trigger,
            ),
        ]
        for i in data_extension:
            extension_area_detector(
                i.scenario,
                i.trigger_manager,
                area_x=i.area_x,
                area_y=i.area_y,
                area_x2=i.area_x2,
                area_y2=i.area_y2,
                trigger_edit=i.trigger_edit,
            )
    else :
        return None


def normal_area_spawn_activate(scenario,trigger_manager):
    scenario_uuid = scenario.uuid
    spawn_list = [
        SpawnZone(
            script="jungle_spawn_river_A_function();",
            rectangles=[
                (177, 186, 184, 193),
                (177, 195, 202, 211),
                (186, 186, 193, 193),
                (177, 177, 184, 184),
                (150, 177, 175, 211),
            ],
        ),

        SpawnZone(
            script="jungle_spawn_mill_A_function();",
            rectangles=[
                (167, 87, 175, 95),
                (177, 87, 184, 94),
                (168, 96, 175, 103),
                (159, 87, 166, 94),
                (150, 69, 175, 85),
            ],
        ),
        SpawnZone(
            script="jungle_spawn_hero_cav_A_function();",
            rectangles=[
                (51, 78, 58, 85),
                (60, 78, 67, 85),
                (51, 87, 58, 94),
                (42, 78, 49, 85),
                (51, 69, 58, 76),
            ],
        ),
        SpawnZone(
            script="jungle_spawn_crusader_function();",
            rectangles=[
                (114, 42, 121, 49),
                (114, 33, 121, 40),
                (87, 33, 112, 58),
                (114, 51, 121, 58),
                (123, 42, 130, 49),
            ],
        ),
        SpawnZone(
            script="dry_spawn_chief_hut_big_A_function();",
            rectangles=[
                (231, 177, 239, 202),
                (213, 186, 230, 193),
                (222, 177, 229, 184),
                (222, 195, 229, 202),
                (204, 238, 213, 238),
            ],
        ),
    ]
    for zone in spawn_list:
        activate_spawn_area = trigger_manager.add_trigger(
            name="Activate the spawn",
            looping=False,
            enabled=True,
        )
        rectangles = zone.rectangles
        total_conditions = 7 * len(rectangles)

        condition_index = 0
        for x1, y1, x2, y2 in zone.rectangles:
            for p in range (1,8):
                activate_spawn_area.new_condition.objects_in_area(
                    source_player=p,
                    quantity=1,
                    area_x1=x1,
                    area_x2=x2,
                    area_y1=y1,
                    area_y2=y2,
                )
                condition_index += 1

                if condition_index < total_conditions:
                    activate_spawn_area.new_condition.or_()
        activate_spawn_area.new_effect.script_call(
            message=zone.script,
        )