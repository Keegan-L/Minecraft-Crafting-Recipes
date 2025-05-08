from flask import Flask, render_template, Response, request, jsonify, send_from_directory, session, redirect
import os
import random
from copy import deepcopy
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'minecraft_crafting_secret_key'  # Required for session

# Initialize visited items in session if not exists
@app.before_request
def before_request():
    if 'visited_items' not in session:
        session['visited_items'] = []

# Serve static files from data directory
@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory('data', filename)

ingredient_images = {
    "Wooden Plank": "https://minecraft.wiki/images/Oak_Planks_JE6_BE3.png?b7e2a",
    "Stick": "https://minecraft.wiki/images/Stick_JE1_BE1.png?7a7a2",
    "Coal": "https://minecraft.wiki/images/Coal_JE4_BE3.png?b2e2a",
    "Wool": "https://minecraft.wiki/images/White_Wool_JE2_BE2.png?2bcdc",
    "Cobblestone": "https://minecraft.wiki/images/Cobblestone_JE5_BE3.png?b6e2a",
    "Iron Ingot": "https://minecraft.wiki/images/Iron_Ingot_JE3_BE2.png?fcfca",
    "Gold Ingot": "https://minecraft.wiki/images/Gold_Ingot_JE4_BE2.png?80cd6&format=original",
    "Diamond": "https://minecraft.wiki/images/Diamond_JE3_BE3.png?9e9ea",
    "String": "https://minecraft.wiki/images/String_JE1_BE1.png?c0c0a",
    "Flint": "https://minecraft.wiki/images/Flint_JE2_BE2.png?9e9ea",
    "Redstone": "https://minecraft.wiki/images/Redstone_Dust_JE2_BE2.png?e1e1a",
    "Feather": "https://minecraft.wiki/images/Feather_JE3_BE2.png?e2e2a",
    "Leather": "https://minecraft.wiki/images/Leather_JE1_BE1.png?c2c2a",
    "Log": "https://minecraft.wiki/images/Oak_Log_%28UD%29_JE5_BE3.png?8a080",
    "Scute": "https://minecraft.wiki/images/Turtle_Scute_JE1_BE1.png?99cc2&format=original",
    "Gold Nugget": "https://minecraft.wiki/images/Gold_Nugget_JE3_BE2.png?4c4ca",
    "Iron": "https://minecraft.wiki/images/Iron_Ingot_JE3_BE2.png?fcfca"
}

item_images = {
    "Wooden Plank": "https://minecraft.wiki/images/Oak_Planks_JE6_BE3.png?b7e2a",
    "Stick": "https://minecraft.wiki/images/Stick_JE1_BE1.png?7a7a2",
    "Torch": "https://minecraft.wiki/images/Torch_%28texture%29_JE3_BE2.png?18a97&format=original",
    "Crafting Table": "https://minecraft.wiki/images/Crafting_Table_JE3_BE2.png?b6e2a",
    "Furnace": "https://minecraft.wiki/images/Furnace_%28S%29_JE4.png?fcfca",
    "Chest": "https://minecraft.wiki/images/Chest_%28S%29_JE1.png?9e9ea",
    "Ladder": "https://minecraft.wiki/images/Ladder_%28texture%29_JE3_BE2.png?c0c0a",
    "Fence": "https://minecraft.wiki/images/Oak_Fence_JE4_BE2.png?9e9ea",
    "Boat": "https://minecraft.wiki/images/Oak_Boat_%28item%29_JE4_BE3.png?e2e2a",
    "Slab": "https://minecraft.wiki/images/Oak_Slab_JE5_BE2.png?c2c2a",
    "Stairs": "https://minecraft.wiki/images/Oak_Stairs_%28N%29_JE7_BE6.png?8a080",
    "Door": "https://minecraft.wiki/images/Oak_Door_%28item%29_JE4_BE3.png?2b2ba",
    "Sign": "https://www.minecraft-crafting.net/app/src/Basic/img/img_sign.png",
    "Bed": "https://minecraft.wiki/images/White_Bed_JE3_BE3.png?fcfca",
    "Pickaxe": "https://minecraft.wiki/images/Wooden_Pickaxe_JE2_BE2.png?b7e2a",
    "Axe": "https://minecraft.wiki/images/Wooden_Axe_JE2_BE2.png?7a7a2",
    "Shovel": "https://minecraft.wiki/images/Wooden_Shovel_JE2_BE2.png?b2e2a",
    "Hoe": "https://minecraft.wiki/images/Wooden_Hoe_JE3_BE3.png?b6e2a",
    "Fishing Rod": "https://minecraft.wiki/images/Fishing_Rod_JE2_BE2.png?fcfca",
    "Flint & Steel": "https://minecraft.wiki/images/Flint_and_Steel_JE2.png?9e9ea",
    "Compass": "https://minecraft.wiki/images/Compass_JE3_BE3.gif?c0c0a",
    "Bucket": "https://minecraft.wiki/images/Bucket_JE2_BE2.png?9e9ea",
    "Shears": "https://minecraft.wiki/images/Shears_JE2_BE2.png?e2e2a",
    "Clock": "https://minecraft.wiki/images/Clock_JE3_BE3.gif?c2c2a",
    "Helmet": "https://minecraft.wiki/images/Leather_Cap_%28item%29_JE4_BE3.png?8a080",
    "Chestplate": "https://minecraft.wiki/images/Leather_Tunic_%28item%29_JE4_BE3.png?2b2ba",
    "Leggings": "https://minecraft.wiki/images/Leather_Pants_%28item%29_JE3_BE2.png?4c4ca",
    "Boots": "https://minecraft.wiki/images/Leather_Boots_%28item%29_JE4_BE3.png?fcfca",
    "Sword": "https://minecraft.wiki/images/Wooden_Sword_JE2_BE2.png?b7e2a",
    "Bow": "https://minecraft.wiki/images/Bow_JE2_BE1.png?7a7a2",
    "Arrow": "https://www.minecraft-crafting.net/app/src/Defence/img/img_arrow.png",
    "Shield": "https://minecraft.wiki/images/Shield_JE2_BE1.png?b6e2a"
}

