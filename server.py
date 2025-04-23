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
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Basic building material. Varies by biome (Oak, Spruce, Birch, Jungle, Acacia, Dark Oak).",
        "madeof": ["Log"],
        "makes": ["Stick", "Crafting Table", "Chest"],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Stick",
        "prev": ""
        "recipe": [
            ["", "", ""],
            ["", "Log", ""],
            ["", "", ""]
        ]
   },
    {
        "name": "Stick",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Used to craft many other items.",
        "madeof": ["Wooden Plank"],
        "makes": ["Torch", "Fence", "Sword", "Ladder", "Sign"],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Torch",
        "prev": "Wooden Plank"
        "recipe": [
            ["", "", ""],
            ["", "Wooden Plank", ""],
            ["", "Wooden Plank", ""]
        ]
   },
    {
        "name": "Torch",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Provides light and melts ice/snow.",
        "madeof": ["Stick", "Coal"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Crafting Table",
        "prev": "Stick"
        "recipe": [
            ["", "", ""],
            ["", "Coal", ""],
            ["", "Stick", ""]
        ]
    },
    {
        "name": "Crafting Table",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Allows player to craft when right clicked.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Furnace",
        "prev": "Torch"
        "recipe": [
            ["", "", ""],
            ["Wooden Plank", "Wooden Plank", ""],
            ["Wooden Plank", "Wooden Plank", ""]
        ]
    },
    {
        "name": "Furnace",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Allows player to smelt (refine ores, cook food, etc.) when right clicked).",
        "madeof": ["Cobblestone"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Chest",
        "prev": "Crafting Table"
        "recipe": [
            ["Cobblestone", "Cobblestone", "Cobblestone"],
            ["Cobblestone", "", "Cobblestone"],
            ["Cobblestone", "Cobblestone", "Cobblestone"]
        ]
    },
    {
        "name": "Chest",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Used to store items.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Ladder",
        "prev": "Furnace"
        "recipe": [
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"],
            ["Wooden Plank", "", "Wooden Plank"],
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"]
        ]
   },
   {
        "name": "Ladder",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Allows player to climb vertically.",
        "madeof": ["Stick"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Fence",
        "prev": "Furnace"
        "recipe": [
            ["Stick", "", "Stick"],
            ["Stick", "Stick", "Stick"],
            ["Stick", "", "Stick"]
        ]
   },
   {
        "name": "Fence",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Barrier that can't be jumped over.",
        "madeof": ["Wooden Plank", "Stick"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Boat",
        "prev": "Ladder"
        "recipe": [
            ["", "", ""],
            ["Wooden Plank", "Stick", "Wooden Plank"],
            ["Wooden Plank", "Stick", "Wooden Plank"]
        ]
   },
   {
        "name": "Boat",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Used to travel over water.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Slab",
        "prev": "Fence"
        "recipe": [
            ["", "", ""],
            ["Wooden Plank", "", "Wooden Plank"],
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"]
        ]
   },
   {
        "name": "Slab",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Used to create gradual slopes.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Stairs",
        "prev": "Boat"
        "recipe": [
            ["", "", ""],
            ["", "", ""],
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"]
        ]
   },
   {
        "name": "Stairs",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Used to build staircases.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Door",
        "prev": "Slab"
        "recipe": [
            ["", "", "Wooden Plank"],
            ["", "Wooden Plank", "Wooden Plank"],
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"]
        ]
   },
   {
        "name": "Door",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Wooden doors can be opened by clicking or redstone power, Iron doors can only be opened by redstone power.",
        "madeof": ["Wooden Plank", "Iron Ingot"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Sign",
        "prev": "Stairs"
        "recipe": [
            ["Wooden Plank", "Wooden Plank", ""],
            ["Wooden Plank", "Wooden Plank", ""],
            ["Wooden Plank", "Wooden Plank", ""]
        ]
   },
   {
        "name": "Sign",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Can display text.",
        "madeof": ["Wooden Plank", "Stick"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Bed",
        "prev": "Door"
        "recipe": [
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"],
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"],
            ["", "Stick", ""]
        ]
   },
   {
        "name": "Bed",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Used to forward from night to day.",
        "madeof": ["Wooden plank", "Wool"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "",
        "prev": "Sign"
        "recipe": [
            ["", "", ""],
            ["Wool", "Wool", "Wool"],
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"]
        ]
   }
]

tools = [
    {
        "name": "Pickaxe",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Used to mine stone blocks and ores.",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Axe",
        "prev": ""
        "recipe": [
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"],
            ["", "Stick", ""],
            ["", "Stick", ""]
        ]
   },
   {
        "name": "Axe",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Used to chop wood blocks faster.",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Torch",
        "prev": "Wooden Plank"
        "recipe": [
            ["Wooden Plank", "Wooden Plank", ""],
            ["Wooden Plank", "Stick", ""],
            ["", "Stick", ""]
        ]
   },
   {
        "name": "Shovel",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Used to dig sand, gravel, dirt, grass, and snow faster.",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingots", "Gold Ingots", "Diamonds"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Hoe",
        "prev": "Axe"
        "recipe": [
            ["", "Wooden Plank", ""],
            ["", "Stick", ""],
            ["", "Stick", ""]
        ]
   },
   {
        "name": "Hoe",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Used to till dirt blocks in preparation for growing crops.",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingots", "Gold Ingots", "Diamonds"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Fishing Rod",
        "prev": "Shovel"
        "recipe": [
            ["Wooden Plank", "Wooden Plank", ""],
            ["", "Stick", ""],
            ["", "Stick", ""]
        ]
   },
   {
        "name": "Fishing Rod",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Can be cast into water to catch fish.",
        "madeof": ["Stick", "String"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Flint & Steel",
        "prev": "Hoe"
        "recipe": [
            ["", "", "Stick"],
            ["", "Stick", "String"],
            ["Stick", "", "String"]
        ]
   },
   {
        "name": "Flint & Steel",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Used to light fires, ignite TNT and open nether portals.",
        "madeof": ["Iron Ingot", "Flint"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Compass",
        "prev": "Fishing Rod"
        "recipe": [
            ["", "", ""],
            ["Iron", "", ""],
            ["", "Coal", ""]
        ]
   },
   {
        "name": "Compass",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Points to the spawn point.",
        "madeof": ["Iron Ingot", "Redstone"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Bucket",
        "prev": "Flint & Steel"
        "recipe": [
            ["", "Iron", ""],
            ["Iron", "Redstone", "Iron"],
            ["", "Iron", ""]
        ]
   },
   {
        "name": "Bucket",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Used to transport water, lava, and milk.",
        "madeof": ["Iron Ingot"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Shears",
        "prev": "Compass"
        "recipe": [
            ["", "", ""],
            ["Iron", "", "Iron"],
            ["", "Iron", ""]
        ]
   },
   {
        "name": "Shears",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Used to collect wool from sheep and leaves from trees.",
        "madeof": ["Iron Ingot"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "",
        "prev": "Bucket"
        "recipe": [
            ["", "", ""],
            ["", "Iron", ""],
            ["Iron", "", ""]
        ]
   }
]

defense = [
    {
        "name": "Helmet",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Head armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Chestplate",
        "prev": ""
        "recipe": [
            ["Leather", "Leather", "Leather"],
            ["Leather", "", "Leather"],
            ["", "", ""]
        ]
   },
   {
        "name": "Chestplate",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Chest armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Leggings",
        "prev": "Helmet"
        "recipe": [
            ["Leather", "", "Leather"],
            ["Leather", "Leather", "Leather"],
            ["Leather", "Leather", "Leather"]
        ]
   },
   {
        "name": "Leggings",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Leg armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Boots",
        "prev": "Chestplate"
        "recipe": [
            ["Leather", "Leather", "Leather"],
            ["Leather", "", "Leather"],
            ["Leather", "", "Leather"]
        ]
   },
   {
        "name": "Boots",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Foot armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Sword",
        "prev": "Leggings"
        "recipe": [
            ["", "", ""],
            ["Leather", "", "Leather"],
            ["Leather", "", "Leather"]
        ]
   },
   {
        "name": "Sword",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Deal damage to mobs and other players.",
        "madeof": ["Stick", "Wooden Planks", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Bow",
        "prev": "Boots"
        "recipe": [
            ["", "Wooden Plank", ""],
            ["", "Wooden Plank", ""],
            ["", "Stick", ""]
        ]
   },
   {
        "name": "Bow",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Used to shoot arrows that deal damage to mobs and other players.",
        "madeof": ["Stick", "String"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Arrow",
        "prev": "Sword"
        "recipe": [
            ["String", "Stick", ""],
            ["String", "", "Stick"],
            ["String", "Stick", ""]
        ]
   },
   {
        "name": "Arrow",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Ammunition for bows.",
        "madeof": ["Stick", "Flint", "Feather"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Shield",
        "prev": "Bow"
        "recipe": [
            ["", "Coal", ""],
            ["", "Stick", ""],
            ["", "Feather", ""]
        ]
   },
   {
        "name": "Shield",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Protects player against attack.",
        "madeof": ["Wooden Plank", "Iron"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "Scute",
        "prev": "Arrow"
        "recipe": [
            ["Wooden Plank", "Iron", "Wooden Plank"],
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"],
            ["", "Wooden Plank", ""]
        ]
   },
   {
        "name": "Scute",
        "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "desc": "Helmet that gives the player water breathing effect.",
        "madeof": ["Turtle Shell"],
        "makes": [],
        "recipeimg": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTP4xlp7Az9BofS3TO91z_EaeLvHusgeBqt_A&s",
        "next": "",
        "prev": "Shield"
        "recipe": [
            ["Turtle Shell", "Turtle Shell", "Turtle Shell"],
            ["Turtle Shell", "", "Turtle Shell"],
            ["", "", ""]
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

if __name__ == '__main__':
   app.run(debug = True, port=5001)
