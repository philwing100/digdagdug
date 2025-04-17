#database creds
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("service_role")

print("🔎 SUPABASE_URL:", SUPABASE_URL)
print("🔐 SUPABASE_KEY:", SUPABASE_KEY[:6] + "..." + SUPABASE_KEY[-4:])


HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def send_sql_query(sql: str):
    url = f"{SUPABASE_URL}/rest/v1/rpc/execute_sql"

    payload = {
        "query": sql
    }

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.ok:
        print("✅ SQL executed successfully")
        return response.json()
    else:
        print("❌ SQL execution failed:", response.text)
        return None
    
    
#Okay so this can execute raw sql on the db    
sql = """
INSERT INTO users (name, city, age)
VALUES ('Alice', 'Dallas', 30)
RETURNING *
"""
#send_sql_query(sql)

def call_stored_proc(name, city, age):
    url = f"{SUPABASE_URL}/rest/v1/rpc/insert_user"

    payload = {
        "name": name,
        "city": city,
        "age": age
    }

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.ok:
        print(f"✅ Stored proc inserted: {name}")
        return response.json()
    else:
        print("❌ Stored proc failed:", response.text)
        return None

#call_stored_proc("Alice", "Dallas", 30)


#Here is the more efficient way to insert users
def insert_bulk_users(records):
    url = f"{SUPABASE_URL}/rest/v1/users"
    
    response = requests.post(url, headers=HEADERS, json=records)
    
    if response.ok:
        print("✅ Bulk insert successful")
    else:
        print("❌ Bulk insert failed:", response.text)
