import discord
import client.values as values

server = None
channel = None

servers = []
channels = []
roles = []
members = []
args = []


# display servers
async def get_servers(client):
    
    i = 0
    for s in client.guilds:

        servers.append(s)
        print('['+str(i)+'] '+str(s)+" - "+str(s.id))
        i += 1

    if server != None:
        print("current server : "+server.name)
    else:
        print("no server set")

# display channels for the current serve if set
async def get_channels(client):
    
    # if the guild is not set
    if server == None:
        channels = client.get_all_channels()
    else:
        channels = server.channels

    i=0
    for c in channels:
        print('['+str(i)+'] '+c.guild.name+' - '+str(c.id)+' - '+c.name)
        i += 1

# set a server
async def set_server(client, id=None, index=None):
   
    global server

    for s in servers:
        print(s)

    if index != None:
        server = servers[int(index)]

    print('server set to '+str(server))

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


async def process(client, request):
    
    args = request.split()[1:]

    global server
    global channel
    global members

    if request.startswith('getsrv'):
        await get_servers(client)

    elif request.startswith('setsrv'):
        guild_index = request.split()[1]
        await set_server(client, index=guild_index)

    elif request.startswith('getch'):
        await get_channels(client)
    
    elif request.startswith('members'):
        await get_members(client)

    elif request.startswith('uinfo'):
        index = args[0]
        await member_info(client,index)

    elif request.startswith('roles'):
        await get_roles(client)
    
    elif request.startswith('remrole'):
        member_id = args[0]
        role_index = args[1]
        await remove_member_role(client,member_id,role_index)

    elif request.startswith('delrole'):
        role_id = args[0]
        await delete_role(client,role_id)

    elif request.startswith('setrole'):
        user = args[0]
        role = args[1]
        await set_role(client,user,role)

    elif request.startswith('addrole'):
    # adds a new role to the server
        role_name = args[0]
        perms_id = args[1]
        await create_role(client, role_name, perms_id)
   
    if request.startswith('$stop'):
        print('closing client')
        await client.logout()

    elif request.startswith('$reset'):
        print('reseting client')
        await client.logout()
        client.run(values.get_value('BOT_TOKEN'))

    elif request.startswith("$getch"):
        for c in client.get_all_channels():
            print(str(c.guild.name)+" - "+str(c.id)+" - "+str(c.name))

    elif request.startswith("$getsrv"):
        global servers

        for s in client.guilds:
            servers.append(s)
            print(str(s)+" - "+str(s.id))

        try:
            print("Current server : "+server.name)
        except:
            print("Failure : No server set")


    elif request.startswith("$setsrv"):
        args = request.split(" ")
        print(str(servers[int(args[1])].name))
        server = servers[int(args[1])]

    elif request.startswith("$setch"):
        args = request.split( )
        try:
            channel = server.get_channel(int(args[1]))
        except IndexError:
            print("This channel doesnt exist")
            return
        print("Channel set to : "+channel.name)

    elif request.startswith('-'):

        msg = request[1:]
        await channel.send(msg)

    elif request.startswith("$dm"):
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

    elif request.startswith("$get_invite"):
        args = request.split( )
        chan_id = args[1]
        chan = server.get_channel(int(chan_id))
        
        invite = await chan.create_invite(max_uses=1)

        print("invite link :\n  "+str(invite))

    elif request.startswith("$create_guild"):
        args = request.split( )
        name = ' '.join(args[1:])
        region = discord.VoiceRegion.eu_west
        icon = values.get_icon('dark')

        await client.create_guild(name, region=region, icon=icon)
    
    elif request.startswith('$create_role'):
        args = request.split( )
        role_name = args[1]
        permissions = discord.Permissions(int(args[2]))

        role = await server.create_role(name=role_name,permissions=permissions)

        await server.get_member(values.get_value('OWNER_ID')).add_roles(role)

    elif request.startswith("$"):
        print("Unrecognized request.")


