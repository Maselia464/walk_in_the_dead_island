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



from unicodedata import category
# Dictionnaire pour le script
from AoE2ScenarioParser.objects.support.area import Area
def xs_function (scenario,trigger_manager):
    xs_input_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\AoE2DE\\resources\\_common\\xs\\security_breach_in_ruin.xs"
    xs_level_function = f"""//XS script for security breach in ruin, feel free to read it to crack the map\n
int pop_cap_res = 32;
float up_value = 0;"""

    for p in range (1,8):
        xs_level_function +=f"""
int P{p}_KILL = 0; //Keep track of the kill P{p} made
int previous_value_P{p} = 0; //used for the IF condition to detect if P{p} made a new kill
int P{p}_level = 0;

float P{p}_required_XP = 36;
float XP_P{p} = 0; // The value for P{p} XP and level
float XP_value_P{p} = 1.0; // The value of XP P{p} receive after each kill, this value is meant to be changed by outside factor
float P{p}_XP_increase = 1.20;
float more_pop_P{p} = 0.0;
float bonus_pop_P{p} = 0.0;
    """
        #XS AURA FUNCTION
    xs_level_function += """
    bool xsAddAura(
    int auraUnit = -1, /* unit to add the aura to */
    int affectedUnit = -1, /* unit or unit class (9xx) to be affected by the aura */
    int player = -1, /* aura unit player, does not work with -1, make multiple calls to all players instead */
    int attribute = -1, /* aura attribute, not all attributes supported by auras */
    float value = 0, /* aura value */ 
    float range = 0,  /* aura range */
    int auraEffectsBitField = 0, /* bit field for aura effects, constants are provided, add them together for multiple effects */
    int targetDiplomacy = 0, /* aura target diplomacy, controls what diplomacy target unit needs to be to be affected, constants are provided */
    int tempAuraDuration = 0, /* only works with cAuraEffectBitTemporary effect, specifies how long the temp aura lasts in seconds */
    int tempAuraCooldown = 0, /* only works with cAuraEffectBitTemporary effect, specifies how long the cooldown period lasts is in seconds */
    int unitsInRangeToTurnOn = 1, /* how many units need to be in range for aura to turn on */
    bool affectSelf = false /* if set makes aura affect auraUnit instead, affectedUnit still needs to be in range to activate */
) {
    /* Function adds an aura to the provided unit based on a your config. 
    Note that adding auras "freezes" the unit for further non task modifications.
    To work around that can respawn the unit or do a double replace with another unit and itself.
    Adding an aura to a unit of the same player that already has an aura for the same attribute and affectedUnit will overwrite it instead.
    Function returns `true` if function parameter validation passed and `false` if it did not (no aura added). */

    /* Validation */
    if (auraUnit < 0 || affectedUnit < 0 || player < 0 || player > 8) {
        return (false);
    }
    if (range < 0 || auraEffectsBitField < 0 || targetDiplomacy < 0 || targetDiplomacy > 6 
        || unitsInRangeToTurnOn < 0 || tempAuraDuration < 0 || tempAuraCooldown < 0) {
        return (false);
    }

    /* Handling gaia player */
    int setCommand = cSetAttribute;
    if (player == 0) {
        setCommand = cGaiaSetAttribute;
    }

    /* Setting right combat ability flags */
    float ca = xsGetObjectAttribute(player, auraUnit, cCombatAbility);
    if (ca < 0) {
        ca = 0;
    }
    float caMod = 0;
    float auraBit = (ca / 32) % 2;
    if (auraBit == 0) {
        caMod = 32;
    }
    float selfBit = (ca / 64) % 2;
    if (affectSelf && selfBit == 0) {
        caMod = caMod + 64;
    } else if (affectSelf == false && selfBit == 1) {
        caMod = caMod - 64;
    }
    if (caMod != 0) {
        xsEffectAmount(setCommand, auraUnit, cCombatAbility, ca + caMod, player);
    }

    /* Setting temporary aura values if enabled */
    int tempEffectBit = (auraEffectsBitField / 8) % 2;
    if (tempEffectBit == 1) {
        float maxCharge = 1;
        float cdRatio = 1000;
        if (tempAuraCooldown > 0) {
            float tacf = tempAuraCooldown;
            cdRatio = maxCharge / tacf;
        }
        xsEffectAmount(setCommand, auraUnit, cMaxCharge, maxCharge, player);
        xsEffectAmount(setCommand, auraUnit, cRechargeRate, cdRatio, player);
        xsEffectAmount(setCommand, auraUnit, cChargeEvent, 0.0 + tempAuraDuration, player);
        xsEffectAmount(setCommand, auraUnit, cChargeType, -3.0, player);
    }

    /* Setting aura task */
    xsResetTaskAmount();
    xsTaskAmount(cTaskAttrWorkValue1, value);
    xsTaskAmount(cTaskAttrWorkValue2, 0.0 + unitsInRangeToTurnOn);
    xsTaskAmount(cTaskAttrWorkRange, range);
    xsTaskAmount(cTaskAttrSearchWaitTime, 0.0 + attribute);
    xsTaskAmount(cTaskAttrCombatLevelFlag, 0.0 + auraEffectsBitField);
    xsTaskAmount(cTaskAttrOwnerType, 0.0 + targetDiplomacy);
    xsTask(auraUnit, 155, affectedUnit, player);

    return (true);
}

bool xsRemoveAura(
    int auraUnit = -1, /* unit from which remove the aura */
    int affectedUnit = -1, /* unit or unit class (9xx) to be affected by the aura */
    int player = -1, /* aura unit player, does not work with -1, make multiple calls to all players instead */
    int attribute = -1, /* aura attribute, not all attributes supported by auras */
    bool removeTempAuraAttributes = false, /* if set removes temp aura attributes from unit */
    bool removeAllAuraAbilities = false /* if set removes unit aura ability disabling all auras and removing indicators */
) { 
    /* Function removes the aura added by xsAddAura. Leaves combat ability unchanged. 
    Removing auras "freezes" the unit for further non task modifications.
    Function returns `true` if function parameter validation passed and `false` if it did not (no aura removed). */

    /* Validation */
    if (auraUnit < 0 || affectedUnit < 0 || player < 0 || player > 8) {
        return (false);
    }

    /* Handling gaia player */
    int setCommand = cSetAttribute;
    if (player == 0) {
        setCommand = cGaiaSetAttribute;
    }

    /* Remove temporary aura values */
    if (removeTempAuraAttributes) {
        float ct = xsGetObjectAttribute(player, auraUnit, cChargeType);
        if (ct == -3) {
            xsEffectAmount(setCommand, auraUnit, cMaxCharge, 0.0, player);
            xsEffectAmount(setCommand, auraUnit, cRechargeRate, 0.0, player);
            xsEffectAmount(setCommand, auraUnit, cChargeEvent, 0.0, player);
            xsEffectAmount(setCommand, auraUnit, cChargeType, 0.0, player);
        }
    }

    /* Remove combat ability */
    if (removeAllAuraAbilities) {
        float ca = xsGetObjectAttribute(player, auraUnit, cCombatAbility);
        float caMod = 0;
        float auraBit = (ca / 32) % 2;
        if (auraBit == 1) {
            caMod = -32;
        }
        float selfBit = (ca / 64) % 2;
        if (selfBit == 1) {
            caMod = caMod - 64;
        }
        if (caMod != 0) {
            xsEffectAmount(setCommand, auraUnit, cCombatAbility, ca + caMod, player);
        }
    }

    /* Setting aura task */
    xsTaskAmount(cTaskAttrSearchWaitTime, 0.0 + attribute);
    xsRemoveTask(auraUnit, 155, affectedUnit, player);

    return (true);
}

extern const int cAuraEffectBitMultiply = 1; /* if not added, value is added instead */
extern const int cAuraEffectBitCircular = 2; /* if not added, aura is square shaped */
extern const int cAuraEffectBitRangeIndicator = 4;
extern const int cAuraEffectBitTemporary = 8;
extern const int cAuraEffectBitAppliedWhenActivatedOnly = 16; /* only works with cAuraEffectBitTemporary */
extern const int cAuraEffectBitAdvancedRangeIndicator = 32;

extern const int cAuraDiplomacyAll = 0;
extern const int cAuraDiplomacyYou = 1;
extern const int cAuraDiplomacyNeutralEnemy = 2;
extern const int cAuraDiplomacyGaia = 3;
extern const int cAuraDiplomacyGaiaYouAlly = 4;
extern const int cAuraDiplomacyGaiaNeutralAlly = 5;
extern const int cAuraDiplomacyAllButYou = 6;
    """



    xs_level_function += """int kill_res = 20; //The id of the Unit killed in resource
rule setup_variable
    active
    minInterval 1
    maxInterval 1 
    {
        xsSetTriggerVariable(1, P1_level);
        xsSetTriggerVariable(2, P1_required_XP);
        xsSetTriggerVariable(3, XP_P1);
        
        xsSetTriggerVariable(4, P2_level);
        xsSetTriggerVariable(5, P2_required_XP);
        xsSetTriggerVariable(6, XP_P2);
        
        xsSetTriggerVariable(7, P3_level);
        xsSetTriggerVariable(8, P3_required_XP);
        xsSetTriggerVariable(9, XP_P3);
        
        xsSetTriggerVariable(10, P4_level);
        xsSetTriggerVariable(11, P4_required_XP);
        xsSetTriggerVariable(12, XP_P4);
        
        xsSetTriggerVariable(13, P5_level);
        xsSetTriggerVariable(14, P5_required_XP);
        xsSetTriggerVariable(15, XP_P5);
        
        xsSetTriggerVariable(16, P6_level);
        xsSetTriggerVariable(17, P6_required_XP);
        xsSetTriggerVariable(18, XP_P6);
        
        xsSetTriggerVariable(19, P7_level);
        xsSetTriggerVariable(20, P7_required_XP);
        xsSetTriggerVariable(21, XP_P7);
        xsDisableSelf();
    }    
    """
    for p in range (1,8):
        if p == PlayerId.ONE:
            variable_1 = 1
            variable_2 = 2
            variable_3 = 3
        elif p == PlayerId.TWO:
            variable_1 = 4
            variable_2 = 5
            variable_3 = 6
        elif p == PlayerId.THREE:
            variable_1 = 7
            variable_2 = 8
            variable_3 = 9
        elif p == PlayerId.FOUR:
            variable_1 = 10
            variable_2 = 11
            variable_3 = 12
        elif p == PlayerId.FIVE:
            variable_1 = 13
            variable_2 = 14
            variable_3 = 15
        elif p == PlayerId.SIX:
            variable_1 = 16
            variable_2 = 17
            variable_3 = 18
        elif p == PlayerId.SEVEN:
            variable_1 = 19
            variable_2 = 20
            variable_3 = 21
        else :
            variable_1 = 0
            variable_2 = 0
            variable_3 = 0
        xs_level_function +=f"""




rule XP_tracker_P{p}
    active
    minInterval 1
    maxInterval 1 
{{
    
    int tracked_player_P{p} = xsGetWorldPlayerId({p});
    P{p}_KILL = xsPlayerAttribute(tracked_player_P{p}, kill_res);
    
    if (previous_value_P{p} < P{p}_KILL) 
    {{
        previous_value_P{p} = previous_value_P{p} + 1; //Is increase BY 1 until it's equal to P{p}_KILL
        
        xsSetTriggerVariable({variable_3}, XP_P{p});
        XP_P{p} = XP_P{p} + XP_value_P{p}; //GIVE THE XP
    }}    
}}

rule P{p}_level_function
    active
    minInterval 1
    maxInterval 1 
{{
    
    if (XP_P{p} >= P{p}_required_XP) 
    {{
        XP_P{p} = 0; //reset xp count 
        int tracked_player_P{p} = xsGetWorldPlayerId({p});
        P{p}_level = P{p}_level + 1;
        P{p}_required_XP = P{p}_required_XP * P{p}_XP_increase;
        more_pop_P{p} = xsPlayerAttribute(tracked_player_P{p}, pop_cap_res);
        bonus_pop_P{p} = more_pop_P{p} + 5;
        xsSetPlayerAttribute(tracked_player_P{p}, pop_cap_res, bonus_pop_P{p});
        xsSetTriggerVariable({variable_1}, P{p}_level);
        xsSetTriggerVariable({variable_2}, P{p}_required_XP);
        xsSetTriggerVariable({variable_3}, XP_P{p});
        up_value = up_value + 0.25;
    }}
}}
    """
    with open(xs_input_path, "w") as script_sister_land_pine:
        script_sister_land_pine.write(xs_level_function)
    return xs_level_function

