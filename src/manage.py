from typing import List

from data.attack import Attack

activeAttacks: List[Attack] = []
loopingAttacks: List[Attack] = []

def users_attacks(userID: int) -> List[Attack]:
    return [x for x in activeAttacks if x.UserID == userID]

def get_attacks() -> List[Attack]:
    return activeAttacks

def get_attack(atk: Attack) -> Attack or bool:
    query = [x for x in activeAttacks if x.IP == atk.IP]
    return query if len(query) > 0 else False

def new_attack(atk: Attack) -> str:
    activeAttacks.append(atk)

def stop_attack(atk: Attack) -> str:
    activeAttacks.remove(atk)

def loop_kill(atk: Attack) -> str:
    query = get_attack(atk)
    if not query: return "**Unable to stop what you're looking for**: `Host not actively running`"

    loopingAttacks.remove(query)
    return f"**Removed from loop**: {atk.IP}:{atk.Port}"

def stop_all() -> str:
    activeAttacks.clear()
    loopingAttacks.clear()