def get_ingredient_img(name):
    return ingredient_images.get(name, "https://minecraft.wiki/images/Oak_Planks_JE6_BE3.png?b7e2a")

def get_item_img(name):
    return item_images.get(name, "https://minecraft.wiki/images/Oak_Planks_JE6_BE3.png?b7e2a")

def get_valid_materials(item_name):
    tool_materials = {
        "Pickaxe": ["Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "Axe": ["Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "Shovel": ["Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "Hoe": ["Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "Sword": ["Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "Helmet": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond", "Scute"],
        "Chestplate": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "Leggings": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "Boots": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
    }
    return tool_materials.get(item_name, [])

basics = [
    {
        "name": "Wooden Plank",
        "img": get_item_img("Wooden Plank"),
        "desc": "Basic building material. Appearance varies by biome depending on type of wood (Oak, Spruce, Birch, Jungle, Acacia, Dark Oak).",
        "madeof": ["Log"],
        "makes": ["Stick", "Crafting Table", "Chest"],
        "next": "Stick",
        "prev": "Wooden Shield",
        "recipe": [
            [{}, {}, {}],
            [{}, {"ingredient": "Log", "pic": get_ingredient_img("Log")}, {}],
            [{}, {}, {}]
        ]
   },
    {
        "name": "Stick",
        "img": get_item_img("Stick"),
        "desc": "Used to craft many other items.",
        "madeof": ["Wooden Plank"],
        "makes": ["Torch", "Fence", "Sword", "Ladder", "Sign"],
        "next": "Torch",
        "prev": "Wooden Plank",
        "recipe": [
            [{}, {}, {}],
            [{}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}],
            [{}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}]
        ]
   },
    {
        "name": "Torch",
        "img": get_item_img("Torch"),
        "desc": "Provides light and melts ice/snow.",
        "madeof": ["Stick", "Coal"],
        "makes": [],
        "next": "Crafting Table",
        "prev": "Stick",
        "recipe": [
            [{}, {}, {}],
            [{}, {"ingredient": "Coal", "pic": get_ingredient_img("Coal")}, {}],
            [{}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}]
        ]
    },
    {
        "name": "Crafting Table",
        "img": get_item_img("Crafting Table"),
        "desc": "Allows player to craft when right clicked.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "next": "Furnace",
        "prev": "Torch",
        "recipe": [
            [{}, {}, {}],
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}],
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}]
        ]
    },
    {
        "name": "Furnace",
        "img": get_item_img("Furnace"),
        "desc": "Used to smelt items and cook food.",
        "madeof": ["Cobblestone"],
        "makes": [],
        "next": "Chest",
        "prev": "Crafting Table",
        "recipe": [
            [{"ingredient": "Cobblestone", "pic": get_ingredient_img("Cobblestone")}, {"ingredient": "Cobblestone", "pic": get_ingredient_img("Cobblestone")}, {"ingredient": "Cobblestone", "pic": get_ingredient_img("Cobblestone")}],
            [{"ingredient": "Cobblestone", "pic": get_ingredient_img("Cobblestone")}, {}, {"ingredient": "Cobblestone", "pic": get_ingredient_img("Cobblestone")}],
            [{"ingredient": "Cobblestone", "pic": get_ingredient_img("Cobblestone")}, {"ingredient": "Cobblestone", "pic": get_ingredient_img("Cobblestone")}, {"ingredient": "Cobblestone", "pic": get_ingredient_img("Cobblestone")}]
        ]
    },
    {
        "name": "Chest",
        "img": get_item_img("Chest"),
        "desc": "Used to store items.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "next": "Ladder",
        "prev": "Furnace",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}],
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}],
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}]
        ]
   },
   {
        "name": "Ladder",
        "img": get_item_img("Ladder"),
        "desc": "Used to climb up and down.",
        "madeof": ["Stick"],
        "makes": [],
        "next": "Fence",
        "prev": "Chest",
        "recipe": [
            [{"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}],
            [{"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}],
            [{"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}]
        ]
   },
   {
        "name": "Fence",
        "img": get_item_img("Fence"),
        "desc": "Used to create barriers.",
        "madeof": ["Stick", "Wooden Plank"],
        "makes": [],
        "next": "Boat",
        "prev": "Ladder",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}],
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}],
            [{}, {}, {}]
        ]
   },
   {
        "name": "Boat",
        "img": get_item_img("Boat"),
        "desc": "Used to travel on water.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "next": "Wooden Slab",
        "prev": "Fence",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}],
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}],
            [{}, {}, {}]
        ]
   },
   {
        "name": "Wooden Slab",
        "img": get_item_img("Slab"),
        "desc": "Used to create gradual slopes. Can be made of many different building materials (Wooden Plank, Cobblestone, Brick, Quartz, etc.).",
        "madeof": ["Wooden Plank"],
        "Variants": "Wooden Plank can be substituted with Cobblestone, Brick, Quartz, and other materials.",
        "makes": [],
        "next": "Wooden Stairs",
        "prev": "Boat",
        "recipe": [
            [{}, {}, {}],
            [{}, {}, {}],
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}]
        ],
        "shapeless": False
   },
   {
        "name": "Wooden Stairs",
        "img": get_item_img("Stairs"),
        "desc": "Used to create stairs for climbing.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "next": "Door",
        "prev": "Wooden Slab",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}, {}],
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}],
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}]
        ]
   },
   {
        "name": "Door",
        "img": get_item_img("Door"),
        "desc": "Used to create entrances and exits.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "next": "Sign",
        "prev": "Wooden Stairs",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}],
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}],
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}]
        ]
   },
   {
        "name": "Sign",
        "img": get_item_img("Sign"),
        "desc": "Used to display text.",
        "madeof": ["Wooden Plank", "Stick"],
        "makes": [],
        "next": "Bed",
        "prev": "Door",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}],
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}],
            [{}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}]
        ]
   },
   {
        "name": "Bed",
        "img": get_item_img("Bed"),
        "desc": "Used to sleep and set spawn point.",
        "madeof": ["Wool", "Wooden Plank"],
        "makes": [],
        "next": "Wooden Pickaxe",
        "prev": "Sign",
        "recipe": [
            [{"ingredient": "Wool", "pic": get_ingredient_img("Wool")}, {"ingredient": "Wool", "pic": get_ingredient_img("Wool")}, {"ingredient": "Wool", "pic": get_ingredient_img("Wool")}],
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}],
            [{}, {}, {}]
        ]
   }
]

