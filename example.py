async for guild in client.fetch_guilds(limit=5):
    async for member in guild.fetch_members(limit=100):
        if member == client.user:
            member.edit(nick='new name goes here')