from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)

basics = [
    {
        "name": "Wooden Plank",
        "img": "",
        "desc": "Basic building material. Varies by biome (Oak, Spruce, Birch, Jungle, Acacia, Dark Oak).",
        "madeof": ["Log"],
        "makes": ["Stick", "Crafting Table", "Chest"],
        "recipeimg": "",
        "next": ["Stick"],
        "prev": []
   },
    {
        "name": "Stick",
        "img": "",
        "desc": "Used to craft many other items.",
        "madeof": ["Wooden Plank"],
        "makes": ["Torch", "Fence", "Sword", "Ladder", "Sign"],
        "recipeimg": "",
        "next": ["Torch"],
        "prev": ["Wooden Plank"]
   },
    {
        "name": "Torch"
        "img": "",
        "desc": "Provides light and melts ice/snow.",
        "madeof": ["Stick, Coal"],
        "makes": [],
        "recipeimg": "",
        "next": ["Crafting Table"],
        "prev": ["Stick"]
    },
    {
        "name": "Crafting Table"
        "img": "",
        "desc": "Allows player to craft when right clicked.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "recipeimg": "",
        "next": ["Furnace"],
        "prev": ["Torch"]
    },
    {
        "name": "Furnace"
        "img": "",
        "desc": "Allows player to smelt (refine ores, cook food, etc.) when right clicked).",
        "madeof": ["Cobblestone"],
        "makes": [],
        "recipeimg": "",
        "next": ["Chest"],
        "prev": ["Crafting Table"]
    },
    {
        "name": "Chest"
        "img": "",
        "desc": "Used to store items.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "recipeimg": "",
        "next": ["Ladder"],
        "prev": ["Furnace"]
   },
   {
        "name": "Ladder"
        "img": "",
        "desc": "Allows player to climb vertically.",
        "madeof": ["Stick"],
        "makes": [],
        "recipeimg": "",
        "next": ["Fence"],
        "prev": ["Furnace"]
   },
   {
        "name": "Fence"
        "img": "",
        "desc": "Barrier that can't be jumped over.",
        "madeof": ["Wooden Plank", "Stick"],
        "makes": [],
        "recipeimg": "",
        "next": ["Boat"],
        "prev": ["Ladder"]
   },
   {
        "name": "Boat"
        "img": "",
        "desc": "Used to travel over water.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "recipeimg": "",
        "next": ["Slab"],
        "prev": ["Fence"]
   },
   {
        "name": "Slab"
        "img": "",
        "desc": "Used to create gradual slopes.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "recipeimg": "",
        "next": ["Stairs"],
        "prev": ["Boat"]
   },
   {
        "name": "Stairs"
        "img": "",
        "desc": "Used to build staircases.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "recipeimg": "",
        "next": ["Door"],
        "prev": ["Slab"]
   },
   {
        "name": "Door"
        "img": "",
        "desc": "Wooden doors can be opened by clicking or redstone power, Iron doors can only be opened by redstone power.",
        "madeof": ["Wooden Plank", "Iron Ingot"],
        "makes": [],
        "recipeimg": "",
        "next": ["Sign"],
        "prev": ["Stairs"]
   },
   {
        "name": "Sign"
        "img": "",
        "desc": "Can display text.",
        "madeof": ["Wooden Plank", "Stick"],
        "makes": [],
        "recipeimg": "",
        "next": ["Bed"],
        "prev": ["Door"]
   },
   {
        "name": "Bed"
        "img": "",
        "desc": "Used to forward from night to day.",
        "madeof": ["Wooden plank", "Wool"],
        "makes": [],
        "recipeimg": "",
        "next": [],
        "prev": ["Sign"]
   }
]