tools = [
    {
        "name": "Wooden Pickaxe",
        "img": get_item_img("Pickaxe"),
        "desc": "Used to mine stone blocks and ores. Durability and Damage varies depending on type of Pickaxe (Wooden, Stone, Iron, Gold, Diamond).",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "Variants": "Wooden Plank can be substituted with Cobblestone, Iron Ingot, Gold Ingot, or Diamond.",
        "makes": [],
        "next": "Wooden Axe",
        "prev": "Bed",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}],
            [{}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}],
            [{}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}]
        ]
   },
   {
        "name": "Wooden Axe",
        "img": get_item_img("Axe"),
        "desc": "Used to chop wood blocks faster. Durability and Damage varies depending on type of Axe (Wooden, Stone, Iron, Gold, Diamond).",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "Variants": "Wooden Plank can be substituted with Cobblestone, Iron Ingot, Gold Ingot, or Diamond.",
        "makes": [],
        "next": "Wooden Shovel",
        "prev": "Wooden Pickaxe",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}],
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}],
            [{}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}]
        ]
   },
   {
        "name": "Wooden Shovel",
        "img": get_item_img("Shovel"),
        "desc": "Used to dig sand, gravel, dirt, grass, and snow faster. Durability and Damage varies depending on type of Shovel (Wooden, Stone, Iron, Gold, Diamond).",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "Variants": "Wooden Plank can be substituted with Cobblestone, Iron Ingot, Gold Ingot, or Diamond.",
        "makes": [],
        "next": "Wooden Hoe",
        "prev": "Wooden Axe",
        "recipe": [
            [{}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}],
            [{}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}],
            [{}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}]
        ]
   },
   {
        "name": "Wooden Hoe",
        "img": get_item_img("Hoe"),
        "desc": "Used to till dirt blocks in preparation for growing crops. Durability and Damage varies depending on type of Hoe (Wooden, Stone, Iron, Gold, Diamond).",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "Variants": "Wooden Plank can be substituted with Cobblestone, Iron Ingot, Gold Ingot, or Diamond.",
        "makes": [],
        "next": "Fishing Rod",
        "prev": "Wooden Shovel",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}],
            [{}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}],
            [{}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}]
        ]
   },
   {
        "name": "Fishing Rod",
        "img": get_item_img("Fishing Rod"),
        "desc": "Can be cast into water to catch fish.",
        "madeof": ["Stick", "String"],
        "makes": [],
        "next": "Flint & Steel",
        "prev": "Wooden Hoe",
        "recipe": [
            [{}, {}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}],
            [{}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {"ingredient": "String", "pic": get_ingredient_img("String")}],
            [{"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}, {"ingredient": "String", "pic": get_ingredient_img("String")}]
        ]
   },
   {
        "name": "Flint & Steel",
        "img": get_item_img("Flint & Steel"),
        "desc": "Used to light fires, ignite TNT and open nether portals.",
        "madeof": ["Iron Ingot", "Flint"],
        "makes": [],
        "next": "Compass",
        "prev": "Fishing Rod",
        "recipe": [
            [{}, {}, {}],
            [{"ingredient": "Iron Ingot", "pic": get_ingredient_img("Iron Ingot")}, {}, {}],
            [{}, {"ingredient": "Coal", "pic": get_ingredient_img("Coal")}, {}]
        ]
   },
   {
        "name": "Compass",
        "img": get_item_img("Compass"),
        "desc": "Points to the spawn point.",
        "madeof": ["Iron Ingot", "Redstone"],
        "makes": [],
        "next": "Bucket",
        "prev": "Flint & Steel",
        "recipe": [
            [{}, {"ingredient": "Iron Ingot", "pic": get_ingredient_img("Iron Ingot")}, {}],
            [{"ingredient": "Iron Ingot", "pic": get_ingredient_img("Iron Ingot")}, {"ingredient": "Redstone", "pic": get_ingredient_img("Redstone")}, {"ingredient": "Iron Ingot", "pic": get_ingredient_img("Iron Ingot")}],
            [{}, {"ingredient": "Iron Ingot", "pic": get_ingredient_img("Iron Ingot")}, {}]
        ]
   },
   {
        "name": "Bucket",
        "img": get_item_img("Bucket"),
        "desc": "Used to transport water, lava, and milk.",
        "madeof": ["Iron Ingot"],
        "makes": [],
        "next": "Shears",
        "prev": "Compass",
        "recipe": [
            [{}, {}, {}],
            [{"ingredient": "Iron Ingot", "pic": get_ingredient_img("Iron Ingot")}, {}, {"ingredient": "Iron Ingot", "pic": get_ingredient_img("Iron Ingot")}],
            [{}, {"ingredient": "Iron Ingot", "pic": get_ingredient_img("Iron Ingot")}, {}]
        ]
   },
   {
        "name": "Shears",
        "img": get_item_img("Shears"),
        "desc": "Used to collect wool from sheep and leaves from trees.",
        "madeof": ["Iron Ingot"],
        "makes": [],
        "next": "Clock",
        "prev": "Bucket",
        "recipe": [
            [{}, {}, {}],
            [{}, {"ingredient": "Iron Ingot", "pic": get_ingredient_img("Iron Ingot")}, {}],
            [{"ingredient": "Iron Ingot", "pic": get_ingredient_img("Iron Ingot")}, {}, {}]
        ]
   },
   {
        "name": "Clock",
        "img": get_item_img("Clock"),
        "desc": "Shows the current time of day.",
        "madeof": ["Gold Ingot", "Redstone"],
        "makes": [],
        "next": "Leather Helmet",
        "prev": "Shears",
        "recipe": [
            [{}, {"ingredient": "Gold Ingot", "pic": get_ingredient_img("Gold Ingot")}, {}],
            [{"ingredient": "Gold Ingot", "pic": get_ingredient_img("Gold Ingot")}, {"ingredient": "Redstone", "pic": get_ingredient_img("Redstone")}, {"ingredient": "Gold Ingot", "pic": get_ingredient_img("Gold Ingot")}],
            [{}, {"ingredient": "Gold Ingot", "pic": get_ingredient_img("Gold Ingot")}, {}]
        ]
   }
]

