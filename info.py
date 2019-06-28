def init(bot, data):
    @bot.command()
    async def add(ctx):
        await ctx.send("Add Ludus to your server: <https://discordapp.com/api/oauth2/authorize?client_id=593828724001079297&permissions=124992&scope=bot>")
    
    @bot.command()
    async def github(ctx):
        await ctx.send("Ludus is open source! You can find the source code here: https://github.com/mninc/ludus")
    
    @bot.command()
    async def server(ctx):
        await ctx.send("You can join the official Ludus discord server here: https://discord.gg/qZQN53p")
    
    @bot.command()
    async def contributors(ctx):
        await ctx.send("Ludus was developed by <@156895789795246081> and <@197059070740398080>, with art from <@253584079113551873>.")

    @bot.command()
    async def website(ctx):
        await ctx.send("Visit our website: https://mninc.github.io/ludus/")
