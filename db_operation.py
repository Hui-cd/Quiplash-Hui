import random
import re
import azure.cosmos as cosmos
import config as cfg
    
client = cosmos.CosmosClient(cfg.settings['db_URI'],cfg.settings['db_key'])
db_client = client.get_database_client(cfg.settings['db_id'])
player_container = db_client.get_container_client(cfg.settings['player_container'])
prompt_container = db_client.get_container_client(cfg.settings['prompt_container'])

def login(username, password):
    query = f"SELECT * FROM c WHERE c.username = '{username}'"
    items = list(player_container.query_items(query=query, enable_cross_partition_query=True))
    if len(items) == 0:
        return False   
    elif items[0]['password'] == password and items[0]['username'] == username:
        return True
    else:
        return False

def check_password(username, password):
    query = f"SELECT * FROM c WHERE c.username = '{username}'"
    items = list(player_container.query_items(query=query, enable_cross_partition_query=True))
    if len(items) == 0:
        return False
    elif password == items[0]['password']:
        return True
    else:
        return False

def check_username(username):
    query = f"SELECT * FROM c WHERE c.username = '{username}'"
    items = list(player_container.query_items(query=query, enable_cross_partition_query=True))
    if len(items) == 0:
        return False
    else:
        return True

def create_player(username, password):
    query = f"SELECT * FROM c "
    items = list(player_container.query_items(query=query, enable_cross_partition_query=True))
    size = len(items)
    id = str(size + 1)
    query_id = f"SELECT * FROM c WHERE c.id = '{id}'"
    items_id = list(player_container.query_items(query=query_id, enable_cross_partition_query=True))
    if id in items_id:
        id = str(get_max_id(items_id) + 1)
    player = {
        'id': id,
        'username': username,
        'password': password,
        'games_played': 0,
        'total_score': 0,
    }
    player_container.create_item(player)
    
def create_prompt(username, text):
    query = f"SELECT * FROM c "
    items = list(prompt_container.query_items(query=query, enable_cross_partition_query=True))
    size = len(items)
    prompt = {
        'id': str(size + 1),
        'username': username,
        'text': text
    }
    prompt_container.create_item(prompt)
    
    
def check_password_len(password):
   
    return 8<=len(password)<=24 

def check_username_len(username):
    return 4<=len(username)<=16

def get_max_id(items):
    max_id = 0
    for item in items:
        if int(item['id']) > max_id:
            max_id = int(item['id'])
    return max_id

def update(username, add_to_games_played, add_to_score):
    query = f"SELECT * FROM c WHERE c.username = '{username}'"
    items = list(player_container.query_items(query=query, enable_cross_partition_query=True))
    if len(items) == 0:
        return False
    else:
        games_played = items[0]['games_played']
        total_score = items[0]['total_score']
        games_played += add_to_games_played
        total_score += add_to_score
        player_container.upsert_item({'id':items[0]['id'],'username':username,'password':items[0]['password'],'games_played':games_played,'total_score':total_score})
        return True



def get_leaderboard(k):
    """
    get the leaderboard of the top k players.
    :param k:
    :return:
    """
    query='SELECT TOP {} p.username,p.games_played,p.total_score FROM players p ORDER BY p.username ASC'.format(k)
    items = list(player_container.query_items(query=query, enable_cross_partition_query=True))
    result = []
    for i in range(k):
        result = result+[{"username": items[i]['username'], "score": items[i]['total_score'],"games_played": items[i]['games_played']}]
    return result   



def edit(id,username,text):
    query = f"SELECT * FROM c WHERE c.id = '{id}' AND c.username = '{username}'"
    items = list(prompt_container.query_items(query=query, enable_cross_partition_query=True))
    text_data = items[0]['text']
    text_data = text
    prompt_container.upsert_item({'id':id,'username':username,'text':text_data})


def check_id(id):
    query = f"SELECT * FROM c WHERE c.id = '{id}'"
    items = list(prompt_container.query_items(query=query, enable_cross_partition_query=True))
    return len(items) == 0



def check_prompt_len(text):
    return 20<=len(text)<=100

def check_prompt(text,username):
    query = f"SELECT * FROM c WHERE c.username = '{username}' AND c.text = '{text}'"
    items = list(prompt_container.query_items(query=query, enable_cross_partition_query=True))
    return len(items) == 0

def get_prompts_by_user(players):
    result = []
    items = []
    for player in players:
        query = f"SELECT * FROM c WHERE c.username = '{player}'"
        items = items+list(prompt_container.query_items(query=query, enable_cross_partition_query=True))
    for i in range(len(items)):
        result = result + [{"id": int(items[i]['id']), "text": items[i]['text'],"username": items[i]['username']}]
    return result

print(get_prompts_by_user(['ci5eh8','yfsq89']))

def getN(n):
    query = f"SELECT * FROM c "
    items = list(prompt_container.query_items(query=query, enable_cross_partition_query=True))
    size = len(items)
    prompt = []
    if n> size:
        random_z = [random.randint(0, size) for i in range(size)]
        for i in random_z:
            prompt = prompt + [{"id": int(items[i]['id']), "text": items[i]['text'],"username": items[i]['username']}]
        return prompt
    else:
        random_n = [random.randint(0, size) for i in range(n)]
        for i in random_n:
            prompt = prompt + [{"id": int(items[i]["id"]), "text": items[i]["text"], "username": items[i]["username"]}]
        return prompt
        

def get_word(word, exact):
    """
    get the word.
    :param word:
    :param exact:
    :return:
    """

    prompts = []
    if exact:
        for prompt in prompt_container.query_items(query='SELECT * FROM c', enable_cross_partition_query=True):
            if len (re.findall(r'\b{}\b'.format(word), prompt['text'])) > 0:
                prompts.append({"id":int(prompt["id"]), "text":prompt["text"], "username":prompt["username"]})
        return prompts
    else:
        for prompt in prompt_container.query_items(query='SELECT * FROM c', enable_cross_partition_query=True):
            if len (re.findall(r'\b{}\b'.format(word), prompt['text'],re.IGNORECASE)) > 0:
                prompts.append({"id":int(prompt["id"]), "text":prompt["text"], "username":prompt["username"]})
        return prompts

def create_prompt(username, text):
    query = f"SELECT * FROM c "
    items = list(prompt_container.query_items(query=query, enable_cross_partition_query=True))
    size = len(items)
    prompt = {
        'id': str(size + 1),
        'username': username,
        'text': text
    }
    prompt_container.create_item(prompt)
    
def check_id_user(id, username):
    """
    check if the id is valid.
    :param id:
    :param username:
    :return:
    """
    query = f"SELECT * FROM c WHERE c.id = '{id}' AND c.username = '{username}'"
    items = list(prompt_container.query_items(query=query, enable_cross_partition_query=True))
    return len(items) == 0

def delete_prompt(id, username):
    """
    delete a prompt.
    :param id:
    :param username:
    :return:
    """
    query = f"SELECT * FROM c WHERE c.id = '{id}' AND c.username = '{username}'"
    items = list(prompt_container.query_items(query=query, enable_cross_partition_query=True))
    prompt_container.delete_item(items[0] ,id)
