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
           message="dry_spawn_knight_function();"
       )
    else :
        return None
