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
from data_tool import barrack_rule


'''

rule test
minInterval 3
maxInterval 3
active
{
float X_coord = 1.0;
float y_coord = 211.0;
vector Spawnpos_test = xsVectorSet(X_coord, y_coord, 0);
int casernes = xsGetPlayerUnitIds(1, 12);
int unit_id = xsCreateUnit(4, 1, Spawnpos_test, false, false, false);

xsSetUnitProperty(unit_id, 5, 60994, 1);
int garrisonedUnits = xsGetGarrisonedUnitIds(60994);
xsTaskUnits(
    garrisonedUnits,
    cActionTypeUngarrison,
);
}

'''

@dataclass
class Building_config:
    # open to the player until they reach it, once they reach enemy can spawn here, otherwise it send back to main
    unit_list: list
    barrack: int
    quantity: list


    spawn_rate: list
    spawn_time : int

    rule: str
    rule_to_activate : str



def barrack_function(scenario):



    barrack_list = {

        "last_area_1":56444,
        "last_area_2": 56445,
        "last_area_3": 56646,
        "last_area_4": 56447,
        "last_area_5": 56648,

        "Mid_defence_zone_1" : 24080,
        "Mid_defence_zone_2" : 24079,
        "Mid_defence_zone_3" : 24078,
        "Mid_defence_zone_4" : 24077,
        "Mid_defence_zone_5" : 24076,
        "Mid_defence_zone_6" : 24081,
        "Mid_defence_zone_7" : 24082,
        "Mid_defence_zone_8" : 24085,
        "Mid_defence_zone_9" : 24086,
        "Mid_defence_zone_10" : 24087,
        "Mid_defence_zone_11" : 24088,

        "Jungle_fortress_big_1" : 35368,
        "Jungle_fortress_big_2" : 35372,

        "Desert_fortress_1" : 30018,
        "Desert_fortress_2" : 29943,
        "Desert_fortress_3" : 29948,
        "Desert_fortress_4" : 30017,

        "Jungle_fortress_small_1" : 35917,
        "Jungle_fortress_small_2" : 35918,
        "Jungle_fortress_small_3" : 35919,
        "Jungle_fortress_small_4" : 35920,
    }

    Stable_list = {
        "dry_stable" : 24922
    }
    barrack_config = [
        Building_config(
            barrack=barrack_list["Desert_fortress_1"] ,
            unit_list=[UnitInfo.LONG_SWORDSMAN.ID,UnitInfo.CROSSBOWMAN.ID,UnitInfo.PIKEMAN.ID],
            quantity=[15,15,30],
            spawn_rate=[5,5,10],
            spawn_time=35,
            rule="dry_fortress_defence_area_1",
            rule_to_activate="dry_fortress_defence_area_2",

        ),
        Building_config(
            barrack=barrack_list["Desert_fortress_1"],
            unit_list=[UnitInfo.XOLOTL_WARRIOR.ID, UnitInfo.SLINGER.ID,UnitInfo.SKIRMISHER.ID],
            quantity=[45, 35, 70],
            spawn_rate=[5, 7, 10],
            spawn_time=45,
            rule="dry_fortress_defence_area_2",
            rule_to_activate="dry_fortress_defence_area_3",

        ),
        Building_config(
            barrack=barrack_list["Desert_fortress_1"],
            unit_list=[UnitInfo.LIGHT_CAVALRY.ID, UnitInfo.OBUCH.ID],
            quantity=[80, 45],
            spawn_rate=[10, 5],
            spawn_time=45,
            rule="dry_fortress_defence_area_3",
            rule_to_activate="dry_fortress_defence_area_1",

        ),
#---------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Desert_fortress_2"],
            unit_list=[UnitInfo.TEUTONIC_KNIGHT.ID, UnitInfo.HAND_CANNONEER.ID],
            quantity=[45, 35],
            spawn_rate=[5, 5],
            spawn_time=45,
            rule="dry_fortress_defence_area_4",
            rule_to_activate="dry_fortress_defence_area_5",

        ),
        Building_config(
            barrack=barrack_list["Desert_fortress_2"],
            unit_list=[UnitInfo.KAMAYUK.ID, UnitInfo.JAGUAR_WARRIOR.ID, UnitInfo.CENTURION.ID],
            quantity=[70, 70, 140],
            spawn_rate=[7, 7, 14],
            spawn_time=45,
            rule="dry_fortress_defence_area_5",
            rule_to_activate="dry_fortress_defence_area_6",

        ),
        Building_config(
            barrack=barrack_list["Desert_fortress_2"],
            unit_list=[UnitInfo.SCORPION.ID, UnitInfo.LIGHT_CAVALRY.ID],
            quantity=[45, 45],
            spawn_rate=[5, 5],
            spawn_time=45,
            rule="dry_fortress_defence_area_6",
            rule_to_activate="dry_fortress_defence_area_4",

        ),