def danger_level(scenario,trigger_manager):
    xs_input_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\AoE2DE\\resources\\_common\\xs\\security_breach_in_ruin.xs"
    xs_script_area ="""
float Age_up_value = 0.0;
float area_reached_value = 0.0;
void area_reach_tracker_small () {
area_reached_value = area_reached_value + 1;
}
void area_reach_tracker_medium () {
area_reached_value = area_reached_value + 2;
}
void area_reach_tracker_big () {
area_reached_value = area_reached_value + 3;
}
void area_reach_tracker_very_big () {
area_reached_value = area_reached_value + 4;
}

void feudal_age_reached (){
    Age_up_value = Age_up_value + 2;
}

void castle_age_reached (){
    Age_up_value = Age_up_value + 4;
}
void imperial_age_reached (){
    Age_up_value = Age_up_value + 5;
}
int value = 0;
    float danger_level = 0.0;
    rule danger_level_operation
    //Minimum time between the execution of the rule
    minInterval 150
    maxInterval 150
    active
    {
    //Status of the rule when the game start, rule is activated in the danger rule function
        
    danger_level = area_reached_value + up_value + Age_up_value;
    xsSetTriggerVariable(25, danger_level);
    xsDisableSelf();
    }
"""
    with open(xs_input_path, "a") as script_sister_land_pine:
        script_sister_land_pine.write(xs_script_area)
