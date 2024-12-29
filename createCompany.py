import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("adminsdk.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://noit10-bks-default-rtdb.europe-west1.firebasedatabase.app/"
})

def create_companies_table():
    """Ensure the 'Companies' node exists in the database."""
    ref = db.reference('Companies')
    if not ref.get():
        ref.set({})
        print("'Companies' node initialized in Firebase.")
    else:
        print("'Companies' node already exists in Firebase.")

def register_company(name):
    """Register a company in Firebase."""
    ref = db.reference('Companies')
    companies = ref.get()

    if companies and name in companies.values():
        print(f"Company '{name}' already exists.")
        return

    new_id = len(companies or []) + 1 
    ref.update({str(new_id): name})
    print(f"Company '{name}' registered successfully.")

if __name__ == "__main__":
    create_companies_table()
    company_name = input("Enter the name of the company: ")
    register_company(company_name)
