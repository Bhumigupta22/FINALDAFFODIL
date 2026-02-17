from flask import Flask
from flask_cors import CORS
import os
import pandas as pd
from app.database import init_db, get_purchase_history

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # 1. Database initialize karein
    init_db()
    
    # 2. Apriori Model Training Logic
    try:
        from app.apriori import engine
        
        # Dataset ki path set karein (backend folder ke andar)
        csv_path = os.path.join(os.path.dirname(app.root_path), 'Groceries_dataset.csv')
        
        if os.path.exists(csv_path):
            print("Dataset mil gaya! AI train ho raha hai (Baskets banaye ja rahe hain)...")
            df = pd.read_csv(csv_path)
            
            # Member aur Date ke hisab se grouping (Baskets)
            baskets = df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list).tolist()
            
            # AI ko dataset sikhayein
            engine.fit(baskets, min_support=0.0005, min_confidence=0.05)
            print(f"✅ Apriori model loaded with {len(engine.rules)} rules from Dataset")
        else:
            print("Warning: Groceries_dataset.csv nahi mila! Purani history use ho rahi hai.")
            history = get_purchase_history()
            if history:
                transactions = [[h['item_name'].lower()] for h in history]
                engine.fit(transactions, min_support=0.001, min_confidence=0.1)
                print(f"Apriori loaded with {len(engine.rules)} rules from Database")
            
    except Exception as e:
        print(f"Warning: Apriori initialize nahi ho paya: {e}")
    
    # 3. Blueprints (Routes) Register karein
    # Dhyaan dein: apriori_routes ke andar 'bp' variable hona chahiye
    from app.routes import shopping_routes, voice_routes, suggestion_routes, apriori_routes
    
    app.register_blueprint(shopping_routes.bp)
    app.register_blueprint(voice_routes.bp)
    app.register_blueprint(suggestion_routes.bp)
    app.register_blueprint(apriori_routes.bp)
    
    return app# Routes package
