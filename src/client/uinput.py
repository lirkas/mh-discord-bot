import discord
import client.utils as utils

class UI:

    def __init__(self, bot):
        self.bot = bot
        self.channel = None
        self.server = None
        self.members = []
        self.servers = []
        self.channels = []

    def display(self, message):
        print(message.author.name+" : "+message.content)
    
    async def process(self, line):
        
        request = line
        args = line.split()[1:]
        client = self.bot

        if request.startswith('getsrv'):
            await get_servers(self)

        elif request.startswith('setsrv'):
            guild_index = request.split()[1]
            await set_server(self, index=guild_index)

        elif request.startswith('getch'):
            await get_channels(self)

        elif request.startswith('setch'):
            chan_index = request.split()[1]
            await set_channel(self, index=chan_index)
 
        elif request.startswith('members'):
            await get_members(self)

        elif request.startswith('uinfo'):
            index = args[0]
            await member_info(self,index)
    
        elif request.startswith('roles'):
            await get_roles(self)
    
        elif request.startswith('remrole'):
            member_id = args[0]
            role_index = args[1]
            await remove_member_role(self,member_id,role_index)

        elif request.startswith('delrole'):
            role_id = args[0]
            await delete_role(ui,role_id)

        elif request.startswith('setrole'):
            user = args[0]
            role = args[1]
            await set_role(ui,user,role)

        elif request.startswith('addrole'):
            role_name = args[0]
            perms_id = args[1]
            await create_role(ui, role_name, perms_id)
   
        elif request.startswith("dm"):
            args = request.split( )
            uid = args[1]

            msg = ' '.join(args[2:])

            user = await client.get_user_info(int(uid))
            print("user set to "+user.name)

            if user.dm_channel == None:
                channel = await user.create_dm()
            else:
                channel = user.dm_channel

            await channel.send(msg)

        elif request.startswith("get_invite"):
            args = request.split( )
            chan_id = args[1]
            chan = server.get_channel(int(chan_id))
        
            invite = await chan.create_invite(max_uses=1)

            print("invite link :\n  "+str(invite))

        elif request.startswith("create_guild"):
            args = request.split( )
            name = ' '.join(args[1:])
            region = discord.VoiceRegion.eu_west
            icon = values.get_icon('dark')

            await client.create_guild(name, region=region, icon=icon)

        elif request.startswith('-'):
            await self.channel.send(request[1:])


# display servers
async def get_servers(ui):
    
    i = 0
    for s in ui.bot.guilds:

        ui.servers.append(s)
        print('['+str(i)+'] '+str(s)+" - "+str(s.id))
        i += 1

    if ui.server != None:
        print("current server : "+ui.server.name)
    else:
        print("no server set")

# display channels for the current serve if set
async def get_channels(ui):
    
    # if the guild is not set
    if ui.server == None:
        ui.channels = ui.bot.get_all_channels()
    else:
        ui.channels = ui.server.channels

    i=0
    for c in ui.channels:
        print('['+str(i)+'] '+c.guild.name+' - '+str(c.id)+' - '+c.name)
        i += 1

# set a server
async def set_server(ui, id=None, index=None):
   
    for s in ui.servers:
        print(s)

    if index != None:
        ui.server = ui.servers[int(index)]

    print('server set to '+str(ui.server))

# set a server
async def set_channel(ui, id=None, index=None):
   
    for c in ui.channels:
        print(c)

    if index != None:
        ui.channel = ui.channels[int(index)]

    print('channel set to '+str(ui.channel))


async def get_roles(client):

    if server == None:
        print('please set a server first')
        await get_servers(client)
        return
    
    roles = server.roles
    i=0
    for role in roles:
        print('['+str(i)+'] '+role.name)
        i+=1

    return roles

async def get_members(client):
     
    if server == None:
        print('please set a server first')
        await get_servers(client)
        return
    
    members = server.members
    i=0
    for member in members:
        print('['+str(i)+'] '+member.name+' '+str(member.id))
        i+=1


async def member_info(client, index):
   
    if int(index) > 9999999:
        member = server.get_member(int(index))
    else:
        member = members[int(index)]

    print('name  : '+member.name)
    print('id    : '+str(member.id))
    print('roles : '+str(member.roles))


async def remove_member_role(client, user_id, role_index):
   
    roles = await get_roles(client)
    member = server.get_member(int(user_id))
    await member.remove_roles(roles[int(role_index)])
    print('role removed ?')

async def set_role(client, user_id, role_index):
    roles = await get_roles(client)
    member = server.get_member(int(user_id))
    await member.add_roles(roles[int(role_index)])
    print('role added to '+member.name)

async def delete_role(client, role_id):

    roles = await get_roles(client)
    await roles[(int(role_id))].delete()

async def create_role(client, role_name, perms_id):

    permissions = discord.Permissions(int(perms_id))
    role = await server.create_role(name=role_name,permissions=permissions)
    print('created role '+role.name)
 
