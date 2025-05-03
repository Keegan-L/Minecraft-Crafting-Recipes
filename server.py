from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from flask import send_from_directory
from flask import session
import os
import random

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

basics = [
    {
        "name": "Wooden Plank",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640",
        "desc": "Basic building material. Appearance varies by biome depending on type of wood (Oak, Spruce, Birch, Jungle, Acacia, Dark Oak).",
        "madeof": ["Log"],
        "makes": ["Stick", "Crafting Table", "Chest"],
        "next": "Stick",
        "prev": "",
        "recipe": [
            [{}, {}, {}],
            [{}, {"ingredient": "Log", "pic": "https://minecraft.wiki/images/Oak_Log_%28UD%29_JE5_BE3.png?8a080"}, {}],
            [{}, {}, {}]
        ]
   },
    {
        "name": "Stick",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441",
        "desc": "Used to craft many other items.",
        "madeof": ["Wooden Plank"],
        "makes": ["Torch", "Fence", "Sword", "Ladder", "Sign"],
        "next": "Torch",
        "prev": "Wooden Plank",
        "recipe": [
            [{}, {}, {}],
            [{}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {}],
            [{}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {}]
        ]
   },
    {
        "name": "Torch",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/90/Torch.gif/revision/latest?cb=20200111190834",
        "desc": "Provides light and melts ice/snow.",
        "madeof": ["Stick", "Coal"],
        "makes": [],
        "next": "Crafting Table",
        "prev": "Stick",
        "recipe": [
            [{}, {}, {}],
            [{}, {"ingredient": "Coal", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/5/58/Coal_JE4_BE3.png/revision/latest/thumbnail/width/360/height/360?cb=20230625214010"}, {}],
            [{}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}]
        ]
    },
    {
        "name": "Crafting Table",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/93/Crafting_Table_JE3_BE2.png/revision/latest?cb=20190606093431",
        "desc": "Allows player to craft when right clicked.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "next": "Furnace",
        "prev": "Torch",
        "recipe": [
            [{}, {}, {}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {}]
        ]
    },
    {
        "name": "Furnace",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/99/Furnace_%28S%29_JE4.png/revision/latest/scale-to-width/360?cb=20210111063232",
        "desc": "Allows player to smelt (refine ores, cook food, etc.) when right clicked). Can be made with Cobblestone or Blackstone",
        "madeof": ["Cobblestone"],
        "makes": [],
        "next": "Chest",
        "prev": "Crafting Table",
        "recipe": [
            [{"ingredient": "Cobblestone", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/6/67/Cobblestone_JE5_BE3.png/revision/latest?cb=20200825032214"}, {"ingredient": "Cobblestone", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/6/67/Cobblestone_JE5_BE3.png/revision/latest?cb=20200825032214"}, {"ingredient": "Cobblestone", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/6/67/Cobblestone_JE5_BE3.png/revision/latest?cb=20200825032214"}],
            [{"ingredient": "Cobblestone", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/6/67/Cobblestone_JE5_BE3.png/revision/latest?cb=20200825032214"}, {}, {"ingredient": "Cobblestone", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/6/67/Cobblestone_JE5_BE3.png/revision/latest?cb=20200825032214"}],
            [{"ingredient": "Cobblestone", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/6/67/Cobblestone_JE5_BE3.png/revision/latest?cb=20200825032214"}, {"ingredient": "Cobblestone", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/6/67/Cobblestone_JE5_BE3.png/revision/latest?cb=20200825032214"}, {"ingredient": "Cobblestone", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/6/67/Cobblestone_JE5_BE3.png/revision/latest?cb=20200825032214"}]
        ]
    },
    {
        "name": "Chest",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/3d/Chest_%28S%29_JE1.png/revision/latest?cb=20200128020353",
        "desc": "Used to store items.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "next": "Ladder",
        "prev": "Furnace",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}]
        ]
   },
   {
        "name": "Ladder",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/af/Ladder_%28texture%29_JE3_BE2.png/revision/latest?cb=20200922000708",
        "desc": "Allows player to climb vertically.",
        "madeof": ["Stick"],
        "makes": [],
        "next": "Fence",
        "prev": "Furnace",
        "recipe": [
            [{"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}],
            [{"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}],
            [{"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}]
        ]
   },
   {
        "name": "Fence",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/f6/Oak_Fence_JE4_BE2.png/revision/latest?cb=20200317191546",
        "desc": "Barrier that can't be jumped over.",
        "madeof": ["Wooden Plank", "Stick"],
        "makes": [],
        "next": "Boat",
        "prev": "Ladder",
        "recipe": [
            [{}, {}, {}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}]
        ]
   },
   {
        "name": "Boat",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/5/58/Oak_Boat_%28item%29_JE4_BE3.png/revision/latest?cb=20200518190533",
        "desc": "Used to travel over water.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "next": "Slab",
        "prev": "Fence",
        "recipe": [
            [{}, {}, {}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}]
        ]
   },
   {
        "name": "Slab",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/ac/Oak_Slab_JE5_BE2.png/revision/latest/scale-to-width/360?cb=20240729071106",
        "desc": "Used to create gradual slopes. Can be made of many different building materials (Wooden Plank, Cobblestone, Brick, Quartz, etc.).",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "next": "Stairs",
        "prev": "Boat",
        "recipe": [
            [{}, {}, {}],
            [{}, {}, {}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}]
        ]
   },
   {
        "name": "Stairs",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/a0/Oak_Stairs_%28N%29_JE7_BE6.png/revision/latest?cb=20200317191626",
        "desc": "Used to build staircases.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "next": "Door",
        "prev": "Slab",
        "recipe": [
            [{}, {}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}],
            [{}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}]
        ]
   },
   {
        "name": "Door",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/2/2a/Oak_Door_%28item%29_JE4_BE3.png/revision/latest?cb=20230319211346",
        "desc": "Wooden doors can be opened by clicking or redstone power, Iron doors can only be opened by redstone power.",
        "madeof": ["Wooden Plank", "Iron Ingot"],
        "makes": [],
        "next": "Sign",
        "prev": "Stairs",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {}]
        ]
   },
   {
        "name": "Sign",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/8/82/Oak_Sign_JE3.png/revision/latest/scale-to-width/360?cb=20211013161856",
        "desc": "Can display text.",
        "madeof": ["Wooden Plank", "Stick"],
        "makes": [],
        "next": "Bed",
        "prev": "Door",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}],
            [{}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}]
        ]
   },
   {
        "name": "Bed",
        "img": "https://static.wikia.nocookie.net/minecraft/images/c/c5/Bed.png/revision/latest?cb=20191103220226",
        "desc": "Used to forward from night to day.",
        "madeof": ["Wooden plank", "Wool"],
        "makes": [],
        "next": "",
        "prev": "Sign",
        "recipe": [
            [{}, {}, {}],
            [{"ingredient": "Wool", "pic": "https://minecraft.wiki/images/White_Wool_JE2_BE2.png?2bcdc"}, {"ingredient": "Wool", "pic": "https://minecraft.wiki/images/White_Wool_JE2_BE2.png?2bcdc"}, {"ingredient": "Wool", "pic": "https://minecraft.wiki/images/White_Wool_JE2_BE2.png?2bcdc"}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}]
        ]
   }
]