# -------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Desert_fortress_3"],
            unit_list=[UnitInfo.THROWING_AXEMAN.ID, UnitInfo.WOAD_RAIDER.ID, UnitInfo.KNIGHT.ID,UnitInfo.HUSKARL.ID],
            quantity=[32, 45, 50, 100],
            spawn_rate=[4, 5, 10, 10],
            spawn_time=25,
            rule="dry_fortress_defence_area_7",
            rule_to_activate="dry_fortress_defence_area_8",

        ),
        Building_config(
            barrack=barrack_list["Desert_fortress_3"],
            unit_list=[UnitInfo.CAVALIER.ID, UnitInfo.COUSTILLIER.ID, UnitInfo.KARAMBIT_WARRIOR.ID],
            quantity=[140, 50, 140],
            spawn_rate=[14, 5, 14],
            spawn_time=25,
            rule="dry_fortress_defence_area_8",
            rule_to_activate="dry_fortress_defence_area_7",

        ),
# -------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Desert_fortress_4"],
            unit_list=[UnitInfo.PIKEMAN.ID, UnitInfo.MANGUDAI.ID, UnitInfo.BATTERING_RAM.ID, UnitInfo.MAMELUKE.ID],
            quantity=[60, 40, 5, 40],
            spawn_rate=[15, 10, 1, 10],
            spawn_time=15,
            rule="dry_fortress_defence_area_9",
            rule_to_activate="dry_fortress_defence_area_10",

        ),
        Building_config(
            barrack=barrack_list["Desert_fortress_4"],
            unit_list=[UnitInfo.LONGBOWMAN.ID, UnitInfo.KONNIK.ID, UnitInfo.FIRE_LANCER.ID,UnitInfo.CHU_KO_NU.ID],
            quantity=[20, 40, 80, 40],
            spawn_rate=[5, 10, 10, 5],
            spawn_time=15,
            rule="dry_fortress_defence_area_10",
            rule_to_activate="dry_fortress_defence_area_9",

        ),
#---------------------------------------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Jungle_fortress_big_1"],
            unit_list=[UnitInfo.KAMAYUK.ID, UnitInfo.JAGUAR_WARRIOR.ID, UnitInfo.XOLOTL_WARRIOR.ID, UnitInfo.CHU_KO_NU.ID],
            quantity=[80, 80, 80, 40],
            spawn_rate=[10, 10, 10, 5],
            spawn_time=15,
            rule="jungle_fortress_big_defence_1",
            rule_to_activate="jungle_fortress_big_defence_2",

        ),
        Building_config(
            barrack=barrack_list["Jungle_fortress_big_1"],
            unit_list=[UnitInfo.CAVALIER.ID, UnitInfo.SCORPION.ID, UnitInfo.CONQUISTADOR.ID,
                       UnitInfo.WINGED_HUSSAR.ID],
            quantity=[70, 45, 120, 120],
            spawn_rate=[10, 5, 15, 15],
            spawn_time=15,
            rule="jungle_fortress_big_defence_2",
            rule_to_activate="jungle_fortress_big_defence_3",

        ),
        Building_config(
            barrack=barrack_list["Jungle_fortress_big_1"],
            unit_list=[UnitInfo.ELITE_JANISSARY.ID, UnitInfo.SHRIVAMSHA_RIDER.ID, UnitInfo.ELEPHANT_ARCHER.ID,
                       UnitInfo.ELITE_TEUTONIC_KNIGHT.ID],
            quantity=[100, 140, 140, 100],
            spawn_rate=[10, 14, 14, 10],
            spawn_time=15,
            rule="jungle_fortress_big_defence_3",
            rule_to_activate="jungle_fortress_big_defence_4",

        ),
        Building_config(
            barrack=barrack_list["Jungle_fortress_big_1"],
            unit_list=[UnitInfo.ELITE_MAMELUKE.ID, UnitInfo.HEAVY_CAVALRY_ARCHER.ID, UnitInfo.ELITE_BOYAR.ID,
                       UnitInfo.HALBERDIER.ID],
            quantity=[120, 70, 70, 140],
            spawn_rate=[15, 7, 7, 14],
            spawn_time=15,
            rule="jungle_fortress_big_defence_4",
            rule_to_activate="jungle_fortress_big_defence_1",

        ),
#-----------------------#
        Building_config(
            barrack=barrack_list["Jungle_fortress_big_2"],
            unit_list=[UnitInfo.ELITE_SERJEANT.ID],
            quantity=[200],
            spawn_rate=[20],
            spawn_time=10,
            rule="jungle_fortress_big_defence_5",
            rule_to_activate="jungle_fortress_big_defence_6",

        ),

        Building_config(
            barrack=barrack_list["Jungle_fortress_big_2"],
            unit_list=[UnitInfo.ELITE_SKIRMISHER.ID, UnitInfo.MANGONEL.ID, UnitInfo.ELITE_KESHIK.ID,
                       UnitInfo.ELITE_KIPCHAK.ID],
            quantity=[120, 20, 120, 100],
            spawn_rate=[15, 2, 15, 10],
            spawn_time=15,
            rule="jungle_fortress_big_defence_6",
            rule_to_activate="jungle_fortress_big_defence_7",

        ),
        Building_config(
            barrack=barrack_list["Jungle_fortress_big_2"],
            unit_list=[UnitInfo.ELITE_ARAMBAI.ID, UnitInfo.ELITE_THROWING_AXEMAN.ID, UnitInfo.BATTLE_ELEPHANT.ID,
                       UnitInfo.BATTERING_RAM.ID],
            quantity=[140, 80, 120, 45],
            spawn_rate=[14, 10, 15, 5],
            spawn_time=15,
            rule="jungle_fortress_big_defence_7",
            rule_to_activate="jungle_fortress_big_defence_8",

        ),
        Building_config(
            barrack=barrack_list["Jungle_fortress_big_2"],
            unit_list=[UnitInfo.ELITE_URUMI_SWORDSMAN.ID, UnitInfo.ELITE_KONNIK.ID, UnitInfo.ELITE_SAMURAI.ID,
                       UnitInfo.HAND_CANNONEER.ID],
            quantity=[100, 100, 100, 50],
            spawn_rate=[20, 20, 20, 10],
            spawn_time=15,
            rule="jungle_fortress_big_defence_8",
            rule_to_activate="jungle_fortress_big_defence_9",

        ),
        Building_config(
            barrack=barrack_list["Jungle_fortress_big_2"],
            unit_list=[UnitInfo.ELITE_EAGLE_WARRIOR.ID, UnitInfo.ELITE_JAGUAR_WARRIOR.ID, UnitInfo.ELITE_PLUMED_ARCHER.ID,
                       UnitInfo.ELITE_BALLISTA_ELEPHANT.ID],
            quantity=[100, 55, 55, 100],
            spawn_rate=[10, 5, 5, 10],
            spawn_time=15,
            rule="jungle_fortress_big_defence_9",
            rule_to_activate="jungle_fortress_big_defence_6",

        ),