def wave_function(scenario, trigger_manager, vector,unit,danger_level,quantity,spawn_rate,rule_name,second_area_vector):

    xs_input_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\AoE2DE\\resources\\_common\\xs\\security_breach_in_ruin.xs"
    #Define the rule and the player
    # In XS  a comment start with //

    # For this ONE I'd like to start with an empty space to separate it form the rest
    xs_script_wave = f"""
"""
    #check if every variable is in order and unpack
    if len(unit) != len(quantity) or len(unit) != len(spawn_rate) :
        raise f"Error : quantity, unit and spawn_rate must have the same lenght if it's not the case the XS code will not work check\n Unit dictionary : {unit} \n quantity : {quantity} \n spawn rate : {spawn_rate} "
    else:
        for i in range (len(unit)):
            unit_id = unit[i]
            quantity_value = quantity[i]
            spawn_rate_value = spawn_rate[i]
            xs_script_wave +=f"""
//Count the total unit spawned
int totalSpawnedEnemy_{rule_name}_{unit_id}_{i} = 0;
//Is the max unit that can spawn when the rule start
int maxSpawnEnemy_{rule_name}_{unit_id}_{i} = {quantity_value};
//Spawn_rate of the unit
int SpawnRateEnemy_{rule_name}_{unit_id}_{i} = {spawn_rate_value};
    """
    # check the length because if not then it will break stuff, although the scenario is rewritten every time so it's just more a way to point it out before entering it

        xs_script_wave += f"""
// Rule name, spawn interval XS required each rule to have a different name
rule {rule_name} 
//Minimum time between the execution of the rule
minInterval 15
maxInterval 15
//Status of the rule when the game start, rule is activated in the danger rule function
inactive

{{ 
// Get player 8 real ID, lobby order mess ID 
int PlayerID = xsGetWorldPlayerId(8);
"""
        if len(unit) != len(vector):
            raise f"Error : Unit and vector must be the same lenght, one vector per unit, to define a vector make list with tuple [(x_coord,y_coord,x_increment,y_increment, limit_x, limit_y), and so on and so on] "
        else:
            for i in range(len(vector)):
                if isinstance(second_area_vector, list):
                    # In case of the second area, we unpack it's value for XS too
                    unit_id = unit[i]
                    second_area_x, second_area_y, x_incrementation_second_area, y_incrementation_second_area, limit_x_sec_area, limit_y_sec_area, open_variable = \
                        second_area_vector[i][0]
                    xs_script_wave += f"""
    //Varible for spawning and coordinate define inside the rule, so it's reset at every interaction with the rule
    float x_spawn_sec_area_{rule_name}_{unit_id}_{i} = {second_area_x};
    float y_spawn_sec_area_{rule_name}_{unit_id}_{i} = {second_area_y};

    float base_x_spawn_sec_area_{rule_name}_{unit_id}_{i} = {second_area_x};
    float base_y_spawn_sec_area_{rule_name}_{unit_id}_{i} = {second_area_y};

    float x_incrementation_sec_area_{rule_name}_{unit_id}_{i} = {x_incrementation_second_area};
    float y_incrementation_sec_area_{rule_name}_{unit_id}_{i} = {y_incrementation_second_area};

    float limit_x_sec_area_{rule_name}_{unit_id}_{i} = {limit_x_sec_area};
    float limit_y_sec_area_{rule_name}_{unit_id}_{i} = {limit_y_sec_area};
    """

                unit_id = unit[i]
                x_spawn, y_spawn, x_incrementation, y_incrementation, limit_x, limit_y = vector[i][0]
                xs_script_wave += f"""
    //Coordinate for the normal spawn, those are always define no matter the choice
    float x_spawn_{rule_name}_{unit_id}_{i} = {x_spawn};
    float y_spawn_{rule_name}_{unit_id}_{i} = {y_spawn};

    float base_x_spawn_{rule_name}_{unit_id}_{i} = {x_spawn};
    float base_y_spawn_{rule_name}_{unit_id}_{i} = {y_spawn};

    float x_incrementation_{rule_name}_{unit_id}_{i} = {x_incrementation};
    float y_incrementation_{rule_name}_{unit_id}_{i} = {y_incrementation};

    float limit_x_{rule_name}_{unit_id}_{i} = {limit_x};
    float limit_y_{rule_name}_{unit_id}_{i} = {limit_y};
            """
    for i in range(len(unit)):
        unit_id = unit[i]
        # create the vectors depending if the secondary area is a case or not
        if not isinstance(second_area_vector, list):
            second_area_vector = None
            vector_line  = f"vector spawnPos_{rule_name}_{unit_id}_{i} = xsVectorSet(x_spawn_{rule_name}_{unit_id}_{i}, y_spawn_{rule_name}_{unit_id}_{i}, 0);"
            vector_second = None
        else :
            vector_line  = f"vector spawnPos_{rule_name}_{unit_id}_{i} = xsVectorSet(x_spawn_{rule_name}_{unit_id}_{i}, y_spawn_{rule_name}_{unit_id}_{i}, 0);"
            vector_second = f"vector spawnPos_sec_area{rule_name}_{unit_id}_{i} = xsVectorSet(x_spawn_sec_area_{rule_name}_{unit_id}_{i}, y_spawn_sec_area_{rule_name}_{unit_id}_{i}, 0);"

        xs_script_wave += f"""
    // ----------------------------------------
        
        
        for (qty_{rule_name}_{unit_id}_{i} = 0; < SpawnRateEnemy_{rule_name}_{unit_id}_{i}) {{
        
"""
        if not isinstance(second_area_vector, list):
            # if the second area isn't define we do a normal rule
            xs_script_wave += f"""
{vector_line}
int newUnit_{rule_name}_{unit_id}_{i} = xsCreateUnit({unit_id}, PlayerID, spawnPos_{rule_name}_{unit_id}_{i}, false, true, false);
totalSpawnedEnemy_{rule_name}_{unit_id}_{i} = totalSpawnedEnemy_{rule_name}_{unit_id}_{i} + 1;
if (x_spawn_{rule_name}_{unit_id}_{i}>= limit_x_{rule_name}_{unit_id}_{i}) {{
    y_spawn_{rule_name}_{unit_id}_{i} = y_incrementation_{rule_name}_{unit_id}_{i} + y_spawn_{rule_name}_{unit_id}_{i};
    x_spawn_{rule_name}_{unit_id}_{i} = base_x_spawn_{rule_name}_{unit_id}_{i};
}} else {{
    x_spawn_{rule_name}_{unit_id}_{i} = x_incrementation_{rule_name}_{unit_id}_{i} + x_spawn_{rule_name}_{unit_id}_{i};
}}

        }}
"""
        else :
            # if the second area is define we do a rule that check if that area has been reached the boolean, if not then we do normal spawn, but the number of unit count is double to reduce the amount of spawn

            xs_script_wave +=f"""
            // if that check is the area is reached
             if ({open_variable} == 1) {{
                {vector_second}
                // it's better to have the spawn function returning is ID to avoid desync
                int newUnitSEC_{rule_name}_{unit_id}_{i} = xsCreateUnit({unit_id}, PlayerID, spawnPos_sec_area{rule_name}_{unit_id}_{i}, false, true, false);
                //Total enemy count, rule disable itself when the count reached it's maximum
                totalSpawnedEnemy_{rule_name}_{unit_id}_{i} = totalSpawnedEnemy_{rule_name}_{unit_id}_{i} + 1;
                // Once X has reached is limit, it goes back to it's value and Y get an increase
                if (x_spawn_sec_area_{rule_name}_{unit_id}_{i}>= limit_x_sec_area_{rule_name}_{unit_id}_{i}) 
                {{
                    //ADD the incrementation to Y
                    y_spawn_sec_area_{rule_name}_{unit_id}_{i} = y_incrementation_sec_area_{rule_name}_{unit_id}_{i} + y_spawn_sec_area_{rule_name}_{unit_id}_{i};
                    //RESET X
                    x_spawn_sec_area_{rule_name}_{unit_id}_{i} = base_x_spawn_sec_area_{rule_name}_{unit_id}_{i};
                }} 
                else 
                {{
                // Well if X hasn't reached is value it get increase
                    x_spawn_{rule_name}_{unit_id}_{i} = x_incrementation_{rule_name}_{unit_id}_{i} + y_spawn_sec_area_{rule_name}_{unit_id}_{i};
                }}
             }}
            else {{
                {vector_line}
                int newUnit_{rule_name}_{unit_id}_{i} = xsCreateUnit({unit_id}, PlayerID, spawnPos_{rule_name}_{unit_id}_{i}, false, true, false);
                totalSpawnedEnemy_{rule_name}_{unit_id}_{i} = totalSpawnedEnemy_{rule_name}_{unit_id}_{i} + 2;
                // Once X has reached is limit, it goes back to it's value and Y get an increase
                if (x_spawn_{rule_name}_{unit_id}_{i}>= limit_x_{rule_name}_{unit_id}_{i}) {{
                    y_spawn_{rule_name}_{unit_id}_{i} = y_incrementation_{rule_name}_{unit_id}_{i} +  y_spawn_{rule_name}_{unit_id}_{i};
                    x_spawn_{rule_name}_{unit_id}_{i} = base_x_spawn_{rule_name}_{unit_id}_{i};
                }} else {{
                    // Well if X hasn't reached is value it get increase
                    x_spawn_{rule_name}_{unit_id}_{i} = x_incrementation_{rule_name}_{unit_id}_{i} + x_spawn_{rule_name}_{unit_id}_{i};
                }}
                            
            }}                 
        }}
            """
    mount_the_bool = """"""
    for i in range (len(unit)):
        unit_id = unit[i]
        if i == len(unit) - 1:

            mount_the_bool += f"""
(totalSpawnedEnemy_{rule_name}_{unit_id}_{i} >= maxSpawnEnemy_{rule_name}_{unit_id}_{i});
"""
        else :
            mount_the_bool += f"""(totalSpawnedEnemy_{rule_name}_{unit_id}_{i} >= maxSpawnEnemy_{rule_name}_{unit_id}_{i}) &&"""
    xs_script_wave += f"""
        //This if disable the rule once all unit has been spawned 
        bool check_disable_{rule_name} = {mount_the_bool}
        if (check_disable_{rule_name} == true) {{
            xsDisableSelf();
            """
    for i in range (len(unit)):
        unit_id = unit[i]
        xs_script_wave += f"""
    //Rule must be re-usable so the total count is reset when we want to disable the rule
 totalSpawnedEnemy_{rule_name}_{unit_id}_{i} = 0;
"""
    xs_script_wave += f"""
        return;
    }}
    
    """
    xs_script_wave += "}"
    #Write inside the XS file
    with open(xs_input_path, "a") as script_sister_land_pine:
        script_sister_land_pine.write(xs_script_wave)
