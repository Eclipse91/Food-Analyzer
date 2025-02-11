from sqlalchemy import create_engine, Column, String, Float, Integer, MetaData, Table

class FoodDatabase:
    def __init__(self, db_path="food_components.db"):
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{self.db_path}")
        self.metadata = MetaData()

    def define_columns(self):
        """Define columns in the table, including 'Food' as the main identifier column."""
        self.columns = [
            ("Food", String),  # Main identifier column

            # Energy
            ("Energy", Float),  # Energy: Total energy content of the food, typically measured in **kilocalories (kcal)** or **kilojoules (kJ)**.
            ("Energy (Atwater General Factors)", Float),  # Energy (Atwater General Factors): Energy calculated using the **Atwater general factors** for protein, carbohydrate, and fat (4 kcal/g for protein and carbs, 9 kcal/g for fat).
            ("Energy (Atwater Specific Factors)", Float),  # Energy (Atwater Specific Factors): Energy calculated using **specific Atwater factors**, accounting for the unique energy content of different foods or food groups.

            # Macronutrients
            ("Protein", Float),  # Protein: An essential macronutrient important for **tissue repair**, **enzyme activity**, and **muscle building**. Found in **meat**, **beans**, **eggs**, and **dairy**.
            ("Total lipid (fat)", Float),  # Total Lipid (Fat): The total amount of fat in the food. **Fats** are important for **energy storage**, **insulation**, and **cell function**. Sources include **butter**, **oils**, **nuts**, and **avocados**.
            ("Carbohydrate, by difference", Float),  # Carbohydrate (by difference): Calculated by subtracting protein, fat, and moisture content from total food weight. Carbs are the primary source of **quick energy** and are found in **grains**, **fruits**, and **vegetables**.
            
            # Dietary Fiber
            ("Total dietary fiber (AOAC 2011.25)", Float),  # Total Dietary Fiber (AOAC 2011.25): The total amount of fiber, as measured by the **AOAC method**, including both soluble and insoluble fibers. Important for **digestive health** and **blood sugar regulation**.
            ("Fiber, total dietary", Float),  # Total Dietary Fiber: Overall amount of fiber in food, vital for **gut health**, **regular bowel movements**, and **heart health**.
            ("Fiber, insoluble", Float),  # Insoluble Fiber: A type of fiber that does not dissolve in water, helping to **promote regularity** and prevent constipation. Found in **whole grains**, **vegetables**, and **seeds**.
            ("Fiber, soluble", Float),  # Soluble Fiber: Dissolves in water and can help **lower cholesterol** and **stabilize blood sugar levels**. Found in **oats**, **beans**, **fruits**, and **vegetables**.

            # Sugars
            ("Sugars, Total", Float),  # Sugars (Total): The total amount of all sugars in food, including both naturally occurring sugars (e.g., in fruits) and added sugars (e.g., in sweets). Important for **quick energy** but should be consumed in moderation.
            ("Total Sugars", Float),  # Total Sugars: Same as "Sugars, Total". A measure of the total **natural and added sugars** present.
            ("Fructose", Float),  # Fructose: A naturally occurring sugar found in **fruits** and **honey**. It's a **simple sugar** (monosaccharide) and an important energy source.
            ("Glucose", Float),  # Glucose: A simple sugar and the **primary energy source** for the body, especially for the **brain** and **muscles**. Found in **fruits**, **vegetables**, and is the main component of **blood sugar**.
            ("Lactose", Float),  # Lactose: A disaccharide sugar found in **milk** and **dairy products**. It is broken down by the enzyme **lactase** in the digestive system.
            ("Maltose", Float),  # Maltose: A disaccharide made of two glucose units, formed during **starch digestion**. Found in **malted barley** and **beer**.
            ("Sucrose", Float),  # Sucrose: The common **table sugar**, composed of one glucose and one fructose molecule. Found in **sugar cane**, **sugar beets**, and many processed foods.
            ("Galactose", Float),  # Galactose: A monosaccharide that is part of **lactose** in milk. It is converted into glucose in the body to provide **energy**.

            # Minerals
            # Essential Minerals
            ("Iron, Fe", Float),  # Iron (required for oxygen transport in the blood)
            ("Magnesium, Mg", Float),  # Magnesium (important for bone health and muscle function)
            ("Phosphorus, P", Float),  # Phosphorus (essential for bone and cell function)
            ("Potassium, K", Float),  # Potassium (important for muscle and nerve function)
            ("Sodium, Na", Float),  # Sodium (important for fluid balance and nerve transmission)
            ("Zinc, Zn", Float),  # Zinc (important for immune function and wound healing)
            ("Copper, Cu", Float),  # Copper (required for iron metabolism and antioxidant functions)
            ("Calcium, Ca", Float),  # Calcium (critical for bone health and nerve function)
            ("Selenium, Se", Float),  # Selenium (important for antioxidant defense and thyroid function)
            ("Iodine, I", Float),  # Iodine (required for thyroid hormone synthesis)
            ("Manganese, Mn", Float),  # Manganese (important for enzyme function and bone health)
            ("Molybdenum, Mo", Float),  # Molybdenum (important for enzyme function)
            ("Fluoride, F", Float),  # Fluoride (important for bone health and dental health)
            # Non-Essential/Other
            ("Nitrogen", Float),  # Nitrogen (not a dietary mineral, but essential for biological compounds like proteins and nucleic acids)

            # Vitamins
            # Vitamin A and Carotenoids
            ("Vitamin A", Float),  # Vitamin A
            ("Vitamin A, IU", Float),  # Vitamin A (International Units)
            ("Vitamin A, RAE", Float),  # Vitamin A (Retinol Activity Equivalents)
            ("Carotene, alpha", Float),  # Carotenoid (precursor to Vitamin A)
            ("Carotene, beta", Float),  # Carotenoid (precursor to Vitamin A)
            ("Cryptoxanthin, beta", Float),  # Carotenoid (precursor to Vitamin A)
            ("Lutein + zeaxanthin", Float),  # Carotenoids (important for eye health)
            # B-Vitamins
            ("Thiamin", Float),  # Vitamin B1 (Thiamine)
            ("Riboflavin", Float),  # Vitamin B2 (Riboflavin)
            ("Niacin", Float),  # Vitamin B3 (Niacin)
            ("Vitamin B-6", Float),  # Vitamin B6 (Pyridoxine)
            ("Biotin", Float),  # Vitamin B7 (Biotin)
            ("Folate, total", Float),  # Vitamin B9 (Folate)
            ("Folic acid", Float),  # Synthetic form of Vitamin B9
            ("Folate, DFE", Float),  # Vitamin B9 (Dietary Folate Equivalent)
            ("Vitamin B-12", Float),  # Vitamin B12 (Cobalamin)
            ("Vitamin B-12, added", Float),  # Added Vitamin B12
            # Vitamin C
            ("Vitamin C, total ascorbic acid", Float),  # Vitamin C (Ascorbic Acid)
            # Vitamin D
            ("Vitamin D (D2 + D3)", Float),  # Vitamin D (Combined D2 and D3)
            ("Vitamin D2 (ergocalciferol)", Float),  # Vitamin D2
            ("Vitamin D3 (cholecalciferol)", Float),  # Vitamin D3
            ("Vitamin D4", Float),  # Vitamin D4 (less common form of Vitamin D)
            ("Ergosterol", Float),  # Ergosterol (precursor to Vitamin D2 in fungi)
            ("Ergosta-7-enol", Float),  # Ergosterol derivative (related to Vitamin D2 metabolism)
            ("Ergosta-7,22-dienol", Float),  # Ergosterol derivative (related to Vitamin D2 metabolism)
            ("Ergosta-5,7-dienol", Float),  # Ergosterol derivative (related to Vitamin D2 metabolism)
            # Vitamin E
            ("Vitamin E (alpha-tocopherol)", Float),  # Vitamin E (Alpha-Tocopherol)
            ("Vitamin E, added", Float),  # Added Vitamin E
            ("Tocopherol, beta", Float),  # Vitamin E (Beta-Tocopherol)
            ("Tocopherol, gamma", Float),  # Vitamin E (Gamma-Tocopherol)
            ("Tocopherol, delta", Float),  # Vitamin E (Delta-Tocopherol)
            ("Tocotrienol, alpha", Float),  # Vitamin E (Alpha-Tocotrienol)
            ("Tocotrienol, beta", Float),  # Vitamin E (Beta-Tocotrienol)
            ("Tocotrienol, gamma", Float),  # Vitamin E (Gamma-Tocotrienol)
            ("Tocotrienol, delta", Float),  # Vitamin E (Delta-Tocotrienol)
            # Vitamin K
            ("Vitamin K (phylloquinone)", Float),  # Vitamin K1 (Phylloquinone)
            ("Vitamin K (Dihydrophylloquinone)", Float),  # Vitamin K1 (Dihydrophylloquinone, reduced form)
            ("Vitamin K (Menaquinone-4)", Float),  # Vitamin K2 (Menaquinone-4)

            # Amino Acids
            # Essential Amino Acids (cannot be made by the body, must be obtained from food)
            ("Tryptophan", Float),      # Essential
            ("Threonine", Float),       # Essential
            ("Methionine", Float),      # Essential
            ("Phenylalanine", Float),   # Essential
            ("Tyrosine", Float),        # Essential (Tyrosine is synthesized from Phenylalanine)
            ("Isoleucine", Float),      # Essential
            ("Leucine", Float),         # Essential
            ("Lysine", Float),          # Essential
            ("Valine", Float),          # Essential
            # Conditionally Essential Amino Acids (usually non-essential, but become essential under certain conditions like illness or stress)
            ("Cysteine", Float),    # Conditionally Essential (can be synthesized from Methionine)
            # ("Tyrosine", Float),    # Conditionally Essential (can be synthesized from Phenylalanine)
            ("Arginine", Float),    # Conditionally Essential (can be synthesized in the body but may be essential during periods of rapid growth or stress)
            ("Histidine", Float),   # Conditionally Essential (essential for infants, can be synthesized by adults)
            # Non-Essential Amino Acids (can be synthesized by the body)
            ("Alanine", Float),         # Non-Essential
            ("Glutamic acid", Float),   # Non-Essential
            ("Glycine", Float),         # Non-Essential
            ("Proline", Float),         # Non-Essential
            ("Aspartic acid", Float),   # Non-Essential
            ("Serine", Float),          # Non-Essential
            ("Cystine", Float),         # Non-Essential (can be formed by two cysteine molecules)
            ("Hydroxyproline", Float),   # Non-Essential (formed by proline in collagen)
            
            # Lipids & Fats
            ("Cholesterol", Float),  # Cholesterol (essential for hormone production, vitamin D, and bile acids)
            # Saturated Fatty Acids (SFA)
            ("SFA 4:0", Float),  # Saturated Fatty Acid (4 carbon atoms)
            ("SFA 6:0", Float),  # Saturated Fatty Acid (6 carbon atoms)
            ("SFA 8:0", Float),  # Saturated Fatty Acid (8 carbon atoms)
            ("SFA 10:0", Float),  # Saturated Fatty Acid (10 carbon atoms)
            ("SFA 12:0", Float),  # Saturated Fatty Acid (12 carbon atoms)
            ("SFA 14:0", Float),  # Saturated Fatty Acid (14 carbon atoms)
            ("SFA 16:0", Float),  # Saturated Fatty Acid (16 carbon atoms)
            ("SFA 18:0", Float),  # Saturated Fatty Acid (18 carbon atoms)
            ("SFA 20:0", Float),  # Saturated Fatty Acid (20 carbon atoms)
            ("SFA 22:0", Float),  # Saturated Fatty Acid (22 carbon atoms)
            ("SFA 24:0", Float),  # Saturated Fatty Acid (24 carbon atoms)
            # Monounsaturated Fatty Acids (MUFA)
            ("MUFA 14:1", Float),  # Monounsaturated Fatty Acid (14 carbon atoms, 1 double bond)
            ("MUFA 16:1", Float),  # Monounsaturated Fatty Acid (16 carbon atoms, 1 double bond)
            ("MUFA 17:1", Float),  # Monounsaturated Fatty Acid (17 carbon atoms, 1 double bond)
            ("MUFA 18:1", Float),  # Monounsaturated Fatty Acid (18 carbon atoms, 1 double bond) - **Omega-9** (found in olive oil, avocados, almonds)
            ("MUFA 20:1", Float),  # Monounsaturated Fatty Acid (20 carbon atoms, 1 double bond)
            ("MUFA 22:1", Float),  # Monounsaturated Fatty Acid (22 carbon atoms, 1 double bond)
            # Polyunsaturated Fatty Acids (PUFA)
            ("PUFA 18:2", Float),  # Polyunsaturated Fatty Acid (18 carbon atoms, 2 double bonds) - **Omega-6** (found in vegetable oils, nuts, seeds)
            ("PUFA 18:3", Float),  # Polyunsaturated Fatty Acid (18 carbon atoms, 3 double bonds) - **Omega-3** (found in flaxseeds, chia seeds, walnuts, and fatty fish)
            ("PUFA 20:4", Float),  # Polyunsaturated Fatty Acid (20 carbon atoms, 4 double bonds) - **Omega-6** (found in vegetable oils, nuts, seeds)
            # Omega-3 Fatty Acids (important for brain and heart health)
            ("PUFA 22:6 n-3 (DHA)", Float),  # Docosahexaenoic Acid (DHA, omega-3 fatty acid) - **Omega-3** (found in fatty fish, algae, important for brain and eye health)
            ("PUFA 20:5 n-3 (EPA)", Float),  # Eicosapentaenoic Acid (EPA, omega-3 fatty acid) - **Omega-3** (found in fatty fish, anti-inflammatory effects)

            # Organic Acids
            ("Citric acid", Float),  # Citric acid: A naturally occurring acid found in **citrus fruits** like **lemons** and **oranges**. It plays a key role in the **Krebs cycle** for energy production and is also used as a preservative and flavoring agent.
            ("Malic acid", Float),  # Malic acid: Found in **apples** and **other fruits**, it contributes to the **tart taste** of many fruits. It plays a role in the **Krebs cycle** and can be used to help alleviate **muscle fatigue**.
            ("Oxalic acid", Float),  # Oxalic acid: Found in **spinach**, **rhubarb**, and **beets**, it is a compound that can form **oxalate crystals** and impact the absorption of certain minerals like **calcium**. It has an **antioxidant** effect but can cause issues when consumed in high amounts.
            ("Quinic acid", Float),  # Quinic acid: Found in **coffee**, **cranberries**, and **apples**, it is involved in the **synthesis of chlorogenic acid**. It has **antioxidant** properties and may contribute to the health benefits of certain fruits and beverages.
            ("Pyruvic acid", Float),  # Pyruvic acid: A key intermediate in the **Krebs cycle** and part of **glucose metabolism**. It is produced during **glycolysis** and plays a role in converting glucose into energy, supporting **muscle function** and **metabolic processes**.

            # Phytochemicals
            ("Lycopene", Float),  # Lycopene: A carotenoid pigment found in tomatoes, red peppers, and watermelon. Known for its **antioxidant** properties, it may help reduce the risk of certain cancers and heart disease.
            ("trans-Lycopene", Float),  # trans-Lycopene: The more common and bioavailable form of lycopene, found primarily in tomatoes. It has similar **antioxidant** benefits as lycopene.
            ("cis-Lycopene", Float),  # cis-Lycopene: Another isomer of lycopene that can be found in fruits like tomatoes. The cis form is less stable but still provides **antioxidant** benefits.
            ("Beta-sitosterol", Float),  # Beta-sitosterol: A plant sterol found in **vegetable oils**, **nuts**, **seeds**, and **avocados**. Known for its potential to **lower cholesterol** and support **prostate health**.
            ("Campesterol", Float),  # Campesterol: A plant sterol found in **vegetable oils** and **nuts**. It may help reduce **cholesterol levels** and have **anti-inflammatory** effects.
            ("Brassicasterol", Float),  # Brassicasterol: A plant sterol found in **cruciferous vegetables** (e.g., broccoli, cabbage) and some **vegetable oils**. It has potential **anti-inflammatory** and **antioxidant** effects.
            ("Stigmasterol", Float),  # Stigmasterol: Found in **soybeans**, **corn oil**, and **vegetable oils**, this plant sterol is known to help **lower cholesterol** and may have **anti-inflammatory** properties.
            ("Phytosterols", Float),  # Phytosterols: A group of plant compounds found in **vegetable oils**, **nuts**, and **seeds** that help **lower cholesterol** and support **heart health**.
            ("Phytoene", Float),  # Phytoene: A carotenoid that is a precursor to other carotenoids like **beta-carotene**. Found in **fruits** and **vegetables** like **tomatoes** and **carrots**, it has **antioxidant** properties.
            ("Phytofluene", Float),  # Phytofluene: A carotenoid found in **tomatoes**, **watermelon**, and **oranges**, known for its **antioxidant** properties and potential to protect against **sun damage** and **skin aging**.

            # Essential Nutrients
            ("Choline, total", Float),  # Choline (essential for liver and brain function)
            ("Choline, free", Float),  # Free Choline (available form in the body)
            ("Choline, from glycerophosphocholine", Float),  # Choline from glycerophosphocholine
            ("Choline, from phosphotidyl choline", Float),  # Choline from phosphatidylcholine
            ("Choline, from phosphocholine", Float),  # Choline from phosphocholine
            ("Choline, from sphingomyelin", Float),  # Choline from sphingomyelin
            ("Betaine", Float),  # Betaine (derived from choline, involved in liver function)

            # Antioxidants and Other Important Compounds
            ("Glutathione", Float),  # Glutathione (antioxidant, not classified as a vitamin or mineral)
            ("Ergothioneine", Float),  # Ergothioneine (antioxidant, conditionally essential)

            # Hydration and Non-Nutrient Compounds
            ("Water", Float),  # Water (essential for hydration)
            ("Ash", Float),  # Ash (inorganic residue after combustion)

            # Biologically Active Compounds
            ("Alcohol, ethyl", Float),  # Ethanol (provides calories, but not a nutrient)
            ("Caffeine", Float),  # Caffeine (a stimulant, not a nutrient)
            ("Theobromine", Float),  # Theobromine (a stimulant, similar to caffeine)
        ]

    def define_table(self):
        """Define the structure of the foods_data table."""
        self.foods_table = Table(
            "foods_data", self.metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),  # Auto-incrementing ID
            *[Column(name, dtype) for name, dtype in self.columns]  # Add all columns dynamically
        )

    def create_table(self):
        """Create the database and table."""
        self.metadata.create_all(self.engine)

    def run(self):
        """Run the process of defining columns, table, and creating the table."""
        self.define_columns()
        self.define_table()
        self.create_table()

# Create instance of the class and run the process
food_db = FoodDatabase()
food_db.run()
