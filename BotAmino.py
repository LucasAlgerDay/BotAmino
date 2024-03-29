from time import sleep as slp
from sys import exit
from json import dumps, load, loads
from pathlib import Path
from threading import Thread
from contextlib import suppress
from unicodedata import normalize
from string import punctuation
from random import choice
# from datetime import datetime
#from aminofix import Client, SubClient, ACM, objects
#from amino import Client, SubClient, ACM, objects
from aminoli import Client, SubClient, ACM, objects
from uuid import uuid4
from inspect import getfullargspec
from urllib.request import urlopen
# from zipfile import ZipFile
import requests
import time

# check if push works
# this is Slimakoi's API with some of my patches
# Modified by vedansh#4039
# API made by ThePhoenix78
# Big optimisation thanks to SempreLEGIT#1378 ♥


path_utilities = "utilities"
path_amino = f'{path_utilities}/amino_list'
path_client = "client.txt"
NoneType = type(None)


with suppress(Exception):
    for i in (path_utilities, path_amino):
        Path(i).mkdir(exist_ok=True)


def print_exception(exc):
    print(repr(exc))


class Command:
    def __init__(self):
        self.commands = {}
        self.conditions = {}

    def execute(self, commande, data, type: str = "command"):
        com = self.commands[type][commande]
        arg = getfullargspec(com).args
        arg.pop(0)
        s = len(arg)
        dico = {}
        if s:
            dico = {key: value for key, value in zip(arg, data.message.split()[0:s])}

        if self.conditions[type].get(commande, None):
            if self.conditions[type][commande](data):
                return self.commands[type][commande](data, **dico)
            return
        return self.commands[type][commande](data, **dico)

    def categorie_exist(self, type: str):
        return type in self.commands.keys()

    def add_categorie(self, type):
        if type not in self.commands.keys():
            self.commands[type] = {}

    def add_condition(self, type):
        if type not in self.conditions.keys():
            self.conditions[type] = {}

    def commands_list(self):
        return [command for command in self.commands["command"].keys()]

    def answer_list(self):
        return [command for command in self.commands["answser"].keys()]

    def command(self, name=None, condition=None):
        type = "command"
        self.add_categorie(type)
        self.add_condition(type)
        if isinstance(name, str):
            name = [name]
        elif not name:
            name = []

        def add_command(command_funct):
            name.append(command_funct.__name__)
            if callable(condition):
                for command in name:
                    self.conditions[type][command] = condition
            for command in name:
                self.commands[type][command.lower()] = command_funct
            return command_funct

        return add_command

    def answer(self, name, condition=None):
        type = "answer"
        self.add_categorie(type)
        self.add_condition(type)

        if isinstance(name, str):
            name = [name]
        elif not name:
            name = []

        def add_command(command_funct):
            # name.append(command_funct.__name__)
            if callable(condition):
                for command in name:
                    self.conditions[type][command] = condition

            for command in name:
                self.commands[type][command.lower()] = command_funct
            return command_funct

        return add_command

    def on_member_join_chat(self, condition=None):
        type = "on_member_join_chat"
        self.add_categorie(type)
        self.add_condition(type)

        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(command_funct):
            self.commands[type][type] = command_funct
            return command_funct
        return add_command

    def on_member_leave_chat(self, condition=None):
        type = "on_member_leave_chat"
        self.add_categorie(type)
        self.add_condition(type)
        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(command_funct):
            self.commands[type][type] = command_funct
            return command_funct
        return add_command

    def on_member_join_amino(self, condition=None):
        type = "on_member_join_amino"
        self.add_categorie(type)
        self.add_condition(type)

        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(command_funct):
            self.commands[type][type] = command_funct
            return command_funct
        return add_command

    def on_message(self, condition=None):
        type = "on_message"
        self.add_categorie(type)
        self.add_condition(type)
        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(command_funct):
            self.commands[type][type] = command_funct
            return command_funct
        return add_command

    def on_other(self, condition=None):
        type = "on_other"
        self.add_categorie(type)
        self.add_condition(type)
        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(command_funct):
            self.commands[type][type] = command_funct
            return command_funct
        return add_command

    def on_remove(self, condition=None):
        type = "on_remove"
        self.add_categorie(type)
        self.add_condition(type)
        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(command_funct):
            self.commands[type][type] = command_funct
            return command_funct
        return add_command

    def on_tip_coin(self, condition=None):
        type = "on_tip_coin"
        self.add_categorie(type)
        self.add_condition(type)
        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(command_funct):
            self.commands[type][type] = command_funct
            return command_funct
        return add_command
    
    def on_invite_chat(self, condition=None):
        type = "on_invite_chat"
        self.add_categorie(type)
        self.add_condition(type)
        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(command_funct):
            self.commands[type][type] = command_funct
            return command_funct
        return add_command
    
    def on_call_channel(self, condition=None):
        type = "on_call_channel"
        self.add_categorie(type)
        self.add_condition(type)
        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(command_funct):
            self.commands[type][type] = command_funct
            return command_funct
        return add_command

    def on_all(self, condition=None):
        type = "on_all"
        self.add_categorie(type)
        self.add_condition(type)
        if callable(condition):
            self.conditions[type][type] = condition

        def add_command(command_funct):
            self.commands[type][type] = command_funct
            return command_funct
        return add_command

    def on_event(self, name, condition=None):
        type = "on_event"
        self.add_categorie(type)
        self.add_condition(type)

        if isinstance(name, str):
            name = [name]
        elif not name:
            name = []

        def add_command(command_funct):
            # name.append(command_funct.__name__)
            if callable(condition):
                for command in name:
                    self.conditions[type][command] = condition

            for command in name:
                self.commands[type][command] = command_funct
            return command_funct

        return add_command


