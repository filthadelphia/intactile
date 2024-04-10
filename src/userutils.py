import inspect
import string
from datetime import datetime, timedelta
from random import choice

from src import jsonutils

active_users = []
    
def gather_user(UserID: int) -> bool:
    return [x for x in jsonutils.load_json('registered.json') if x['UserID'] == UserID]

def plan_info(UserID: int) -> str:
    UserInfo = gather_user(UserID)[0]

    return inspect.cleandoc(f"""
        **Username**: `{UserInfo['User']}`
        **Expiration**: `{UserInfo['Expiration']}`
        **Concurrents**: `{UserInfo['Cons']}` """)

def is_active(UserID: int) -> bool:
    UserInfo = gather_user(UserID)
    if not UserInfo: return False

    UserInfo = UserInfo[0]

    if datetime.strptime(UserInfo['Expiration'], "%Y-%m-%d %H:%M:%S.%f") < datetime.now(): 
        return False

    return True

def is_admin(ctx) -> bool:
    return ctx.author.id in [954411856968167475, 786090352464363558]

def register(message, token: str = None) -> bool:
    if token == None: return "**Proper Usage**: `pk.register <token>`"

    tokenData = jsonutils.load_json("tokens.json")
    userData = jsonutils.load_json("registered.json")

    TokenInfo = [x for x in tokenData if x['Token'] == token]
    if not TokenInfo: return "**Invalid Token**"
    if TokenInfo[0]['Used']: return "**Token Already Used**"
    
    TokenInfo = TokenInfo[0]
    tokenData.remove(TokenInfo)
    TokenInfo['Used'] = True
    tokenData.append(TokenInfo) 

    jsonutils.update_json("Tokens.json", tokenData)

    expiration = str(datetime.now() + timedelta(TokenInfo['Days']))

    [userData.remove(x) for x in userData if x['UserID'] == message.author.id]

    userData.append({
        "User": f"{message.author.name}#{message.author.discriminator}",
        "UserID": message.author.id,
        "Cons": TokenInfo['Concurrents'],
        "Expiration": expiration
    })

    jsonutils.update_json("registered.json", userData)

    return inspect.cleandoc(f"""
        **Register Status**: `Successful`

        **Expiration**: `{expiration}`
        **Concurrents**: `{TokenInfo['Concurrents']}`    """)

def token_gen(days: int = 0, cons: int = 0) -> str:
    if days == 0 or cons == 0: 
        return "**Proper Usage**: `pk.createtoken <days> <cons>`"

    Token = ''.join((choice(string.ascii_uppercase)) for x in range(20)).upper()
    Data = {
        "Token": Token, 
        "Days": days,
        "Concurrents": cons,
        "Used": False
    }

    tokenInfo = jsonutils.load_json("tokens.json")
    tokenInfo.append(Data)
    jsonutils.update_json("tokens.json", tokenInfo)

    return inspect.cleandoc(f"""
        **Token Status**: `Generated`

        **Token**: `{Token}`
        **Concurrents**: `{cons}`
        **Length**: `{days}` """)