tools = [
    {
        "name": "Pickaxe",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/0/0b/Wooden_Pickaxe_JE2_BE2.png/revision/latest?cb=20200217231203",
        "desc": "Used to mine stone blocks and ores. Durability and Damage varies depending on type of Pickaxe (Wooden, Stone, Iron, Gold, Diamond).",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "next": "Axe",
        "prev": "",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}],
            [{}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}],
            [{}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}]
        ]
   },
   {
        "name": "Axe",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/5/56/Wooden_Axe_JE2_BE2.png/revision/latest/scale-to-width/360?cb=20200217234355",
        "desc": "Used to chop wood blocks faster. Durability and Damage varies depending on type of Axe (Wooden, Stone, Iron, Gold, Diamond).",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "next": "Torch",
        "prev": "Wooden Plank",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, "Stick", {}],
            [{}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}]
        ]
   },
   {
        "name": "Shovel",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/2/26/Wooden_Shovel_JE2_BE2.png/revision/latest/scale-to-width/360?cb=20200217234949",
        "desc": "Used to dig sand, gravel, dirt, grass, and snow faster. Durability and Damage varies depending on type of Shovel (Wooden, Stone, Iron, Gold, Diamond).",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingots", "Gold Ingots", "Diamonds"],
        "makes": [],
        "next": "Hoe",
        "prev": "Axe",
        "recipe": [
            [{}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {}],
            [{}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}],
            [{}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}]
        ]
   },
   {
        "name": "Hoe",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/cd/Wooden_Hoe_JE3_BE3.png/revision/latest/scale-to-width/360?cb=20200226194121",
        "desc": "Used to till dirt blocks in preparation for growing crops. Durability and Damage varies depending on type of Hoe (Wooden, Stone, Iron, Gold, Diamond).",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingots", "Gold Ingots", "Diamonds"],
        "makes": [],
        "next": "Fishing Rod",
        "prev": "Shovel",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {}],
            [{}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}],
            [{}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}]
        ]
   },
   {
        "name": "Fishing Rod",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7f/Fishing_Rod_JE2_BE2.png/revision/latest/thumbnail/width/360/height/360?cb=20200201063839",
        "desc": "Can be cast into water to catch fish.",
        "madeof": ["Stick", "String"],
        "makes": [],
        "next": "Flint & Steel",
        "prev": "Hoe",
        "recipe": [
            [{}, {}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}],
            [{}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {"ingredient": "String", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c0/String_JE1_BE1.png/revision/latest?cb=20200128023538"}],
            [{"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}, {"ingredient": "String", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c0/String_JE1_BE1.png/revision/latest?cb=20200128023538"}]
        ]
   },
   {
        "name": "Flint & Steel",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fd/Flint_and_Steel_JE2.png/revision/latest?cb=20200128083122",
        "desc": "Used to light fires, ignite TNT and open nether portals.",
        "madeof": ["Iron Ingot", "Flint"],
        "makes": [],
        "next": "Compass",
        "prev": "Fishing Rod",
        "recipe": [
            [{}, {}, {}],
            [{"ingredient": "Iron Ingot", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Iron_Ingot_JE3_BE2.png/revision/latest?cb=20230613175240"}, {}, {}],
            [{}, {"ingredient": "Coal", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/5/58/Coal_JE4_BE3.png/revision/latest/thumbnail/width/360/height/360?cb=20230625214010"}, {}]
        ]
   },
   {
        "name": "Compass",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b3/Compass_JE3_BE3.gif/revision/latest/thumbnail/width/360/height/360?cb=20201125191224",
        "desc": "Points to the spawn point.",
        "madeof": ["Iron Ingot", "Redstone"],
        "makes": [],
        "next": "Bucket",
        "prev": "Flint & Steel",
        "recipe": [
            [{}, {"ingredient": "Iron Ingot", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Iron_Ingot_JE3_BE2.png/revision/latest?cb=20230613175240"}, {}],
            [{"ingredient": "Iron Ingot", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Iron_Ingot_JE3_BE2.png/revision/latest?cb=20230613175240"}, {"ingredient": "Redstone", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/e/e1/Redstone_Dust_JE2_BE2.png/revision/latest?cb=20210427032319"}, {"ingredient": "Iron Ingot", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Iron_Ingot_JE3_BE2.png/revision/latest?cb=20230613175240"}],
            [{}, {"ingredient": "Iron Ingot", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Iron_Ingot_JE3_BE2.png/revision/latest?cb=20230613175240"}, {}]
        ]
   },
   {
        "name": "Bucket",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Bucket_JE2_BE2.png/revision/latest/thumbnail/width/360/height/360?cb=20200510234539",
        "desc": "Used to transport water, lava, and milk.",
        "madeof": ["Iron Ingot"],
        "makes": [],
        "next": "Shears",
        "prev": "Compass",
        "recipe": [
            [{}, {}, {}],
            [{"ingredient": "Iron Ingot", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Iron_Ingot_JE3_BE2.png/revision/latest?cb=20230613175240"}, {}, {"ingredient": "Iron Ingot", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Iron_Ingot_JE3_BE2.png/revision/latest?cb=20230613175240"}],
            [{}, {"ingredient": "Iron Ingot", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Iron_Ingot_JE3_BE2.png/revision/latest?cb=20230613175240"}, {}]
        ]
   },
   {
        "name": "Shears",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/5/5a/Shears_JE2_BE2.png/revision/latest/thumbnail/width/360/height/360?cb=20191012183756",
        "desc": "Used to collect wool from sheep and leaves from trees.",
        "madeof": ["Iron Ingot"],
        "makes": [],
        "next": "",
        "prev": "Bucket",
        "recipe": [
            [{}, {}, {}],
            [{}, {"ingredient": "Iron Ingot", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Iron_Ingot_JE3_BE2.png/revision/latest?cb=20230613175240"}, {}],
            [{"ingredient": "Iron Ingot", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Iron_Ingot_JE3_BE2.png/revision/latest?cb=20230613175240"}, {}, {}]
        ]
   }
]

defense = [
    {
        "name": "Helmet",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c5/Leather_Cap_%28item%29_JE4_BE3.png/revision/latest?cb=20190910050904",
        "desc": "Head armor. Durability varies depending on type of helmet (Wooden, Stone, Iron, Gold, Diamond, Turtle Shell). Turtle shell helmet gives the player water breathing effect.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond", "Scute"],
        "makes": [],
        "next": "Chestplate",
        "prev": "",
        "recipe": [
            [{"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}, {"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}, {"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}],
            [{"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}, {}, {"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}],
            [{}, {}, {}]
        ]
   },
   {
        "name": "Chestplate",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/71/Leather_Tunic_%28item%29_JE4_BE3.png/revision/latest?cb=20190910050828",
        "desc": "Chest armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "next": "Leggings",
        "prev": "Helmet",
        "recipe": [
            [{"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}, {}, {"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}],
            [{"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}, {"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}, {"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}],
            [{"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}, {"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}, {"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}]
        ]
   },
   {
        "name": "Leggings",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/2/2f/Leather_Pants_%28item%29_JE3_BE2.png/revision/latest?cb=20201104115305",
        "desc": "Leg armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "next": "Boots",
        "prev": "Chestplate",
        "recipe": [
            [{"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}, {"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}, {"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}],
            [{"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}, {}, {"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}],
            [{"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}, {}, {"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}]
        ]
   },
   {
        "name": "Boots",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b5/Leather_Boots_%28item%29_JE4_BE3.png/revision/latest?cb=20190910050749",
        "desc": "Foot armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "next": "Sword",
        "prev": "Leggings",
        "recipe": [
            [{}, {}, {}],
            [{"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}, {}, {"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}],
            [{"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}, {}, {"ingredient": "Leather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c2/Leather_JE1_BE1.png/revision/latest?cb=20200130100649"}]
        ]
   },
   {
        "name": "Sword",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d5/Wooden_Sword_JE2_BE2.png/revision/latest/scale-to-width/360?cb=20200217235747",
        "desc": "Deal damage to mobs and other players. Durability and Damage varies depending on type of Sword (Wooden, Stone, Iron, Gold, Diamond).",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "next": "Bow",
        "prev": "Boots",
        "recipe": [
            [{}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {}],
            [{}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {}],
            [{}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}]
        ]
   },
   {
        "name": "Bow",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/99/Bow_JE2_BE1.png/revision/latest/scale-to-width/360?cb=20200128015144",
        "desc": "Used to shoot arrows that deal damage to mobs and other players.",
        "madeof": ["Stick", "String"],
        "makes": [],
        "next": "Arrow",
        "prev": "Sword",
        "recipe": [
            [{"ingredient": "String", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c0/String_JE1_BE1.png/revision/latest?cb=20200128023538"}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}],
            [{"ingredient": "String", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c0/String_JE1_BE1.png/revision/latest?cb=20200128023538"}, {}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}],
            [{"ingredient": "String", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c0/String_JE1_BE1.png/revision/latest?cb=20200128023538"}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}]
        ]
   },
   {
        "name": "Arrow",
        "img": "https://static.wikia.nocookie.net/minecraft/images/4/41/Arrow.png/revision/latest/thumbnail/width/360/height/360?cb=20200118044944",
        "desc": "Ammunition for bows.",
        "madeof": ["Stick", "Flint", "Feather"],
        "makes": [],
        "next": "Shield",
        "prev": "Bow",
        "recipe": [
            [{}, {"ingredient": "Coal", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/5/58/Coal_JE4_BE3.png/revision/latest/thumbnail/width/360/height/360?cb=20230625214010"}, {}],
            [{}, {"ingredient": "Stick", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441"}, {}],
            [{}, {"ingredient": "Feather", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/e/e2/Feather_JE3_BE2.png/revision/latest/thumbnail/width/360/height/360?cb=20190430052113"}, {}]
        ]
   },
   {
        "name": "Shield",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c6/Shield_JE2_BE1.png/revision/latest?cb=20190725172341",
        "desc": "Protects player against attack.",
        "madeof": ["Wooden Plank", "Iron"],
        "makes": [],
        "next": "",
        "prev": "Arrow",
        "recipe": [
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Iron Ingot", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Iron_Ingot_JE3_BE2.png/revision/latest?cb=20230613175240"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}],
            [{"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}],
            [{}, {"ingredient": "Wooden Plank", "pic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/37/Oak_Planks_JE6_BE3.png/revision/latest?cb=20200317041640"}, {}]
        ]
   }
]

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
    
    return render_template('learn.html', 
                         item=selected, 
                         category=category,
                         craftable_items=craftable_items)

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
    
    return render_template('category.html', 
                         category_name=category_name,
                         items=items,
                         visited_items=session.get('visited_items', []))

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
    # Check if all items have been visited
    total_items = len(basics) + len(tools) + len(defense)
    visited_count = len(session.get('visited_items', []))
    
    if visited_count < total_items:
        return "Please visit all items before taking the quiz", 403
    
    # Combine all items
    all_items = basics + tools + defense
    # Select a random item
    correct_item = random.choice(all_items)
    # Get two other random items
    other_items = random.sample([item for item in all_items if item != correct_item], 2)
    # Combine and shuffle options
    options = [correct_item] + other_items
    random.shuffle(options)
    
    # Format options for template
    formatted_options = []
    for item in options:
        formatted_options.append({
            'name': item['name'],
            'url': '/quiz/check/' + item['name']
        })
    
    return render_template('quiz.html',
                         description=correct_item['desc'],
                         options=formatted_options)

@app.route('/quiz/check/<string:answer>')
def check_answer(answer):
    # Find the item that matches this description
    all_items = basics + tools + defense
    for item in all_items:
        if item['name'] == answer:
            # This is the correct item
            # Get all possible ingredients
            all_ingredients = []
            for i in all_items:
                all_ingredients.extend(i['madeof'])
            all_ingredients = list(set(all_ingredients))  # Remove duplicates
            
            # Get the required ingredients
            required_ingredients = item['madeof']
            
            # Add some random ingredients
            extra_ingredients = random.sample(
                [i for i in all_ingredients if i not in required_ingredients],
                min(5, len(all_ingredients) - len(required_ingredients))
            )
            
            # Combine and shuffle
            ingredients = required_ingredients + extra_ingredients
            random.shuffle(ingredients)
            
            return render_template('crafting.html',
                                item_name=item['name'],
                                ingredients=ingredients)
    
    # If we get here, it was the wrong answer
    return render_template('wrong_answer.html')

@app.route('/verify_recipe', methods=['POST'])
def verify_recipe():
    data = request.get_json()
    item_name = data.get('item_name')
    recipe = data.get('recipe', [])
    
    # Find the item in our data
    all_items = basics + tools + defense
    target_item = None
    for item in all_items:
        if item['name'] == item_name:
            target_item = item
            break
    
    if not target_item:
        return jsonify({'correct': False, 'error': 'Item not found'})
    
    # Convert recipe to 3x3 grid
    recipe_grid = [recipe[i:i+3] for i in range(0, 9, 3)]
    
    # Get the correct recipe grid
    correct_recipe = target_item['recipe']
    
    # Compare the recipes
    is_correct = True
    for i in range(3):
        for j in range(3):
            if recipe_grid[i][j] != correct_recipe[i][j]:
                is_correct = False
                break
        if not is_correct:
            break
    
    return jsonify({'correct': is_correct})

if __name__ == '__main__':
   app.run(debug = True, port=5001)