class TimeOut:
    users_dict = {}

    def time_user(self, uid, end: int = 5):
        if uid not in self.users_dict.keys():
            self.users_dict[uid] = {"start": 0, "end": end}
            Thread(target=self.timer, args=[uid]).start()

    def timer(self, uid):
        while self.users_dict[uid]["start"] <= self.users_dict[uid]["end"]:
            self.users_dict[uid]["start"] += 1
            slp(1)
        del self.users_dict[uid]

    def timed_out(self, uid):
        if uid in self.users_dict.keys():
            return self.users_dict[uid]["start"] >= self.users_dict[uid]["end"]
        return True


class BannedWords:
    def filtre_message(self, message, code):
        para = normalize('NFD', message).encode(code, 'ignore').decode("utf8").strip().lower()
        para = para.translate(str.maketrans("", "", punctuation))
        return para

    def check_banned_words(self, args, staff=True):
        for word in ("ascii", "utf8"):
            with suppress(Exception):
                para = self.filtre_message(args.message, word).split()
                if para != [""]:
                    with suppress(Exception):
                        for elem in para:
                            if elem in args.subClient.banned_words:
                                args.subClient.delete_message(args.chatId, args.messageId, reason=f"Banned word : {elem}\nAuthor : {args.author}", asStaff=staff)
                                return


class Parameters:
    __slots__ = (
                    "subClient", "chatId", "authorId", "author", "message", "messageId", "level", "reputation", "json",
                    "authorIcon", "comId", "replySrc", "replyMsg", "replyId", "info", "replyAuthor", "mentions", "role", "replyinfo", "replyNickname", "replyIcon"
                 )

    def __init__(self, data: objects.Event, subClient):
        self.subClient = subClient
        self.chatId = data.message.chatId
        self.authorId = data.message.author.userId
        self.author = data.message.author.nickname
        self.message = data.message.content
        self.messageId = data.message.messageId
        self.authorIcon = data.message.author.icon
        self.role = data.message.author.role
        try: self.level = data.message.author.level
        except: pass
        try: self.json = data.message.json
        except: pass
        try: self.reputation = data.message.author.reputation
        except: pass
        self.comId = data.comId

        self.replySrc = None
        self.replyId = None
        if data.message.extensions and data.message.extensions.get('replyMessage', None) and data.message.extensions['replyMessage'].get('mediaValue', None):
            self.replySrc = data.message.extensions['replyMessage']['mediaValue'].replace('_00.', '_hq.')
            self.replyId = data.message.extensions['replyMessage']['messageId']

        self.replyMsg = None
        if data.message.extensions and data.message.extensions.get('replyMessage', None) and data.message.extensions['replyMessage'].get('content', None):
            self.replyMsg = data.message.extensions['replyMessage']['content']
            self.replyId = data.message.extensions['replyMessage']['messageId']



        self.replyAuthor = None
        self.replyNickname = None
        self.replyIcon = None
        if data.message.extensions and data.message.extensions.get('replyMessage', None):
            self.replyAuthor = data.message.extensions['replyMessage']['author']['uid']
            self.replyNickname = data.message.extensions['replyMessage']['author']['nickname']
            self.replyIcon = data.message.extensions['replyMessage']['author']['icon']


        self.replyinfo = None
        if data.message.extensions:
            self.replyinfo = data.message.extensions


        self.mentions = None
        if data.message.extensions and data.message.extensions.get('mentionedArray', None):
            lista = []
            users = data.message.extensions["mentionedArray"]
            for user in users: lista.append(user["uid"])
            self.mentions = lista



        self.info: objects.Event = data


