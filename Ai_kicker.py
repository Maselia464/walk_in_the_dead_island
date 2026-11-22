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

def ai_kick(scenario: AoE2DEScenario) :
    trigger_manager = scenario.trigger_manager
    scenario_uuid = scenario.uuid
    area = Area.from_uuid(scenario_uuid)
    clean_off = trigger_manager.add_trigger(
        name="Clean off",
        enabled=True,
        looping=False,
    )
    clean_off.new_condition.timer(
        timer=60,
    )
    clean_off.new_effect.remove_object(
        source_player=PlayerId.GAIA,
        object_list_unit_id=UnitInfo.CAMEL_SCOUT.ID,
        area_x1=0,
        area_x2=37,
        area_y1=4,
        area_y2=98,
    )
    clean_off.new_effect.remove_object(
        source_player=PlayerId.GAIA,
        object_list_unit_id=UnitInfo.CAMEL_SCOUT.ID,
        area_x1=99,
        area_x2=127,
        area_y1=0,
        area_y2=4,
    )
    for p in range (1,8):
        check_ai = trigger_manager.add_trigger(
            name=f"Are you a robot {p}?",
            enabled=True,
            looping=False,
        )
        kick_ai = trigger_manager.add_trigger(
            name=f"GET THE F OUT OF MY MAP YOU METAL PIECE OF JUNK {p}!",
            enabled=True,
            looping=False,
        )
        check_ai.new_condition.timer(
            timer=3,
        )
        check_ai.new_condition.objects_in_area(
            source_player=p,
            quantity=1,
            **area.select_entire_map().to_dict(),
            object_list=UnitInfo.CAMEL_SCOUT.ID,
        )
        check_ai.new_effect.deactivate_trigger(
            trigger_id=kick_ai.trigger_id,
        )
        kick_ai.new_condition.timer(
            timer=45,
        )
        kick_ai.new_effect.declare_victory(
            enabled=False,
            source_player=p,
        )
        clean_off.new_effect.remove_object(
            source_player=p,
            object_list_unit_id=UnitInfo.CAMEL_SCOUT.ID,
            area_x1=0,
            area_x2=37,
            area_y1=4,
            area_y2=98,
        )
        clean_off.new_effect.remove_object(
            source_player=p,
            object_list_unit_id=UnitInfo.CAMEL_SCOUT.ID,
            area_x1=99,
            area_x2=127,
            area_y1=0,
            area_y2=4,
        )
        clean_off.new_effect.remove_object(
            source_player=p,
            object_list_unit_id=OtherInfo.FLAG_A.ID,
            area_x1=0,
            area_x2=37,
            area_y1=4,
            area_y2=98,
        )
        clean_off.new_effect.remove_object(
            source_player=p,
            object_list_unit_id=OtherInfo.FLAG_A.ID,
            area_x1=99,
            area_x2=127,
            area_y1=0,
            area_y2=4,
        )
