
from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
DATABASE = "recipes.db"

SUBSTITUTIONS = {
    "butter": ["olive oil", "coconut oil", "margarine"],
    "milk": ["soy milk", "oat milk", "almond milk"],
    "egg": ["mashed banana", "applesauce", "flaxseed mixed with water"],
    "eggs": ["mashed banana", "applesauce", "flaxseed mixed with water"],
    "sugar": ["honey", "maple syrup", "jaggery"],
    "cream": ["coconut cream", "evaporated milk"],
    "yogurt": ["sour cream", "plain yogurt"],
    "lemon": ["lime juice", "vinegar"],
    "rice": ["quinoa", "bulgur"],
    "flour": ["oat flour", "whole wheat flour"],
    "tomato": ["canned tomatoes", "tomato puree"],
    "cheese": ["nutritional yeast", "vegan cheese"],
    "soy sauce": ["tamari", "coconut aminos"],
    "baking powder": ["baking soda with an appropriate acid"],
    "oil": ["melted butter", "applesauce for some baking recipes"]
}


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection



def initialize_database():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    count = connection.execute(
        "SELECT COUNT(*) FROM recipes"
    ).fetchone()[0]

    if count == 0:
        recipes = [
            ("Vegetable Fried Rice",
             "rice, carrot, beans, onion, soy sauce",
             "Cook rice. Stir-fry vegetables, add rice and soy sauce.",
             "Lunch"),
            ("Pancakes",
             "flour, milk, egg, sugar, baking powder",
             "Mix ingredients and cook the batter on a hot pan.",
             "Breakfast"),
            ("Tomato Pasta",
             "pasta, tomato, garlic, onion, oil",
             "Cook pasta and mix with prepared tomato sauce.",
             "Dinner"),
            ("Banana Smoothie",
             "banana, milk, honey",
             "Blend all ingredients until smooth.",
             "Drinks"),
            ("Vegetable Omelette",
             "egg, onion, tomato, salt, pepper",
             "Beat eggs, add vegetables and cook in a pan.",
             "Breakfast"),
            ("Potato Sandwich",
             "bread, potato, onion, salt, pepper",
             "Mash cooked potato, fill bread and toast.",
             "Snacks")
        ]

        connection.executemany("""
            INSERT INTO recipes
            (name, ingredients, instructions, category)
            VALUES (?, ?, ?, ?)
        """, recipes)

    connection.commit()

    # Add more recipes without deleting existing records.
    extra_recipes = [
        ("Idli", "rice, urad dal, salt", "Soak rice and urad dal, grind, ferment the batter and steam in idli moulds.", "Breakfast"),
        ("Masala Dosa", "rice, urad dal, potato, onion, spices", "Prepare fermented dosa batter, make potato masala and cook thin crispy dosas.", "Breakfast"),
        ("Appam", "rice, coconut milk, yeast, sugar, salt", "Prepare fermented batter and cook in an appam pan.", "Breakfast"),
        ("Puttu", "rice flour, coconut, salt, water", "Moisten rice flour, layer with coconut and steam in a puttu maker.", "Breakfast"),
        ("Poori", "wheat flour, water, salt, oil", "Knead dough, roll small discs and deep-fry until puffed.", "Breakfast"),
        ("Upma", "rava, onion, green chilli, water, oil", "Roast rava, sauté seasonings, add water and stir until cooked.", "Breakfast"),
        ("Poha", "flattened rice, onion, peanuts, turmeric, lemon", "Rinse poha, sauté seasonings and peanuts, then mix and finish with lemon.", "Breakfast"),
        ("Oats Porridge", "oats, milk, banana, honey", "Cook oats in milk and serve with banana and honey.", "Breakfast"),
        ("French Toast", "bread, egg, milk, sugar, cinnamon", "Dip bread in egg and milk mixture and pan-fry until golden.", "Breakfast"),
        ("Vegetable Sandwich", "bread, cucumber, tomato, onion, butter", "Layer sliced vegetables between bread and toast if desired.", "Breakfast"),
        ("Chole Bhature", "chickpeas, flour, onion, tomato, spices", "Cook spiced chickpeas and serve with deep-fried bhature.", "Lunch"),
        ("Rajma Rice", "kidney beans, rice, onion, tomato, spices", "Cook soaked kidney beans in tomato gravy and serve with rice.", "Lunch"),
        ("Vegetable Biryani", "basmati rice, carrot, beans, peas, spices", "Cook vegetables with spices, layer with rice and steam until done.", "Lunch"),
        ("Chicken Biryani", "chicken, basmati rice, onion, yogurt, spices", "Marinate chicken, prepare spiced rice and cook together until done.", "Lunch"),
        ("Lemon Rice", "rice, lemon, peanuts, mustard seeds, curry leaves", "Temper spices and peanuts, then mix with cooked rice and lemon juice.", "Lunch"),
        ("Curd Rice", "rice, yogurt, mustard seeds, curry leaves", "Mix cooled rice with yogurt and add a mustard seed tempering.", "Lunch"),
        ("Sambar Rice", "rice, toor dal, vegetables, tamarind, spices", "Cook dal and vegetables with tamarind and spices, then combine with rice.", "Lunch"),
        ("Palak Paneer", "spinach, paneer, onion, tomato, spices", "Cook spinach, blend into a sauce and simmer with paneer.", "Lunch"),
        ("Vegetable Pulao", "rice, peas, carrot, beans, whole spices", "Sauté vegetables and spices, add rice and water, then cook covered.", "Lunch"),
        ("Fish Curry", "fish, coconut milk, chilli, turmeric, tamarind", "Simmer fish gently in a spiced coconut or tamarind gravy until cooked.", "Lunch"),
        ("Kerala Fish Fry", "fish, chilli powder, turmeric, lemon, oil", "Marinate fish with spices and lemon, then pan-fry until cooked.", "Lunch"),
        ("Avial", "mixed vegetables, coconut, yogurt, curry leaves", "Cook vegetables and combine with ground coconut mixture and seasoning.", "Lunch"),
        ("Erissery", "pumpkin, beans, coconut, cumin, mustard seeds", "Cook pumpkin and beans, add ground coconut and finish with seasoning.", "Lunch"),
        ("Kalan", "raw banana, yam, yogurt, coconut, pepper", "Cook vegetables with pepper, add coconut mixture and yogurt.", "Lunch"),
        ("Kerala Sambar", "toor dal, drumstick, carrot, tamarind, spices", "Cook dal and vegetables, add tamarind and sambar spices.", "Lunch"),
        ("Thoran", "cabbage, coconut, mustard seeds, curry leaves", "Stir-fry shredded cabbage with coconut and a mustard seed tempering.", "Lunch"),
        ("Puttu and Kadala Curry", "rice flour, coconut, black chickpeas, onion, spices", "Steam layered puttu and serve with cooked black chickpea curry.", "Breakfast"),
        ("Kerala Parotta", "flour, water, salt, oil", "Prepare elastic dough, roll, fold, cook on a hot pan and separate layers.", "Dinner"),
        ("Vegetable Korma", "mixed vegetables, coconut, onion, spices", "Cook vegetables in a mildly spiced coconut gravy.", "Dinner"),
        ("Paneer Butter Masala", "paneer, tomato, butter, cream, spices", "Prepare a tomato-based gravy and simmer paneer in it.", "Dinner"),
        ("Dal Tadka", "toor dal, onion, tomato, garlic, spices", "Cook dal and finish with a hot tempering of garlic and spices.", "Dinner"),
        ("Aloo Gobi", "potato, cauliflower, turmeric, cumin, spices", "Cook potato and cauliflower with spices until tender.", "Dinner"),
        ("Mushroom Masala", "mushroom, onion, tomato, ginger, spices", "Sauté mushrooms and simmer in spiced onion-tomato gravy.", "Dinner"),
        ("Egg Curry", "egg, onion, tomato, coconut milk, spices", "Boil eggs and simmer in a prepared spiced gravy.", "Dinner"),
        ("Chicken Curry", "chicken, onion, tomato, ginger, spices", "Cook chicken in a spiced gravy until fully cooked.", "Dinner"),
        ("Vegetable Noodles", "noodles, carrot, cabbage, capsicum, soy sauce", "Cook noodles and toss with stir-fried vegetables and sauce.", "Dinner"),
        ("Garlic Bread", "bread, garlic, butter, parsley", "Spread garlic butter on bread and bake until crisp.", "Snacks"),
        ("French Fries", "potato, oil, salt", "Cut potatoes into strips, dry well and fry until golden.", "Snacks"),
        ("Onion Pakoda", "onion, gram flour, chilli, salt, oil", "Mix sliced onions with seasoned gram flour and fry spoonfuls until crisp.", "Snacks"),
        ("Samosa", "potato, peas, flour, spices, oil", "Fill pastry with spiced potato and peas, seal and fry until golden.", "Snacks"),
        ("Vegetable Cutlet", "potato, carrot, peas, breadcrumbs, spices", "Mash cooked vegetables, shape, coat with breadcrumbs and shallow-fry.", "Snacks"),
        ("Banana Chips", "raw banana, oil, salt", "Slice raw banana thinly and fry until crisp.", "Snacks"),
        ("Masala Peanuts", "peanuts, gram flour, chilli powder, salt", "Coat peanuts with seasoned flour and roast or fry until crisp.", "Snacks"),
        ("Popcorn", "corn kernels, oil, salt", "Heat kernels in a covered pot until popping slows.", "Snacks"),
        ("Tomato Soup", "tomato, onion, garlic, stock, pepper", "Cook tomatoes and aromatics, blend and season the soup.", "Soups"),
        ("Sweet Corn Soup", "sweet corn, carrot, beans, stock, pepper", "Simmer vegetables and corn in stock until tender.", "Soups"),
        ("Mango Lassi", "mango, yogurt, milk, sugar", "Blend mango with yogurt, milk and sugar until smooth.", "Drinks"),
        ("Lemon Juice", "lemon, water, sugar, salt", "Mix lemon juice with water and adjust sweetness and salt.", "Drinks"),
        ("Watermelon Juice", "watermelon, lime, mint", "Blend watermelon and strain if desired, then add lime.", "Drinks"),
        ("Cold Coffee", "coffee, milk, sugar, ice", "Blend coffee, chilled milk, sugar and ice.", "Drinks"),
        ("Hot Chocolate", "milk, cocoa powder, sugar, chocolate", "Heat milk and whisk in cocoa, sugar and chocolate.", "Drinks"),
        ("Chocolate Cake", "flour, cocoa powder, sugar, eggs, butter", "Mix cake ingredients and bake until a tester comes out clean.", "Desserts"),
        ("Vanilla Cupcakes", "flour, sugar, butter, eggs, vanilla", "Prepare batter, divide into cupcake cases and bake until set.", "Desserts"),
        ("Brownies", "chocolate, butter, sugar, eggs, flour", "Mix melted chocolate and other ingredients, then bake until set.", "Desserts"),
        ("Rice Pudding", "rice, milk, sugar, cardamom, nuts", "Simmer rice in milk, stirring until soft and creamy.", "Desserts"),
        ("Gulab Jamun", "milk powder, flour, milk, sugar, cardamom", "Make soft dough balls, fry gently and soak in warm sugar syrup.", "Desserts"),
        ("Fruit Salad", "apple, banana, grapes, orange, honey", "Chop fruit and mix gently with honey or lemon juice.", "Desserts"),
        ("Carrot Halwa", "carrot, milk, sugar, ghee, nuts", "Cook grated carrot with milk, add sugar and finish with ghee and nuts.", "Desserts"),
        ("Payasam", "vermicelli, milk, sugar, cardamom, cashews", "Roast vermicelli, cook in milk and sweeten with sugar.", "Desserts"),
        ("Paal Payasam", "rice, milk, sugar, cardamom", "Slowly simmer rice in milk until creamy and sweeten to taste.", "Desserts"),
        ("Unniyappam", "rice flour, banana, jaggery, coconut, cardamom", "Mix ingredients into a thick batter and cook in an unniyappam pan.", "Desserts"),
        ("Ada Pradhaman", "ada, jaggery, coconut milk, cardamom, ghee", "Cook ada, combine with jaggery syrup and coconut milk.", "Desserts"),
        ("Pazham Pori", "ripe banana, flour, sugar, turmeric, oil", "Dip banana slices in batter and fry until golden.", "Snacks"),
        ("Uzhunnu Vada", "urad dal, green chilli, ginger, curry leaves", "Grind soaked dal, mix seasonings, shape rings and fry until crisp.", "Snacks"),
        ("Medu Vada", "urad dal, pepper, curry leaves, ginger", "Prepare a thick dal batter, shape into rings and fry.", "Breakfast"),
        ("Vegetable Momos", "flour, cabbage, carrot, onion, ginger", "Fill dough wrappers with seasoned vegetables and steam until cooked.", "Snacks"),
        ("Spring Rolls", "spring roll wrappers, cabbage, carrot, capsicum, soy sauce", "Fill wrappers with stir-fried vegetables, roll and fry until crisp.", "Snacks"),
        ("Hummus", "chickpeas, tahini, lemon, garlic, olive oil", "Blend cooked chickpeas with tahini, lemon, garlic and olive oil.", "Snacks"),
        ("Guacamole", "avocado, lime, onion, tomato, salt", "Mash avocado and mix with chopped vegetables and lime juice.", "Snacks"),
        ("Greek Salad", "cucumber, tomato, onion, olives, feta", "Chop vegetables and toss with olives, feta and dressing.", "Salads"),
        ("Chickpea Salad", "chickpeas, cucumber, tomato, onion, lemon", "Combine cooked chickpeas and chopped vegetables with lemon dressing.", "Salads"),
        ("Caesar Salad", "lettuce, croutons, parmesan, Caesar dressing", "Toss lettuce with dressing and top with croutons and parmesan.", "Salads"),
        ("Grilled Cheese Sandwich", "bread, cheese, butter", "Fill bread with cheese and toast in butter until golden.", "Snacks"),
        ("Chicken Sandwich", "cooked chicken, bread, lettuce, mayonnaise", "Combine cooked chicken with dressing and serve in bread with lettuce.", "Snacks"),
        ("Chicken Soup", "chicken, carrot, onion, garlic, stock", "Simmer chicken and vegetables in stock until cooked and tender.", "Soups"),
        ("Mushroom Soup", "mushroom, onion, milk, butter, pepper", "Cook mushrooms and onion, add milk or stock and blend if desired.", "Soups"),
        ("Vegetable Stew", "potato, carrot, beans, coconut milk, curry leaves", "Simmer vegetables until tender and finish with coconut milk.", "Dinner"),
        ("Idiyappam", "rice flour, hot water, salt", "Prepare a soft dough, press through an idiyappam mould and steam.", "Breakfast"),
        ("Kadala Curry", "black chickpeas, onion, coconut, spices", "Cook soaked chickpeas and simmer with roasted coconut masala.", "Breakfast"),
        ("Kerala Egg Roast", "egg, onion, tomato, chilli, spices", "Boil eggs and simmer in a thick, caramelized onion masala.", "Breakfast"),
        ("Kappa Puzhukku", "tapioca, coconut, garlic, cumin, curry leaves", "Boil tapioca until tender, then mash with seasoned coconut mixture.", "Lunch"),
        ("Kerala Chicken Roast", "chicken, onion, tomato, ginger, spices", "Marinate chicken, cook with spices and roast until fully cooked.", "Dinner"),
        ("Coconut Chutney", "coconut, green chilli, ginger, salt", "Grind ingredients with water and finish with a mustard seed tempering.", "Breakfast"),
        ("Mint Chutney", "mint, coriander, green chilli, lemon", "Blend herbs with chilli, lemon and salt.", "Breakfast"),
        ("Tomato Chutney", "tomato, onion, garlic, chilli, oil", "Cook tomatoes and aromatics, then blend into a chutney.", "Breakfast"),
        ("Peanut Butter Toast", "bread, peanut butter, banana", "Toast bread and spread peanut butter, adding banana slices if desired.", "Breakfast"),
        ("Baked Potatoes", "potato, olive oil, salt, pepper", "Prick potatoes, coat lightly with oil and bake until tender.", "Dinner"),
        ("Vegetable Quesadilla", "tortilla, cheese, capsicum, onion, corn", "Fill tortilla with vegetables and cheese, fold and toast until crisp.", "Snacks"),
        ("Margherita Pizza", "pizza dough, tomato sauce, mozzarella, basil", "Top dough with sauce and cheese, then bake until crust is cooked.", "Dinner"),
        ("Paneer Tikka", "paneer, yogurt, capsicum, chilli, spices", "Marinate paneer and vegetables, then grill or bake until lightly charred.", "Snacks"),
        ("Tandoori Chicken", "chicken, yogurt, lemon, chilli, spices", "Marinate chicken thoroughly and roast until safely cooked through.", "Dinner"),
        ("Vegetable Manchurian", "cabbage, carrot, flour, garlic, soy sauce", "Shape vegetable mixture into balls, cook and toss in prepared sauce.", "Dinner"),
        ("Chilli Paneer", "paneer, capsicum, onion, garlic, soy sauce", "Sauté paneer and vegetables and toss with a savoury sauce.", "Dinner"),
        ("Prawn Curry", "prawns, coconut milk, onion, chilli, spices", "Simmer prawns in seasoned gravy until opaque and fully cooked.", "Dinner"),
        ("Tuna Salad", "tuna, cucumber, onion, lemon, pepper", "Combine cooked or canned tuna with vegetables and lemon dressing.", "Lunch"),
        ("Omelette Wrap", "egg, tortilla, onion, tomato, cheese", "Cook an omelette and wrap it in a warm tortilla with fillings.", "Breakfast"),
        ("Apple Crumble", "apple, flour, butter, sugar, cinnamon", "Top seasoned apples with crumble mixture and bake until golden.", "Desserts"),
        ("Chia Pudding", "chia seeds, milk, honey, banana", "Stir chia seeds into milk, refrigerate until thick and add toppings.", "Breakfast"),
        ("Overnight Oats", "oats, milk, yogurt, banana, chia seeds", "Mix ingredients and refrigerate overnight before serving.", "Breakfast"),
        ("Energy Balls", "oats, dates, peanut butter, cocoa powder", "Blend ingredients, roll into small balls and chill until firm.", "Snacks"),
        ("Lemon Garlic Pasta", "pasta, garlic, lemon, olive oil, parsley", "Cook pasta and toss with sautéed garlic, lemon and olive oil.", "Dinner"),
        ("Spinach Dal", "spinach, lentils, garlic, onion, turmeric", "Cook lentils and spinach together and season with garlic tempering.", "Lunch"),
        ("Vegetable Fried Noodles", "noodles, cabbage, carrot, soy sauce, garlic", "Cook noodles and stir-fry with vegetables and garlic sauce.", "Dinner"),
        ("Cucumber Raita", "cucumber, yogurt, cumin, salt", "Mix grated cucumber into yogurt and season with cumin and salt.", "Lunch"),
        ("Besan Chilla", "gram flour, onion, tomato, chilli, water", "Make a pourable batter, add vegetables and cook like a savoury pancake.", "Breakfast"),
        ("Rava Kesari", "rava, sugar, ghee, water, cardamom", "Roast rava, cook with water and sugar, and finish with ghee.", "Desserts"),
        ("Bread Pudding", "bread, milk, egg, sugar, cinnamon", "Soak bread in custard mixture and bake until set.", "Desserts"),
        ("Homemade Lemon Cake", "flour, sugar, butter, egg, lemon", "Mix cake batter with lemon zest and juice, then bake until done.", "Desserts"),
        ("Vegetable Dalia", "broken wheat, carrot, peas, onion, spices", "Cook broken wheat with vegetables and seasoning until tender.", "Breakfast"),
        ("Corn Chaat", "sweet corn, onion, tomato, lemon, chilli", "Mix cooked corn with chopped vegetables, lemon and spices.", "Snacks"),
        ("Aloo Paratha", "wheat flour, potato, coriander, spices", "Fill rolled dough with spiced mashed potato and cook on a hot griddle.", "Breakfast"),
        ("Chana Masala", "chickpeas, onion, tomato, ginger, spices", "Simmer cooked chickpeas in a spiced onion-tomato gravy.", "Lunch"),
        ("Vegetable Clear Soup", "carrot, cabbage, beans, garlic, stock", "Simmer chopped vegetables in stock until tender.", "Soups"),
        ("Coconut Rice", "rice, coconut, cashews, curry leaves, mustard seeds", "Toast coconut and seasonings, then mix with cooked rice.", "Lunch"),
        ("Stuffed Capsicum", "capsicum, potato, peas, onion, spices", "Fill capsicum halves with seasoned vegetables and bake until tender.", "Dinner")
    ]

    connection.executemany("""
        INSERT INTO recipes (name, ingredients, instructions, category)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM recipes WHERE name = ?
        )
    """, [(*recipe, recipe[0]) for recipe in extra_recipes])

    connection.commit()
    connection.close()



