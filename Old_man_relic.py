from dataclasses import dataclass
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
def old_man_relic_function(scenario, trigger_manager, activation_triggers):
    unit_manager =scenario.unit_manager
    scenario_uuid = scenario.uuid
    player = PlayerId.ONE
    scenario_uuid = scenario.uuid
    area = Area.from_uuid(scenario_uuid)
    player = PlayerId.ONE
    shared_trigger = trigger_manager.add_trigger(
        name="Old_man_setup",
        enabled=True,
        looping=False,
    )
    shared_trigger.new_effect.script_call(
        message="setup_old_man();"
    )
    for p in range(1, 8):
        player = p
        set_up_old_man_tech = [
            technology_setup(
                name="Enchanted boots",
                description="Buy enchanted boots cost 5 artifact points : All units get +5% movement speed",
                tech_id=TechInfo.BLANK_TECHNOLOGY_15.ID,
                location=BuildingInfo.MACEDONIAN_COMMAND_POST.ID,
                button=1,
                enabled=True,
                player=player,
                research_time=20,
                cost_type=(Attribute.UNUSED_RESOURCE_500, None),
                cost_quantity=(5, None),
                icon_id=64,
            ),
            technology_setup(
                name="Spears with cursed barb tip",
                description="Spears with cursed barb tip cost 5 artifact points : Spearmen line and skimisher line, break armor and give bleeding to enemy units, although those spears reduce their hp by 10",
                tech_id=TechInfo.BLANK_TECHNOLOGY_16.ID,
                location=BuildingInfo.MACEDONIAN_COMMAND_POST.ID,
                button=2,
                enabled=True,
                player=player,
                research_time=20,
                cost_type=(Attribute.UNUSED_RESOURCE_500, None),
                cost_quantity=(5, None),
                icon_id=17,
            ),
            technology_setup(
                name="Hungry doll of Maz kuz",
                description="Buy the hungry doll of Maz kuz cost 4 artifact points : once you buy this, every 5 to 10 minutes the doll will feed on your villager killing 15 of then and giving +5 attacks to your troops, if he can't feed it will take away 10 attacks from your units, the attack bonus only affects unit on the map",
                tech_id=TechInfo.BLANK_TECHNOLOGY_17.ID,
                location=BuildingInfo.MACEDONIAN_COMMAND_POST.ID,
                button=3,
                enabled=True,
                player=player,
                research_time=20,
                cost_type=(Attribute.UNUSED_RESOURCE_500, None),
                cost_quantity=(4, None),
                icon_id=59,
            ),
            technology_setup(
                name="Requiem experience of the blacksmith",
                description="Buy requiem experience of the blacksmith 5 artifact points : All tech at the blacksmiths become available again, you better research all the tech at the blacksmith before buying this",
                tech_id=TechInfo.BLANK_TECHNOLOGY_18.ID,
                location=BuildingInfo.MACEDONIAN_COMMAND_POST.ID,
                button=4,
                enabled=True,
                player=player,
                research_time=20,
                cost_type=(Attribute.UNUSED_RESOURCE_500, None),
                cost_quantity=(5, None),
                icon_id=59,
            ),
            technology_setup(
                name="Wheat from the enchanted soil at the back of the Macedonian temple",
                description="Wheat that cost 4 artifact points : Your cavalry units gain 20% attack speed and +3 attacks but loose 1 armor and piercing and 20 hp",
                tech_id=TechInfo.BLANK_TECHNOLOGY_19.ID,
                location=BuildingInfo.MACEDONIAN_COMMAND_POST.ID,
                button=5,
                enabled=True,
                player=player,
                research_time=20,
                cost_type=(Attribute.UNUSED_RESOURCE_500, None),
                cost_quantity=(4, None),
                icon_id=59,
            ),
            technology_setup(
                name="Buy the eating relics",
                description="Buy the eating relics for 2 artifact points : This object will feed on your gold arround 2500 to 5000, once he finish eating your gold, it will give you 15 artifact point, skill point and power points ",
                tech_id=TechInfo.BLANK_TECHNOLOGY_20.ID,
                location=BuildingInfo.MACEDONIAN_COMMAND_POST.ID,
                button=6,
                enabled=True,
                player=player,
                research_time=600,
                cost_type=(Attribute.UNUSED_RESOURCE_500, None),
                cost_quantity=(2, None),
                icon_id=59,
            ),
            technology_setup(
                name="Enchanted head totem",
                description="Buy the head totem for 10 artifact points : All military building (expect castle and towers) has an aura that reduce the attacks of enemy units",
                tech_id=TechInfo.BLANK_TECHNOLOGY_21.ID,
                location=BuildingInfo.MACEDONIAN_COMMAND_POST.ID,
                button=7,
                enabled=True,
                player=player,
                research_time=10,
                cost_type=(Attribute.UNUSED_RESOURCE_500, None),
                cost_quantity=(10, None),
                icon_id=59,
            ),
            technology_setup(
                name="Quartz powder",
                description="Buy quartz powder cost 10 artifact points: this magic powder make infantry feel less damage and therefore upgrade their armor by 5 points and piercing by 3 point.",
                tech_id=TechInfo.BLANK_TECHNOLOGY_22.ID,
                location=BuildingInfo.MACEDONIAN_COMMAND_POST.ID,
                button=8,
                enabled=True,
                player=player,
                research_time=10,
                cost_type=(Attribute.UNUSED_RESOURCE_500, None),
                cost_quantity=(10, None),
                icon_id=59,
            ),

            ]
        set_up_old_man_object = [
            object_setup(
                object=HeroInfo.THE_BLACK_PRINCE.ID,
                name="Old man relic handbook",
                description="You can buy the old man relic in exchange for artifact points, you gain 1 artifact points every 5 levels, you have <cost> points",
                building=BuildingInfo.MACEDONIAN_COMMAND_POST.ID,
                button=15,
                enabled_object=True,
                player=player,
                cost_type=(Attribute.STONE_STORAGE, Attribute.UNUSED_RESOURCE_500),
                cost_quantity=(1, 10000),
            ),
        ]

        for cfg in set_up_old_man_tech:
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
        for cfg in set_up_old_man_object :
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

    doll_triggers = {}
    tech_xs_list = [
        (TechInfo.BLANK_TECHNOLOGY_15.ID, "enchanted_boots_{p}();"),
        (TechInfo.BLANK_TECHNOLOGY_16.ID, "cursed_spears_{p}();"),
        (TechInfo.BLANK_TECHNOLOGY_17.ID, "hungry_doll_{p}();"),
        (TechInfo.BLANK_TECHNOLOGY_19.ID, "enchanted_wheat_{p}();"),
        (TechInfo.BLANK_TECHNOLOGY_20.ID, "buy_hungry_relic_{p}();"),
        (TechInfo.BLANK_TECHNOLOGY_21.ID, "enchanted_totem_{p}();"),
        (TechInfo.BLANK_TECHNOLOGY_22.ID, "quartz_powder_{p}();"),
    ]
    blacksmith_techs = [
        TechInfo.FORGING.ID,
        TechInfo.IRON_CASTING.ID,
        TechInfo.BLAST_FURNACE.ID,
        TechInfo.SCALE_MAIL_ARMOR.ID,
        TechInfo.CHAIN_MAIL_ARMOR.ID,
        TechInfo.PLATE_MAIL_ARMOR.ID,
        TechInfo.SCALE_BARDING_ARMOR.ID,
        TechInfo.CHAIN_BARDING_ARMOR.ID,
        TechInfo.PLATE_BARDING_ARMOR.ID,
        TechInfo.FLETCHING.ID,
        TechInfo.BODKIN_ARROW.ID,
        TechInfo.BRACER.ID,
        TechInfo.PADDED_ARCHER_ARMOR.ID,
        TechInfo.LEATHER_ARCHER_ARMOR.ID,
        TechInfo.RING_ARCHER_ARMOR.ID,
    ]
    for p in range (1,8):
        requiem_blacksmith = trigger_manager.add_trigger(
            name="Requiem blacksmith",
            enabled=True,
            looping=False,
            execute_on_load=True,
        )
        requiem_blacksmith.new_condition.research_technology(
            source_player=p,
            technology=TechInfo.BLANK_TECHNOLOGY_18.ID,
        )
        for i in range (len(blacksmith_techs)):
            requiem_blacksmith.new_effect.enable_disable_technology(
                source_player=p,
                enabled=False,
                technology=blacksmith_techs[i]
            )
            requiem_blacksmith.new_effect.enable_disable_technology(
                source_player=p,
                enabled=True,
                technology=blacksmith_techs[i]
            )
    for p in range (1,8):
        doll_feeding = trigger_manager.add_trigger(
            name=f"Doll feeding player {p}",
            enabled=False,
            looping=True,
        )
        doll_feeding.new_condition.script_call(
            xs_function=f"doll_feed_check_{p}();",
        )
        doll_feeding.new_effect.kill_object(
            source_player=p,
            object_group=ObjectClass.CIVILIAN,
            max_units_affected=15,
            **area.select_entire_map().to_dict(),
        )
        doll_feeding.new_effect.change_object_attack(
            source_player=p,
            **area.select_entire_map().to_dict(),
            armour_attack_quantity=5,
            armour_attack_class=3,
            operation=Operation.ADD,
        )
        doll_feeding.new_effect.change_object_attack(
            source_player=p,
            **area.select_entire_map().to_dict(),
            armour_attack_quantity=5,
            armour_attack_class=4,
            operation=Operation.ADD,
        )

        doll_starving = trigger_manager.add_trigger(
            name=f"Doll starving player {p}",
            enabled=False,
            looping=True,
        )
        doll_starving.new_condition.script_call(
            xs_function=f"doll_starve_check_{p}();",
        )
        doll_starving.new_effect.change_object_attack(
            source_player=p,
            **area.select_entire_map().to_dict(),
            armour_attack_quantity=10,
            armour_attack_class=3,
            operation=Operation.SUBTRACT,
        )
        doll_starving.new_effect.change_object_attack(
            source_player=p,
            **area.select_entire_map().to_dict(),
            armour_attack_quantity=10,
            armour_attack_class=4,
            operation=Operation.SUBTRACT,
        )
        doll_triggers[p] = (doll_feeding, doll_starving)
    for p in range(1, 8):
        for tech_id, xs_call in tech_xs_list:
            tech_trigger = trigger_manager.add_trigger(
                name=f"Tech {tech_id} player {p}",
                enabled=True,
                looping=False,
                execute_on_load=True,
            )
            tech_trigger.new_condition.research_technology(
                source_player=p,
                technology=tech_id,
            )
            tech_trigger.new_effect.script_call(
                message=xs_call.format(p=p),
            )
            if tech_id == TechInfo.BLANK_TECHNOLOGY_17.ID:
                doll_feeding, doll_starving = doll_triggers[p]
                tech_trigger.new_effect.activate_trigger(
                    trigger_id=doll_feeding.trigger_id,
                )
                tech_trigger.new_effect.activate_trigger(
                    trigger_id=doll_starving.trigger_id,
                )
    area_x = 194
    area_y = 230
    area_x2 = 204
    area_y2 = 238

    list_command_post_trigger = []

    # ---------------- Capture du camp, un trigger par joueur ----------------
    for p in range(1, 8):
        command_post_capture = trigger_manager.add_trigger(
            name=f"Command post capture P{p}",
            enabled=False,
            looping=True,
        )
        command_post_capture.new_condition.objects_in_area(
            source_player=PlayerId.GAIA,
            object_list=BuildingInfo.MACEDONIAN_COMMAND_POST.ID,
            quantity=1,
            area_x1=area_x,
            area_y1=area_y,
            area_x2=area_x2,
            area_y2=area_y2,
        )
        for other_player in range(1, 8):
            if other_player == p:
                inverted_check = False
            else:
                inverted_check = True
            command_post_capture.new_condition.objects_in_area(
                source_player=other_player,
                quantity=1,
                object_type=ObjectType.MILITARY,
                inverted=inverted_check,
                area_x1=area_x,
                area_y1=area_y,
                area_x2=area_x2,
                area_y2=area_y2,
            )
        command_post_capture.new_effect.change_ownership(
            source_player=PlayerId.GAIA,
            target_player=p,
            object_list_unit_id=BuildingInfo.MACEDONIAN_COMMAND_POST.ID,
            area_x1=area_x,
            area_y1=area_y,
            area_x2=area_x2,
            area_y2=area_y2,
        )
        list_command_post_trigger.append(command_post_capture)

    # ---------------- Retour à Gaia si la zone est vide ----------------
    command_post_release = trigger_manager.add_trigger(
        name="Command post back to Gaia",
        enabled=False,
        looping=True,
    )
    command_post_release.new_condition.objects_in_area(
        source_player=PlayerId.GAIA,
        object_list=BuildingInfo.MACEDONIAN_COMMAND_POST.ID,
        quantity=1,
        inverted=True,
        area_x1=area_x,
        area_y1=area_y,
        area_x2=area_x2,
        area_y2=area_y2,
    )
    for p in range(1, 8):
        command_post_release.new_condition.objects_in_area(
            source_player=p,
            quantity=1,
            object_type=ObjectType.MILITARY,
            inverted=True,
            area_x1=area_x,
            area_y1=area_y,
            area_x2=area_x2,
            area_y2=area_y2,
        )
    for p in range(1, 8):
        command_post_release.new_effect.change_ownership(
            source_player=p,
            target_player=PlayerId.GAIA,
            object_list_unit_id=BuildingInfo.MACEDONIAN_COMMAND_POST.ID,
            area_x1=area_x,
            area_y1=area_y,
            area_x2=area_x2,
            area_y2=area_y2,
        )
    list_command_post_trigger.append(command_post_release)

    # ---------------- Activation du système ----------------
    command_post_activation = trigger_manager.add_trigger(
        name="Activate command post system",
        enabled=True,
        looping=False,
        execute_on_load=True,
    )
    command_post_activation.new_condition.timer(
        timer=10
    )
    command_post_activation.new_effect.change_ownership(
        source_player=PlayerId.EIGHT,
        target_player=PlayerId.GAIA,
        area_x1=area_x,
        area_y1=area_y,
        area_x2=area_x2,
        area_y2=area_y2,
        object_list_unit_id=BuildingInfo.MACEDONIAN_COMMAND_POST.ID,
    )
    for i in range(len(list_command_post_trigger)):
        command_post_activation.new_effect.activate_trigger(
            trigger_id=list_command_post_trigger[i].trigger_id,
        )
    trigger_id = activation_triggers["old_man"]
    trigger_id.new_effect.activate_trigger(
        trigger_id=command_post_activation.trigger_id,
    )