def danger_rule_spawn (scenario,trigger_manager,configs,rule_name):
    xs_input_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\AoE2DE\\resources\\_common\\xs\\security_breach_in_ruin.xs"
    xs_script_danger_rule ="""
//This rule is just a huge IF ELIF, every 5 minutes a check is done to see which spawn rule can be fired
rule danger_level_spawn_trigger
//Minimum time between the execution of the rule
minInterval 300
maxInterval 300
//Status of the rule when the game start, rule is activated in the danger rule function
active
//This is the brace of the rule 
{
    xsEnableRule("danger_level_operation");
    """
    for i, cfg in enumerate(configs):
        min_danger_level, max_danger_level = cfg.danger_level
        xs_script_danger_rule += f"""
float minimum_danger_level_{cfg.rule_name} = {min_danger_level};
float maximum_danger_level_{cfg.rule_name} = {max_danger_level};
bool can_we_activate_{cfg.rule_name} = (minimum_danger_level_{cfg.rule_name} < danger_level) && (maximum_danger_level_{cfg.rule_name} > danger_level);

            """
    for i, cfg in enumerate(configs):
        xs_script_danger_rule += f"""
        """
        if i == 0:
            xs_script_danger_rule += f"""        
if (can_we_activate_{cfg.rule_name} == true) {{
    xsEnableRule("{cfg.rule_name}");
    return;
}}
"""
        else:
            xs_script_danger_rule += f"""
else if (can_we_activate_{cfg.rule_name} == true) {{
    xsEnableRule("{cfg.rule_name}");
    return;
            }}
        
"""
    xs_script_danger_rule +="\n}"
    with open(xs_input_path, "a") as script_sister_land_pine:
        script_sister_land_pine.write(xs_script_danger_rule)



