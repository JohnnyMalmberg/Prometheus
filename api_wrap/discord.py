def get_channel_by_name(name, server):
    return next(channel for channel in server.channels if channel.name == name)
    
async def get_self_as_member(client, server):
    async for member in server.fetch_members(limit=100):
        if member == client.user:
            return member
    raise Exception('No self!')

async def set_nickname(client, server, nickname):
    botMember = await get_self_as_member(client, server)
    await botMember.edit(nick=nickname)