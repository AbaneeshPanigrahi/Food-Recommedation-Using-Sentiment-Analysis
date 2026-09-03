import pandas as pd

def add_instructions_to_recipes():
    print("Loading recipes.csv...")
    df = pd.read_csv('datasets/recipes.csv')
    
    if 'Instructions' in df.columns:
        print("Instructions column already exists!")
        return

    print("Generating synthetic instructions for", len(df), "recipes...")
    instructions = []
    
    for idx, row in df.iterrows():
        title = str(row['Title'])
        ingredients = str(row['Ingredients'])
        
        # Determine some basic cooking methods from the title to make it slightly smart
        method = "Cook"
        if "Bake" in title or "Roasted" in title or "Pizza" in title or "Casserole" in title:
            method = "Bake in the oven"
        elif "Soup" in title or "Stew" in title or "Curry" in title:
            method = "Simmer"
        elif "Salad" in title:
            method = "Toss together"
        elif "Fried" in title or "Stir-Fry" in title:
            method = "Stir-fry"
        elif "Grilled" in title or "Barbecue" in title:
            method = "Grill on medium heat"
            
        step_text = f"1. Prepare and measure out the following: {ingredients}.\n2. {method} the ingredients thoroughly until fully prepared.\n3. Plate the {title} and serve hot. Enjoy!"
        instructions.append(step_text)
        
    df['Instructions'] = instructions
    
    print("Saving updated recipes.csv...")
    df.to_csv('datasets/recipes.csv', index=False)
    print("Done! Added synthetic cooking steps.")

if __name__ == "__main__":
    add_instructions_to_recipes()