class BotAmino(Command, Client, TimeOut, BannedWords):
    def __init__(self, email: str = None, password: str = None, sid: str = None, deviceId: str = None, proxies: str = None, certificatePath: str = None, bot_name: str = "Bot", types: str = "Login", barra_color: str = "FFFFFF", fondo_barra: str = "FFFFFF", color_texto: str = "FFFFFF", background_api: str = "", embed_image: str = "", kemoji: list = [""], autoanswer: str = "Hi"):
        Command.__init__(self)
        Client.__init__(self, deviceId=deviceId, certificatePath=certificatePath, proxies=proxies)

        if types.lower() == "login":
            if email and password:
                self.login(email=email, password=password, device = deviceId)
            elif sid:
                self.login_sid(SID=sid)
            else:
                try:
                    with open(path_client, "r") as file_:
                        para = file_.readlines()
                    self.login(email=para[0].strip(), password=para[1].strip(), device=para[2].strip())
                except FileNotFoundError:
                    with open(path_client, 'w') as file_:
                        file_.write('email\npassword\ndevice')
                    print("Please enter your email, password and deviceId in the file client.txt")
                    print("-----end-----")
                    exit(1)
        elif types.lower() == "logout":
            self.logout()
        else:
            print("Only you can set 'login' or 'logout'")

        self.communaute = {}
        self.botId = self.userId
        self.len_community = 0
        self.perms_list = []
        self.prefix = "!"
        self.activity = False
        self.wait = 0
        self.bio = None
        self.self_callable = False
        self.no_command_message = ""
        self.spam_message = "You are spamming, be careful"
        self.lock_message = "Command locked sorry"
        self.launched = False
        self.message_bvn_status = True
        self.show_online = True
        self.double_check = False
        self.bot_name = bot_name
        self.barra_color= barra_color
        self.fondo_barra = fondo_barra
        self.color_texto = color_texto
        self.background_api = background_api
        self.embed_image = embed_image
        self.kemoji = kemoji
        self.autoanswer = autoanswer

    def tradlist(self, sub):
        sublist = []
        for elem in sub:
            with suppress(Exception):
                val = self.get_from_code(f"http://aminoapps.com/u/{elem}").objectId
                sublist.append(val)
                continue
            sublist.append(elem)
        return sublist

    def add_community(self, comId):
        self.communaute[comId] = Bot(self, comId, self.prefix, self.bio, self.activity, self.bot_name, self.barra_color, self.color_texto,self.fondo_barra, self.background_api, self.embed_image, self.kemoji, self.autoanswer)

    def get_community(self, comId):
        return self.communaute[comId]

    def is_it_bot(self, uid):
        return uid == self.botId and not self.self_callable

    def is_it_admin(self, uid):
        return uid in self.perms_list

    def generate_transaction_id(self):
        return str(uuid4())

    def set_message_bvn_status(self, status: bool):
        self.message_bvn_status = status

    def start_video_chat(self, comId: str, chatId: str, joinType: int = 1):
        data = {
            "o": {
                "ndcId": comId,
                "threadId": chatId,
                "joinRole": joinType,
                "id": "2154531"  # Need to change?
            },
            "t": 112
        }
        data = dumps(data)
        self.send(data)

        data = {
            "o": {
                "ndcId": int(comId),
                "threadId": chatId,
                "joinRole": joinType,
                "channelType": 4,
                "id": "2154531"  # Need to change?
            },
            "t": 108
        }
        data = dumps(data)
        self.send(data)

    def start_screen_room(self, comId: str, chatId: str, joinType: int = 1):
        data = {
            "o": {
                "ndcId": comId,
                "threadId": chatId,
                "joinRole": joinType,
                "id": "2154531"  # Need to change?
            },
            "t": 112
        }
        data = dumps(data)
        self.send(data)

        data = {
            "o": {
                "ndcId": int(comId),
                "threadId": chatId,
                "joinRole": joinType,
                "channelType": 5,
                "id": "2154531"  # Need to change?
            },
            "t": 108
        }
        data = dumps(data)
        self.send(data)

    def join_screen_room(self, comId: str, chatId: str, joinType: int = 1):
        data = {
            "o":
                {
                    "ndcId": int(comId),
                    "threadId": chatId,
                    "joinRole": 2,
                    "id": "72446"
                },
            "t": 112
        }
        data = dumps(data)
        self.send(data)

    def start_voice_room(self, comId: str, chatId: str, joinType: int = 1):
        data = {
            "o": {
                "ndcId": comId,
                "threadId": chatId,
                "joinRole": joinType,
                "id": "2154531"  # Need to change?
            },
            "t": 112
        }
        data = dumps(data)
        self.send(data)
        data = {
            "o": {
                "ndcId": comId,
                "threadId": chatId,
                "channelType": 1,
                "id": "2154531"  # Need to change?
            },
            "t": 108
        }
        data = dumps(data)
        self.send(data)

    def end_voice_room(self, comId: str, chatId: str, joinType: int = 2):
        data = {
            "o": {
                "ndcId": comId,
                "threadId": chatId,
                "joinRole": joinType,
                "id": "2154531"  # Need to change?
            },
            "t": 112
        }
        data = dumps(data)
        self.send(data)

    def show_online(self, comId):
        data = {
            "o": {
                "actions": ["Browsing"],
                "target": f"ndc://x{comId}/",
                "ndcId": int(comId),
                "id": "82333"
            },
            "t":304}
        data = dumps(data)
        slp(2)
        self.send(data)


    def check(self, args, *can, id_=None):
        id_ = id_ if id_ else args.authorId
        foo = {'staff': args.subClient.is_in_staff,
               'bot': self.is_it_bot, 'admin': self.is_it_admin}

        for i in can:
            if foo[i](id_):
                return True

    def check_all(self):
        amino_list = self.sub_clients()
        for com in amino_list.comId:
            try:
                self.communaute[com].check_in()
            except Exception:
                pass

    def threadLaunch(self, commu, passive: bool = False):
        self.communaute[commu] = Bot(self, commu, self.prefix, self.bio, passive, self.bot_name, self.barra_color,self.color_texto, self.fondo_barra, self.background_api, self.embed_image, self.kemoji, self.autoanswer)
        slp(30)
        if passive:
            self.communaute[commu].passive()

    def launch_events(self):
        if self.categorie_exist("command") or self.categorie_exist("answer"):
            self.launch_text_message()

        if self.categorie_exist("on_member_join_chat"):
            self.launch_on_member_join_chat()

        if self.categorie_exist("on_member_join_amino"):
            self.launch_on_live_user_join()

        if self.categorie_exist("on_member_leave_chat"):
            self.launch_on_member_leave_chat()

        if self.categorie_exist("on_other"):
            self.launch_other_message()

        if self.categorie_exist("on_remove"):
            self.launch_removed_message()

        if self.categorie_exist("on_tip_coin"):
            self.launch_tip_coin()

        if self.categorie_exist("on_invite_chat"):
            self.launch_chat_invited()

        if self.categorie_exist("on_call_channel"):
            self.launch_call_channel()

        if self.categorie_exist("on_all"):
            self.launch_all_message()

    def launch(self, passive: bool = False):
        amino_list = self.sub_clients(size = 100)
        self.len_community = len(amino_list.comId)
        [Thread(target=self.threadLaunch, args=[commu, passive]).start() for commu in amino_list.comId]

        if self.launched:
            return

        self.launch_events()

        self.launched = True


    def single_launch(self, commu, passive: bool = False):
        amino_list = self.sub_clients()
        self.len_community = len(amino_list.comId)
        Thread(target=self.threadLaunch, args=[commu, passive]).start()

        if self.launched:
            return

        self.launch_events()

        self.launched = True

    def message_analyse(self, data, type):
        try:
            commuId = data.comId
            subClient = self.get_community(commuId)
        except Exception:
            return

        args = Parameters(data, subClient)
        Thread(target=self.execute, args=[type, args, type]).start()

    def on_member_event(self, data, type):
        try:
            commuId = data.comId
            subClient = self.get_community(commuId)
        except Exception:
            return

        args = Parameters(data, subClient)

        if not self.check(args, "bot"):
            Thread(target=self.execute, args=[type, args, type]).start()

    def launch_text_message(self):
        def text_message(data):
            try:
                commuId = data.comId
                subClient = self.get_community(commuId)
            except Exception:
                return

            args = Parameters(data, subClient)

            if "on_message" in self.commands.keys():
                Thread(target=self.execute, args=["on_message", args, "on_message"]).start()

            if self.check(args, 'staff', 'bot') and subClient.banned_words:
                self.check_banned_words(args)

            elif self.double_check and subClient.banned_words:
                self.check_banned_words(args, False)

            if not self.timed_out(args.authorId) and args.message.startswith(subClient.prefix) and not self.check(args, "bot"):
                subClient.send_message(args.chatId, self.spam_message)
                return

            elif "command" in self.commands.keys() and args.message.startswith(subClient.prefix) and not self.check(args, "bot"):
                print(f"{args.author} : {args.message}")
                command = args.message.lower().split()[0][len(subClient.prefix):]

                if command in subClient.locked_command:
                    subClient.send_message(args.chatId, self.lock_message)
                    return

                args.message = ' '.join(args.message.split()[1:])
                self.time_user(args.authorId, self.wait)
                if command.lower() in self.commands["command"].keys():
                    Thread(target=self.execute, args=[command, args]).start()

                elif self.no_command_message:
                    subClient.send_message(args.chatId, self.no_command_message)
                return

            elif "answer" in self.commands.keys() and args.message.lower() in self.commands["answer"] and not self.check(args, "bot"):
                print(f"{args.author} : {args.message}")
                self.time_user(args.authorId, self.wait)
                Thread(target=self.execute, args=[args.message.lower(), args, "answer"]).start()
                return
        try:
            @self.callbacks.event("on_text_message")
            def on_text_message(data):
                text_message(data)
        except Exception:
            @self.event("on_text_message")
            def on_text_message(data):
                text_message(data)


    def launch_other_message(self):
        for type_name in ("on_strike_message", "on_voice_chat_not_answered",
                          "on_voice_chat_not_cancelled", "on_voice_chat_not_declined",
                          "on_video_chat_not_answered", "on_video_chat_not_cancelled",
                          "on_video_chat_not_declined", "on_voice_chat_start", "on_video_chat_start",
                          "on_voice_chat_end", "on_video_chat_end", "on_screen_room_start",
                          "on_screen_room_end", "on_avatar_chat_start", "on_avatar_chat_end"):
            @self.event(type_name)
            def on_other_message(data):
                self.message_analyse(data, "on_other")


    def launch_all_message(self):
        for x in (self.chat_methods):
            @self.event(self.chat_methods[x].__name__)
            def on_all_message(data):
                self.message_analyse(data, "on_all")


    def launch_removed_message(self):
        for type_name in ("on_chat_removed_message", "on_text_message_force_removed", "on_text_message_removed_by_admin", "on_delete_message"):
            @self.event(type_name)
            def on_chat_removed(data):
                self.message_analyse(data, "on_remove")

    def launch_on_member_join_chat(self):
        @self.event("on_group_member_join")
        def on_group_member_join(data):
            self.on_member_event(data, "on_member_join_chat")

    def launch_on_member_leave_chat(self):
        @self.event("on_group_member_leave")
        def on_group_member_leave(data):
            self.on_member_event(data, "on_member_leave_chat")

    def launch_on_live_user_join(self):
        @self.event("on_live_user_update")
        def on_live_user_update(data):
            self.on_member_event(data, "on_member_join_amino")

    def launch_tip_coin(self):
        @self.event("on_chat_tip")
        def on_chat_tip(data):
            self.on_member_event(data, "on_tip_coin")

    def launch_call_channel(self):
        @self.event("on_fetch_channel")
        def on_fetch_channel(data):
            self.on_member_event(data, "on_call_channel")


    def launch_chat_invited(self):
        for type_name in ("on_invite_message", "on_chat_invite"):
            @self.event(type_name)
            def on_invited(data):
                self.message_analyse(data, "on_invite_chat")