def Blacksmith_of_takoas(scenario, trigger_manager,activation_triggers):
    scenario_uuid = scenario.uuid
    area = Area.from_uuid(scenario_uuid)
    shared_trigger = trigger_manager.add_trigger(
        name="Blacksmith of Takoas",
        enabled=True,
        looping=False,
    )
    shared_trigger.new_effect.script_call(
        message="setup_forge();"
    )
    for p in range (1,8):
        player = p
        set_up_blacksmith_of_takoas_tech = [
            technology_setup(
                name="Forge of the sword",
                description="Cost 3 blacksmith points : All melee units gain +1 attack. Every 3rd research grants an additional +1 attack. Can be researched repeatedly; bonuses are permanent.",
                tech_id=TechInfo.BLANK_TECHNOLOGY_30.ID,
                location=BuildingInfo.CHIEFS_YURT.ID,
                button=1,
                enabled=True,
                player=player,
                research_time=20,
                cost_type=(Attribute.UNUSED_RESOURCE_499, None),
                cost_quantity=(3, None),
                icon_id=64,
            ),
            technology_setup(
                name="Forge of the chestplate",
                description="Cost 6 blacksmith points : All melee units gain +1 armor and piercing, Every 5 relic you posses you gain an extra armor and piercing points",
                tech_id=TechInfo.BLANK_TECHNOLOGY_31.ID,
                location=BuildingInfo.CHIEFS_YURT.ID,
                button=2,
                enabled=True,
                player=player,
                research_time=20,
                cost_type=(Attribute.UNUSED_RESOURCE_499, None),
                cost_quantity=(6, None),
                icon_id=17,
            ),
            technology_setup(
                name="silk cord",
                description="Cost 7 blacksmith point : Archer, skimishers and cav archer gain 5% attack speed, the cost of this tech is reduce by 1 every time you research it (max 4)",
                tech_id=TechInfo.BLANK_TECHNOLOGY_32.ID,
                location=BuildingInfo.CHIEFS_YURT.ID,
                button=3,
                enabled=True,
                player=player,
                research_time=20,
                cost_type=(Attribute.UNUSED_RESOURCE_499, None),
                cost_quantity=(7, None),
                icon_id=59,
            ),
            technology_setup(
                name="Nailed Iron on Leather",
                description="Nailed iron on leather cost 6 blacksmith point  : Archer, cav archer and hand canon gain +1 armor and 1 piercing, The most present unit type on the map at the moment this tech is search  gain an extra armor and piercing ",
                tech_id=TechInfo.BLANK_TECHNOLOGY_33.ID,
                location=BuildingInfo.CHIEFS_YURT.ID,
                button=4,
                enabled=True,
                player=player,
                research_time=20,
                cost_type=(Attribute.UNUSED_RESOURCE_499, None),
                cost_quantity=(6, None),
                icon_id=59,
            ),
            technology_setup(
                name="Tipped arrows",
                description="Tipped arrows cost 5 blacksmith point : Archer and CAV Archer gain +1 attack and an extra attack for every two archer tech searched in this blacksmith",
                tech_id=TechInfo.BLANK_TECHNOLOGY_34.ID,
                location=BuildingInfo.CHIEFS_YURT.ID,
                button=5,
                enabled=True,
                player=player,
                research_time=20,
                cost_type=(Attribute.UNUSED_RESOURCE_499, None),
                cost_quantity=(5, None),
                icon_id=59,
            ),
            technology_setup(
                name="Explosive power of the cave",
                description="Explosive power of the cave cost 6 blacksmith point : Handcanon unit and mounted hand canon unit gain +1 damage, gain an extra bullet every 10 blacksmith point spent ",
                tech_id=TechInfo.BLANK_TECHNOLOGY_35.ID,
                location=BuildingInfo.CHIEFS_YURT.ID,
                button=6,
                enabled=True,
                player=player,
                research_time=600,
                cost_type=(Attribute.UNUSED_RESOURCE_499, None),
                cost_quantity=(6, None),
                icon_id=59,
            ),
            technology_setup(
                name="Rivet remplacement",
                description="Rivet remplacement cost 8 : siege weapons gain +15 hp + 5 extra hp for every 20 piece of siege of each siege equipement",
                tech_id=TechInfo.BLANK_TECHNOLOGY_36.ID,
                location=BuildingInfo.CHIEFS_YURT.ID,
                button=7,
                enabled=True,
                player=player,
                research_time=10,
                cost_type=(Attribute.UNUSED_RESOURCE_499, None),
                cost_quantity=(8, None),
                icon_id=59,
            ),
            technology_setup(
                name="precious metal restoration",
                description="precious metal restoration cost 4 : You gain 0.25 extra experience points per kills, for every 10 convertion and 15 razed building you gain an extra 0.15 experience points",
                tech_id=TechInfo.BLANK_TECHNOLOGY_37.ID,
                location=BuildingInfo.CHIEFS_YURT.ID,
                button=8,
                enabled=True,
                player=player,
                research_time=10,
                cost_type=(Attribute.UNUSED_RESOURCE_499, None),
                cost_quantity=(4, None),
                icon_id=59,
            ),
            ]
        set_up_takoas_object = [
            object_setup(
                object=HeroInfo.GAWAIN.ID,
                name="takoas handbook",
                description="The blacksmith of takoas speak in is native langage, he will gladly help you to fight the curse of is home, exchange your blacksmiths point for upgrade but pay attention to the quirk to get the maximum value, the stone cost is the amount of point you have, you have <cost> points",
                building=BuildingInfo.CHIEFS_YURT.ID,
                button=15,
                enabled_object=True,
                player=player,
                cost_type=(Attribute.STONE_STORAGE, Attribute.UNUSED_RESOURCE_499),
                cost_quantity=(1, 10000),
            ),
        ]
        for cfg in set_up_blacksmith_of_takoas_tech:
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
        for cfg in set_up_takoas_object :
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
    list_trigger_silk_id = []
    list_trigger_silk = []
    for p in range (1,8):
        for t in range(1, 4):
            cost_tech = 7 - t
            reduce_cost_silk_coord = trigger_manager.add_trigger(
                name=f"reduce cost {p} {t}",
                enabled=True,
                looping=False,
            )
            reduce_cost_silk_coord.new_condition.script_call(
                xs_function=f"reduce_cost_silk_cord_{p}_{t}();",
            )
            reduce_cost_silk_coord.new_effect.change_technology_cost(
                source_player=p,
                resource_1=Attribute.UNUSED_RESOURCE_499,
                resource_1_quantity=cost_tech,
                technology=TechInfo.BLANK_TECHNOLOGY_32.ID,
            )
            reduce_cost_silk_coord.new_effect.change_technology_description(
                source_player=p,
                technology=TechInfo.BLANK_TECHNOLOGY_32.ID,
                message=f"Cost {cost_tech} blacksmith point : Archer, skimishers and cav archer gain 5% attack speed, the cost of this tech is reduce by 1 every time you research it (max 4)",
            )
            list_trigger_silk_id.append(reduce_cost_silk_coord.trigger_id)
            list_trigger_silk.append(reduce_cost_silk_coord)
        for t in range(0, 2):
            list_trigger_silk[t].new_effect.activate_trigger(
                trigger_id=list_trigger_silk_id[t + 1],
            )
        research_cost_silk_coord = trigger_manager.add_trigger(
            name=f"research silk_cord {p}",
            enabled=True,
            looping=True,
        )
        research_cost_silk_coord.new_condition.research_technology(
            source_player=p,
            technology=TechInfo.BLANK_TECHNOLOGY_32.ID,
        )
        research_cost_silk_coord.new_effect.script_call(
            message=f"silk_coord_of_the_forge_{p}();"
        )
        research_cost_silk_coord.new_effect.enable_disable_technology(
            source_player=p,
            technology=TechInfo.BLANK_TECHNOLOGY_32.ID,
            enabled=False,
        )
        research_cost_silk_coord.new_effect.enable_disable_technology(
            source_player=p,
            technology=TechInfo.BLANK_TECHNOLOGY_32.ID,
            enabled=True,
        )


    forge_xs_list = [
        (TechInfo.BLANK_TECHNOLOGY_30.ID, "forge_of_the_sword_{p}();"),
        (TechInfo.BLANK_TECHNOLOGY_31.ID, "chestplate_of_the_forge_{p}();"),
        (TechInfo.BLANK_TECHNOLOGY_33.ID, "nailed_leather_of_the_forge_{p}();"),
        (TechInfo.BLANK_TECHNOLOGY_34.ID, "tipped_arrow_of_the_forge_{p}();"),
        (TechInfo.BLANK_TECHNOLOGY_35.ID, "gun_powder_of_the_forge_{p}();"),
        (TechInfo.BLANK_TECHNOLOGY_36.ID, "siege_forge_tech_{p}();"),
        (TechInfo.BLANK_TECHNOLOGY_37.ID, "precious_metal_{p}();"),
    ]
    for p in range(1, 8):
        for tech_id, xs_call in forge_xs_list:
            forge_trigger = trigger_manager.add_trigger(
                name=f"Forge tech {tech_id} player {p}",
                enabled=True,
                looping=True,
            )
            forge_trigger.new_condition.research_technology(
                source_player=p,
                technology=tech_id,
            )
            forge_trigger.new_effect.script_call(
                message=xs_call.format(p=p),
            )
            forge_trigger.new_effect.enable_disable_technology(
                source_player=p,
                technology=tech_id,
                enabled=False,
            )
            forge_trigger.new_effect.enable_disable_technology(
                source_player=p,
                technology=tech_id,
                enabled=True,
            )
    area_x = 234
    area_y = 232
    area_x2 = 238
    area_y2 = 238
    list_command_post_trigger = []
    for p in range(1, 8):
        command_post_capture = trigger_manager.add_trigger(
            name=f"forge capture P{p}",
            enabled=False,
            looping=True,
        )
        command_post_capture.new_condition.objects_in_area(
            source_player=PlayerId.GAIA,
            object_list=BuildingInfo.CHIEFS_YURT.ID,
            quantity=1,
            area_x1=area_x,
            area_y1=area_y,
            area_x2=area_x2,
            area_y2=area_y2,
        )
        for other_player in range(1, 8):
            if other_player == p:
                inverted_check = False
            else:
                inverted_check = True
            command_post_capture.new_condition.objects_in_area(
                source_player=other_player,
                quantity=1,
                object_type=ObjectType.MILITARY,
                inverted=inverted_check,
                area_x1=area_x,
                area_y1=area_y,
                area_x2=area_x2,
                area_y2=area_y2,
            )
        command_post_capture.new_effect.change_ownership(
            source_player=PlayerId.GAIA,
            target_player=p,
            object_list_unit_id=BuildingInfo.CHIEFS_YURT.ID,
            area_x1=area_x,
            area_y1=area_y,
            area_x2=area_x2,
            area_y2=area_y2,
        )
        list_command_post_trigger.append(command_post_capture)
    command_post_activation = trigger_manager.add_trigger(
        name="Activate forge system",
        enabled=True,
        looping=False,
        execute_on_load=True,
    )
    command_post_activation.new_condition.timer(
        timer=10
    )
    command_post_activation.new_effect.change_ownership(
        source_player=PlayerId.EIGHT,
        target_player=PlayerId.GAIA,
        area_x1=area_x,
        area_y1=area_y,
        area_x2=area_x2,
        area_y2=area_y2,
        object_list_unit_id=BuildingInfo.CHIEFS_YURT.ID,
    )
    command_post_release = trigger_manager.add_trigger(
        name="forge post back to Gaia",
        enabled=False,
        looping=True,
    )
    command_post_release.new_condition.objects_in_area(
        source_player=PlayerId.GAIA,
        object_list=BuildingInfo.CHIEFS_YURT.ID,
        quantity=1,
        inverted=True,
        area_x1=area_x,
        area_y1=area_y,
        area_x2=area_x2,
        area_y2=area_y2,
    )
    for p in range(1, 8):
        command_post_release.new_condition.objects_in_area(
            source_player=p,
            quantity=1,
            object_type=ObjectType.MILITARY,
            inverted=True,
            area_x1=area_x,
            area_y1=area_y,
            area_x2=area_x2,
            area_y2=area_y2,
        )
    for p in range(1, 8):
        command_post_release.new_effect.change_ownership(
            source_player=p,
            target_player=PlayerId.GAIA,
            object_list_unit_id=BuildingInfo.CHIEFS_YURT.ID,
            area_x1=area_x,
            area_y1=area_y,
            area_x2=area_x2,
            area_y2=area_y2,
        )
    list_command_post_trigger.append(command_post_release)
    for i in range(len(list_command_post_trigger)):
        command_post_activation.new_effect.activate_trigger(
            trigger_id=list_command_post_trigger[i].trigger_id,
        )
    trigger_id = activation_triggers["forge"]
    trigger_id.new_effect.activate_trigger(
        trigger_id=command_post_activation.trigger_id,
    )