# ----------------- For john Galver

def john_galverg_XS():
    xs_input_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\AoE2DE\\resources\\_common\\xs\\security_breach_in_ruin.xs"
    XS_general_ID = [900, 936, 944, 912, 947, 955, 913, 923,906, 912, 947]
    melee_general_ID = [906, 912, 947]
    size = len(XS_general_ID)
    txt_array_name = '"class_id_unit"'
    xs_array = f"class_id_units = xsArrayCreateInt({size}, 0, {txt_array_name});\n"
    for i in range (len(XS_general_ID)):
        class_id = XS_general_ID[i]
        xs_array += f"xsArraySetInt(class_id_units, {i},{class_id});\n"
    xs_john = f"""
    int john_expedition_manager = {UnitInfo.KING.ID} ;
    float expedition_area_size = 5;
    float expedition_attack_reload = 0.1;
    float expedition_regen_rate = 10;
    float workrate_john = 0.5 ;
    int available_manager = 1;
    int class_id_units = -1;
void setup_aura_blue() {{
    int john_galverb = xsGetWorldPlayerId(1);
    int permaAuraEffects = cAuraEffectBitMultiply ;
    int permaAuraregen = 0;
    xsEffectAmount(cSetAttribute,john_expedition_manager, 0, 150, john_galverb);
    xsEffectAmount(cSetAttribute,john_expedition_manager, cCombatAbility, 32, john_galverb);
    xsEffectAmount(cSetAttribute,john_expedition_manager, {ObjectAttribute.AVAILABLE_UNIT_FLAG}, available_manager, john_galverb);
    xsEffectAmount(cSetAttribute,john_expedition_manager, {ObjectAttribute.DISABLED_UNIT_FLAG}, 4, john_galverb);
    {xs_array}
for (i = 0; < xsArrayGetSize(class_id_units)) {{
    int class_id_value = xsArrayGetInt(class_id_units, i);
    bool expedition_manager_speed = xsAddAura(john_expedition_manager, class_id_value, john_galverb, {ObjectAttribute.ATTACK_RELOAD_TIME}, expedition_attack_reload, expedition_area_size, permaAuraEffects, cAuraDiplomacyGaiaYouAlly);    
    bool expedition_manager_regen = xsAddAura(john_expedition_manager, class_id_value, john_galverb, {ObjectAttribute.REGENERATION_RATE}, expedition_regen_rate, expedition_area_size, permaAuraregen, cAuraDiplomacyGaiaYouAlly);  
    }}
    bool expedition_manager_workrate = xsAddAura(john_expedition_manager, 904, john_galverb, {ObjectAttribute.WORK_RATE}, workrate_john, expedition_area_size, permaAuraregen, cAuraDiplomacyGaiaYouAlly);  

    
}}
void dispatch_management(){{
    int john_galverb = xsGetWorldPlayerId(1);
    available_manager = available_manager + 2;
    int permaAuraEffects = cAuraEffectBitMultiply ;
    xsEffectAmount(cSetAttribute,john_expedition_manager, {ObjectAttribute.AVAILABLE_UNIT_FLAG}, available_manager, john_galverb);
}}
void economy_direction() {{
    int john_galverb = xsGetWorldPlayerId(1);
    workrate_john = workrate_john * 1.05;
    int permaAuraEffects = cAuraEffectBitMultiply ;
    bool expedition_manager_workrate = xsAddAura(john_expedition_manager, 904, john_galverb, {ObjectAttribute.WORK_RATE}, workrate_john, expedition_area_size, permaAuraEffects, cAuraDiplomacyGaiaYouAlly);  

}}
void troop_management() {{
    int john_galverb = xsGetWorldPlayerId(1);
    expedition_attack_reload = expedition_attack_reload * 1.04;
    expedition_regen_rate = expedition_regen_rate * 1.05;
    int permaAuraEffects = cAuraEffectBitMultiply ;
    int permaAuraregen = 0;
    for (i = 0; < xsArrayGetSize(class_id_units)) {{
        int class_id_value = xsArrayGetInt(class_id_units, i);
        bool expedition_manager_speed = xsAddAura(john_expedition_manager, class_id_value, john_galverb, {ObjectAttribute.ATTACK_RELOAD_TIME}, expedition_attack_reload, expedition_area_size, permaAuraEffects, cAuraDiplomacyGaiaYouAlly);    
        bool expedition_manager_regen = xsAddAura(john_expedition_manager, class_id_value, john_galverb, {ObjectAttribute.REGENERATION_RATE}, expedition_regen_rate, expedition_area_size, permaAuraregen, cAuraDiplomacyGaiaYouAlly);  
        }}
}}
void extend_peremiters() {{
int john_galverb = xsGetWorldPlayerId(1);
expedition_area_size = expedition_area_size + 0.75;
int permaAuraEffects = cAuraEffectBitMultiply ;
int permaAuraregen = 0;
for (i = 0; < xsArrayGetSize(class_id_units)) {{
        int class_id_value = xsArrayGetInt(class_id_units, i);
        bool expedition_manager_speed = xsAddAura(john_expedition_manager, class_id_value, john_galverb, {ObjectAttribute.ATTACK_RELOAD_TIME}, expedition_attack_reload, expedition_area_size, permaAuraEffects, cAuraDiplomacyGaiaYouAlly);    
        bool expedition_manager_regen = xsAddAura(john_expedition_manager, class_id_value, john_galverb, {ObjectAttribute.REGENERATION_RATE}, expedition_regen_rate, expedition_area_size, permaAuraregen, cAuraDiplomacyGaiaYouAlly);  
        }}
    bool expedition_manager_workrate = xsAddAura(john_expedition_manager, 904, john_galverb, {ObjectAttribute.WORK_RATE}, workrate_john, expedition_area_size, permaAuraEffects, cAuraDiplomacyGaiaYouAlly);  

}}
    """
    joh_tech_list = [(TechInfo.BLANK_TECHNOLOGY_0.ID,"dispatch_management();"),(TechInfo.BLANK_TECHNOLOGY_1.ID,"economy_direction();"),
                     (TechInfo.BLANK_TECHNOLOGY_2.ID,"troop_management();"),(TechInfo.BLANK_TECHNOLOGY_3.ID,"extend_peremiters();")]
    with open(xs_input_path, "a") as script_sister_land_pine:
        script_sister_land_pine.write(xs_john)
    return xs_john

