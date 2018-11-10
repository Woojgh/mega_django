import discord

client = discord.Client()

channel_id = 350751933327474688
async def get_channel(channel_id):
    return self._channels.get(channel_id)
lst = []
for server in client.servers:
    for channel in server.channels:
        lst.append(channel)

@client.event
async def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    await client.send_message(server, fmt.format(member, server))

@client.event
async def on_ready():
    # import pdb; pdb.set_trace()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

monkey = discord.Client()
# monkey.run('MzA0ODc1MzMzMTA5NDE1OTM2.Dr16DA.--DeKIr2d6pv9FH2o7fHrl0DIiw')
# monkey.run('flippygonmad@gmail.com', '189645Jts!')


client.run("NTA3NTI4NzA3NTE5NTQ1MzQ4.Dr_OKQ.IrIxR5HIW8HAtw20wnhpMZyZ_sA")
