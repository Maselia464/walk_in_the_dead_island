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
from XS import xs_function,danger_level, wave_function, danger_rule_spawn, Gary_buerg_xs, Markus_skioliose_XS, Morange_legellan_xs,hamish_davelton_xs, warmer_stephano_xs, harris_galvas_xs, area_open, xs_old_man_relic, xs_forge, xs_function_creator
from level_display import level_display
from wave_composition import spawn_data_wave
from Class_function import John_Galverb, Gary_buerg,Markus_skoliose, Morange_legellan, Hamish_davelton, Warmer_stephano, Haris_galvas
from special_area import special_area_function
from Barrack_defense import barrack_function
from Old_man_relic import old_man_relic_function, Blacksmith_of_takoas
from unicodedata import category
# Dictionnaire pour le script
from AoE2ScenarioParser.objects.support.area import Area

input_path = "C:\\Users\\redma\\Games\\Age of Empires 2 DE\\76561198382316787\\resources\\_common\\scenario\\7V1 security breach in the ruins.aoe2scenario"
output_path = "C:\\Users\\redma\\Games\\Age of Empires 2 DE\\76561198382316787\\resources\\_common\\scenario\\7V1 security breach in the ruins v0-1.aoe2scenario"

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
activation_triggers = {}
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
        simple_area.new_condition.objects_in_area(
            source_player=PlayerId.GAIA,
            quantity=1,
            area_x1=area_x,
            area_y1=area_y,
            area_x2=area_x2,
            area_y2=area_y2,
            object_state=ObjectState.ALMOST_DEAD,
            object_type=ObjectType.MILITARY,
        )
        simple_area.new_condition.or_()
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
        simple_area.new_effect.change_ownership(
            source_player=PlayerId.GAIA,
            target_player=PlayerId.EIGHT,
            area_x1=area_x,
            area_y1=area_y,
            area_x2=area_x2,
            area_y2=area_y2,
            object_type=ObjectType.BUILDING,
        )
        simple_area.new_effect.script_call(
            message=xs_name,
        )
        special_area_function(scenario, trigger_manager, x_coordinate, y_coordinate, simple_area)
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
        if x_coordinate == 211.5 and y_coordinate == 213.5:
            activation_triggers["old_man"] = simple_area
        if x_coordinate == 238.5 and y_coordinate == 204.5:
            activation_triggers["forge"] = simple_area
        if x_coordinate == 139.5 and y_coordinate == 6.5:
            simple_area.new_effect.change_ownership(
                source_player=PlayerId.GAIA,
                target_player=PlayerId.EIGHT,
                area_x1=132,
                area_y1=14,
                area_x2=139,
                area_y2=31,
                object_type=ObjectType.MILITARY,
            )
            simple_area.new_effect.change_ownership(
                source_player=PlayerId.GAIA,
                target_player=PlayerId.EIGHT,
                area_x1=132,
                area_y1=14,
                area_x2=139,
                area_y2=31,
                object_type=ObjectType.BUILDING,
            )
            simple_area.new_effect.change_ownership(
                source_player=PlayerId.GAIA,
                target_player=PlayerId.EIGHT,
                area_x1=132,
                area_y1=14,
                area_x2=139,
                area_y2=31,
                object_type=ObjectType.MILITARY,
            )
            simple_area.new_effect.change_ownership(
                source_player=PlayerId.GAIA,
                target_player=PlayerId.EIGHT,
                area_x1=124,
                area_y1=24,
                area_x2=131,
                area_y2=31,
                object_type=ObjectType.BUILDING,
            )
            simple_area.new_effect.script_call(
                message="dry_spawn_L_A_function();\ndry_spawn_L_B_function();"

            )
        if x_coordinate == 238.5 and y_coordinate == 6.5:
            simple_area.new_effect.change_ownership(
                source_player=PlayerId.GAIA,
                target_player=PlayerId.EIGHT,
                area_x1=222,
                area_y1=6,
                area_x2=238,
                area_y2=22,
                object_type=ObjectType.MILITARY,
            )
            simple_area.new_effect.change_ownership(
                source_player=PlayerId.GAIA,
                target_player=PlayerId.EIGHT,
                area_x1=222,
                area_y1=6,
                area_x2=238,
                area_y2=22,
                object_type=ObjectType.BUILDING,
            )
            simple_area.new_effect.change_ownership(
                source_player=PlayerId.GAIA,
                target_player=PlayerId.EIGHT,
                area_x1=213,
                area_y1=15,
                area_x2=221,
                area_y2=22,
                object_type=ObjectType.MILITARY,
            )
            simple_area.new_effect.change_ownership(
                source_player=PlayerId.GAIA,
                target_player=PlayerId.EIGHT,
                area_x1=213,
                area_y1=15,
                area_x2=221,
                area_y2=22,
                object_type=ObjectType.BUILDING,
            )
            simple_area.new_effect.change_ownership(
                source_player=PlayerId.GAIA,
                target_player=PlayerId.EIGHT,
                area_x1=222,
                area_y1=23,
                area_x2=229,
                area_y2=31,
                object_type=ObjectType.MILITARY,
            )
            simple_area.new_effect.script_call(
                message="dry_spawn_fortress_A_function();"
            )
        if x_coordinate == 229.5 and y_coordinate == 177.5 or x_coordinate == 238.5 and y_coordinate == 141.5 or x_coordinate == 220.5 and y_coordinate == 186.5 or x_coordinate == 229.5 and y_coordinate == 195.5 or x_coordinate == 238.5 and y_coordinate == 204.5 :
            simple_area.new_effect.script_call(
                message="dry_spawn_chief_hut_big_A_function();"
            )
        if x_coordinate == 193.5 and y_coordinate == 186.5 or x_coordinate == 202.5 and y_coordinate == 195.5 or x_coordinate == 175.5 and y_coordinate == 177.5 or x_coordinate == 184.5 and y_coordinate == 177.5 :
            simple_area.new_effect.script_call(
                message="jungle_spawn_river_A_function();"
            )
        if x_coordinate == 121.5 and y_coordinate == 33.5 or x_coordinate == 130.5 and y_coordinate == 42.5 or x_coordinate == 121.5 and y_coordinate == 51.5 or x_coordinate == 112.5 and y_coordinate == 33.5 :
            simple_area.new_effect.script_call(
                message="jungle_spawn_crusader_function();"
            )
        if x_coordinate == 175.5 and y_coordinate == 69.5 or x_coordinate == 184.5 and y_coordinate == 87.5 or x_coordinate == 175.5 and y_coordinate == 96.5 or x_coordinate == 166.5 and y_coordinate == 87.5 :
            simple_area.new_effect.script_call(
                message="jungle_spawn_mill_A_function();"
            )
        if x_coordinate == 67.5 and y_coordinate == 78.5 or x_coordinate == 58.5 and y_coordinate == 87.5 or x_coordinate == 49.5 and y_coordinate == 78.5 or x_coordinate == 58.5 and y_coordinate == 69.5 :
            simple_area.new_effect.script_call(
                message="jungle_spawn_hero_cav_A_function();"
            )
        if x_coordinate == 238.5 and y_coordinate == 204.5 :
            simple_area.new_effect.script_call(
                message="Desert_fortress_1_defence_function();"
            )
        if x_coordinate == 40.5 and y_coordinate == 204.5:
            simple_area.new_effect.script_call(
                message="last_defence();"
            )
            for p in range(1, 8):
                area_x = 0
                area_y = 204
                area_x2 = 40
                area_y2 = 239
                simple_area.new_condition.objects_in_area(
                    source_player=p,
                    quantity=1,
                    area_x1=area_x,
                    area_y1=area_y,
                    area_x2=area_x2,
                    area_y2=area_y2,
                )
                if p != PlayerId.SEVEN:
                    #It's Ugly to do it like this but it's working we need one passage and P7 is the last soooo...
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
                    simple_area.new_effect.change_ownership(
                        source_player=PlayerId.GAIA,
                        target_player=PlayerId.EIGHT,
                        area_x1=area_x,
                        area_y1=area_y,
                        area_x2=area_x2,
                        area_y2=area_y2,
                        object_type=ObjectType.BUILDING,
                    )
        if x_coordinate == 211.5 and y_coordinate == 213.5:
            simple_area.new_effect.script_call(
                message="Jungle_fortress_big_function();"
            )
        if x_coordinate == 130.5 and y_coordinate == 114.5:
            simple_area.new_effect.script_call(
                message="Mid_area_defence_function();"
            )
            area_x = 6
            area_y = 114
            area_x2 = 130
            area_y2 = 130
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
                    # Horrible pratice do not do it !
            simple_area.new_effect.change_ownership(
                source_player=PlayerId.GAIA,
                target_player=PlayerId.EIGHT,
                area_x1=area_x,
                area_y1=area_y,
                area_x2=area_x2,
                area_y2=area_y2,
                object_type=ObjectType.MILITARY,
            )
            simple_area.new_effect.change_ownership(
                source_player=PlayerId.GAIA,
                target_player=PlayerId.EIGHT,
                area_x1=area_x,
                area_y1=area_y,
                area_x2=area_x2,
                area_y2=area_y2,
                object_type=ObjectType.BUILDING,
            )
            area_x = 114
            area_y = 114
            area_x2 = 130
            area_y2 = 238
            simple_area.new_condition.or_()
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
            simple_area.new_effect.change_ownership(
                source_player=PlayerId.GAIA,
                target_player=PlayerId.EIGHT,
                area_x1=area_x,
                area_y1=area_y,
                area_x2=area_x2,
                area_y2=area_y2,
                object_type=ObjectType.BUILDING,
            )
        if x_coordinate == 31.5 and y_coordinate == 78.5:
            simple_area.new_effect.script_call(
                message="Jungle_fortress_small_function();"
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
             (OtherInfo.FLAG_D.ID,16,25,"2x3 area ","area_reach_tracker_big();"),(OtherInfo.FLAG_G.ID,34,16,"3x4 area ","area_reach_tracker_very_big();"),(OtherInfo.FLAG_H.ID,16,34,"4x3 area ","area_reach_tracker_very_big();")
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
danger_level(scenario,trigger_manager)

#------------------------------------ CLASS SETUP -------------------------------

John_Galverb(scenario,trigger_manager)
Gary_buerg(scenario,trigger_manager)
Gary_buerg_xs(scenario,trigger_manager)
Markus_skioliose_XS(scenario,trigger_manager)
Markus_skoliose(scenario,trigger_manager)
Morange_legellan_xs(scenario,trigger_manager)
Morange_legellan(scenario,trigger_manager)
hamish_davelton_xs(scenario,trigger_manager)
Hamish_davelton(scenario,trigger_manager)
warmer_stephano_xs(scenario, trigger_manager)
Warmer_stephano(scenario,trigger_manager)
harris_galvas_xs(scenario,trigger_manager)
Haris_galvas(scenario,trigger_manager)

xs_old_man_relic(scenario,trigger_manager)
old_man_relic_function(scenario,trigger_manager,activation_triggers)
xs_forge(scenario,trigger_manager)
Blacksmith_of_takoas(scenario,trigger_manager,activation_triggers)
#------------------------------------ Area spawn setup -------------------------------

area_open(scenario,trigger_manager)
spawn_zone_list = ["dry_spawn_chief_hut_big_A", "dry_spawn_knight_A", "dry_spawn_knight_B",
                   "dry_spawn_fortress_A", "dry_spawn_L_A", "dry_spawn_L_B",
                   "jungle_spawn_river_A", "jungle_spawn_mill_A", "jungle_spawn_hero_cav_A",
                   "jungle_spawn_crusader"]
xs_function_creator(scenario, spawn_zone_list)


level_display(scenario,trigger_manager)

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


for p in range (1,8):
    age_tech = [TechInfo.FEUDAL_AGE.ID,TechInfo.CASTLE_AGE.ID,TechInfo.IMPERIAL_AGE.ID]
    xs_call = ["feudal_age_reached();","castle_age_reached();","imperial_age_reached();"]
    for i in range (len(age_tech)):
        xs = xs_call[i]
        tech_id = age_tech[i]
        age_check = trigger_manager.add_trigger(
            name=xs,
            enabled=True,
            looping=False,
            execute_on_load=True,
        )
        age_check.new_condition.research_technology(
            source_player=p,
            technology=tech_id,
        )
        age_check.new_effect.script_call(
            message=xs,
        )
        age_check.new_effect.deactivate_trigger(
            trigger_id=age_check.trigger_id,
        )
barrack_function(scenario)

scenario.write_to_file(output_path)