tools = [
    {
        "name": "Pickaxe",
        "img": "",
        "desc": "Used to mine stone blocks and ores.",
        "madeof": ["Sticks", "Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "",
        "next": ["Axe"],
        "prev": []
   },
   {
        "name": "Axe",
        "img": "",
        "desc": "Used to chop wood blocks faster.",
        "madeof": ["Sticks", "Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "",
        "next": ["Torch"],
        "prev": ["Wooden Plank"]
   },
   {
        "name": "Shovel"
        "img": "",
        "desc": "Used to dig sand, gravel, dirt, grass, and snow faster.",
        "madeof": ["Sticks", "Wooden Plank", "Cobblestone", "Iron Ingots", "Gold Ingots", "Diamonds"],
        "makes": [],
        "recipeimg": "",
        "next": ["Hoe"],
        "prev": ["Axe"]
   },
   {
        "name": "Hoe"
        "img": "",
        "desc": "Used to till dirt blocks in preparation for growing crops.",
        "madeof": ["Sticks", "Wooden Plank", "Cobblestone", "Iron Ingots", "Gold Ingots", "Diamonds"],
        "makes": [],
        "recipeimg": "",
        "next": ["Fishing Rod"],
        "prev": ["Shovel"]
   },
   {
        "name": "Fishing Rod"
        "img": "",
        "desc": "Can be cast into water to catch fish.",
        "madeof": ["Stick", "String"],
        "makes": [],
        "recipeimg": "",
        "next": ["Flint & Steel"],
        "prev": ["Hoe"]
   },
   {
        "name": "Flint & Steel"
        "img": "",
        "desc": "Used to light fires, ignite TNT and open nether portals.",
        "madeof": ["Iron Ingot", "Flint"],
        "makes": [],
        "recipeimg": "",
        "next": ["Compass"],
        "prev": ["Fishing Rod"]
   },
   {
        "name": "Compass"
        "img": "",
        "desc": "Points to the spawn point.",
        "madeof": ["Iron Ingot", "Redstone"],
        "makes": [],
        "recipeimg": "",
        "next": ["Bucket"],
        "prev": ["Flint & Steel"]
   },
   {
        "name": "Bucket"
        "img": "",
        "desc": "Used to transport water, lava, and milk.",
        "madeof": ["Iron Ingot"],
        "makes": [],
        "recipeimg": "",
        "next": ["Shears"],
        "prev": ["Compass"]
   },
   {
        "name": "Shears"
        "img": "",
        "desc": "Used to collect wool from sheep and leaves from trees.",
        "madeof": ["Iron Ingot"],
        "makes": [],
        "recipeimg": "",
        "next": [""],
        "prev": ["Bucket"]
   }
]

defense = [
    {
        "name": "Helmet",
        "img": "",
        "desc": "Head armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "",
        "next": ["Chestplate"],
        "prev": []
   },
   {
        "name": "Chestplate",
        "img": "",
        "desc": "Chest armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "",
        "next": ["Leggings"],
        "prev": ["Helmet"]
   },
   {
        "name": "Leggings"
        "img": "",
        "desc": "Leg armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "",
        "next": ["Boots"],
        "prev": ["Chestplate"]
   },
   {
        "name": "Boots"
        "img": "",
        "desc": "Foot armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "",
        "next": ["Sword"],
        "prev": ["Leggings"]
   },
   {
        "name": "Sword"
        "img": "",
        "desc": "Deal damage to mobs and other players.",
        "madeof": ["Stick", "Wooden Planks", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "",
        "next": ["Bow"],
        "prev": ["Boots"]
   },
   {
        "name": "Bow"
        "img": "",
        "desc": "Used to shoot arrows that deal damage to mobs and other players.",
        "madeof": ["Stick", "String"],
        "makes": [],
        "recipeimg": "",
        "next": ["Arrow"],
        "prev": ["Sword"]
   },
   {
        "name": "Arrow"
        "img": "",
        "desc": "Ammunition for bows.",
        "madeof": ["Stick", "Flint", "Feather"],
        "makes": [],
        "recipeimg": "",
        "next": ["Scute"],
        "prev": ["Bow"]
   },
   {
        "name": "Scute"
        "img": "",
        "desc": "Helmet that gives the player water breathing effect.",
        "madeof": ["Turtle Shell"],
        "makes": [],
        "recipeimg": "",
        "next": ["Crossbow"],
        "prev": ["Arrow"]
   },
   {
        "name": "Crossbow"
        "img": "",
        "desc": "Weapon used to fire arrows further and more accurately than a bow.",
        "madeof": ["Iron Ingot"],
        "makes": [],
        "recipeimg": "",
        "next": [""],
        "prev": ["Bucket"]
   }
]

# ROUTES

@app.route('/learn/basics/<string:name>')
def learnbasics(name):
    selected = next((b for b in basics if b["name"] == name), None)
    if selected is None:
        return: "item not found", 404
    return render_template('learn.html', item=selected)

@app.route('/getbasics', methods=['GET'])
def getdata():
    return jsonify({"basics": basics})

@app.route('/gettools', methods=['GET'])
def getdata():
    return jsonify({"tools": tools})

@app.route('/getdefense', methods=['GET'])
def getdata():
    return jsonify({"defense": defense})

if __name__ == '__main__':
   app.run(debug = True, port=5001)