import json
import os
import re
import tempfile
import time


FRIENDS_FILE = os.path.join(os.path.dirname(__file__), "friends.json")
ID_PATTERN = re.compile(r"^\d{5,20}$")


# تحميل بيانات الأصدقاء من ملف DAJAL/friends.json
def load_friends_store():
    if not os.path.exists(FRIENDS_FILE):
        return {"users": {}}

    with open(FRIENDS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        return {"users": {}}

    data.setdefault("users", {})
    return data


# حفظ البيانات بشكل آمن حتى لا يتلف ملف التخزين أثناء التشغيل
def save_friends_store(data):
    directory = os.path.dirname(FRIENDS_FILE)
    os.makedirs(directory, exist_ok=True)

    fd, temp_path = tempfile.mkstemp(prefix="friends_", suffix=".json", dir=directory)
    with os.fdopen(fd, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    os.replace(temp_path, FRIENDS_FILE)


def normalize_id(value):
    friend_id = str(value).strip()
    if not ID_PATTERN.match(friend_id):
        raise ValueError("invalid_id")
    return friend_id


def add_friend(owner_id, friend_id, name=None):
    owner_id = normalize_id(owner_id)
    friend_id = normalize_id(friend_id)

    if owner_id == friend_id:
        return False, "self"

    data = load_friends_store()
    user_friends = data["users"].setdefault(owner_id, {})

    if friend_id in user_friends:
        return False, "exists"

    user_friends[friend_id] = {
        "id": friend_id,
        "name": name.strip() if name and name.strip() else "",
        "added_at": int(time.time()),
    }
    save_friends_store(data)
    return True, user_friends[friend_id]


def remove_friend(owner_id, friend_id):
    owner_id = normalize_id(owner_id)
    friend_id = normalize_id(friend_id)

    data = load_friends_store()
    user_friends = data["users"].setdefault(owner_id, {})

    if friend_id not in user_friends:
        return False, "missing"

    removed_friend = user_friends.pop(friend_id)
    if not user_friends:
        data["users"].pop(owner_id, None)
    save_friends_store(data)
    return True, removed_friend


def list_friends(owner_id):
    owner_id = normalize_id(owner_id)
    data = load_friends_store()
    friends = data["users"].get(owner_id, {})
    return sorted(friends.values(), key=lambda item: item.get("added_at", 0))


def has_friend(owner_id, friend_id):
    owner_id = normalize_id(owner_id)
    friend_id = normalize_id(friend_id)
    data = load_friends_store()
    return friend_id in data["users"].get(owner_id, {})