defense = [
    {
        "name": "Leather Helmet",
        "img": get_item_img("Helmet"),
        "desc": "Head armor. Durability varies depending on type of helmet (Wooden, Stone, Iron, Gold, Diamond, Turtle Shell). Turtle shell helmet gives the player water breathing effect.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond", "Scute"],
        "Variants": "Leather can be substituted with Iron Ingot, Gold Ingot, Diamond, or Scute.",
        "makes": [],
        "next": "Leather Chestplate",
        "prev": "Clock",
        "recipe": [
            [{}, {}, {}],
            [{"ingredient": "Leather", "pic": get_ingredient_img("Leather")}, {"ingredient": "Leather", "pic": get_ingredient_img("Leather")}, {"ingredient": "Leather", "pic": get_ingredient_img("Leather")}],
            [{"ingredient": "Leather", "pic": get_ingredient_img("Leather")}, {}, {"ingredient": "Leather", "pic": get_ingredient_img("Leather")}]
        ]
   },
   {
        "name": "Leather Chestplate",
        "img": get_item_img("Chestplate"),
        "desc": "Chest armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "Variants": "Leather can be substituted with Iron Ingot, Gold Ingot, or Diamond.",
        "makes": [],
        "next": "Leather Leggings",
        "prev": "Leather Helmet",
        "recipe": [
            [{"ingredient": "Leather", "pic": get_ingredient_img("Leather")}, {}, {"ingredient": "Leather", "pic": get_ingredient_img("Leather")}],
            [{"ingredient": "Leather", "pic": get_ingredient_img("Leather")}, {"ingredient": "Leather", "pic": get_ingredient_img("Leather")}, {"ingredient": "Leather", "pic": get_ingredient_img("Leather")}],
            [{"ingredient": "Leather", "pic": get_ingredient_img("Leather")}, {"ingredient": "Leather", "pic": get_ingredient_img("Leather")}, {"ingredient": "Leather", "pic": get_ingredient_img("Leather")}]
        ]
   },
   {
        "name": "Leather Leggings",
        "img": get_item_img("Leggings"),
        "desc": "Leg armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "Variants": "Leather can be substituted with Iron Ingot, Gold Ingot, or Diamond.",
        "makes": [],
        "next": "Leather Boots",
        "prev": "Leather Chestplate",
        "recipe": [
            [{"ingredient": "Leather", "pic": get_ingredient_img("Leather")}, {"ingredient": "Leather", "pic": get_ingredient_img("Leather")}, {"ingredient": "Leather", "pic": get_ingredient_img("Leather")}],
            [{"ingredient": "Leather", "pic": get_ingredient_img("Leather")}, {}, {"ingredient": "Leather", "pic": get_ingredient_img("Leather")}],
            [{"ingredient": "Leather", "pic": get_ingredient_img("Leather")}, {}, {"ingredient": "Leather", "pic": get_ingredient_img("Leather")}]
        ]
   },
   {
        "name": "Leather Boots",
        "img": get_item_img("Boots"),
        "desc": "Foot armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "Variants": "Leather can be substituted with Iron Ingot, Gold Ingot, or Diamond.",
        "makes": [],
        "next": "Wooden Sword",
        "prev": "Leather Leggings",
        "recipe": [
            [{}, {}, {}],
            [{"ingredient": "Leather", "pic": get_ingredient_img("Leather")}, {}, {"ingredient": "Leather", "pic": get_ingredient_img("Leather")}],
            [{"ingredient": "Leather", "pic": get_ingredient_img("Leather")}, {}, {"ingredient": "Leather", "pic": get_ingredient_img("Leather")}]
        ]
   },
   {
        "name": "Wooden Sword",
        "img": get_item_img("Sword"),
        "desc": "Deal damage to mobs and other players. Durability and Damage varies depending on type of Sword (Wooden, Stone, Iron, Gold, Diamond).",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "Variants": "Wooden Plank can be substituted with Cobblestone, Iron Ingot, Gold Ingot, or Diamond.",
        "makes": [],
        "next": "Wooden Bow",
        "prev": "Leather Boots",
        "recipe": [
            [{}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}],
            [{}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}],
            [{}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}]
        ]
   },
   {
        "name": "Wooden Bow",
        "img": get_item_img("Bow"),
        "desc": "Used to shoot arrows that deal damage to mobs and other players.",
        "madeof": ["Stick", "String"],
        "makes": [],
        "next": "Arrow",
        "prev": "Wooden Sword",
        "recipe": [
            [{"ingredient": "String", "pic": get_ingredient_img("String")}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}],
            [{"ingredient": "String", "pic": get_ingredient_img("String")}, {}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}],
            [{"ingredient": "String", "pic": get_ingredient_img("String")}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}]
        ]
   },
   {
        "name": "Arrow",
        "img": get_item_img("Arrow"),
        "desc": "Ammunition for bows.",
        "madeof": ["Stick", "Flint", "Feather"],
        "makes": [],
        "next": "Wooden Shield",
        "prev": "Wooden Bow",
        "recipe": [
            [{}, {"ingredient": "Coal", "pic": get_ingredient_img("Coal")}, {}],
            [{}, {"ingredient": "Stick", "pic": get_ingredient_img("Stick")}, {}],
            [{}, {"ingredient": "Feather", "pic": get_ingredient_img("Feather")}, {}]
        ]
   },
   {
        "name": "Wooden Shield",
        "img": get_item_img("Shield"),
        "desc": "Protects player against attack.",
        "madeof": ["Wooden Plank", "Iron Ingot"],
        "makes": [],
        "next": "Wooden Plank",
        "prev": "Arrow",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Iron Ingot", "pic": get_ingredient_img("Iron Ingot")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}],
            [{"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}],
            [{}, {"ingredient": "Wooden Plank", "pic": get_ingredient_img("Wooden Plank")}, {}]
        ]
   }
]