def Gary_buerg_xs(scenario,trigger_manager):
    xs_input_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\AoE2DE\\resources\\_common\\xs\\security_breach_in_ruin.xs"
    XS_general_ID = [900, 936, 944, 906, 912, 947, 955, 913, 923, 906, 912, 947]
    melee_general_ID = [906, 912, 947]
    xs_gary = f"""
int relic_count_check = 0;
int five_relic_check_positive = 5;
int five_relic_check_negative = 0;
int ten_relic_check_positive = 10;
int ten_relic_check_negative = 0;
int digging_treasure_cost = 2500;
const int BASE_COST = 2500;
rule relic_check_count_P2
active
minInterval 1
maxInterval 1
{{
int relic_capture = 7;
int gary_buerg = xsGetWorldPlayerId(2);
int P2_relic = xsPlayerAttribute(gary_buerg, relic_capture);

if (relic_count_check < P2_relic) {{
    XP_value_P2 = XP_value_P2 + 0.50;
    relic_count_check = relic_count_check + 1;
}}
 else if (relic_count_check > P2_relic) {{
    XP_value_P2 = XP_value_P2 - 0.50;
    relic_count_check = relic_count_check - 1;
}}
if (P2_relic >= five_relic_check_positive) {{
    five_relic_check_negative = five_relic_check_positive ; 
    five_relic_check_positive = five_relic_check_positive + 5;
    for (i = 0; < xsArrayGetSize(class_id_units)) {{
    int class_id_value = xsArrayGetInt(class_id_units, i);
    bool check_melee = (class_id_value == 906) || (class_id_value == 912) || (class_id_value == 947) ;
    if (check_melee == true) {{
            xsEffectAmount(cAddAttribute,class_id_value, {ObjectAttribute.ATTACK}, 256 * 4 + 1, gary_buerg);
            }}
    else {{
            xsEffectAmount(cAddAttribute,class_id_value, {ObjectAttribute.ATTACK}, 256 * 3 + 1, gary_buerg);
    }}
    }}
}}
 else if (five_relic_check_negative > P2_relic) {{
    five_relic_check_positive = five_relic_check_negative;
    five_relic_check_negative = five_relic_check_negative - 5;
    for (y = 0; < xsArrayGetSize(class_id_units)) {{
    int class_id_value_B = xsArrayGetInt(class_id_units, y);
    bool check_melee_B = (class_id_value_B == 906) || (class_id_value == 912) || (class_id_value == 947) ;
    if (check_melee_B == true) {{
            xsEffectAmount(cAddAttribute,class_id_value_B, {ObjectAttribute.ATTACK}, -256*4 - 1, gary_buerg);
            }}
    else {{
            xsEffectAmount(cAddAttribute,class_id_value_B, {ObjectAttribute.ATTACK}, -256*3 - 1, gary_buerg);
    }}
    }}
}}


int paliers = P2_relic / 10;
float f = BASE_COST;
for(v = 0; < paliers) {{ f = f * 0.80; }}
int new_cost = f;
xsEffectAmount(cModifyTech, {TechInfo.LOOM.ID}, cAttrSetGoldCost, new_cost, gary_buerg);
}}

int relic_digged = 1;
int digged_count = 0;
int relic_id = {OtherInfo.RELIC.ID} ;
int tent_c = {BuildingInfo.TENT_C.ID} ;
void drill_reward() {{
    int gary_buerg = xsGetWorldPlayerId(2);
    digged_count = digged_count + 1;
    
    xsEffectAmount(cModResource, cAttributeSpawnCap, cAttributeSet, 1);
    xsEffectAmount(cSpawnUnit, relic_id, tent_c, relic_digged, gary_buerg);
    if (digged_count == 3) {{
        relic_digged = relic_digged + 1 ;
    }}
    else if (digged_count == 7) {{
        relic_digged = relic_digged + 1 ;
    }}
    else if (digged_count == 11){{
        relic_digged = 1;
    }}
    xsEffectAmount(cAddAttribute,904, {ObjectAttribute.ARMOR}, -256*3 - 2, gary_buerg);
    xsEffectAmount(cAddAttribute,904, {ObjectAttribute.ARMOR}, -256*4 - 1, gary_buerg);
    xsEffectAmount(cAddAttribute,904, {ObjectAttribute.HIT_POINTS}, -15, gary_buerg);
}}
void setup_gary() {{
    int gary_buerg = xsGetWorldPlayerId(2);
    xsEffectAmount(cAddAttribute,{BuildingInfo.MONASTERY.ID}, {ObjectAttribute.GARRISON_CAPACITY}, 5, gary_buerg);
    xsEffectAmount(cAddAttribute,904, {ObjectAttribute.ARMOR}, 256*3 - 2, gary_buerg);
    xsEffectAmount(cAddAttribute,904, {ObjectAttribute.ARMOR}, 256*4 - 1, gary_buerg);
    xsEffectAmount(cAddAttribute,904, {ObjectAttribute.HIT_POINTS}, 15, gary_buerg);
}}
    
    """
    with open(xs_input_path, "a") as script_sister_land_pine:
        script_sister_land_pine.write(xs_gary)
    return xs_gary

