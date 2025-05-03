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
        "desc": "Basic building material. Varies by biome (Oak, Spruce, Birch, Jungle, Acacia, Dark Oak).",
        "madeof": ["Log"],
        "makes": ["Stick", "Crafting Table", "Chest"],
        "recipeimg": "",
        "next": "Stick",
        "prev": "",
        "recipe": [
            ["", "", ""],
            ["", "Log", ""],
            ["", "", ""]
        ]
   },
    {
        "name": "Stick",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7a/Stick_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20200128023441",
        "desc": "Used to craft many other items.",
        "madeof": ["Wooden Plank"],
        "makes": ["Torch", "Fence", "Sword", "Ladder", "Sign"],
        "recipeimg": "",
        "next": "Torch",
        "prev": "Wooden Plank",
        "recipe": [
            ["", "", ""],
            ["", "Wooden Plank", ""],
            ["", "Wooden Plank", ""]
        ]
   },
    {
        "name": "Torch",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/90/Torch.gif/revision/latest?cb=20200111190834",
        "desc": "Provides light and melts ice/snow.",
        "madeof": ["Stick", "Coal"],
        "makes": [],
        "recipeimg": "",
        "next": "Crafting Table",
        "prev": "Stick",
        "recipe": [
            ["", "", ""],
            ["", "Coal", ""],
            ["", "Stick", ""]
        ]
    },
    {
        "name": "Crafting Table",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/93/Crafting_Table_JE3_BE2.png/revision/latest?cb=20190606093431",
        "desc": "Allows player to craft when right clicked.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "recipeimg": "",
        "next": "Furnace",
        "prev": "Torch",
        "recipe": [
            ["", "", ""],
            ["Wooden Plank", "Wooden Plank", ""],
            ["Wooden Plank", "Wooden Plank", ""]
        ]
    },
    {
        "name": "Furnace",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/99/Furnace_%28S%29_JE4.png/revision/latest/scale-to-width/360?cb=20210111063232",
        "desc": "Allows player to smelt (refine ores, cook food, etc.) when right clicked).",
        "madeof": ["Cobblestone"],
        "makes": [],
        "recipeimg": "",
        "next": "Chest",
        "prev": "Crafting Table",
        "recipe": [
            ["Cobblestone", "Cobblestone", "Cobblestone"],
            ["Cobblestone", "", "Cobblestone"],
            ["Cobblestone", "Cobblestone", "Cobblestone"]
        ]
    },
    {
        "name": "Chest",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/3d/Chest_%28S%29_JE1.png/revision/latest?cb=20200128020353",
        "desc": "Used to store items.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "recipeimg": "",
        "next": "Ladder",
        "prev": "Furnace",
        "recipe": [
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"],
            ["Wooden Plank", "", "Wooden Plank"],
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"]
        ]
   },
   {
        "name": "Ladder",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/af/Ladder_%28texture%29_JE3_BE2.png/revision/latest?cb=20200922000708",
        "desc": "Allows player to climb vertically.",
        "madeof": ["Stick"],
        "makes": [],
        "recipeimg": "",
        "next": "Fence",
        "prev": "Furnace",
        "recipe": [
            ["Stick", "", "Stick"],
            ["Stick", "Stick", "Stick"],
            ["Stick", "", "Stick"]
        ]
   },
   {
        "name": "Fence",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/f6/Oak_Fence_JE4_BE2.png/revision/latest?cb=20200317191546",
        "desc": "Barrier that can't be jumped over.",
        "madeof": ["Wooden Plank", "Stick"],
        "makes": [],
        "recipeimg": "",
        "next": "Boat",
        "prev": "Ladder",
        "recipe": [
            ["", "", ""],
            ["Wooden Plank", "Stick", "Wooden Plank"],
            ["Wooden Plank", "Stick", "Wooden Plank"]
        ]
   },
   {
        "name": "Boat",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/5/58/Oak_Boat_%28item%29_JE4_BE3.png/revision/latest?cb=20200518190533",
        "desc": "Used to travel over water.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "recipeimg": "",
        "next": "Slab",
        "prev": "Fence",
        "recipe": [
            ["", "", ""],
            ["Wooden Plank", "", "Wooden Plank"],
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"]
        ]
   },
   {
        "name": "Slab",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/ac/Oak_Slab_JE5_BE2.png/revision/latest/scale-to-width/360?cb=20240729071106",
        "desc": "Used to create gradual slopes.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "recipeimg": "",
        "next": "Stairs",
        "prev": "Boat",
        "recipe": [
            ["", "", ""],
            ["", "", ""],
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"]
        ]
   },
   {
        "name": "Stairs",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/a0/Oak_Stairs_%28N%29_JE7_BE6.png/revision/latest?cb=20200317191626",
        "desc": "Used to build staircases.",
        "madeof": ["Wooden Plank"],
        "makes": [],
        "recipeimg": "",
        "next": "Door",
        "prev": "Slab",
        "recipe": [
            ["", "", "Wooden Plank"],
            ["", "Wooden Plank", "Wooden Plank"],
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"]
        ]
   },
   {
        "name": "Door",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/2/2a/Oak_Door_%28item%29_JE4_BE3.png/revision/latest?cb=20230319211346",
        "desc": "Wooden doors can be opened by clicking or redstone power, Iron doors can only be opened by redstone power.",
        "madeof": ["Wooden Plank", "Iron Ingot"],
        "makes": [],
        "recipeimg": "",
        "next": "Sign",
        "prev": "Stairs",
        "recipe": [
            ["Wooden Plank", "Wooden Plank", ""],
            ["Wooden Plank", "Wooden Plank", ""],
            ["Wooden Plank", "Wooden Plank", ""]
        ]
   },
   {
        "name": "Sign",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/8/82/Oak_Sign_JE3.png/revision/latest/scale-to-width/360?cb=20211013161856",
        "desc": "Can display text.",
        "madeof": ["Wooden Plank", "Stick"],
        "makes": [],
        "recipeimg": "",
        "next": "Bed",
        "prev": "Door",
        "recipe": [
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"],
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"],
            ["", "Stick", ""]
        ]
   },
   {
        "name": "Bed",
        "img": "https://static.wikia.nocookie.net/minecraft/images/c/c5/Bed.png/revision/latest?cb=20191103220226",
        "desc": "Used to forward from night to day.",
        "madeof": ["Wooden plank", "Wool"],
        "makes": [],
        "recipeimg": "",
        "next": "",
        "prev": "Sign",
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
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/0/0b/Wooden_Pickaxe_JE2_BE2.png/revision/latest?cb=20200217231203",
        "desc": "Used to mine stone blocks and ores.",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "",
        "next": "Axe",
        "prev": "",
        "recipe": [
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"],
            ["", "Stick", ""],
            ["", "Stick", ""]
        ]
   },
   {
        "name": "Axe",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/5/56/Wooden_Axe_JE2_BE2.png/revision/latest/scale-to-width/360?cb=20200217234355",
        "desc": "Used to chop wood blocks faster.",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "",
        "next": "Torch",
        "prev": "Wooden Plank",
        "recipe": [
            ["Wooden Plank", "Wooden Plank", ""],
            ["Wooden Plank", "Stick", ""],
            ["", "Stick", ""]
        ]
   },
   {
        "name": "Shovel",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/2/26/Wooden_Shovel_JE2_BE2.png/revision/latest/scale-to-width/360?cb=20200217234949",
        "desc": "Used to dig sand, gravel, dirt, grass, and snow faster.",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingots", "Gold Ingots", "Diamonds"],
        "makes": [],
        "recipeimg": "",
        "next": "Hoe",
        "prev": "Axe",
        "recipe": [
            ["", "Wooden Plank", ""],
            ["", "Stick", ""],
            ["", "Stick", ""]
        ]
   },
   {
        "name": "Hoe",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/cd/Wooden_Hoe_JE3_BE3.png/revision/latest/scale-to-width/360?cb=20200226194121",
        "desc": "Used to till dirt blocks in preparation for growing crops.",
        "madeof": ["Stick", "Wooden Plank", "Cobblestone", "Iron Ingots", "Gold Ingots", "Diamonds"],
        "makes": [],
        "recipeimg": "",
        "next": "Fishing Rod",
        "prev": "Shovel",
        "recipe": [
            ["Wooden Plank", "Wooden Plank", ""],
            ["", "Stick", ""],
            ["", "Stick", ""]
        ]
   },
   {
        "name": "Fishing Rod",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7f/Fishing_Rod_JE2_BE2.png/revision/latest/thumbnail/width/360/height/360?cb=20200201063839",
        "desc": "Can be cast into water to catch fish.",
        "madeof": ["Stick", "String"],
        "makes": [],
        "recipeimg": "",
        "next": "Flint & Steel",
        "prev": "Hoe",
        "recipe": [
            ["", "", "Stick"],
            ["", "Stick", "String"],
            ["Stick", "", "String"]
        ]
   },
   {
        "name": "Flint & Steel",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fd/Flint_and_Steel_JE2.png/revision/latest?cb=20200128083122",
        "desc": "Used to light fires, ignite TNT and open nether portals.",
        "madeof": ["Iron Ingot", "Flint"],
        "makes": [],
        "recipeimg": "",
        "next": "Compass",
        "prev": "Fishing Rod",
        "recipe": [
            ["", "", ""],
            ["Iron", "", ""],
            ["", "Coal", ""]
        ]
   },
   {
        "name": "Compass",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b3/Compass_JE3_BE3.gif/revision/latest/thumbnail/width/360/height/360?cb=20201125191224",
        "desc": "Points to the spawn point.",
        "madeof": ["Iron Ingot", "Redstone"],
        "makes": [],
        "recipeimg": "",
        "next": "Bucket",
        "prev": "Flint & Steel",
        "recipe": [
            ["", "Iron", ""],
            ["Iron", "Redstone", "Iron"],
            ["", "Iron", ""]
        ]
   },
   {
        "name": "Bucket",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Bucket_JE2_BE2.png/revision/latest/thumbnail/width/360/height/360?cb=20200510234539",
        "desc": "Used to transport water, lava, and milk.",
        "madeof": ["Iron Ingot"],
        "makes": [],
        "recipeimg": "",
        "next": "Shears",
        "prev": "Compass",
        "recipe": [
            ["", "", ""],
            ["Iron", "", "Iron"],
            ["", "Iron", ""]
        ]
   },
   {
        "name": "Shears",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/5/5a/Shears_JE2_BE2.png/revision/latest/thumbnail/width/360/height/360?cb=20191012183756",
        "desc": "Used to collect wool from sheep and leaves from trees.",
        "madeof": ["Iron Ingot"],
        "makes": [],
        "recipeimg": "",
        "next": "",
        "prev": "Bucket",
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
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c5/Leather_Cap_%28item%29_JE4_BE3.png/revision/latest?cb=20190910050904",
        "desc": "Head armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "",
        "next": "Chestplate",
        "prev": "",
        "recipe": [
            ["Leather", "Leather", "Leather"],
            ["Leather", "", "Leather"],
            ["", "", ""]
        ]
   },
   {
        "name": "Chestplate",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/71/Leather_Tunic_%28item%29_JE4_BE3.png/revision/latest?cb=20190910050828",
        "desc": "Chest armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "",
        "next": "Leggings",
        "prev": "Helmet",
        "recipe": [
            ["Leather", "", "Leather"],
            ["Leather", "Leather", "Leather"],
            ["Leather", "Leather", "Leather"]
        ]
   },
   {
        "name": "Leggings",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/2/2f/Leather_Pants_%28item%29_JE3_BE2.png/revision/latest?cb=20201104115305",
        "desc": "Leg armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "",
        "next": "Boots",
        "prev": "Chestplate",
        "recipe": [
            ["Leather", "Leather", "Leather"],
            ["Leather", "", "Leather"],
            ["Leather", "", "Leather"]
        ]
   },
   {
        "name": "Boots",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b5/Leather_Boots_%28item%29_JE4_BE3.png/revision/latest?cb=20190910050749",
        "desc": "Foot armor.",
        "madeof": ["Leather", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "",
        "next": "Sword",
        "prev": "Leggings",
        "recipe": [
            ["", "", ""],
            ["Leather", "", "Leather"],
            ["Leather", "", "Leather"]
        ]
   },
   {
        "name": "Sword",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d5/Wooden_Sword_JE2_BE2.png/revision/latest/scale-to-width/360?cb=20200217235747",
        "desc": "Deal damage to mobs and other players.",
        "madeof": ["Stick", "Wooden Planks", "Cobblestone", "Iron Ingot", "Gold Ingot", "Diamond"],
        "makes": [],
        "recipeimg": "",
        "next": "Bow",
        "prev": "Boots",
        "recipe": [
            ["", "Wooden Plank", ""],
            ["", "Wooden Plank", ""],
            ["", "Stick", ""]
        ]
   },
   {
        "name": "Bow",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/99/Bow_JE2_BE1.png/revision/latest/scale-to-width/360?cb=20200128015144",
        "desc": "Used to shoot arrows that deal damage to mobs and other players.",
        "madeof": ["Stick", "String"],
        "makes": [],
        "recipeimg": "",
        "next": "Arrow",
        "prev": "Sword",
        "recipe": [
            ["String", "Stick", ""],
            ["String", "", "Stick"],
            ["String", "Stick", ""]
        ]
   },
   {
        "name": "Arrow",
        "img": "https://static.wikia.nocookie.net/minecraft/images/4/41/Arrow.png/revision/latest/thumbnail/width/360/height/360?cb=20200118044944",
        "desc": "Ammunition for bows.",
        "madeof": ["Stick", "Flint", "Feather"],
        "makes": [],
        "recipeimg": "",
        "next": "Shield",
        "prev": "Bow",
        "recipe": [
            ["", "Coal", ""],
            ["", "Stick", ""],
            ["", "Feather", ""]
        ]
   },
   {
        "name": "Shield",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c6/Shield_JE2_BE1.png/revision/latest?cb=20190725172341",
        "desc": "Protects player against attack.",
        "madeof": ["Wooden Plank", "Iron"],
        "makes": [],
        "recipeimg": "",
        "next": "Scute",
        "prev": "Arrow",
        "recipe": [
            ["Wooden Plank", "Iron", "Wooden Plank"],
            ["Wooden Plank", "Wooden Plank", "Wooden Plank"],
            ["", "Wooden Plank", ""]
        ]
   },
   {
        "name": "Scute",
        "img": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/cc/Scute_JE1_BE1.png/revision/latest/thumbnail/width/360/height/360?cb=20190403193903",
        "desc": "Helmet that gives the player water breathing effect.",
        "madeof": ["Turtle Shell"],
        "makes": [],
        "recipeimg": "",
        "next": "",
        "prev": "Shield",
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
