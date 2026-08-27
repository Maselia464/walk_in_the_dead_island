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
from XS import xs_function,danger_level, wave_function, danger_rule_spawn, Gary_buerg_xs
from level_display import level_display
from wave_composition import spawn_data_wave
from Class_function import John_Galverb, Gary_buerg
from unicodedata import category
# Dictionnaire pour le script
from AoE2ScenarioParser.objects.support.area import Area

input_path = "C:\\Users\\USER\\Games\\Age of Empires 2 DE\\[ID]\\resources\\_common\\scenario\\7V1 security breach in the ruins.aoe2scenario"
output_path = "C:\\Users\\USER\\Games\\Age of Empires 2 DE\\[ID]\\resources\\_common\\scenario\\7V1 security breach in the ruins v0-1.aoe2scenario"

scenario = AoE2DEScenario.from_file(input_path)
scenario_uuid = scenario.uuid
area = Area.from_uuid(scenario_uuid)
trigger_manager = scenario.trigger_manager
unit_manager =scenario.unit_manager
# Get TC object of all players
unit_manager.filter_units_by_const(unit_consts=[BuildingInfo.TOWN_CENTER.ID])
# Get TC object of only player one and two
unit_manager.filter_units_by_const(unit_consts=[BuildingInfo.TOWN_CENTER.ID], player_list=[PlayerId.ONE, PlayerId.TWO])
# Get all objects of player one except for the villagers
list_flag_A = unit_manager.filter_units_by_const(
    unit_consts=[OtherInfo.FLAG_A.ID],
    blacklist=False,  # <-- When True, everything in the unit_consts list will be excluded instead of included
    player_list=[PlayerId.EIGHT],
)
list_flag_C = unit_manager.filter_units_by_const(
    unit_consts=[OtherInfo.FLAG_C.ID],
    blacklist=False,  # <-- When True, everything in the unit_consts list will be excluded instead of included
    player_list=[PlayerId.EIGHT],
)
list_flag_D = unit_manager.filter_units_by_const(
    unit_consts=[OtherInfo.FLAG_D.ID],
    blacklist=False,  # <-- When True, everything in the unit_consts list will be excluded instead of included
    player_list=[PlayerId.EIGHT],
)

def AREA_maker(scenario,flag,x_calculus,y_calculus,name,xs_name):
    list_flag = unit_manager.filter_units_by_const(
        unit_consts=[flag],
        blacklist=False,  # <-- When True, everything in the unit_consts list will be excluded instead of included
        player_list=[PlayerId.EIGHT],
    )
    for i in range(len(list_flag)):
        x_coordinate = list_flag[i].x
        y_coordinate = list_flag[i].y
        area_x = int(x_coordinate)
        area_y = int(y_coordinate)
        area_x2 = area_x - x_calculus
        area_y2 = area_y + y_calculus
        simple_area = trigger_manager.add_trigger(
            name=f"{name} {i} at {x_coordinate} {y_coordinate}",
            enabled=True,
            looping=False,
            execute_on_load=True,
        )
        for p in range(1, 8):
            simple_area.new_condition.objects_in_area(
                source_player=p,
                quantity=1,
                area_x1=area_x,
                area_y1=area_y,
                area_x2=area_x2,
                area_y2=area_y2,
            )
            if p != PlayerId.SEVEN:
                simple_area.new_condition.or_()
        simple_area.new_effect.change_ownership(
            source_player=PlayerId.GAIA,
            target_player=PlayerId.EIGHT,
            area_x1=area_x,
            area_y1=area_y,
            area_x2=area_x2,
            area_y2=area_y2,
            object_type=ObjectType.MILITARY,
        )
        simple_area.new_effect.script_call(
            message=xs_name,
        )
        if flag == OtherInfo.FLAG_K.ID:
            for p in range (1,8):
                simple_area.new_effect.play_sound(
                    sound_name="ALERT_AREA_WAKE_UP",
                    source_player=p,
                )
            simple_area.new_effect.remove_object(
                area_x1=area_x,
                area_y1=area_y,
                area_x2=area_x2,
                area_y2=area_y2,
                source_player=PlayerId.EIGHT,
                object_list_unit_id=BuildingInfo.PALISADE_WALL.ID,
            )
