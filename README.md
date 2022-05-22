# Building Gadgets Schematic Editor

## ... lets you to change blocks within schematics for the [Building Gadgets](https://www.curseforge.com/minecraft/mc-mods/building-gadgets) Minecraft mod. 

## Introduction

This tool can hopefully help you if: 
* You would like to have a specific build in your Minecraft world, but you dont have the exact same blocks available?
* You wish to make a build cheaper for your survival world?
* You like a build, but don't have the required mods for specific blocks it requires?
* You like the architecture of a build, but prefer another color scheme?

The idea to build this simple python tool came from really wishing to add the [Potion Shop](https://www.reddit.com/r/9x9/comments/njklyc/potion_shop_schematic_any_116/) to my Engimatica 6 Expert world, but not willing to add the Biomes O' Plenty mod. 


## TL;DR

1. Install the dependencies in the requirements chapter below
2. Run `py sedit.py unpack -s /path/schematic.json -m /path/map-file.json`
3. Edit the values in the mapfile for the new blocks you wish to use.
4. Run `py sedit.py repack -s /path/schematic.json -m /path/map-file.json -o /path/new-schematic.json`
5. Use the JSON in /path/new-schematic.json as you would use any other Building Gadgets Schematic


## Requirements

To run this tool you should: 

**Install Python 3.10.4 and pip**

You can download and install Python from the official website: https://www.python.org/downloads/
If you use the default installation settings, it will also install pip (Package Installer for Python) for you.
For simplified use of the tool, I recommend you mark the box that says "Add Python to PATH".

**Install the nbtlib package**

This tool uses [nbtlib](https://github.com/vberlier/nbtlib) to edit the nbt content embedded in the schematic.

Run the following command in your [Windows Powershell](https://www.digitalcitizen.life/ways-launch-powershell-windows-admin/): 

`pip install "nbtlib==2.0.4"`

If you checkmarked "Add Python to PATH" in the installation step, this should work automatically for you.

## How to use this tool

Download the tool from the [Releases](https://github.com/mlaidma/bg-sedit/releases) page or clone it with git.

This tool is a command line tool (no GUI). Therfore you must run the commands listed below in your [Windows Powershell](https://www.digitalcitizen.life/ways-launch-powershell-windows-admin/) in the folder where you unpacked or cloned the tool. To open a Powershell window in the folder of interest Shift + Right Click in the folder and choose "Open Powershell window here". You do not need admin rights for this tool.

You should also place the schematic that you wish to edit in the same folder. To achieve that, copy the content of the schematic as you would to use it with Building Gadgets. Paste the entire JSON into a new file (using Notepad for example) and save it (e.g potion-shop.json) where you have the `sedit` tool. 

**For help on the tool**

For help on how to use the tool you can run the help command: 
`py sedit.py -h`

This tool works in two separate stages.

**1) Unpacking the Schematic**

The first stage unpacks the schematic and maps all the used blogs in the design into a JSON file further referred as the map file. The content of this file is [block ID's](https://gamingsection.net/news/how-do-i-find-a-modded-block-id/#:~:text=You%20can%20press%20F3%20%2B%20H,block%20to%20see%20its%20id.) that are mapped 1-1 to themselves. 

To achieve this, run the following command in your Powershell window: 

`py sedit.py unpack -s /path/to/schematic -m /path/to/mapfile `

The name for the mapfile you can specify yourself. The path to the schematic should be the filename (if in the same folder) or the entire path to where your schematic is stored. 

Example: 

With the schematic file potion-shop.json stored in the same folder as the tool I would run: 

`py sedit.py unpack -s potion-shop.json -m potion-shop-swap-map.json`

The swap map is where you specify which blocks will be swapped for which other blocks using the [Block IDs](https://gamingsection.net/news/how-do-i-find-a-modded-block-id/#:~:text=You%20can%20press%20F3%20%2B%20H,block%20to%20see%20its%20id.). You can press F3 + H in Minecraft which will enable tooltips. You can now hover over an item or block to see its id. 

For example to swap all the Palm blocks from Biomes O Plenty to the Palm blocks added by the Atum mod, I have edited the file as shown on this screenshot:

![map-file](https://user-images.githubusercontent.com/5418506/169712862-c6d60b10-ac1e-4acc-9240-8355dceea2e8.png)

The Block ID's in the map file are always stored as "key" : "value" pairs. Key being the original block used, value being the new block you wish to use instead of it. Only change the ones that you wish to replace. Only edit the value. 

**2) Repacking the schematic**

The second stage will compare the blocks in the map file you specified, find the ones you wish to change and change those block IDs in the schematic file and produce a new file with the new schematic that uses your new blocks. Running the commands works the same way as specificed in the first stage. After making your changes in the mapfile, run the following command: 

`py sedit.py repack -s /path/to/schematic -m /path/to/mapfile -o /path/to/new-schematic`

For example: 

`py sedit.py repack -s potion-shop.json -m potion-shop-swap-map.json -o potion-shop-edited.json`

Afterwards use the new schematic file as you would use any other Building Gadgets schematic.

## Known Issues

**Error Handling**

The current release of this tool has no error handling whatsover. If the execution of this tool encounters any issues, it will crash. This means for example you must provide the schematic in a proper JSON format or it will not work. It will also not give you any meaningful error reports, but only the actual python error trace. Feel free to submit an [Issue](https://github.com/mlaidma/bg-sedit/issues) and attach the schematic you tried to use.

**Block States**

Apparently blocks in the minecraft world have properties or block states - think along the lines of whether the block is waterlogged or not. I am not even sure whether they are the same thing or not, but the tool has no regards for these whatsoever. This means the blocks are swapped in the NBT data brutally as-is. I have not tested this in any way so this could (perhaps) potentially lead to crashes or corrputed worlds. Read the Disclaimer below!

The tool should work (or at least did for me) for replacing simple blocks in a build like planks/stairs/fences for other planks/stairs/fences for example to change the color scheme of a build.

I have not tested this for any contraptions, machines or complex builds.

## Bugs & Issues

If you encounter any issues using this tool, feel free to submit an issue on the [Issues](https://github.com/mlaidma/bg-sedit/issues) page of this repository. As my needs for this tool are currently met, I can not promise I will actually fix the bug or that I will help you resolve it, but I will take a look, decide on a case-by-case basis and reply. 

## Disclaimer

I am in no way associated with the Building Gadgets mod or any of its authors. This is a standalone tool that operates independently on the schematics files that the Building Gadgets mod uses for the Copy-Paste Tool. 

I take no responsibility of any issues or corruptions to your Minecraft world or design that this tool creates. Always make a backup of your world as well as any original schematics files that you use.

Use this tool on your responsibility!