# ---------------------------------------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Jungle_fortress_small_1"],
            unit_list=[UnitInfo.PALADIN.ID, UnitInfo.ELITE_CONQUISTADOR.ID],
            quantity=[40, 40],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="jungle_fortress_small_defence_1",
            rule_to_activate="jungle_fortress_small_defence_2",

        ),
        Building_config(
            barrack=barrack_list["Jungle_fortress_small_1"],
            unit_list=[UnitInfo.ELITE_TEMPLE_GUARD.ID, UnitInfo.HEAVY_CROSSBOWMAN.ID],
            quantity=[40, 40],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="jungle_fortress_small_defence_2",
            rule_to_activate="jungle_fortress_small_defence_1",

        ),
        Building_config(
            barrack=barrack_list["Jungle_fortress_small_2"],
            unit_list=[HeroInfo.AETHELFRITH.ID],
            quantity=[80],
            spawn_rate=[10],
            spawn_time=15,
            rule="jungle_fortress_small_defence_3",
            rule_to_activate="jungle_fortress_small_defence_4",

        ),
        Building_config(
            barrack=barrack_list["Jungle_fortress_small_2"],
            unit_list=[UnitInfo.ELITE_PLUMED_ARCHER.ID, UnitInfo.ONAGER.ID],
            quantity=[40, 20],
            spawn_rate=[10, 5],
            spawn_time=15,
            rule="jungle_fortress_small_defence_4",
            rule_to_activate="jungle_fortress_small_defence_3",

        ),

        Building_config(
            barrack=barrack_list["Jungle_fortress_small_3"],
            unit_list=[UnitInfo.CENTURION.ID,UnitInfo.LEGIONARY.ID],
            quantity=[40,50],
            spawn_rate=[10,10],
            spawn_time=15,
            rule="jungle_fortress_small_defence_5",
            rule_to_activate="jungle_fortress_small_defence_6",

        ),
        Building_config(
            barrack=barrack_list["Jungle_fortress_small_3"],
            unit_list=[UnitInfo.ELITE_LONGBOWMAN.ID, UnitInfo.URUMI_SWORDSMAN.ID],
            quantity=[40, 40],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="jungle_fortress_small_defence_6",
            rule_to_activate="jungle_fortress_small_defence_5",

        ),

        Building_config(
            barrack=barrack_list["Jungle_fortress_small_4"],
            unit_list=[UnitInfo.ELITE_SERJEANT.ID, UnitInfo.ELITE_KIPCHAK.ID],
            quantity=[30, 30],
            spawn_rate=[5, 5],
            spawn_time=15,
            rule="jungle_fortress_small_defence_7",
            rule_to_activate="jungle_fortress_small_defence_8",

        ),
        Building_config(
            barrack=barrack_list["Jungle_fortress_small_4"],
            unit_list=[UnitInfo.CHAMPION.ID, UnitInfo.ELITE_LEITIS.ID],
            quantity=[40, 40],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="jungle_fortress_small_defence_8",
            rule_to_activate="jungle_fortress_small_defence_7",

        ),
#--------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Mid_defence_zone_1"],
            unit_list=[HeroInfo.FRANKISH_PALADIN.ID, HeroInfo.CHARLEMAGNE.ID],
            quantity=[60, 60],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_1",
            rule_to_activate="Mid_area_defence_2",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_1"],
            unit_list=[HeroInfo.DMITRY_OF_MOSCOW.ID, HeroInfo.IVAYLO.ID],
            quantity=[40, 40],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_2",
            rule_to_activate="Mid_area_defence_3",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_1"],
            unit_list=[UnitInfo.ARBALESTER.ID, HeroInfo.HENRY_THE_LION.ID],
            quantity=[75, 90],
            spawn_rate=[15, 15],
            spawn_time=15,
            rule="Mid_area_defence_3",
            rule_to_activate="Mid_area_defence_4",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_1"],
            unit_list=[HeroInfo.CUSI_YUPANQUI.ID, HeroInfo.PACAL_II.ID],
            quantity=[80, 80],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_4",
            rule_to_activate="Mid_area_defence_1",

        ),