print(list_flag_A)
Gaia_change = trigger_manager.add_trigger(
        name=f"Everything become GAIA",
        enabled=True,
        looping=False,
        execute_on_load=True,
    )
Gaia_change.new_effect.change_ownership(
        source_player=PlayerId.EIGHT,
        target_player=PlayerId.GAIA,
        area_x1 = 11,
        area_y1 = 5,
        area_x2 = 239,
        area_y2 = 238,
        object_type=ObjectType.MILITARY
    )
Gaia_change.new_effect.change_ownership(
        source_player=PlayerId.EIGHT,
        target_player=PlayerId.GAIA,
        area_x1 = 11,
        area_y1 = 5,
        area_x2 = 239,
        area_y2 = 238,
        object_type=ObjectType.BUILDING
    )
Gaia_change.new_effect.change_ownership(
        source_player=PlayerId.EIGHT,
        target_player=PlayerId.GAIA,
        area_x1 = 0,
        area_y1 = 12,
        area_x2 = 10,
        area_y2 = 239,
        object_type=ObjectType.BUILDING,
    )
Gaia_change.new_effect.change_ownership(
        source_player=PlayerId.EIGHT,
        target_player=PlayerId.GAIA,
        area_x1 = 0,
        area_y1 = 12,
        area_x2 = 10,
        area_y2 = 239,
        object_type=ObjectType.MILITARY,
    )
flag_list = [(OtherInfo.FLAG_A.ID,7,7,"Simple area","area_reach_tracker_small();"),(OtherInfo.FLAG_C.ID,25,16,"3x2 area ","area_reach_tracker_big();"),(OtherInfo.FLAG_B.ID,16,16,"Bigger square ","area_reach_tracker_medium();"),
             (OtherInfo.FLAG_D.ID,16,25,"2x3 area ","area_reach_tracker_big();"),(OtherInfo.FLAG_G.ID,34,16,"3x4 area ","area_reach_tracker_very_big();"),(OtherInfo.FLAG_H.ID,16,34,"4x3 area ","area_reach_tracker_very_big();"),(OtherInfo.FLAG_I.ID,25,25,"4x3 area","area_reach_tracker_very_big();")
             ,(OtherInfo.FLAG_E.ID,7,16,"1x2 area","area_reach_tracker_small();"),(OtherInfo.FLAG_F.ID,16,7,"1x2 area","area_reach_tracker_small();"),(OtherInfo.FLAG_I.ID,25,25,"Big area","area_reach_tracker_very_big();"),(OtherInfo.FLAG_J.ID,25,34,"very Big area","area_reach_tracker_very_big();")
             ,(OtherInfo.FLAG_K.ID,16,16,"ALERT square","area_reach_tracker_very_big();")]
for m in range (len(flag_list)):
    flag, x , y, name, XS= flag_list[m]
    AREA_maker(
        scenario,
        name=name,
        x_calculus=x,
        y_calculus=y,
        flag=flag,
        xs_name=XS,
    )


xs_function(scenario,trigger_manager)
level_display(scenario,trigger_manager)
danger_level(scenario,trigger_manager)
for cfg in spawn_data_wave:
    wave_function(
        scenario,
        trigger_manager,
        vector=cfg.main_vector,
        second_area_vector=cfg.second_area_vector,
        unit=cfg.unit,
        danger_level=cfg.danger_level,
        quantity=cfg.quantity,
        spawn_rate=cfg.spawn_rate,
        rule_name=cfg.rule_name,
    )
danger_rule_spawn(
    scenario,
    trigger_manager,
    configs=spawn_data_wave,   # on passe toute la liste
    rule_name=cfg.rule_name,
)
#------------------------------------ CLASS SETUP -------------------------------
John_Galverb(scenario,trigger_manager)
Gary_buerg(scenario,trigger_manager)
Gary_buerg_xs(scenario,trigger_manager)
scenario.write_to_file(output_path)