# Add these constants after other constants
SCORES_FILE = 'data/scores.json'

# Add these functions before the routes
def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_score(score):
    scores = load_scores()
    scores.append({
        'score': score,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    # Sort scores by score (descending) and date (descending)
    scores.sort(key=lambda x: (-x['score'], x['date']))
    # Keep only top 10 scores
    scores = scores[:10]
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)
    return scores

# ROUTES

@app.route('/')
def index():
    return render_template('index.html', 
                         basics=basics, 
                         tools=tools, 
                         defense=defense,
                         visited_items=session.get('visited_items', []))

@app.route('/learn/<string:name>')
def learn(name):
    selected = None
    category = None
    
    # Create a list of all craftable items
    craftable_items = []
    for item in basics:
        craftable_items.append(item["name"])
    for item in tools:
        craftable_items.append(item["name"])
    for item in defense:
        craftable_items.append(item["name"])
    
    # Search in basics
    for item in basics:
        if item["name"] == name:
            selected = item
            category = "basics"
            break
    
    # If not found in basics, search in tools
    if not selected:
        for item in tools:
            if item["name"] == name:
                selected = item
                category = "tools"
                break
    
    # If not found in tools, search in defense
    if not selected:
        for item in defense:
            if item["name"] == name:
                selected = item
                category = "defense"
                break
    
    if not selected:
        return "Item not found", 404
    
    # Add item to visited items if not already there
    visited_items = session.get('visited_items', [])
    if name not in visited_items:
        visited_items.append(name)
        session['visited_items'] = visited_items
        session.modified = True  # Mark session as modified
    
    # Calculate total items
    total_items = len(basics) + len(tools) + len(defense)
    
    return render_template('learn.html', 
                         item=selected, 
                         category=category,
                         craftable_items=craftable_items,
                         visited_count=len(visited_items),
                         total_items=total_items,
                         visited_items=visited_items,
                         item_images=item_images,
                         ingredient_images=ingredient_images)

@app.route('/getbasics', methods=['GET'])
def get_basics():
    return jsonify({"basics": basics})

@app.route('/gettools', methods=['GET'])
def get_tools():
    return jsonify({"tools": tools})

@app.route('/getdefense', methods=['GET'])
def get_defense():
    return jsonify({"defense": defense})

@app.route('/category/<string:category>')
def show_category(category):
    items = []
    category_name = ""
    
    if category == 'basics':
        items = basics
        category_name = 'Basic'
    elif category == 'tools':
        items = tools
        category_name = 'Tool'
    elif category == 'defense':
        items = defense
        category_name = 'Defense'
    else:
        return "Category not found", 404
    
    visited_items = session.get('visited_items', [])
    category_visited_count = sum(1 for item in items if item["name"] in visited_items)
    category_total = len(items)
    
    return render_template('category.html', 
                         category_name=category_name,
                         items=items,
                         visited_items=visited_items,
                         category_visited_count=category_visited_count,
                         category_total=category_total)

@app.route('/getprogress')
def get_progress():
    total_items = len(basics) + len(tools) + len(defense)
    visited_count = len(session.get('visited_items', []))
    return jsonify({
        'visited': visited_count,
        'total': total_items,
        'completed': visited_count >= total_items
    })

@app.route('/quiz')
def start_quiz():
    total_items = len(basics) + len(tools) + len(defense)
    visited_count = len(session.get('visited_items', []))

    all_items = basics + tools + defense
    quiz_items = random.sample(all_items, 5)
    session['quiz_items'] = [item['name'] for item in quiz_items]
    session['quiz_index'] = 0
    session['quiz_answers'] = []
    session['quiz_state'] = 'question'

    # Prepare first question
    current_item = quiz_items[0]
    other_items = random.sample([item for item in all_items if item != current_item], 2)
    options = [current_item] + other_items
    random.shuffle(options)
    formatted_options = [{'name': item['name'], 'url': f"/quiz/check/{item['name']}"} for item in options]

    return render_template('quiz.html',
        description=current_item['desc'],
        options=formatted_options,
        show_popup=False,
        popup_message='',
        popup_type='',
        visited_items=session.get('visited_items', [])
    )

@app.route('/quiz/check/<string:answer>')
def check_answer(answer):
    all_items = basics + tools + defense
    quiz_items = session.get('quiz_items', [])
    quiz_index = session.get('quiz_index', 0)
    quiz_answers = session.get('quiz_answers', [])
    quiz_state = session.get('quiz_state', 'question')

    if not quiz_items or quiz_index >= len(quiz_items):
        return redirect('/quiz')

    correct_item_name = quiz_items[quiz_index]
    correct = (answer == correct_item_name)

    if quiz_state == 'question':
        quiz_answers.append({
            'question': correct_item_name,
            'selected': answer,
            'correct': correct,
            'crafted': None
        })
        session['quiz_answers'] = quiz_answers

        if correct:
            session['quiz_state'] = 'crafting'
            return render_template('quiz.html',
                description=next(i for i in all_items if i['name'] == correct_item_name)['desc'],
                options=[{'name': answer, 'url': '#'}],
                show_popup=True,
                popup_message='Correct!',
                popup_type='success',
                next_url=f"/quiz/craft/{correct_item_name}",
                visited_items=session.get('visited_items', [])
            )
        else:
            session['quiz_index'] = quiz_index + 1
            session['quiz_state'] = 'question'
            if session['quiz_index'] >= 5:
                return redirect('/quiz/results')
            next_item = next(i for i in all_items if i['name'] == quiz_items[session['quiz_index']])
            other_items = random.sample([item for item in all_items if item != next_item], 2)
            options = [next_item] + other_items
            random.shuffle(options)
            formatted_options = [{'name': item['name'], 'url': f"/quiz/check/{item['name']}"} for item in options]
            return render_template('quiz.html',
                description=next_item['desc'],
                options=formatted_options,
                show_popup=True,
                popup_message='Incorrect!',
                popup_type='error',
                next_url='/quiz/next',
                visited_items=session.get('visited_items', [])
            )

@app.route('/quiz/next')
def quiz_next():
    all_items = basics + tools + defense
    quiz_items = session.get('quiz_items', [])
    quiz_index = session.get('quiz_index', 0)
    if not quiz_items or quiz_index >= len(quiz_items):
        return redirect('/quiz')
    next_item = next(i for i in all_items if i['name'] == quiz_items[quiz_index])
    other_items = random.sample([item for item in all_items if item != next_item], 2)
    options = [next_item] + other_items
    random.shuffle(options)
    formatted_options = [{'name': item['name'], 'url': f"/quiz/check/{item['name']}"} for item in options]
    return render_template('quiz.html',
        description=next_item['desc'],
        options=formatted_options,
        show_popup=False,
        popup_message='',
        popup_type='',
        visited_items=session.get('visited_items', [])
    )

@app.route('/quiz/craft/<string:item_name>')
def quiz_craft(item_name):
    all_items = basics + tools + defense
    item = next((i for i in all_items if i['name'] == item_name), None)
    if not item:
        return redirect('/quiz')
    # Gather all possible unique ingredients
    all_ingredients = set()
    for i in all_items:
        all_ingredients.update(i['madeof'])
    required_ingredients = set(item['madeof'])
    distractors = list(all_ingredients - required_ingredients)
    extra_ingredients = random.sample(distractors, min(5, len(distractors)))
    ingredient_objs = [{'name': ing, 'img': get_ingredient_img(ing)} for ing in required_ingredients] + \
                      [{'name': ing, 'img': get_ingredient_img(ing)} for ing in extra_ingredients]
    random.shuffle(ingredient_objs)
    return render_template('crafting.html',
        item_name=item['name'],
        ingredients=ingredient_objs,
        show_popup=False,
        popup_message='',
        popup_type='',
        next_url='/quiz/next_craft',
        visited_items=session.get('visited_items', [])
    )

@app.route('/quiz/submit_craft', methods=['POST'])
def quiz_submit_craft():
    data = request.get_json()
    item_name = data.get('item_name')
    recipe = data.get('recipe', [])
    all_items = basics + tools + defense
    target_item = next((i for i in all_items if i['name'] == item_name), None)
    quiz_answers = session.get('quiz_answers', [])
    quiz_index = session.get('quiz_index', 0)

    if not target_item or not quiz_answers or quiz_index > len(quiz_answers):
        return jsonify({'redirect': '/quiz', 'popup_message': 'Error!', 'popup_type': 'error'})

    recipe_grid = [recipe[i:i+3] for i in range(0, 9, 3)]
    correct_recipe = target_item['recipe']
    if is_shapeless(correct_recipe):
        is_correct = match_shapeless(recipe_grid, correct_recipe)
    else:
        is_correct = match_shaped(recipe_grid, correct_recipe, item_name)

    quiz_answers[quiz_index-1]['crafted'] = is_correct
    quiz_answers[quiz_index-1]['fully_correct'] = quiz_answers[quiz_index-1]['correct'] and is_correct
    session['quiz_answers'] = quiz_answers

    if is_correct:
        popup_message = 'Correct recipe!'
        popup_type = 'success'
    else:
        popup_message = 'Incorrect recipe.'
        popup_type = 'error'

    session['quiz_index'] = quiz_index + 1
    session['quiz_state'] = 'question'

    if session['quiz_index'] >= 5:
        redirect_url = '/quiz/results'
    else:
        redirect_url = '/quiz/next'

    return jsonify({'redirect': redirect_url, 'popup_message': popup_message, 'popup_type': popup_type})

@app.route('/quiz/results')
def quiz_results():
    all_items = basics + tools + defense
    quiz_answers = session.get('quiz_answers', [])
    results = []
    for ans in quiz_answers:
        item = next((i for i in all_items if i['name'] == ans['question']), None)
        results.append({
            'name': ans['question'],
            'img': get_item_img(ans['question']),
            'correct': ans['correct'],
            'crafted': ans.get('crafted', None),
            'fully_correct': ans.get('fully_correct', False),
            'selected': ans['selected']
        })
    
    score = sum(1 for a in quiz_answers if a.get('fully_correct'))
    top_scores = save_score(score)
    
    # Clear quiz session data
    session.pop('quiz_items', None)
    session.pop('quiz_index', None)
    session.pop('quiz_answers', None)
    session.pop('quiz_state', None)
    
    return render_template('quiz_results.html',
        results=results,
        score=score,
        top_scores=top_scores,
        visited_items=session.get('visited_items', [])
    )

@app.route('/quiz/next_craft')
def quiz_next_craft():
    quiz_items = session.get('quiz_items', [])
    quiz_index = session.get('quiz_index', 0)
    quiz_answers = session.get('quiz_answers', [])
    # Mark the current crafting as skipped (crafted: False, fully_correct: False)
    if quiz_index > 0 and len(quiz_answers) >= quiz_index:
        quiz_answers[quiz_index-1]['crafted'] = False
        quiz_answers[quiz_index-1]['fully_correct'] = False
        session['quiz_answers'] = quiz_answers
    session['quiz_index'] = quiz_index + 1
    session['quiz_state'] = 'question'
    if session['quiz_index'] >= 5:
        return redirect('/quiz/results')
    else:
        return redirect('/quiz/next')

def is_shapeless(recipe_grid):
    # Heuristic: if all non-empty ingredients are the same and contiguous, treat as shaped; else, shapeless
    # For now, treat as shapeless if only one row or column is filled, or if all non-empty slots are not contiguous
    non_empty = [cell for row in recipe_grid for cell in row if cell]
    return len(non_empty) > 0 and (len(set(tuple(cell.items()) if isinstance(cell, dict) else cell for cell in non_empty)) > 1 or len(non_empty) < 3)

def normalize_ingredient(cell):
    if isinstance(cell, dict) and 'ingredient' in cell:
        return cell['ingredient']
    return cell if cell else ''

def match_shapeless(user_grid, correct_grid):
    user_ings = sorted([normalize_ingredient(cell) for row in user_grid for cell in row if normalize_ingredient(cell)])
    correct_ings = sorted([normalize_ingredient(cell) for row in correct_grid for cell in row if normalize_ingredient(cell)])
    return user_ings == correct_ings

def match_shaped(user_grid, correct_grid, item_name):
    # Find the bounding box of the correct recipe
    min_row, max_row, min_col, max_col = 2, 0, 2, 0
    for i in range(3):
        for j in range(3):
            if correct_grid[i][j]:
                min_row = min(min_row, i)
                max_row = max(max_row, i)
                min_col = min(min_col, j)
                max_col = max(max_col, j)
    shape_h = max_row - min_row + 1
    shape_w = max_col - min_col + 1
    # Extract the shape
    shape = [[correct_grid[i][j] for j in range(min_col, max_col+1)] for i in range(min_row, max_row+1)]
    valid_materials = get_valid_materials(item_name)
    # Try all possible positions in user_grid
    for row_off in range(3-shape_h+1):
        for col_off in range(3-shape_w+1):
            match = True
            for i in range(shape_h):
                for j in range(shape_w):
                    correct_cell = shape[i][j]
                    user_cell = user_grid[row_off+i][col_off+j]
                    if correct_cell:
                        correct_ing = correct_cell.get("ingredient") if isinstance(correct_cell, dict) else correct_cell
                        user_ing = user_cell if isinstance(user_cell, str) else (user_cell.get("ingredient") if isinstance(user_cell, dict) else user_cell)
                        # If this is a tool/armor, allow any valid material
                        if valid_materials and correct_ing in valid_materials:
                            if user_ing not in valid_materials:
                                match = False
                                break
                        else:
                            if normalize_ingredient(user_cell) != normalize_ingredient(correct_cell):
                                match = False
                                break
                    else:
                        if user_cell:
                            match = False
                            break
                if not match:
                    break
            # Check that all other cells are empty
            if match:
                for i in range(3):
                    for j in range(3):
                        if not (row_off <= i < row_off+shape_h and col_off <= j < col_off+shape_w):
                            if user_grid[i][j]:
                                match = False
                if match:
                    return True
    return False

@app.route('/reset_session')
def reset_session():
    session.clear()
    return redirect('/')

@app.route('/api/top-scores')
def get_top_scores():
    return jsonify(load_scores())

if __name__ == '__main__':
   app.run(debug = True, port=5001)
