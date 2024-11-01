import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands
import sqlite3

load_dotenv()
TOKEN = os.getenv("TOKEN")
VOUCH_CHANNEL_ID = int(os.getenv("VOUCH_LOG_CHANNEL_ID"))

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Database setup
conn = sqlite3.connect("vouch_db.sqlite")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS vouches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    target_id INTEGER,
    vote_type TEXT,
    comment TEXT
)
''')
conn.commit()


@bot.slash_command(description="Vote for a member with /vouch @member +/- comment")
async def vouch(inter, member: disnake.Member, vote_type: str, comment: str):
    if vote_type not in ["+", "-"]:
        await inter.response.send_message("Please specify vote type as + or -", ephemeral=True)
        return

    cursor.execute(
        "INSERT INTO vouches (user_id, target_id, vote_type, comment) VALUES (?, ?, ?, ?)",
        (inter.author.id, member.id, vote_type, comment)
    )
    conn.commit()

    embed = disnake.Embed(
        title="New Vouch",
        color=disnake.Color.green() if vote_type == "+" else disnake.Color.red()
    )
    embed.add_field(name="Voter", value=inter.author.mention, inline=True)
    embed.add_field(name="Target", value=member.mention, inline=True)
    embed.add_field(name="Vote Type", value="👍 Positive" if vote_type == "+" else "👎 Negative", inline=True)
    embed.add_field(name="Comment", value=comment, inline=False)

    channel = bot.get_channel(VOUCH_CHANNEL_ID)
    if channel is not None:
        await channel.send(embed=embed)
    else:
        await inter.response.send_message("Error: Vouch channel not found.", ephemeral=True)
        return

    await inter.response.send_message(
        f"Vote recorded for {member.mention}. Type: {'Positive' if vote_type == '+' else 'Negative'}, Comment: {comment}",
        ephemeral=True
    )


@bot.slash_command(description="View the reputation profile of a member")
async def profile(inter, member: disnake.Member):
    cursor.execute("SELECT vote_type, comment FROM vouches WHERE target_id = ?", (member.id,))
    vouches = cursor.fetchall()

    if not vouches:
        await inter.response.send_message(f"No vouches found for {member.mention}.", ephemeral=True)
        return

    positive_votes = sum(1 for v in vouches if v[0] == "+")
    negative_votes = sum(1 for v in vouches if v[0] == "-")
    reputation_score = positive_votes - negative_votes

    # Create an embed for the profile
    embed = disnake.Embed(
        title=f"Reputation Profile for {member.display_name}",
        color=disnake.Color.blue()
    )
    embed.add_field(name="Reputation Score", value=str(reputation_score), inline=True)
    embed.add_field(name="👍 Positive Votes", value=str(positive_votes), inline=True)
    embed.add_field(name="👎 Negative Votes", value=str(negative_votes), inline=True)

    comments_section = "\n".join(
        f"{'👍' if vote_type == '+' else '👎'} {comment}" for vote_type, comment in vouches
    )
    embed.add_field(name="Comments", value=comments_section if comments_section else "No comments", inline=False)

    await inter.response.send_message(embed=embed)


bot.run(TOKEN)