@app.route("/")
def home():
    connection = get_db()
    recipes = connection.execute(
        "SELECT * FROM recipes ORDER BY name"
    ).fetchall()
    connection.close()

    # Map each recipe to its own relevant image.
    image_urls = {
        "idli": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=600&q=80",
        "masala dosa": "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=600&q=80",
        "appam": "https://images.unsplash.com/photo-1630383249896-424e482df921?auto=format&fit=crop&w=600&q=80",
        "puttu": "https://images.unsplash.com/photo-1626500155537-93690c24099e?auto=format&fit=crop&w=600&q=80",
        "vegetable biryani": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?auto=format&fit=crop&w=600&q=80",
        "chicken biryani": "https://images.unsplash.com/photo-1563379091339-03246963d96c?auto=format&fit=crop&w=600&q=80",
        "pancakes": "https://images.unsplash.com/photo-1528207776546-365bb710ee93?auto=format&fit=crop&w=600&q=80",
        "tomato pasta": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=600&q=80",
        "banana smoothie": "https://images.unsplash.com/photo-1505252585461-04db1eb84625?auto=format&fit=crop&w=600&q=80",
        "vegetable fried rice": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?auto=format&fit=crop&w=600&q=80",
        "pizza": "https://images.unsplash.com/photo-157 pizza?auto=format&fit=crop&w=600&q=80",
        "chocolate cake": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=600&q=80",
        "french fries": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=600&q=80",
        "samosa": "https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=600&q=80",
        "mango lassi": "https://images.unsplash.com/photo-1546173159-315724a31696?auto=format&fit=crop&w=600&q=80",
        "fruit salad": "https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?auto=format&fit=crop&w=600&q=80"
    }

    default_image = (
        "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
        "?auto=format&fit=crop&w=600&q=80"
    )

    recipe_list = []

    for recipe in recipes:
        item = dict(recipe)
        item["image_url"] = image_urls.get(
            item["name"].lower(), default_image
        )
        recipe_list.append(item)

    return render_template("index.html", recipes=recipe_list)


