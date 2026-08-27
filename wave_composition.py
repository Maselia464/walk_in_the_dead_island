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
from dataclasses import dataclass
from typing import Optional



@dataclass
class SpawnConfig:
    main_vector : list #XS use vector to handle coordinate, vector contains X Y AND Z, Z is never used because AOE 2 has fake height
    second_area_vector : list #This value is optionnal, basically certain part of the map aren't
    # open to the player until they reach it, once they reach enemy can spawn here, otherwise it send back to main
    unit: list      # The unit ID, using the unit dataset of parser, can take multiple unit
    danger_level: list #XS function I made, basically it's a value that keep increasing diificulty inb this case danger level must be between two value to activate the rule

    quantity: list #Number of total unit
    spawn_rate: list # Number of unit that spawn in one volley
    rule_name: str #The name of the rule important since XS kinda hate same name, even if the documentation say otherwise, DESYNC EXIST, AND DESYNC LOVE TO DO RANDOM BS
coord_spawn_main_spawn = {
#Dictionary that will contains all the possible spawning area and spawn variation

    #Some_area_name = [(X_coord,Y_coord
    # ,incrementation of X(only positive), incrementation of Y (only positive)
    # ,coord where the x stop at, coord where the y stop at]

    "right side a": [(1.0,1.0,
                      1.0,1.0,
                      15,8)],

    "right side b": [(8.0,8.0,
                      7.0,7.0,
                      15,8)],
    "up_corner_spawn" : [(
                          194.0,0.0
                          ,1.0,1.0,
                          5,30,"value")]

}
spawn_data_wave = [ #Here for this wave I summon 35 longbowman five per volley and 77 royal janisary seven per volley at the same place
    #Making list allow me to place multiple unit in the same rule avoiding endless of CTRL C and CTRL V or for loop with list in for loop
    SpawnConfig(
        second_area_vector=[
            coord_spawn_main_spawn["up_corner_spawn"],
            coord_spawn_main_spawn["up_corner_spawn"],
        ],
        main_vector=[
        coord_spawn_main_spawn["right side a"],
        coord_spawn_main_spawn["right side b"],
    ],
        unit=[UnitInfo.MILITIA.ID,UnitInfo.SPEARMAN.ID],
        danger_level=[0,15],
        quantity=[45,45],
        spawn_rate=[5,7],
        rule_name="Main_wave_start",
    ),

SpawnConfig(
        second_area_vector=[
            coord_spawn_main_spawn["up_corner_spawn"],
            coord_spawn_main_spawn["up_corner_spawn"],
        ],
        main_vector=[
        coord_spawn_main_spawn["right side a"],
        coord_spawn_main_spawn["right side b"],
    ],
        unit=[UnitInfo.LONGBOWMAN.ID,UnitInfo.ROYAL_JANISSARY.ID],
        danger_level=[35,45],
        quantity=[35,77],
        spawn_rate=[5,7],
        rule_name="Side_wave",
    ),
]