#------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Mid_defence_zone_2"],
            unit_list=[HeroInfo.FRANKISH_PALADIN.ID, HeroInfo.CHARLEMAGNE.ID],
            quantity=[60, 60],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_5",
            rule_to_activate="Mid_area_defence_6",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_2"],
            unit_list=[HeroInfo.ARTAPHERNES.ID, HeroInfo.BRASIDAS.ID],
            quantity=[70, 70],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_6",
            rule_to_activate="Mid_area_defence_8",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_2"],
            unit_list=[UnitInfo.JIAN_SWORDSMAN_TWO_HANDED.ID, HeroInfo.ARCHER_OF_THE_EYES.ID],
            quantity=[140, 100],
            spawn_rate=[14, 10],
            spawn_time=15,
            rule="Mid_area_defence_8",
            rule_to_activate="Mid_area_defence_9",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_2"],
            unit_list=[HeroInfo.BAYINNAUNG.ID, HeroInfo.PACAL_II.ID],
            quantity=[120, 120],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_9",
            rule_to_activate="Mid_area_defence_5",

        ),
# ------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Mid_defence_zone_3"],
            unit_list=[HeroInfo.GAWAIN.ID, HeroInfo.RAJENDRA_CHOLA.ID],
            quantity=[60, 60],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_10",
            rule_to_activate="Mid_area_defence_11",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_3"],
            unit_list=[HeroInfo.MASTER_OF_THE_TEMPLAR.ID, HeroInfo.VASCO_DA_GAMA.ID],
            quantity=[70, 70],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_11",
            rule_to_activate="Mid_area_defence_12",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_3"],
            unit_list=[UnitInfo.JANISSARY.ID, UnitInfo.CATAPHRACT.ID],
            quantity=[140, 100],
            spawn_rate=[14, 10],
            spawn_time=15,
            rule="Mid_area_defence_12",
            rule_to_activate="Mid_area_defence_13",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_3"],
            unit_list=[UnitInfo.HUSKARL.ID],
            quantity=[300],
            spawn_rate=[30],
            spawn_time=15,
            rule="Mid_area_defence_13",
            rule_to_activate="Mid_area_defence_10",

        ),
# ------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Mid_defence_zone_4"],
            unit_list=[UnitInfo.ELITE_SERJEANT.ID, UnitInfo.ELEPHANT_ARCHER.ID],
            quantity=[120, 120],
            spawn_rate=[20, 20],
            spawn_time=15,
            rule="Mid_area_defence_14",
            rule_to_activate="Mid_area_defence_15",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_4"],
            unit_list=[UnitInfo.ELITE_JANISSARY.ID, UnitInfo.ELITE_SAMURAI.ID],
            quantity=[100, 110],
            spawn_rate=[20, 10],
            spawn_time=15,
            rule="Mid_area_defence_15",
            rule_to_activate="Mid_area_defence_16",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_4"],
            unit_list=[UnitInfo.CHAMPION.ID, UnitInfo.ARBALESTER.ID],
            quantity=[140, 100],
            spawn_rate=[20, 10],
            spawn_time=15,
            rule="Mid_area_defence_16",
            rule_to_activate="Mid_area_defence_17",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_4"],
            unit_list=[UnitInfo.ELITE_BALLISTA_ELEPHANT.ID, UnitInfo.ELITE_MONASPA.ID],
            quantity=[120, 120],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_17",
            rule_to_activate="Mid_area_defence_14",

        ),
#----------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Mid_defence_zone_5"],
            unit_list=[UnitInfo.ELITE_ARAMBAI.ID, UnitInfo.ELITE_KESHIK.ID],
            quantity=[120, 120],
            spawn_rate=[20, 20],
            spawn_time=15,
            rule="Mid_area_defence_18",
            rule_to_activate="Mid_area_defence_19",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_5"],
            unit_list=[UnitInfo.ELITE_WHITE_FEATHER_GUARD.ID, UnitInfo.ELITE_TARKAN.ID],
            quantity=[100, 110],
            spawn_rate=[20, 10],
            spawn_time=15,
            rule="Mid_area_defence_19",
            rule_to_activate="Mid_area_defence_20",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_5"],
            unit_list=[UnitInfo.ELITE_GHULAM.ID, UnitInfo.ELITE_RATHA_RANGED.ID],
            quantity=[140, 140],
            spawn_rate=[20, 20],
            spawn_time=15,
            rule="Mid_area_defence_20",
            rule_to_activate="Mid_area_defence_21",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_5"],
            unit_list=[HeroInfo.BABUR.ID, HeroInfo.HROLF_THE_GANGER.ID],
            quantity=[120, 120],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_21",
            rule_to_activate="Mid_area_defence_18",

        ),
