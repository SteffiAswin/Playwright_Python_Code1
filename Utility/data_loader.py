import json

def loadjsonall(path="/Users/apple/Desktop/Playwright_Python/Test_data/user_data.json"):
    with open(path) as f:
        return json.load(f)["users"]
    
    
def selecteduser(path="/Users/apple/Desktop/Playwright_Python/Test_data/user_data.json", usernames="none"):
    with open(path) as f:
        users = json.load(f)["users"]
        return [a for a in users if a["username"] in usernames]

    