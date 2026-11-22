import os
import shutil
import copy
import zipfile
from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from link_file import All_scenario_link
from AoE2ScenarioParser.datasets.units import UnitInfo
from genieutils.datfile import DatFile
from genieutils.sound import Sound, SoundItem
from AoE2ScenarioParser.datasets.other import OtherInfo
DAT_PATH = 'C:\\Users\\redma\\PycharmProjects\\walk_in_the_dead_island\\the_ruins\\resources\\_common\\dat\\empires2_x2_p1.dat'

SOUND_UNITS = [
    "unwished_treasure_of_the_ruins",
    "lambda_core",
    "last_two_legs",
    "Venger_sound",
    "Vortal_combat",
    "silence",
]


RESOURCE_BALANCE = {
    UnitInfo.WILD_BOAR.ID: 1750,
    OtherInfo.GOLD_MINE.ID: 1800,
    OtherInfo.STONE_MINE.ID: 1000,
    OtherInfo.FORAGE_BUSH.ID: 450,
    OtherInfo.TREE_JUNGLE.ID: 400,
    UnitInfo.DEER.ID:400,
    UnitInfo.SHEEP.ID:400,
    UnitInfo.RHINOCEROS.ID:2000,
    UnitInfo.GUANACO.ID : 400,
    UnitInfo.TAPIR.ID : 700,
    OtherInfo.FRUIT_BUSH.ID : 750,
    OtherInfo.BUSH_A.ID : 450,
    OtherInfo.TREE_BIRCH.ID : 550,
    OtherInfo.TREE_DEAD.ID:300,
    OtherInfo.TREE_MONKEY_PUZZLE.ID:1500,
    UnitInfo.IBEX.ID : 800,
}

House_list = {
    70:10,
    191:10,
    192:10,
    463:10,
    464:10,
    465:10,
}

deposit_building = {
    562:50,
    563:50,
    564:50,
    565:50,
    584:50,
    585:50,
    586:50,
    587:50,
    68:50,
    129:50,
    130:50,
    131:50,
}
collision_list = {
    83:0.1,
    293:0.1,
    124:0.1,
    220:0.1,
    579:0.1,
    581:0.1,
    123:0.1,
    218:0.1,
    120:0.1,
    354:0.1,
    56:0.1,
    57:0.1,
    590:0.1,
    592:0.1,
    122:0.1,
    216:0.1,
    118:0.1,
    212:0.1,
}

def copy_the_file(src, dst):
    if os.path.isdir(src):
        dst = os.path.join(dst, os.path.basename(src))
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        shutil.copy(src, dst)


def modify_data():
    data = DatFile.parse(DAT_PATH)
    for sound_name in SOUND_UNITS:
        new_id = len(data.civs[0].units)
        sound_id = len(data.sounds)

        item = SoundItem(filename=sound_name, resource_id=-1, probability=100,
                         civilization=-1, icon_set=-1)
        data.sounds.append(Sound(id=sound_id, play_delay=0, cache_time=300000, total_probability=100,
                                 items=[item]))

        for civ in data.civs:
            if civ.units[4] is None:
                civ.units.append(None)
                continue
            unit = copy.deepcopy(civ.units[4])
            unit.id = new_id
            unit.copy_id = new_id
            unit.base_id = new_id
            unit.enabled = 0
            unit.train_sound = sound_id
            unit.wwise_train_sound_id = 0
            unit.hit_points = 0
            civ.units.append(unit)

        data.unit_headers.append(copy.deepcopy(data.unit_headers[4]))
        print(f"{sound_name} -> Unité : {new_id} | Son : {sound_id}")

    for unit_id, amount in RESOURCE_BALANCE.items():
        for civ in data.civs:
            unit = civ.units[unit_id]
            if unit is None:
                continue
            unit.resource_storages[0].amount = amount
        print(f"Ressource {unit_id} -> {amount}")
    for unit_id, amount in House_list.items():
        for civ in data.civs:
            print(f"Villager display {civ.units[83]}")
            unit = civ.units[unit_id]
            if unit is None:
                continue
            for storage in unit.resource_storages:
                if storage.type == 4:
                    storage.amount = amount
                    print(unit_id, unit.name, storage.type, storage.amount)
    for unit_id, amount in deposit_building.items():
        for civ in data.civs:
            unit = civ.units[unit_id]
            if unit is None or unit.creatable is None:
                continue
            for cost in unit.creatable.resource_costs:
                if cost.type == 1:
                    cost.amount = amount
                    print(unit_id, unit.name, cost.type, cost.amount)

                    print(unit_id, unit.name, cost.type, cost.amount)
    for unit_id, amount in collision_list.items():
        for civ in data.civs:
            unit = civ.units[unit_id]
            if unit is None:
                continue
            unit.collision_size_x = amount
            unit.collision_size_y = amount
            unit.obstruction_type = 12
            print(unit_id, amount)
    data.save(DAT_PATH)

def zip_file(resource_folder, zip_path):
    resource_folder = os.path.abspath(resource_folder)
    zip_path = os.path.abspath(zip_path)
    if not os.path.isdir(resource_folder):
        raise FileNotFoundError(f"Dossier a zipper introuvable : {resource_folder}")
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)
    parent = resource_folder
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(resource_folder):
            for name in files:
                full_path = os.path.join(root, name)
                zf.write(full_path, arcname=os.path.relpath(full_path, parent))
    print(f"Zip cree : {zip_path}")


def main(output_path):
    copy_the_file(All_scenario_link["default_dat_path"],
                  All_scenario_link["mod_dat"])
    copy_the_file(All_scenario_link["XS_PATH"],
                  All_scenario_link["mod_xs"])
    modify_data()
    copy_the_file(output_path,
                  All_scenario_link["mod_scenario"])
    copy_the_file(All_scenario_link["Mod_folder"],
                  All_scenario_link["push_loca_mod"])
    zip_output = All_scenario_link.get(
        "zip_output",
        os.path.join(os.path.dirname(All_scenario_link["Mod_folder"]), "resource.zip"),
    )
    zip_file(All_scenario_link["resource_folder"], zip_output)