# ----------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Mid_defence_zone_6"],
            unit_list=[UnitInfo.ELITE_KESHIK.ID, UnitInfo.ELITE_MAMELUKE.ID],
            quantity=[80, 80],
            spawn_rate=[20, 20],
            spawn_time=15,
            rule="Mid_area_defence_22",
            rule_to_activate="Mid_area_defence_23",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_6"],
            unit_list=[UnitInfo.ELITE_CHU_KO_NU.ID, UnitInfo.ELITE_FIRE_LANCER.ID],
            quantity=[100, 110],
            spawn_rate=[20, 10],
            spawn_time=15,
            rule="Mid_area_defence_23",
            rule_to_activate="Mid_area_defence_25",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_6"],
            unit_list=[UnitInfo.ELITE_IRON_PAGODA.ID, UnitInfo.PALADIN.ID],
            quantity=[150, 150],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_25",
            rule_to_activate="Mid_area_defence_26",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_6"],
            unit_list=[HeroInfo.BABUR.ID, HeroInfo.HROLF_THE_GANGER.ID],
            quantity=[120, 120],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_26",
            rule_to_activate="Mid_area_defence_22",

        ),
# ----------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Mid_defence_zone_7"],
            unit_list=[UnitInfo.BERSERK.ID, 2704],
            quantity=[120, 120],
            spawn_rate=[20, 20],
            spawn_time=15,
            rule="Mid_area_defence_27",
            rule_to_activate="Mid_area_defence_28",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_7"],
            unit_list=[UnitInfo.WAR_ELEPHANT.ID, UnitInfo.ELEPHANT_ARCHER.ID],
            quantity=[110, 110],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_28",
            rule_to_activate="Mid_area_defence_29",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_7"],
            unit_list=[UnitInfo.ELITE_BLACKWOOD_ARCHER.ID, UnitInfo.SIEGE_ONAGER.ID],
            quantity=[140, 14],
            spawn_rate=[20, 1],
            spawn_time=15,
            rule="Mid_area_defence_29",
            rule_to_activate="Mid_area_defence_31",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_7"],
            unit_list=[UnitInfo.MAGYAR_HUSZAR.ID, HeroInfo.HROLF_THE_GANGER.ID],
            quantity=[120, 120],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_31",
            rule_to_activate="Mid_area_defence_27",

        ),
# ----------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Mid_defence_zone_8"],
            unit_list=[UnitInfo.ELITE_PATTIYODHA_LONGBOWMAN.ID, UnitInfo.ELITE_TEMPLE_GUARD.ID],
            quantity=[180, 200],
            spawn_rate=[10, 20],
            spawn_time=15,
            rule="Mid_area_defence_32",
            rule_to_activate="Mid_area_defence_33",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_8"],
            unit_list=[UnitInfo.ELITE_TIGER_CAVALRY.ID, UnitInfo.ELITE_SKIRMISHER.ID],
            quantity=[110, 110],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_33",
            rule_to_activate="Mid_area_defence_34",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_8"],
            unit_list=[UnitInfo.HEAVY_CAVALRY_ARCHER.ID, UnitInfo.IMPERIAL_CAMEL_RIDER.ID],
            quantity=[140, 14],
            spawn_rate=[20, 1],
            spawn_time=15,
            rule="Mid_area_defence_34",
            rule_to_activate="Mid_area_defence_35",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_8"],
            unit_list=[UnitInfo.HEAVY_HEI_GUANG_CAVALRY.ID, HeroInfo.FREDERICK_BARBAROSSA.ID],
            quantity=[120, 120],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_35",
            rule_to_activate="Mid_area_defence_32",

        ),
# ----------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Mid_defence_zone_9"],
            unit_list=[UnitInfo.HEAVY_CROSSBOWMAN.ID, UnitInfo.ELITE_WOAD_RAIDER.ID],
            quantity=[120, 120],
            spawn_rate=[20, 20],
            spawn_time=15,
            rule="Mid_area_defence_36",
            rule_to_activate="Mid_area_defence_37",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_9"],
            unit_list=[UnitInfo.EASTERN_SWORDSMAN.ID],
            quantity=[400],
            spawn_rate=[40],
            spawn_time=15,
            rule="Mid_area_defence_37",
            rule_to_activate="Mid_area_defence_38",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_9"],
            unit_list=[UnitInfo.HAND_CANNONEER.ID, UnitInfo.SIEGE_RAM.ID],
            quantity=[140, 14],
            spawn_rate=[20, 1],
            spawn_time=15,
            rule="Mid_area_defence_38",
            rule_to_activate="Mid_area_defence_39",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_9"],
            unit_list=[UnitInfo.ELITE_MONASPA.ID, HeroInfo.CHARLEMAGNE.ID],
            quantity=[120, 120],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_39",
            rule_to_activate="Mid_area_defence_36",

        ),
# ----------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Mid_defence_zone_10"],
            unit_list=[UnitInfo.HALBERDIER.ID, UnitInfo.ELITE_PLUMED_ARCHER.ID],
            quantity=[120, 120],
            spawn_rate=[20, 20],
            spawn_time=15,
            rule="Mid_area_defence_40",
            rule_to_activate="Mid_area_defence_41",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_10"],
            unit_list=[UnitInfo.LEGIONARY.ID,UnitInfo.CATAPHRACT.ID],
            quantity=[200,200],
            spawn_rate=[20,20],
            spawn_time=15,
            rule="Mid_area_defence_41",
            rule_to_activate="Mid_area_defence_42",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_10"],
            unit_list=[UnitInfo.HEAVY_CAMEL_RIDER.ID, UnitInfo.ELITE_MAMELUKE.ID],
            quantity=[140, 140],
            spawn_rate=[20, 20],
            spawn_time=15,
            rule="Mid_area_defence_42",
            rule_to_activate="Mid_area_defence_43",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_10"],
            unit_list=[UnitInfo.ELITE_CAMEL_ARCHER.ID, UnitInfo.CAVALIER.ID],
            quantity=[120, 120],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_43",
            rule_to_activate="Mid_area_defence_40",

        ),