class Bot(SubClient, ACM):
    def __init__(self, client, community, prefix: str = "!", bio=None, activity=False, bot_name: str = "Bot", barra_color: str = "FFFFFF", color_texto: str = "FFFFFF", fondo_barra: str = "FFFFFF", background_api: str = None, embed_image: str = None, kemoji: list = [], autoanswer: str = None) -> None:
        self.client = client
        self.marche = True
        self.prefix = prefix
        self.bio_contents = bio
        self.activity = activity
        self.bot_name = bot_name
        self.barra_color = barra_color
        self.fondo_barra = fondo_barra
        self.color_texto = color_texto
        self.background_api = background_api
        self.embed_image = embed_image
        self.kemoji = kemoji
        self.autoanswer = autoanswer

        if isinstance(community, int):
            self.community_id = community
            self.community = self.client.get_community_info(comId=self.community_id)
            self.community_amino_id = self.community.aminoId
        else:
            self.community = self.client.get_community_info(comId= community)

        self.community_name = self.community.name

        super().__init__(comId=self.community_id, profile=self.client.profile)

        try:
            self.community_leader_agent_id = self.community.json["agent"]["uid"]
        except Exception:
            self.community_leader_agent_id = "-"

        try:
            self.community_staff_list = self.community.json["communityHeadList"]
        except Exception:
            self.community_staff_list = ""

        if self.community_staff_list:
            self.community_leaders = [elem["uid"] for elem in self.community_staff_list if elem["role"] in (100, 102)]
            self.community_curators = [elem["uid"] for elem in self.community_staff_list if elem["role"] == 101]
            self.community_staff = [elem["uid"] for elem in self.community_staff_list]

        if not Path(f'{path_amino}/{self.community_amino_id}.json').exists():
            self.create_community_file()

        old_dict = self.get_file_dict()
        new_dict = self.create_dict()

        def do(k, v): old_dict[k] = v
        def undo(k): del old_dict[k]

        [do(k, v) for k, v in new_dict.items() if k not in old_dict]
        [undo(k) for k in new_dict.keys() if k not in old_dict]

        self.update_file(old_dict)


        self.banned_words = self.get_file_info("banned_words")
        self.locked_command = self.get_file_info("locked_command")
        self.message_bvn = self.get_file_info("welcome")
        self.welcome_chat = self.get_file_info("welcome_chat")
        self.prefix = self.get_file_info("prefix")
        self.favorite_users = self.get_file_info("favorite_users")
        self.favorite_chats = self.get_file_info("favorite_chats")
        self.confesiones = self.get_file_info("confesiones")
        self.coin_channel = self.get_file_info("coin_channel")
        self.welcom_status = self.get_file_info("wel_status")
        self.goodbye_status = self.get_file_info("goodbye_status")
        self.welcome_chat_message = self.get_file_info("welcome_chat_message")
        self.goodbye_chat_message = self.get_file_info("goodbye_chat_message")
        self.status_coin = self.get_file_info("status_coin")
        self.bot_names = self.get_file_info("bot_name")
        self.status_bot = self.get_file_info("status_bot")
        self.status_antiraid = self.get_file_info("antiraid")
        self.barra_colores = self.get_file_info("barra_color")
        self.fondo_barras = self.get_file_info("fondo_barra")
        self.color_textos = self.get_file_info("color_texto")
        self.backgrounds_api = self.get_file_info("background_api")
        self.embed_images = self.get_file_info("embed_image")
        self.answers = self.get_file_info("answer")
        self.kemojis = self.get_file_info("kemoji")
        self.update_file()
        self.activity_status("on")
        new_users = self.get_all_users(start=0, size=30, type="recent")

        self.new_users = [elem["uid"] for elem in new_users.json["userProfileList"]]

    def create_community_file(self):
        with open(f'{path_amino}/{self.community_amino_id}.json', 'w', encoding='utf8') as file:
            dict = self.create_dict()
            file.write(dumps(dict, sort_keys=False, indent=4))

    def create_dict(self):
        return {"welcome": "", "prefix": self.prefix, "welcome_chat": "", "locked_command": [], "favorite_users": [], "favorite_chats": [], "banned_words": [], "confesiones": "", "coin_channel": "",  "wel_status": True, "goodbye_status": True, "welcome_chat_message": "", "goodbye_chat_message": "", "status_coin": True, "bot_name": self.bot_name, "status_bot": True, "antiraid": False, "barra_color": self.barra_color, "fondo_barra": self.fondo_barra, "color_texto": self.color_texto, "background_api": self.background_api, "embed_image": self.embed_image,"answer": self.autoanswer, "kemoji": self.kemoji}
 
    def get_dict(self):
        return {"welcome": self.message_bvn, "prefix": self.prefix, "welcome_chat": self.welcome_chat, "locked_command": self.locked_command,
                "favorite_users": self.favorite_users, "favorite_chats": self.favorite_chats, "banned_words": self.banned_words,  "confesiones": self.confesiones, "coin_channel": self.coin_channel, "wel_status": self.welcom_status, "goodbye_status": self.goodbye_status, "welcome_chat_message": self.welcome_chat_message, "goodbye_chat_message": self.goodbye_chat_message, "status_coin": self.status_coin, "bot_name": self.bot_names, "status_bot": self.status_bot, "antiraid": self.status_antiraid, "barra_color": self.barra_colores, "fondo_barra": self.fondo_barras, "color_texto": self.color_textos, "background_api": self.backgrounds_api, "embed_image": self.embed_images,"answer": self.answers, "kemoji": self.kemojis}

    def update_file(self, dict=None):
        if not dict:
            dict = self.get_dict()
        with open(f"{path_amino}/{self.community_amino_id}.json", "w", encoding="utf8") as file:
            file.write(dumps(dict, sort_keys=False, indent=4))

    def get_file_info(self, info: str = None):
        with open(f"{path_amino}/{self.community_amino_id}.json", "r", encoding="utf8") as file:
            return load(file)[info]

    def get_file_dict(self, info: str = None):
        with open(f"{path_amino}/{self.community_amino_id}.json", "r", encoding="utf8") as file:
            return load(file)

    def get_banned_words(self):
        return self.banned_words

    def set_prefix(self, prefix: str):
        self.prefix = prefix
        self.update_file()

    def delete_all_kemojis(self):
        self.kemojis = [""]
        self.update_file()

    def delete_kemojis(self, kemoji: str):
        if kemoji in self.kemojis:
            self.kemojis.remove(kemoji)
            self.update_file()

    def set_kemojis(self, kemoji: str):
        if "" in self.kemojis:
            self.kemojis.remove("")
        self.kemojis.append(kemoji)
        self.update_file()

    def set_bot_answer(self, answer: str):
        self.answers = answer
        self.update_file()

    def set_bot_name(self, bot_name: str):
        self.bot_names = bot_name
        self.update_file()

    def unset_bot_name(self):
        self.bot_names = self.bot_name
        self.update_file()

    def set_background_api(self, image: str):
        self.backgrounds_api = image
        self.update_file()

    def set_embed_image(self, image: str):
        self.embed_images = image
        self.update_file()

    def set_barra_color(self, color: str):
        self.barra_colores = color
        self.update_file()

    def set_color_textos(self, color: str):
        self.color_textos = color
        self.update_file()

    def set_fondo_barras(self, color: str):
        self.fondo_barras = color
        self.update_file()
    
    def set_status_bots(self):
        self.status_bot = True
        self.update_file()
    
    def unset_status_bots(self):
        self.status_bot = False
        self.update_file()

    def set_status_antiraid(self):
        self.status_antiraid = True
        self.update_file()
    
    def unset_status_antiraid(self):
        self.status_antiraid = False
        self.update_file()

    def set_welcome_message(self, message: str):
        self.message_bvn = message.replace('"', '“')
        self.update_file()

    def unset_welcome_message(self):
        self.message_bvn = ""
        self.update_file()

    def set_welcome_chat(self, chatId: str):
        self.welcome_chat = chatId
        self.update_file()

    def unset_welcome_chat(self):
        self.welcome_chat = ""
        self.update_file()

    def set_welcome_chat_message(self, message: str):
        self.welcome_chat_message = message
        self.update_file()

    def unset_welcome_chat_message(self):
        self.welcome_chat_message = ""
        self.update_file()

    def set_goodbye_chat_message(self, message: str):
        self.goodbye_chat_message = message
        self.update_file()

    def unset_goodbye_chat_message(self):
        self.goodbye_chat_message = ""
        self.update_file()

    def set_welcom_status(self):
        self.welcom_status = True
        self.update_file()

    def unset_welcom_status(self):
        self.welcom_status = False
        self.update_file()

    def set_coin_status(self):
        self.status_coin = True
        self.update_file()

    def unset_coin_status(self):
        self.status_coin = False
        self.update_file()

    def set_goodbye_status(self):
        self.goodbye_status = True
        self.update_file()

    def unset_goodbye_status(self):
        self.goodbye_status = False
        self.update_file()

    def set_coin_channel(self, chatId: str):
        self.coin_channel = chatId
        self.update_file()

    def unset_coin_channel(self):
        self.coin_channel= ""
        self.update_file()

    def set_confesiones(self, chatId: str):
        self.confesiones = chatId
        self.update_file()

    def unset_confesiones(self):
        self.confesiones = ""
        self.update_file()

    def add_favorite_users(self, value: str):
        self.favorite_users.append(value)
        self.update_file()

    def add_favorite_chats(self, value: str):
        self.favorite_chats.append(value)
        self.update_file()

    def add_banned_words(self, liste: list):
        self.banned_words.extend(liste)
        self.update_file()

    def add_locked_command(self, liste: list):
        self.locked_command.extend(liste)
        self.update_file()

    def remove_favorite_users(self, value: str):
        liste = [value]
        [self.favorite_users.remove(elem) for elem in liste if elem in self.favorite_users]
        self.update_file()

    def remove_favorite_chats(self, value: str):
        liste = [value]
        [self.favorite_chats.remove(elem) for elem in liste if elem in self.favorite_chats]
        self.update_file()

    def remove_banned_words(self, liste: list):
        [self.banned_words.remove(elem) for elem in liste if elem in self.banned_words]
        self.update_file()

    def remove_locked_command(self, liste: list):
        [self.locked_command.remove(elem) for elem in liste if elem in self.locked_command]
        self.update_file()

    def unset_welcome_chat(self):
        self.welcome_chat = ""
        self.update_file()

    def is_in_staff(self, uid):
        return uid in self.community_staff

    def is_leader(self, uid):
        return uid in self.community_leaders

    def is_curator(self, uid):
        return uid in self.community_curators

    def is_agent(self, uid):
        return uid == self.community_leader_agent_id

    def accept_role(self, rid: str = None):
        with suppress(Exception):
            self.accept_organizer(rid)
            return True
        with suppress(Exception):
            self.promotion(noticeId=rid)
            return True
        return False

    def stop_instance(self):
        self.marche = False

    def start_instance(self):
        self.marche = True
        Thread(target=self.passive).start()

    def leave_amino(self):
        self.marche = False
        for elem in self.get_public_chat_threads().chatId:
            with suppress(Exception):
                self.leave_chat(elem)
        self.client.leave_community(comId=self.community_id)

    def feature_chats(self):
        for elem in self.favorite_chats:
            with suppress(Exception):
                self.favorite(time=2, chatId=elem)

    def feature_users(self):
        featured = [elem["uid"] for elem in self.get_featured_users().json["userProfileList"]]
        for elem in self.favorite_users:
            if elem not in featured:
                with suppress(Exception):
                    self.favorite(time=1, userId=elem)


    def generate_transaction_id(self):
        return str(uuid4())

    def pay(self, coins: int = 0, blogId: str = None, chatId: str = None, objectId: str = None, transactionId: str = None):
        if not transactionId:
            transactionId = self.generate_transaction_id()
        self.send_coins(coins=coins, blogId=blogId, chatId=chatId, objectId=objectId, transactionId=transactionId)

    def favorite(self, time: int = 1, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None):
        self.feature(time=time, userId=userId, chatId=chatId, blogId=blogId, wikiId=wikiId)

    def unfavorite(self, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None):
        self.unfeature(userId=userId, chatId=chatId, blogId=blogId, wikiId=wikiId)

    def join_chatroom(self, chat: str = None, chatId: str = None):
        if not chat:
            with suppress(Exception):
                self.join_chat(chatId)
                return ""

        with suppress(Exception):
            chati = self.get_from_code(f"{chat}").objectId
            self.join_chat(chati)
            return chat

        chats = self.get_public_chat_threads()
        for title, chat_id in zip(chats.title, chats.chatId):
            if chat == title:
                self.join_chat(chat_id)
                return title

        chats = self.get_public_chat_threads()
        for title, chat_id in zip(chats.title, chats.chatId):
            if chat.lower() in title.lower() or chat == chat_id:
                self.join_chat(chat_id)
                return title

        return False

    def start_screen_room(self, chatId: str, joinType: int = 1):
        self.client.join_video_chat(comId=self.community_id, chatId=chatId, joinType=joinType)

    def start_video_chat(self, chatId: str, joinType: int = 1):
        self.client.join_video_chat(comId=self.community_id, chatId=chatId, joinType=joinType)

    def start_voice_room(self, chatId: str, joinType: int = 1):
        self.client.join_voice_chat(comId=self.community_id, chatId=chatId, joinType=joinType)

    def join_screen_room(self, chatId: str, joinType: int = 1):
        self.client.join_video_chat_as_viewer(comId=self.community_id, chatId=chatId, joinType=joinType)

    def join_all_chat(self):
        for elem in self.get_public_chat_threads(type="recommended", start=0, size=100).chatId:
            with suppress(Exception):
                time.sleep(5)
                self.join_chat(elem)

    def leave_all_chats(self):
        for elem in self.get_public_chat_threads(type="recommended", start=0, size=100).chatId:
            with suppress(Exception):
                time.sleep(5)
                self.leave_chat(elem)


    def add_title(self, uid: str, title: str, color: str = None):
        member = self.get_member_titles(uid)
        try:
            titles = [i['title'] for i in member] + [title]
            colors = [i['color'] for i in member] + [color]
        except TypeError:
            titles = [title]
            colors = [color]

        self.edit_titles(uid, titles, colors)
        return True

    def remove_title(self, uid: str, title: str):
        member = self.get_member_titles(uid)
        tlist = []
        clist = []

        for t in member:
            if t["title"] != title:
                tlist.append(t["title"])
                clist.append(t["color"])
        self.edit_titles(uid, tlist, clist)
        return True

    def passive(self):
        def upt_activity():
            timeNow = int(time.time())
            timeEnd = timeNow + 300
            try:
                self.send_active_obj(startTime=timeNow, endTime=timeEnd)
            except:
                pass

        def show_online():
            try:
                self.activity_status('on')
            except:
                pass

        j = 0
        k = 0
        while self.marche:
            show_online()
            if self.activity:
                upt_activity()

            slp(30)
            j += 1
            k += 1