def Markus_skioliose_XS(scenario, trigger_manager):
    xs_input_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\AoE2DE\\resources\\_common\\xs\\security_breach_in_ruin.xs"
    xs_function = f"""
int tech_selection = 0;
void vintage_point {{
    int markus_skoliose = xsGetWorldPlayerId(1);
    int tower_range = 1 + tech_selection;
    int tower_atk = 1 + tech_selection + tech_selection;
    int XS_markus_tower = xsArrayCreateInt(11, 0, "XS_markus_tower");
    xsArraySetInt(XS_markus_tower, 0, {BuildingInfo.WATCH_TOWER.ID});
    xsArraySetInt(XS_markus_tower, 1, {BuildingInfo.GUARD_TOWER.ID});
    xsArraySetInt(XS_markus_tower, 2, {BuildingInfo.DONJON.ID});
    xsArraySetInt(XS_markus_tower, 3, {BuildingInfo.BOMBARD_TOWER.ID});
    xsArraySetInt(XS_markus_tower, 3, {BuildingInfo.KEEP.ID});
    for (i = 0; < xsArrayGetSize(XS_markus_tower))
        {{
            int tower_id = xsArrayGetInt(XS_markus_tower, i);
            xsEffectAmount(cSetAttribute,john_expedition_manager, cAttack, 256*3 + tower_atk, markus_skoliose);
            xsEffectAmount(cSetAttribute,john_expedition_manager, {ObjectAttribute.MAXIMUM_RANGE}, tower_range, markus_skoliose);
        }}
}}
    
    """