@app.route("/recipes")
def recipes_page():
    connection = get_db()
    recipes = connection.execute(
        "SELECT * FROM recipes ORDER BY name"
    ).fetchall()
    connection.close()

    image_urls = {
        "idli": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=600&q=80",
        "masala dosa": "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=600&q=80",
        "pancakes": "https://images.unsplash.com/photo-1528207776546-365bb710ee93?auto=format&fit=crop&w=600&q=80",
        "tomato pasta": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=600&q=80",
        "chicken biryani": "https://images.unsplash.com/photo-1563379091339-03246963d96c?auto=format&fit=crop&w=600&q=80",
    }

    default_image = (
        "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
        "?auto=format&fit=crop&w=600&q=80"
    )

    recipe_list = []

    for recipe in recipes:
        item = dict(recipe)
        item["image_url"] = image_urls.get(
            item["name"].lower(), default_image
        )
        recipe_list.append(item)

    return render_template("recipes.html", recipes=recipe_list)

@app.route("/api/recipes")
def get_recipes():
    connection = get_db()
    recipes = connection.execute(
        "SELECT * FROM recipes ORDER BY name"
    ).fetchall()
    connection.close()
    return jsonify([dict(recipe) for recipe in recipes])


@app.route("/api/substitute", methods=["POST"])
def substitute():
    data = request.get_json(silent=True) or {}
    ingredient = data.get("ingredient", "").strip().lower()

    if not ingredient:
        return jsonify({"error": "Enter an ingredient."}), 400

    substitutes = SUBSTITUTIONS.get(ingredient)

    if substitutes:
        return jsonify({
            "ingredient": ingredient,
            "substitutes": substitutes
        })

    return jsonify({
        "ingredient": ingredient,
        "substitutes": [
            "No saved substitute found. Try a similar ingredient."
        ]
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    ingredients = data.get("ingredients", "").strip()

    if not ingredients:
        return jsonify({"error": "Please enter your ingredients."}), 400

    # Use an AI model if an API key is configured.
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful cooking assistant. Suggest "
                            "two or three practical recipes using the "
                            "ingredients the user lists. For each recipe, "
                            "give a name, extra ingredients if needed, "
                            "simple steps, and approximate cooking time. "
                            "Mention important food safety concerns."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            "Ingredients I have: " + ingredients
                        )
                    }
                ],
                max_tokens=600
            )

            reply = response.choices[0].message.content
            return jsonify({"reply": reply})

        except Exception:
            app.logger.exception("AI recipe generation failed")
            return jsonify({
                "error": (
                    "The AI service could not respond. Check your API "
                    "key, API access, and available credits."
                )
            }), 502

    # Fallback: recommend saved recipes matching the ingredients.
    available = {
        item.strip().lower()
        for item in ingredients.split(",")
        if item.strip()
    }

    connection = get_db()
    recipes = connection.execute(
        "SELECT * FROM recipes"
    ).fetchall()
    connection.close()

    matches = []

    for recipe in recipes:
        recipe_ingredients = {
            item.strip().lower()
            for item in recipe["ingredients"].split(",")
        }

        common = available.intersection(recipe_ingredients)

        if common:
            matches.append((len(common), recipe, common))

    matches.sort(key=lambda item: item[0], reverse=True)

    if not matches:
        return jsonify({
            "reply": (
                "I couldn't find a close match in the saved recipes. "
                "Try listing ingredients separated by commas, such as "
                "egg, onion, tomato."
            )
        })

    lines = ["Here are some recipes matching your ingredients:\n"]

    for _, recipe, common in matches[:3]:
        lines.append(
            f"🍲 {recipe['name']}\n"
            f"Matching ingredients: {', '.join(sorted(common))}\n"
            f"Ingredients: {recipe['ingredients']}\n"
            f"Instructions: {recipe['instructions']}\n"
        )

    lines.append(
        "These are matches from the saved recipe collection, "
        "not newly generated AI recipes."
    )

    return jsonify({"reply": "\n".join(lines)})


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
