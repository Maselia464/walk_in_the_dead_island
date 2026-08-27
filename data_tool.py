from importlib.util import source_hash

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
from XS import xs_function,danger_level, wave_function, danger_rule_spawn
from level_display import level_display
from wave_composition import spawn_data_wave

from unicodedata import category
# Dictionnaire pour le script
from AoE2ScenarioParser.objects.support.area import Area
def tech_define(scenario, trigger_manager,tech_id,player, name, description, location, button, research_time, trigger,enabled,cost_type,cost_quantity,icon_id):
    if trigger == None :
        tech_preparation = trigger_manager.add_trigger(
            name=f"Technology setup for {name}",
            enabled=True,
            looping=False,
            execute_on_load=False
        )
    else :
        tech_preparation = trigger

    tech_preparation.new_effect.change_technology_name(
        technology=tech_id,
        message=name,
        source_player=player,
    )
    tech_preparation.new_effect.change_technology_description(
        technology=tech_id,
        message=description,
        source_player=player,
    )
    tech_preparation.new_effect.change_technology_location(
        source_player=player,
        object_list_unit_id_2=location,
        technology=tech_id,
        button_location=button,
    )
    tech_preparation.new_effect.change_technology_research_time(
        source_player=player,
        technology=tech_id,
        quantity=research_time,
    )
    tech_preparation.new_effect.enable_disable_technology(
        technology=tech_id,
        enabled=enabled,
        source_player=player,
    )
    if len(cost_type) == 1:
        res_1 = cost_type
        qua_1 = cost_quantity
        res_2 = None
        qua_2 = None
        res_3 = None
        qua_3 = None
    elif len(cost_type) == 2:
        res_1, res_2 = cost_type
        qua_1, qua_2 = cost_quantity
        res_3 = None
        qua_3 = None
    elif len(cost_type) == 3:
        res_1, res_2, res_3 = cost_type
        qua_1, qua_2, qua_3 = cost_quantity
    else:
        res_1 = None
        qua_1 = None
        res_2 = None
        qua_2 = None
        res_3 = None
        qua_3 = None
    tech_preparation.new_effect.change_technology_cost(
        source_player=player,
        technology=tech_id,
        resource_1=res_1,
        resource_2=res_2,
        resource_3=res_3,
        resource_1_quantity=qua_1,
        resource_2_quantity=qua_2,
        resource_3_quantity=qua_3,
    )
    tech_preparation.new_effect.change_technology_icon(
        source_player=player,
        technology=tech_id,
        quantity=icon_id,
    )
    return tech_preparation

def object_define(scenario,trigger_manager,player,object,building,button,enabled_object,trigger,name,description,cost_type,cost_quantity):
    if trigger == None :
        obj_preparation = trigger_manager.add_trigger(
            name=f"Object setup for {name} player {player}",
            enabled=True,
            looping=False,
            execute_on_load=False
        )
    else :
        obj_preparation = trigger
    obj_preparation.new_effect.modify_attribute(
        source_player=player,
        object_list_unit_id=object,
        message=name,
        quantity=0,
        operation=Operation.SET,
        object_attributes=ObjectAttribute.OBJECT_NAME_ID,
    )
    obj_preparation.new_effect.change_object_description(
        source_player=player,
        message=description,
        object_list_unit_id=object,
    )
    obj_preparation.new_effect.change_train_location(
        source_player=player,
        object_list_unit_id=object,
        object_list_unit_id_2=building,
        button_location=button,
    )
    if object == UnitInfo.VILLAGER_MALE.ID:
        obj_preparation.new_effect.change_train_location(
            source_player=player,
            object_list_unit_id=object,
            object_list_unit_id_2=UnitInfo.VILLAGER_FEMALE.ID,
            button_location=button,
        )
    elif object == UnitInfo.VILLAGER_FEMALE.ID:
        obj_preparation.new_effect.change_train_location(
            source_player=player,
            object_list_unit_id=object,
            object_list_unit_id_2=UnitInfo.VILLAGER_MALE.ID,
            button_location=button,
        )
    obj_preparation.new_effect.enable_disable_object(
        source_player=player,
        enabled=enabled_object,
        object_list_unit_id=object,
    )
    if len(cost_type) == 1:
        res_1 = cost_type
        qua_1 = cost_quantity
        res_2 = None
        qua_2 = None
        res_3 = None
        qua_3 = None
    elif len(cost_type) == 2:
        res_1, res_2 = cost_type
        qua_1, qua_2 = cost_quantity
        res_3 = None
        qua_3 = None
    elif len(cost_type) == 3:
        res_1, res_2, res_3 = cost_type
        qua_1, qua_2, qua_3 = cost_quantity
    else:
        res_1 = None
        qua_1 = None
        res_2 = None
        qua_2 = None
        res_3 = None
        qua_3 = None
    obj_preparation.new_effect.change_object_cost(
        source_player=player,
        object_list_unit_id=object,
        resource_1=res_1,
        resource_2=res_2,
        resource_3=res_3,
        resource_1_quantity=qua_1,
        resource_2_quantity=qua_2,
        resource_3_quantity=qua_3,
    )
    return obj_preparation