import json
from pkgutil import iter_modules
import sys

import argparse
from ast import arg, parse


COMMAND_UNPACK = "unpack"
COMMAND_REPACK = "repack"


def unpack(schematic, map):

    with open(schematic) as file:
        json_schematic = json.load(file)

    schematic_header = json_schematic["header"]

    item_list = schematic_header["material_list"]["root_entry"]

    swap_map = dict()

    for item in item_list:
        block_id = item["item"]["id"]
        swap_map[block_id] = block_id

    with open(map, "w") as mapfile:
        json.dump(swap_map, mapfile,indent=4)


def repack(schematic, output, map):
    pass





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

    

print("Done!")