"""
Script to populate the grocery_items table with sample data
including prices, brands, and sizes
"""
import sqlite3
from app.config import Config

DATABASE = Config.DATABASE

SAMPLE_ITEMS = [
    # Produce - Apples
    ('Red Apples', 'produce', None, 'medium', 1.99, 'Fresh red apples'),
    ('Organic Apples', 'produce', 'organic', 'large', 3.99, 'Fresh organic apples'),
    ('Pink Lady Apples', 'produce', None, 'large', 4.49, 'Premium pink lady apples'),
    ('Budget Apples', 'produce', 'budget', 'medium', 1.49, 'Budget friendly apples'),
    ('Granny Smith Apples', 'produce', None, 'large', 2.99, 'Tart granny smith apples'),
    
    # Produce - Bananas
    ('Yellow Bananas', 'produce', None, None, 0.59, 'Fresh yellow bananas per lb'),
    ('Organic Bananas', 'produce', 'organic', None, 1.29, 'Organic bananas per lb'),
    
    # Produce - Oranges
    ('Navel Oranges', 'produce', None, 'medium', 2.49, 'Fresh navel oranges'),
    ('Organic Oranges', 'produce', 'organic', 'large', 3.99, 'Organic navel oranges'),
    ('Blood Oranges', 'produce', None, 'medium', 3.49, 'Exotic blood oranges'),
    
    # Produce - Lettuce
    ('Romaine Lettuce', 'produce', None, None, 2.49, 'Fresh romaine lettuce'),
    ('Organic Lettuce', 'produce', 'organic', None, 3.99, 'Organic mixed greens'),
    ('Iceberg Lettuce', 'produce', 'budget', None, 1.49, 'Budget iceberg lettuce'),
    
    # Produce - Tomatoes
    ('Beefsteak Tomatoes', 'produce', None, 'large', 3.49, 'Large beefsteak tomatoes'),
    ('Cherry Tomatoes', 'produce', None, 'small', 2.99, 'Sweet cherry tomatoes'),
    ('Organic Tomatoes', 'produce', 'organic', 'medium', 4.99, 'Organic heirloom tomatoes'),
    ('Roma Tomatoes', 'produce', None, None, 2.49, 'Fresh roma tomatoes'),
    
    # Dairy - Milk
    ('Whole Milk', 'dairy', None, 'large', 3.29, 'Whole milk 1 gallon'),
    ('Organic Milk', 'dairy', 'organic', 'large', 5.99, 'Organic whole milk'),
    ('Skim Milk', 'dairy', None, 'large', 2.99, 'Skim milk 1 gallon'),
    ('2% Milk', 'dairy', None, 'large', 3.49, '2% reduced fat milk'),
    ('Almond Milk', 'dairy', None, 'large', 3.99, 'Unsweetened almond milk'),
    ('Oat Milk', 'dairy', None, 'large', 4.49, 'Plant-based oat milk'),
    
    # Dairy - Yogurt
    ('Greek Yogurt', 'dairy', None, 'large', 5.99, 'Greek yogurt plain'),
    ('Standard Yogurt', 'dairy', 'budget', 'large', 3.99, 'Standard yogurt variety pack'),
    ('Organic Yogurt', 'dairy', 'organic', 'large', 6.99, 'Organic plain yogurt'),
    ('Vanilla Yogurt', 'dairy', None, None, 4.49, 'Flavored vanilla yogurt'),
    
    # Dairy - Cheese
    ('Cheddar Cheese', 'dairy', None, 'large', 6.99, 'Aged cheddar cheese'),
    ('Mozzarella Cheese', 'dairy', None, 'medium', 5.49, 'Fresh mozzarella'),
    ('Cheese Slices', 'dairy', 'budget', 'medium', 3.99, 'Processed cheese slices'),
    ('Parmesan Cheese', 'dairy', None, None, 7.99, 'Grated parmesan cheese'),
    ('Swiss Cheese', 'dairy', None, 'large', 8.99, 'Premium swiss cheese'),
    
    # Pantry - Bread
    ('Whole Wheat Bread', 'pantry', None, None, 2.99, 'Fresh whole wheat bread'),
    ('Organic Bread', 'pantry', 'organic', None, 4.49, 'Organic whole grain bread'),
    ('White Bread', 'pantry', 'budget', None, 1.99, 'Budget white bread'),
    ('Sourdough Bread', 'pantry', None, None, 3.99, 'Artisan sourdough bread'),
    ('Rye Bread', 'pantry', None, None, 3.49, 'Dark rye bread'),
    
    # Pantry - Rice
    ('White Rice', 'pantry', None, 'large', 2.99, 'Long grain white rice'),
    ('Brown Rice', 'pantry', None, 'large', 3.49, 'Organic brown rice'),
    ('Jasmine Rice', 'pantry', None, None, 4.49, 'Fragrant jasmine rice'),
    ('Budget Rice', 'pantry', 'budget', 'large', 1.99, 'Budget white rice'),
    
    # Pantry - Pasta
    ('Spaghetti Pasta', 'pantry', None, None, 1.49, 'Durum wheat spaghetti'),
    ('Organic Pasta', 'pantry', 'organic', None, 2.99, 'Organic whole wheat pasta'),
    ('Penne Pasta', 'pantry', None, None, 1.49, 'Classic penne pasta'),
    ('Whole Wheat Pasta', 'pantry', None, None, 2.49, 'Nutritious whole wheat pasta'),
    
    # Meat - Chicken
    ('Chicken Breast', 'meat', None, None, 7.99, 'Fresh boneless chicken breast'),
    ('Whole Chicken', 'meat', None, None, 6.49, 'Whole roasting chicken'),
    ('Organic Chicken', 'meat', 'organic', None, 10.99, 'Organic free-range chicken'),
    ('Chicken Thighs', 'meat', None, None, 5.99, 'Boneless chicken thighs'),
    ('Chicken Wings', 'meat', None, None, 4.99, 'Fresh chicken wings'),
    
    # Meat - Beef
    ('Ground Beef', 'meat', None, None, 6.99, 'Lean ground beef 1 lb'),
    ('Beef Steak', 'meat', None, None, 10.99, 'Premium beef ribeye steak'),
    ('Organic Beef', 'meat', 'organic', None, 14.99, 'Grass-fed organic beef'),
    ('Beef Roast', 'meat', None, None, 9.99, 'Chuck roast for slow cooking'),
    
    # Meat - Pork
    ('Pork Chops', 'meat', None, None, 5.99, 'Boneless pork chops'),
    ('Ground Pork', 'meat', None, None, 4.99, 'Lean ground pork 1 lb'),
    ('Pork Tenderloin', 'meat', None, None, 8.99, 'Whole pork tenderloin'),
    
    # Beverages - Juice
    ('Orange Juice', 'beverages', None, 'large', 3.49, 'Fresh orange juice'),
    ('Organic Orange Juice', 'beverages', 'organic', 'large', 5.99, 'Organic orange juice'),
    ('Apple Juice', 'beverages', None, 'large', 3.49, 'Natural apple juice'),
    ('Orange Juice Concentrate', 'beverages', 'budget', 'small', 2.49, 'Orange juice concentrate'),
    ('Cranberry Juice', 'beverages', None, 'large', 4.49, 'Pure cranberry juice'),
    
    # Beverages - Other
    ('Bottle Water', 'beverages', None, 'large', 3.99, 'Pack of 24 bottled water'),
    ('Sparkling Water', 'beverages', None, None, 4.99, 'Carbonated sparkling water'),
    ('Cola Soda', 'beverages', None, 'large', 4.99, 'Classic cola 2-liter bottle'),
    ('Iced Tea', 'beverages', None, None, 2.99, 'Brewed iced tea'),
    
    # Snacks - Chips
    ('Potato Chips', 'snacks', None, 'large', 3.49, 'Classic potato chips'),
    ('Organic Chips', 'snacks', 'organic', None, 4.99, 'Organic vegetable chips'),
    ('Tortilla Chips', 'snacks', None, None, 2.99, 'Crispy tortilla chips'),
    ('Budget Chips', 'snacks', 'budget', None, 1.99, 'Budget potato chips'),
    
    # Snacks - Cookies
    ('Chocolate Cookies', 'snacks', None, None, 3.49, 'Homestyle chocolate cookies'),
    ('Organic Cookies', 'snacks', 'organic', None, 4.99, 'Organic whole grain cookies'),
    ('Sugar Cookies', 'snacks', None, None, 2.99, 'Classic sugar cookies'),
    
    # Snacks - Nuts
    ('Almonds', 'snacks', None, 'medium', 7.99, 'Roasted almonds 1 lb'),
    ('Organic Almonds', 'snacks', 'organic', None, 9.99, 'Organic raw almonds'),
    ('Mixed Nuts', 'snacks', None, None, 8.99, 'Assorted mixed nuts'),
    ('Peanuts', 'snacks', 'budget', None, 3.99, 'Roasted peanuts'),
    
    # Health & Beauty - Toothpaste
    ('Toothpaste', 'health', 'budget', 'medium', 2.99, 'Budget toothpaste'),
    ('Standard Toothpaste', 'health', None, 'medium', 3.49, 'Standard toothpaste'),
    ('Whitening Toothpaste', 'health', None, 'medium', 4.99, 'Whitening toothpaste'),
    ('Organic Toothpaste', 'health', 'organic', None, 5.99, 'Natural organic toothpaste'),
    ('Charcoal Toothpaste', 'health', None, None, 4.49, 'Activated charcoal toothpaste'),
    
    # Health & Beauty - Soap
    ('Bar Soap', 'health', None, 'medium', 1.99, 'Classic bar soap'),
    ('Organic Soap', 'health', 'organic', None, 3.99, 'Organic natural soap'),
    ('Antibacterial Soap', 'health', None, None, 2.49, 'Antibacterial hand soap'),
    
    # Health & Beauty - Shampoo
    ('Shampoo', 'health', None, None, 3.99, 'Daily use shampoo'),
    ('Organic Shampoo', 'health', 'organic', None, 6.99, 'Organic natural shampoo'),
    ('Dandruff Shampoo', 'health', None, None, 5.99, 'Anti-dandruff shampoo'),
    
    # Frozen - Vegetables
    ('Frozen Broccoli', 'frozen', None, None, 2.49, 'Frozen broccoli florets'),
    ('Frozen Mixed Vegetables', 'frozen', None, None, 2.99, 'Frozen veggie mix'),
    ('Organic Frozen Vegetables', 'frozen', 'organic', None, 4.49, 'Organic frozen vegetables'),
    
    # Frozen - Pizza
    ('Frozen Pizza', 'frozen', None, 'medium', 4.99, 'Frozen cheese pizza'),
    ('Premium Frozen Pizza', 'frozen', None, 'large', 7.99, 'Gourmet frozen pizza'),
    ('Budget Pizza', 'frozen', 'budget', None, 2.99, 'Budget frozen pizza'),
    
    # Frozen - Ice Cream
    ('Vanilla Ice Cream', 'frozen', None, 'large', 4.99, 'Classic vanilla ice cream'),
    ('Organic Ice Cream', 'frozen', 'organic', None, 6.99, 'Organic premium ice cream'),
    ('Chocolate Ice Cream', 'frozen', None, None, 5.49, 'Rich chocolate ice cream'),
    
    # Additional Items
    ('Honey', 'pantry', None, None, 5.99, 'Pure honey jar'),
    ('Olive Oil', 'pantry', None, None, 7.99, 'Extra virgin olive oil'),
    ('Peanut Butter', 'pantry', None, None, 3.99, 'Creamy peanut butter'),
    ('Jam', 'pantry', None, None, 2.99, 'Fruit jam assorted'),
    ('Coffee', 'beverages', None, None, 6.99, 'Ground coffee beans'),
    ('Tea', 'beverages', None, None, 3.99, 'Herbal tea variety'),
    ('Eggs', 'dairy', None, None, 3.49, 'Dozen eggs'),
    ('Salmon', 'meat', None, None, 12.99, 'Fresh salmon fillet'),
    ('Tuna', 'meat', None, None, 3.99, 'Canned tuna'),
    ('Olive Oil Spray', 'pantry', None, None, 4.49, 'Cooking spray olive oil'),
    ('Butter', 'dairy', None, None, 4.99, 'Salted butter'),
    ('Carrots', 'produce', None, None, 0.99, 'Fresh carrots per lb'),
    ('Broccoli', 'produce', None, None, 2.49, 'Fresh broccoli head'),
    ('Spinach', 'produce', None, None, 2.99, 'Fresh baby spinach'),
    ('Garlic', 'produce', None, None, 0.99, 'Garlic bulbs'),
    ('Onions', 'produce', None, None, 0.79, 'Yellow onions per lb'),
    ('Potatoes', 'produce', None, None, 1.49, 'Russet potatoes per lb'),
    ('Corn', 'frozen', None, None, 1.99, 'Frozen corn kernels'),
    ('Peas', 'frozen', None, None, 1.99, 'Frozen peas'),
    
    # Additional Produce
    ('Bell Peppers Red', 'produce', None, None, 2.49, 'Fresh red bell peppers'),
    ('Bell Peppers Green', 'produce', None, None, 1.99, 'Fresh green bell peppers'),
    ('Bell Peppers Yellow', 'produce', None, None, 2.29, 'Fresh yellow bell peppers'),
    ('Cucumbers', 'produce', None, None, 1.49, 'Fresh cucumbers'),
    ('Zucchini', 'produce', None, None, 1.99, 'Fresh zucchini squash'),
    ('Mushrooms', 'produce', None, None, 3.99, 'Fresh mushrooms 1 lb'),
    ('Strawberries', 'produce', None, 'medium', 4.99, 'Fresh strawberries'),
    ('Blueberries', 'produce', None, 'medium', 5.99, 'Fresh blueberries'),
    ('Raspberries', 'produce', None, 'small', 4.49, 'Fresh raspberries'),
    ('Grapes Red', 'produce', None, None, 3.49, 'Fresh red grapes'),
    ('Grapes Green', 'produce', None, None, 3.49, 'Fresh green grapes'),
    ('Watermelon', 'produce', None, 'large', 5.99, 'Fresh watermelon'),
    ('Cantaloupe', 'produce', None, None, 3.99, 'Fresh cantaloupe'),
    ('Pineapple', 'produce', None, 'large', 4.99, 'Fresh pineapple'),
    ('Mango', 'produce', None, None, 2.99, 'Fresh mango tropical fruit'),
    ('Avocado', 'produce', None, None, 2.49, 'Fresh ripe avocado'),
    ('Limes', 'produce', None, None, 0.99, 'Fresh limes per lb'),
    ('Lemons', 'produce', None, None, 1.49, 'Fresh lemons'),
    ('Ginger', 'produce', None, None, 2.99, 'Fresh ginger root'),
    ('Celery', 'produce', None, None, 2.49, 'Fresh celery bunch'),
    
    # Additional Dairy
    ('Cottage Cheese', 'dairy', None, 'large', 3.99, 'Cottage cheese container'),
    ('Sour Cream', 'dairy', None, 'medium', 2.49, 'Sour cream'),
    ('Cream Cheese', 'dairy', None, None, 3.49, 'Cream cheese 8 oz'),
    ('Feta Cheese', 'dairy', None, None, 5.99, 'Crumbled feta cheese'),
    ('Goat Cheese', 'dairy', None, None, 6.99, 'Fresh goat cheese'),
    ('Butter Salted', 'dairy', None, None, 4.99, 'Salted butter 1 lb'),
    ('Butter Unsalted', 'dairy', None, None, 5.49, 'Unsalted butter 1 lb'),
    ('Heavy Cream', 'dairy', None, None, 3.99, 'Heavy whipping cream'),
    ('Evaporated Milk', 'dairy', None, 'medium', 1.99, 'Evaporated milk'),
    ('Condensed Milk', 'dairy', None, 'medium', 1.99, 'Sweetened condensed milk'),
    
    # Additional Meat
    ('Turkey Breast', 'meat', None, None, 8.99, 'Fresh turkey breast'),
    ('Ground Turkey', 'meat', None, None, 5.99, 'Lean ground turkey'),
    ('Lamb Chops', 'meat', None, None, 11.99, 'Fresh lamb chops'),
    ('Duck Breast', 'meat', None, None, 9.99, 'Fresh duck breast'),
    ('Bacon', 'meat', None, None, 5.99, 'Crispy bacon 1 lb'),
    ('Sausage', 'meat', None, None, 4.99, 'Pork sausage links'),
    ('Hot Dogs', 'meat', None, None, 3.99, 'Hot dog franks pack'),
    ('Deli Turkey', 'meat', None, None, 5.99, 'Sliced deli turkey'),
    ('Deli Ham', 'meat', None, None, 5.99, 'Sliced deli ham'),
    ('Ground Lamb', 'meat', None, None, 9.99, 'Ground lamb 1 lb'),
    
    # Additional Pantry
    ('Cereal Cornflakes', 'pantry', None, 'large', 3.99, 'Corn flakes cereal'),
    ('Oatmeal', 'pantry', None, 'large', 4.49, 'Quick oats container'),
    ('Granola', 'pantry', 'organic', None, 5.99, 'Organic granola cereal'),
    ('Flour All-Purpose', 'pantry', None, 'large', 3.49, 'All-purpose flour 5 lb'),
    ('Flour Whole Wheat', 'pantry', None, 'large', 4.49, 'Whole wheat flour'),
    ('Sugar White', 'pantry', None, 'large', 2.99, 'Granulated sugar'),
    ('Brown Sugar', 'pantry', None, None, 2.99, 'Brown sugar'),
    ('Baking Powder', 'pantry', None, None, 2.49, 'Baking powder canister'),
    ('Baking Soda', 'pantry', None, None, 1.99, 'Baking soda box'),
    ('Vanilla Extract', 'pantry', None, None, 6.99, 'Pure vanilla extract'),
    ('Bean Black', 'pantry', None, 'large', 1.99, 'Canned black beans'),
    ('Bean Kidney', 'pantry', None, 'large', 1.99, 'Canned kidney beans'),
    ('Bean Pinto', 'pantry', None, 'large', 1.99, 'Canned pinto beans'),
    ('Chickpeas', 'pantry', None, None, 1.99, 'Canned chickpeas'),
    ('Lentils', 'pantry', None, 'large', 2.49, 'Dried lentils'),
    ('Tomato Sauce', 'pantry', None, None, 1.49, 'Tomato sauce jar'),
    ('Tomato Paste', 'pantry', None, None, 1.99, 'Tomato paste tube'),
    ('Peanut Butter Creamy', 'pantry', None, 'large', 3.99, 'Creamy peanut butter'),
    ('Peanut Butter Crunchy', 'pantry', None, 'large', 3.99, 'Crunchy peanut butter'),
    ('Almond Butter', 'pantry', 'organic', None, 6.99, 'Organic almond butter'),
    
    # Additional Beverages
    ('Milk Chocolate', 'beverages', None, 'large', 3.99, 'Chocolate milk'),
    ('Coffee Ground', 'beverages', None, 'large', 6.99, 'Ground coffee 1 lb'),
    ('Coffee Instant', 'beverages', None, None, 5.99, 'Instant coffee'),
    ('Tea Black', 'beverages', None, None, 3.49, 'Black tea bags'),
    ('Tea Green', 'beverages', None, None, 4.49, 'Green tea bags'),
    ('Tea Chamomile', 'beverages', None, None, 3.99, 'Chamomile tea bags'),
    ('Lemonade', 'beverages', None, 'large', 2.99, 'Fresh lemonade'),
    ('Iced Coffee', 'beverages', None, 'large', 4.99, 'Bottled iced coffee'),
    ('Kombucha', 'beverages', 'organic', None, 3.49, 'Fermented kombucha drink'),
    ('Energy Drink', 'beverages', None, None, 2.49, 'Energy drink'),
    
    # Additional Snacks
    ('Granola Bar', 'snacks', None, None, 0.99, 'Granola bar single'),
    ('Protein Bar', 'snacks', None, None, 1.49, 'Protein bar pack'),
    ('Crackers Cheese', 'snacks', None, None, 2.99, 'Cheese flavored crackers'),
    ('Crackers Saltine', 'snacks', 'budget', None, 1.99, 'Saltine crackers'),
    ('Popcorn', 'snacks', None, None, 2.49, 'Microwave popcorn pack'),
    ('Pretzels', 'snacks', None, None, 2.99, 'Salted pretzels'),
    ('Trail Mix', 'snacks', None, None, 4.99, 'Nuts and raisins trail mix'),
    ('Beef Jerky', 'snacks', None, None, 5.99, 'Beef jerky 3 oz'),
    ('Dried Fruit', 'snacks', None, None, 4.49, 'Mixed dried fruit'),
    ('Candy Chocolate', 'snacks', None, None, 1.49, 'Chocolate candy bar'),
    
    # Additional Health & Beauty
    ('Deodorant', 'health', None, None, 3.49, 'Deodorant stick'),
    ('Shaving Cream', 'health', None, None, 2.99, 'Shaving cream gel'),
    ('Razor Blades', 'health', None, None, 5.99, 'Razor blade pack'),
    ('Lip Balm', 'health', None, None, 1.99, 'Lip balm stick'),
    ('Face Wash', 'health', None, None, 3.99, 'Face wash cleanser'),
    ('Hand Lotion', 'health', None, None, 2.99, 'Hand lotion pump'),
    ('Body Wash', 'health', None, None, 3.49, 'Body wash shower gel'),
    ('Conditioner', 'health', None, None, 3.99, 'Hair conditioner'),
    ('Hair Gel', 'health', None, None, 3.49, 'Hair styling gel'),
    ('Mouthwash', 'health', None, None, 2.99, 'Mouthwash bottle'),
    
    # Specialty/International
    ('Pasta Sauce', 'pantry', None, None, 2.49, 'Italian pasta marinara sauce'),
    ('Soy Sauce', 'pantry', None, None, 3.99, 'Soy sauce bottle'),
    ('Worcestershire Sauce', 'pantry', None, None, 3.49, 'Worcestershire sauce'),
    ('Hot Sauce', 'pantry', None, None, 2.99, 'Spicy hot sauce'),
    ('Salsa', 'pantry', None, None, 2.99, 'Fresh salsa jar'),
    ('Hummus', 'pantry', None, None, 3.99, 'Chickpea hummus'),
    ('Guacamole', 'pantry', None, None, 4.99, 'Fresh guacamole'),
    ('BBQ Sauce', 'pantry', None, None, 2.49, 'BBQ sauce bottle'),
    ('Mustard', 'pantry', None, None, 2.29, 'Yellow mustard'),
    ('Mayonnaise', 'pantry', None, None, 3.99, 'Mayonnaise large jar'),
    ('Ketchup', 'pantry', None, None, 2.99, 'Tomato ketchup bottle'),
    ('Vinegar Apple Cider', 'pantry', None, None, 3.99, 'Apple cider vinegar'),
    
    # More Frozen Items
    ('Frozen Fries', 'frozen', None, 'large', 3.49, 'Frozen french fries'),
    ('Frozen Chicken Nuggets', 'frozen', None, 'large', 4.99, 'Frozen chicken nuggets'),
    ('Frozen Fish Sticks', 'frozen', None, None, 4.49, 'Frozen fish sticks'),
    ('Frozen Vegetables Alfredo', 'frozen', None, None, 3.99, 'Frozen vegetables in alfredo'),
    ('Frozen Burritos', 'frozen', None, None, 5.99, 'Frozen burritos pack'),
    ('Frozen Waffles', 'frozen', None, None, 3.49, 'Frozen waffles box'),
    ('Frozen Pancakes', 'frozen', None, None, 3.49, 'Frozen pancakes box'),
    
    # Condiments
    ('Relish', 'pantry', None, None, 2.49, 'Pickle relish jar'),
    ('Pickles Dill', 'pantry', None, 'large', 2.99, 'Dill pickle jar'),
    ('Pickles Sweet', 'pantry', None, 'large', 2.99, 'Sweet pickle jar'),
    ('Capers', 'pantry', None, None, 3.99, 'Caper berries jar'),
    ('Olives Green', 'pantry', None, None, 3.49, 'Green olives jar'),
    ('Olives Black', 'pantry', None, None, 3.49, 'Black olives jar'),
    ('Coconut Oil', 'pantry', 'organic', None, 7.99, 'Organic coconut oil'),
    ('Sesame Oil', 'pantry', None, None, 5.99, 'Sesame seed oil'),
    ('Balsamic Vinegar', 'pantry', None, None, 4.99, 'Balsamic vinegar'),
    
    # Baking Items
    ('Chocolate Chips', 'pantry', None, None, 2.99, 'Chocolate chips bag'),
    ('Sprinkles Rainbow', 'pantry', None, None, 2.49, 'Rainbow cake sprinkles'),
    ('Nuts Walnuts', 'pantry', None, 'large', 6.99, 'Walnuts 1 lb'),
    ('Nuts Pecans', 'pantry', None, 'large', 7.99, 'Pecans 1 lb'),
    ('Nuts Cashews', 'pantry', None, 'large', 8.99, 'Cashews 1 lb'),
    ('Cocoa Powder', 'pantry', None, None, 3.99, 'Cocoa powder'),
    ('Maple Syrup', 'pantry', 'organic', None, 7.99, 'Pure maple syrup'),
    ('Corn Syrup', 'pantry', None, None, 2.99, 'Light corn syrup'),
    
    # Spices/Seasonings
    ('Black Pepper', 'pantry', None, None, 2.99, 'Ground black pepper'),
    ('Sea Salt', 'pantry', None, None, 2.49, 'Sea salt container'),
    ('Garlic Powder', 'pantry', None, None, 2.99, 'Garlic powder'),
    ('Onion Powder', 'pantry', None, None, 2.99, 'Onion powder'),
    ('Italian Seasoning', 'pantry', None, None, 3.49, 'Italian herb seasoning'),
    ('Paprika', 'pantry', None, None, 3.49, 'Paprika powder'),
    ('Cumin', 'pantry', None, None, 3.99, 'Ground cumin'),
    ('Cinnamon', 'pantry', None, None, 2.99, 'Ground cinnamon'),
    ('Thyme', 'pantry', None, None, 2.99, 'Dried thyme'),
    ('Oregano', 'pantry', None, None, 2.99, 'Dried oregano'),
]

def populate_grocery_items():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Clear existing items
    cursor.execute('DELETE FROM grocery_items')
    
    # Insert sample items
    for item in SAMPLE_ITEMS:
        cursor.execute('''
            INSERT INTO grocery_items (item_name, category, brand, size, price, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', item)
    
    conn.commit()
    conn.close()
    print(f"Successfully populated {len(SAMPLE_ITEMS)} grocery items")

if __name__ == '__main__':
    populate_grocery_items()