# ----------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["Mid_defence_zone_11"],
            unit_list=[UnitInfo.ELITE_JAGUAR_WARRIOR.ID, UnitInfo.ELITE_LONGBOWMAN.ID],
            quantity=[120, 120],
            spawn_rate=[20, 20],
            spawn_time=15,
            rule="Mid_area_defence_44",
            rule_to_activate="Mid_area_defence_45",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_11"],
            unit_list=[UnitInfo.ELITE_BERSERK.ID,UnitInfo.TWO_HANDED_SWORDSMAN.ID],
            quantity=[100,150],
            spawn_rate=[10,15],
            spawn_time=15,
            rule="Mid_area_defence_45",
            rule_to_activate="Mid_area_defence_46",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_11"],
            unit_list=[UnitInfo.JARL.ID, UnitInfo.HOUFNICE.ID],
            quantity=[45, 14],
            spawn_rate=[5, 1],
            spawn_time=15,
            rule="Mid_area_defence_46",
            rule_to_activate="Mid_area_defence_48",

        ),
        Building_config(
            barrack=barrack_list["Mid_defence_zone_11"],
            unit_list=[UnitInfo.ORGAN_GUN.ID, UnitInfo.ELITE_MANGUDAI.ID],
            quantity=[120, 120],
            spawn_rate=[10, 10],
            spawn_time=15,
            rule="Mid_area_defence_48",
            rule_to_activate="Mid_area_defence_44",

        ),
        # ----------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["last_area_1"],
            unit_list=[HeroInfo.GAJAH_MADA.ID, HeroInfo.MUSTAFA_PASHA.ID, HeroInfo.FRANCISCO_DE_ORELLANA.ID],
            quantity=[300, 200, 150],
            spawn_rate=[20, 20, 15],
            spawn_time=15,
            rule="Final_area_defence_1",
            rule_to_activate="Final_area_defence_2",

        ),
        Building_config(
            barrack=barrack_list["last_area_1"],
            unit_list=[HeroInfo.ABRAHA_ELEPHANT.ID, HeroInfo.GAWAIN.ID, HeroInfo.ROBIN_HOOD.ID],
            quantity=[400, 300, 150],
            spawn_rate=[20, 15, 15],
            spawn_time=15,
            rule="Final_area_defence_2",
            rule_to_activate="Final_area_defence_3",

        ),
        Building_config(
            barrack=barrack_list["last_area_1"],
            unit_list=[HeroInfo.SALADIN.ID, UnitInfo.HALBERDIER.ID, HeroInfo.THEODORIC_THE_GOTH.ID,
                       HeroInfo.POPE_LEO_I.ID],
            quantity=[230, 300, 150, 100],
            spawn_rate=[23, 30, 15, 10],
            spawn_time=15,
            rule="Final_area_defence_3",
            rule_to_activate="Final_area_defence_4",

        ),
        Building_config(
            barrack=barrack_list["last_area_1"],
            unit_list=[HeroInfo.TARIQ_IBN_ZIYAD.ID, HeroInfo.SUBOTAI.ID, HeroInfo.GENGHIS_KHAN.ID,
                       HeroInfo.CUMAN_CHIEF.ID],
            quantity=[120, 130, 130, 200],
            spawn_rate=[12, 13, 13, 10],
            spawn_time=15,
            rule="Final_area_defence_4",
            rule_to_activate="Final_area_defence_5",

        ),
        Building_config(
            barrack=barrack_list["last_area_1"],
            unit_list=[HeroInfo.AETHELFRITH.ID, HeroInfo.THEODORIC_THE_GOTH.ID, HeroInfo.FREDERICK_BARBAROSSA.ID,
                       UnitInfo.SIEGE_ONAGER.ID],
            quantity=[300, 150, 300, 60],
            spawn_rate=[15, 15, 15, 10],
            spawn_time=15,
            rule="Final_area_defence_5",
            rule_to_activate="Final_area_defence_1",

        ),
        # ----------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["last_area_2"],
            unit_list=[HeroInfo.BABUR.ID, HeroInfo.EDWARD_LONGSHANKS.ID, HeroInfo.ERIK_THE_RED.ID,
                       UnitInfo.HEAVY_SCORPION.ID],
            quantity=[150, 200, 120, 100],
            spawn_rate=[15, 20, 12, 10],
            spawn_time=35,
            rule="Final_area_defence_6",
            rule_to_activate="Final_area_defence_7",

        ),
        Building_config(
            barrack=barrack_list["last_area_2"],
            unit_list=[UnitInfo.ELITE_BERSERK.ID, HeroInfo.THEODORIC_THE_GOTH.ID, HeroInfo.ATTILA_THE_HUN.ID,
                       HeroInfo.BAYINNAUNG.ID, HeroInfo.GUGLIELMO_EMBRIACO.ID],
            quantity=[75, 5, 150, 200, 140],
            spawn_rate=[75, 5, 15, 20, 14],
            spawn_time=35,
            rule="Final_area_defence_7",
            rule_to_activate="Final_area_defence_8",

        ),
        Building_config(
            barrack=barrack_list["last_area_2"],
            unit_list=[HeroInfo.IVANE.ID, HeroInfo.GAWAIN.ID, HeroInfo.GIDAJAN.ID, HeroInfo.EL_CID_CAMPEADOR.ID],
            quantity=[140, 140, 200, 120],
            spawn_rate=[14, 14, 20, 12],
            spawn_time=35,
            rule="Final_area_defence_8",
            rule_to_activate="Final_area_defence_9",

        ),
        Building_config(
            barrack=barrack_list["last_area_2"],
            unit_list=[HeroInfo.KITABATAKE.ID, UnitInfo.SIEGE_ONAGER.ID, HeroInfo.MORDRED.ID, HeroInfo.BELISARIUS.ID,
                       UnitInfo.ELITE_HUSSITE_WAGON.ID],
            quantity=[170, 45, 175, 175, 75],
            spawn_rate=[17, 15, 15, 15, 15],
            spawn_time=35,
            rule="Final_area_defence_9",
            rule_to_activate="Final_area_defence_10",

        ),
        Building_config(
            barrack=barrack_list["last_area_2"],
            unit_list=[HeroInfo.KING_ARTHUR.ID, HeroInfo.GENERAL_ARAIYAN.ID, HeroInfo.HENRY_THE_LION.ID,
                       HeroInfo.HEPHAISTION.ID, UnitInfo.HOUFNICE.ID],
            quantity=[175, 200, 175, 175, 15],
            spawn_rate=[15, 20, 15, 15, 15],
            spawn_time=35,
            rule="Final_area_defence_10",
            rule_to_activate="Final_area_defence_6",

        ),
        # ----------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["last_area_3"],
            unit_list=[HeroInfo.EL_CID.ID, HeroInfo.FREDERICK_BARBAROSSA.ID, HeroInfo.THEODORIC_THE_GOTH.ID,
                       UnitInfo.ELITE_THROWING_AXEMAN.ID],
            quantity=[175, 175, 175, 175],
            spawn_rate=[15, 15, 15, 15],
            spawn_time=15,
            rule="Final_area_defence_11",
            rule_to_activate="Final_area_defence_12",

        ),
        Building_config(
            barrack=barrack_list["last_area_3"],
            unit_list=[UnitInfo.ELITE_WAR_ELEPHANT.ID, UnitInfo.ELITE_ELEPHANT_ARCHER.ID],
            quantity=[200, 200],
            spawn_rate=[20, 20],
            spawn_time=25,
            rule="Final_area_defence_12",
            rule_to_activate="Final_area_defence_13",

        ),
        Building_config(
            barrack=barrack_list["last_area_3"],
            unit_list=[HeroInfo.ALGIRDAS.ID, HeroInfo.KHOSRAU.ID, UnitInfo.FLAMING_CAMEL.ID,
                       UnitInfo.HEAVY_ROCKET_CART.ID],
            quantity=[175, 175, 90, 5],
            spawn_rate=[15, 15, 30, 5],
            spawn_time=15,
            rule="Final_area_defence_13",
            rule_to_activate="Final_area_defence_14",

        ),
        Building_config(
            barrack=barrack_list["last_area_3"],
            unit_list=[HeroInfo.ROBIN_HOOD.ID, HeroInfo.MUSA_IBN_NUSAYR.ID, HeroInfo.ARTAPHERNES.ID,
                       UnitInfo.SIEGE_RAM.ID],
            quantity=[175, 180, 180, 20],
            spawn_rate=[15, 18, 18, 20],
            spawn_time=25,
            rule="Final_area_defence_14",
            rule_to_activate="Final_area_defence_15",

        ),
        Building_config(
            barrack=barrack_list["last_area_3"],
            unit_list=[HeroInfo.SHERIFF_OF_NOTTINGHAM.ID, HeroInfo.THEODORIC_THE_GOTH.ID, HeroInfo.GAWAIN.ID,
                       HeroInfo.MORDRED.ID, HeroInfo.JOAN_OF_ARC.ID],
            quantity=[200, 200, 200, 175, 200],
            spawn_rate=[20, 20, 20, 15, 20],
            spawn_time=30,
            rule="Final_area_defence_15",
            rule_to_activate="Final_area_defence_11",

        ),
        # ----------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["last_area_4"],
            unit_list=[HeroInfo.GAJAH_MADA.ID, HeroInfo.CHARLEMAGNE.ID, HeroInfo.ROBERT_GUISCARD.ID,
                       HeroInfo.AMOGHAVARSHA.ID, HeroInfo.GONZALO_PIZARRO.ID],
            quantity=[150, 150, 150, 150, 200],
            spawn_rate=[15, 15, 15, 15, 20],
            spawn_time=45,
            rule="Final_area_defence_16",
            rule_to_activate="Final_area_defence_17",

        ),
        Building_config(
            barrack=barrack_list["last_area_4"],
            unit_list=[HeroInfo.ALEXANDER_NEVSKI.ID, HeroInfo.HARALD_HARDRADA.ID, HeroInfo.CUAUHTEMOC.ID,
                       HeroInfo.EMPEROR_SIGISMUND.ID, HeroInfo.ARCHER_OF_THE_EYES.ID],
            quantity=[200, 150, 150, 175, 200],
            spawn_rate=[20, 15, 15, 15, 20],
            spawn_time=45,
            rule="Final_area_defence_17",
            rule_to_activate="Final_area_defence_18",

        ),
        Building_config(
            barrack=barrack_list["last_area_4"],
            unit_list=[HeroInfo.ABRAHA_ELEPHANT.ID, HeroInfo.BABUR.ID, HeroInfo.ARISTAGORAS.ID, UnitInfo.CENTURION.ID,
                       HeroInfo.DINH_LE.ID],
            quantity=[100, 100, 200, 200, 120],
            spawn_rate=[10, 10, 20, 20, 12],
            spawn_time=35,
            rule="Final_area_defence_18",
            rule_to_activate="Final_area_defence_19",

        ),
        Building_config(
            barrack=barrack_list["last_area_4"],
            unit_list=[UnitInfo.ELITE_BERSERK.ID, UnitInfo.ELITE_THROWING_AXEMAN.ID, UnitInfo.ELITE_TEUTONIC_KNIGHT.ID,
                       UnitInfo.ELITE_COUSTILLIER.ID, UnitInfo.ELITE_JANISSARY.ID,
                       UnitInfo.ELITE_KAMAYUK.ID, UnitInfo.ELITE_HUSKARL.ID, UnitInfo.ELITE_URUMI_SWORDSMAN.ID,
                       UnitInfo.ELITE_BALLISTA_ELEPHANT.ID, UnitInfo.SIEGE_RAM.ID],
            quantity=[30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
            spawn_rate=[10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            spawn_time=25,
            rule="Final_area_defence_19",
            rule_to_activate="Final_area_defence_16",

        ),
        # ----------------------------------------------------------------------------------------------
        Building_config(
            barrack=barrack_list["last_area_5"],
            unit_list=[HeroInfo.ITZCOATL.ID, HeroInfo.PACAL_II.ID, UnitInfo.SIEGE_RAM.ID],
            quantity=[300, 300, 50],
            spawn_rate=[15, 15, 5],
            spawn_time=15,
            rule="Final_area_defence_20",
            rule_to_activate="Final_area_defence_21",

        ),
        Building_config(
            barrack=barrack_list["last_area_5"],
            unit_list=[HeroInfo.NORSE_CHIEFTAIN.ID, UnitInfo.ELITE_BERSERK.ID, HeroInfo.DATIS.ID,
                       UnitInfo.HEAVY_SCORPION.ID],
            quantity=[120, 120, 150, 75],
            spawn_rate=[12, 12, 15, 15],
            spawn_time=25,
            rule="Final_area_defence_21",
            rule_to_activate="Final_area_defence_22",

        ),
        Building_config(
            barrack=barrack_list["last_area_5"],
            unit_list=[UnitInfo.ELITE_FIRE_ARCHER.ID, UnitInfo.ELITE_CATAPHRACT.ID, HeroInfo.GUACOLDA.ID,
                       HeroInfo.KOTYAN_KHAN.ID, UnitInfo.FLAMING_CAMEL.ID],
            quantity=[175, 175, 45, 100, 15],
            spawn_rate=[15, 15, 45, 10, 15],
            spawn_time=15,
            rule="Final_area_defence_22",
            rule_to_activate="Final_area_defence_23",

        ),
        Building_config(
            barrack=barrack_list["last_area_5"],
            unit_list=[HeroInfo.LUU_NHAN_CHU.ID, HeroInfo.MASTER_OF_THE_TEMPLAR.ID, UnitInfo.BOMBARD_CANNON.ID,
                       UnitInfo.SIEGE_RAM.ID, UnitInfo.ELITE_KAMAYUK.ID],
            quantity=[200, 200, 45, 45, 300],
            spawn_rate=[20, 20, 5, 5, 30],
            spawn_time=20,
            rule="Final_area_defence_23",
            rule_to_activate="Final_area_defence_24",

        ),
        Building_config(
            barrack=barrack_list["last_area_5"],
            unit_list=[HeroInfo.MINAMOTO.ID, HeroInfo.MUSTAFA_PASHA.ID, HeroInfo.OSMAN.ID, HeroInfo.ORNLU_THE_WOLF.ID,
                       UnitInfo.FLAMETHROWER.ID, HeroInfo.SUBOTAI.ID],
            quantity=[175, 175, 175, 200, 175, 175],
            spawn_rate=[15, 15, 15, 20, 15, 15],
            spawn_time=15,
            rule="Final_area_defence_24",
            rule_to_activate="Final_area_defence_20",

        ),
    ]
# def barrack_rule(scenario,unit_list,barrack,spawn_rate,spawn_time,quantity,rule,rule_to_activate)
    for cfg in barrack_config:
        barrack_rule(
            scenario,
            unit_list=cfg.unit_list,
            barrack=cfg.barrack,
            spawn_rate=cfg.spawn_rate,
            spawn_time=cfg.spawn_time,
            quantity = cfg.quantity,
            rule = cfg.rule,
            rule_to_activate = cfg.rule_to_activate,
        )