import copy
import json
from pkgutil import iter_modules
import sys

import argparse
from typing import OrderedDict

import base64

import nbtlib 
from nbtlib import String


COMMAND_UNPACK = "unpack"
COMMAND_REPACK = "repack"


def unpack(schematic_path, map_path):

    print(f"Listing all blocks used in {schematic_path} to {map_path}\n\r")

    with open(schematic_path) as file:
        json_schematic = json.load(file, object_pairs_hook=OrderedDict)

    item_list = json_schematic["header"]["material_list"]["root_entry"]

    swap_map = OrderedDict()

    for item in item_list:
        block_id = item["item"]["id"]
        swap_map[block_id] = block_id

    with open(map_path, "w") as mapfile:
        json.dump(swap_map, mapfile, indent=4)


def repack(schematic_path, output_path, map_path):

    print(f"Repacking changes in {schematic_path} from {map_path} to {output_path}")
    print("")
    
    # 
    # Load map of changed blocks
    # 

    with open(map_path) as mapfile:
        swap_map = json.load(mapfile, object_pairs_hook=OrderedDict)

    swapped_blocks = OrderedDict()

    for key, value in swap_map.items():
        if key != value: 
            swapped_blocks[key] = value
            print(f"Block {key} changed to {value}")

    print("")
    
    #
    # Swap blocks in the schematic header
    #

    with open(schematic_path) as schematic_file:
        input_schematic = json.load(schematic_file, object_pairs_hook=OrderedDict)
    
    output_schematic = copy.deepcopy(input_schematic)

    material_list_input = input_schematic["header"]["material_list"]["root_entry"]
    material_list_output = copy.deepcopy(material_list_input)

    for index, list_item in enumerate(material_list_input):
        block_id = list_item["item"]["id"]
        if block_id in swapped_blocks.keys():
            material_list_output[index]["item"]["id"] = swapped_blocks[block_id]
            print(f"Swapped {block_id} for {swapped_blocks[block_id]} in schematic header")

    print("")

    output_schematic["header"]["material_list"]["root_entry"] = material_list_output

    # 
    # Swap blocks in the schematic body
    #
    
    schematic_body_input = input_schematic["body"]

    decoded_body = base64.b64decode(schematic_body_input)

    #Write a temporary nbt file to use existing NBT library (https://github.com/vberlier/nbtlib)
    #that does not support loading bytes objects directly and needs files
    with open("sedit.nbt", "wb") as tempfile:
        tempfile.write(decoded_body)

    with nbtlib.load("sedit.nbt") as nbtfile:
        for tag in nbtfile["data"]:
            block_id = tag["state"]["Name"]

            if block_id in swapped_blocks.keys():
                tag["state"].update({"Name": String(swapped_blocks[block_id])})
                print(f"Swapped {block_id} for {swapped_blocks[block_id]} in schematic body")

        print("")

        nbtfile.save()

    with open("sedit.nbt", "rb") as nbtfile:
        nbt_data = nbtfile.read()

    encoded_body = base64.b64encode(nbt_data).decode("utf-8")
    output_schematic["body"] = encoded_body

    with open(output_path, "w") as output_file:
        json.dump(output_schematic, output_file, indent=4)

    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Swap blocks within a Building Gadgets schematic")

    parser.add_argument("command", choices=["unpack", "repack"],
        help="Action for the tool to perform. Unpack a new schematic into a block map or repack the new schematic")

    parser.add_argument("-s", "--schematic", help="Specifies the input schematic file")
    parser.add_argument("-o", "--output", help="Specifies the output schematic file with the swapped blocks")

    parser.add_argument("-m", "--map", help="Specifies the file in which to store the block swap map") 

    args = parser.parse_args()

    if args.command == COMMAND_UNPACK:
        
        if not (args.schematic and args.map):
            raise argparse.ArgumentTypeError("Both the -s and -m arguments required for unpacking. Run sedit.py -h for more info")

        unpack(args.schematic, args.map)
        print(f"Finished unpacking {args.schematic}. Swap map is stored in {args.map}")

    if args.command == COMMAND_REPACK:
        
        if not (args.schematic and args.map and args.output):
            raise argparse.ArgumentTypeError("The -s -m and -o arguments are all required for repacking. Run sedit.py -h for more info")

        repack(args.schematic, args.output, args.map)
        print(f"Finished repacking {args.schematic} with {args.map}. New schematic is in {args.output}")
        print("")

print("Done!")
sys.exit()