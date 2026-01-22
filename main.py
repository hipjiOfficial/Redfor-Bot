import discord
import os
from discord.ext import commands
from discord import app_commands
from datetime import datetime, date, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# env variables
if Path(".env").exists():
    load_dotenv()

connection_string = os.getenv("DB_CONNECTION_STRING")
bot_token = os.getenv("BOT_TOKEN")

if not connection_string:
    raise RuntimeError("connection_string is not set")

if not bot_token:
    raise RuntimeError("bot_token is not set")

ascii_blufor = r"""                                                                                              
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%####%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#********########%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*+++****###############%@@@@@@@@@@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*:-+***####################%@@@@@@@@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*-:-+**########################%@@@@@@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#==++**##########################%@@@@@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#++***##############################@@@@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@%*****###############################%@@@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@#****###############**++++**#####**+*#@@@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@#***########**++*@@##########*++++++*#@@@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@######*%@%#**##############*+++++++++@@@@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@##*+**#######**###########*++++++++++#@@@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@############++*##########++++++++++++%@@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%*#########*++*##**+++++++++++++++++*@@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*+*#####**++++++++++++++++++++++++++%@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+++++++++++++++++++++++++++++++++++*@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%+++++++++++++++++++++++++++++++++++%@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*+++++++++++++++****+++++++++++++++%@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%++++++++*%@@@@@%%#*++++++++++++++#@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*+++++%@%*++++++++++++++++++++++*%@@@@@@@@@@@@@@@@@@@      
      @@@@@@@@@@@@@@@@@@@@@##%%%%%%@@@@@@@++++++++++++++++++++++++*###################%%%%%%%%      
      @@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%#=====+++++++++++++++++*****#%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@@@@@@%%%%%%%%%%*+++++++++++++++++++++++*****#%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@@@@@%%%%%%%%%%%*+++++++++++++++++++++++*****#%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@@@@@%%%%%%%%%%%*+++++++++++++++++++++++*****#%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@@@@%%%%%%%%%%%%*+++++++++++++++++++++++*****#%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@@@@%%%%%%%%%%%%*+++++++++++++++++++++++*****#%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@@@@%%%%%%%%%%%%*+++++++++++++++++++++++******%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@@@@%%%%%%%%%%%%*+++++++++++++++++++++++******%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@@@%%%%%%%%%%%%%*+++++++++++++++++++++++******%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@@@%%%%%%%%%%%%%*+++++++++++++++++++++++******%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@@@%%%%%%%%%%%%%*+++++++++++++++++++++++******%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@@%%%%%%%%%%%%%%*+++++++++++++++++++++++******%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@@%%%%%%%%%%%%%%*+++++++++++++++++++++++******%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@@%%%%%%%%%%%%%%*+++++++++++++++++++++++******%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@%%%%%%%%%%%%%%%*+++++++++++++++++++++++******%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@%%%%%%%%%%%%%%%*+++++++++++++++++++++++******%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@@%%%%%%%%%%%%%%%*+++++++++++++++++++++++******%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@%%%%%%%%%%%%%%%%*+++++++++++++++++++++++******%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@%%%%%%%%%%%%%%%%*+++++++++++++++++++++++******%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@@%%%%%%%%%%%%%%%%*+++++++++++++++++++++++******%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@%%%%%%%%%%%%%%%%%*++++++++++++++++++++++*******#%%%%%%%%%%%%%%%%%%%%%%%%%%%      
      @@@@@@@@@@@@@%%%%%%%%%%%%%%%%%*++++++++++++++++++++++*******#%%%%%%%%%%%%%%%%%%%%%%%%%%%                                                                                                   
"""

ascii_redfor = r"""
                                                                                                    
                                                                                                    
                                                                                                    
                                            ******#########                                         
                                     ********###############                                        
                                ********#####################                                       
                            ===-=+***#########################                                      
                          +====+**#############################                                     
                          ++****###############################                                     
                         ****###################################                                    
                         ***############*##%%#*+++++*###########                                    
                         ***######*#%@@#+*#@@#++++++*############                                   
                          **##**++++*@@*+++%@*+++++++*###########                                   
                          **##*++++++#%*++++++++++***############                                   
                          **###*+++++++**#########################                                  
                           *###**++**#############################                                  
                           **######################################                                 
                            *######################################                                 
                            **#####################################                                 
                            #*#####################################                                 
                             *#####################################                                 
                              ####################################                                  
                              #################*******####################%%%%%%%%%%%%%%%%%%%%%%    
                  ##########*++*###########**+++***########%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@   
                 %%%%%%%%%%#****##########********###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@   
                 %%%%%%%%%%#******######**********###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@   
                 %%%%%%%%%%#**********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
                %%%%%%%%%%%#**********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
                %%%%%%%%%%%#**********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
                %%%%%%%%%%%***********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
                %%%%%%%%%%%***********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
                %%%%%%%%%%%***********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
               %%%%%%%%%%%%***********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@  
               %%%%%%%%%%%%***********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
               %%%%%%%%%%%%***********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
               %%%%%%%%%%%%***********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
               %%%%%%%%%%%%**********************####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
              %%%%%%%%%%%%%***********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
              %%%%%%%%%%%%%**********************####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
              %%%%%%%%%%%%%**********************####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@  
              %%%%%%%%%%%%%**********************####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@  
             %%%%%%%%%%%%%%**********************####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@  
             %%%%%%%%%%%%%%**********************####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
             %%%%%%%%%%%%%%**********************#####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
             %%%%%%%%%%%%%%**********************#####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
             %%%%%%%%%%%%%%**********************#####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@  
            %%%%%%%%%%%%%%%**********************#####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
            %%%%%%%%%%%%%%#**********************#####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
             %%%%%%%%%%%%%#**********************#####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@  
               @%%%%%%%%%%#**********************#####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@@  
"""

ascii_redfor_small = r"""
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                ****#*###                                           
                                        ******#############                                         
                                ++++****#####################                                       
                              -:-=+**########################                                       
                             +++**############################                                      
                            ****###############################                                     
                            ***##########*#%@%*+++++###########                                     
                            **####***#@@#++#@%++++++*###########                                    
                             *##*+++++#@*+++**++++++*###########                                    
                             *###*+++++++*#######################                                   
                             #*##*****###########################                                   
                              ###################################                                   
                              **#################################                                   
                               *#################################                                   
                               *#################################                                   
                                ################################%%%%%%%%%%%%%%%%%%%%%%%             
                     ***######%%############*++++++*##***########%%%%%%%%%%%%%%%%%%%%%%%%%%%        
                    %%%%%%%%%#****#########*******###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                    %%%%%%%%%#******#####*********###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                    %%%%%%%%%#********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                    %%%%%%%%%#********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                   %%%%%%%%%%#********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                   %%%%%%%%%%#********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                   %%%%%%%%%%*********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                   %%%%%%%%%%*********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                  %%%%%%%%%%%*********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                  %%%%%%%%%%%*********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                  %%%%%%%%%%%*********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                  %%%%%%%%%%%*********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                  %%%%%%%%%%%*********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                 %%%%%%%%%%%%*********************###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                 %%%%%%%%%%%%********************####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                 %%%%%%%%%%%%********************####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                 %%%%%%%%%%%%********************####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                 %%%%%%%%%%%%********************####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                %%%%%%%%%%%%%********************####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                %%%%%%%%%%%%%********************####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                  @%%%%%%%%%%********************####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@       
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
                                                                                                    
"""

#time until shop reset
"""

"""



def get_pc_info(card_name):
    conn = psycopg2.connect(connection_string)
    
    try: 
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ci."Rarity",
                    cc.chance_to_appear
                FROM card_info ci
                LEFT JOIN pc_chances cc
                    ON cc.pc_name = ci."Card"
                WHERE ci."Card" = %s
                """,
                (card_name,)
            )
            return cur.fetchone()
    finally:
        conn.close()

def get_missing_pcs():
    with open("missingpcs.txt", "r") as f:
        return f.read()

#simple commands

#get shop commad
@bot.tree.command(name="getshop", description="Get the shop for today or a specific date")
@app_commands.describe(shop_date="Date in format YYYY-MM-DD")
async def get_shop_items(interaction: discord.Interaction, shop_date: str | None = None):
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()

    now = datetime.now(timezone.utc)
    next_midnight = (now + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    unix = int(next_midnight.timestamp())
    next_shop_reset = f"<t:{unix}:R>"

    query_date = None

    if shop_date is not None:
        try:
            query_date = datetime.strptime(shop_date, "%Y-%m-%d").date()
        except ValueError:
            await interaction.response.send_message("Invalid date format. Use `YYYY-MM-DD`.", ephemeral=True)
            return
        
        cur.execute(
            """
            SELECT pc1, pc2, pc3, log_date
            FROM shop_log
            WHERE log_date = %s
            ORDER BY log_date DESC
            LIMIT 1
            """,
            (query_date,)
        )

    else:
        today = date.today()

        cur.execute(
                """
                SELECT pc1, pc2, pc3, log_date
                FROM shop_log
                WHERE log_date <= %s
                ORDER BY log_date DESC
                LIMIT 1
                """,
                (today,)
            )
    
    row = cur.fetchone()

    if not row:
        await interaction.response.send_message(f"No shop data found.", ephemeral=True)
        return
    
    pc1, pc2, pc3, log_date = row

    #decide which header to display
    shop_date_str = log_date.strftime("%A, %B %d, %Y")
    user_provided_date = shop_date is not None
    if user_provided_date:
        header = f"**Shop for {shop_date_str}:**\nNext shop reset is {next_shop_reset}\n(Not every card is stored at the moment. If there is an image missing, it will not be sent.)"
    else:
        header = f"**Here's the shop right now:**\nNext shop reset is {next_shop_reset}\n(Not every card is stored at the moment. If there is an image missing, it will not be sent.)"

    pc_directory = "./BomblinePCs"
    extensions = [".png", ".gif"]
    pc_list = [pc1, pc2, pc3]

    files = []
    embeds = []

    for i, pc in enumerate(pc_list):
        if not pc:
            continue

        path = None
        used_ext = None
        
        for ext in extensions:
            candidate = os.path.join(pc_directory, pc + ext)
            if os.path.exists(candidate):
                path = candidate
                used_ext = ext
                break

        if not path:
            continue

        filename = f"{pc}{used_ext}"

        file = discord.File(path, filename=filename)
        files.append(file)

        embed = discord.Embed(
            title=f"Playercard {i + 1}",
            description=pc,
            color=discord.Color.dark_grey()
        )
        embed.set_image(url=f"attachment://{filename}")

        embeds.append(embed)
    
    cur.close()
    conn.close()

    await interaction.response.send_message(
        content=header,
        embeds=embeds,
        files=files
    )
    
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(ascii_redfor)
    print(f"Mission time started. Plant the bomb at one of the bombsites.")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="status", description="Check the bot's status")
async def status_slash(interaction: discord.Interaction):
    await interaction.response.send_message("Bot is online.")   

@bot.tree.command(name="info", description="Get info regarding the bot")
async def info_slash(interaction: discord.Interaction):
    await interaction.response.send_message("Redfor Bot is a utility bot for bombline. It is a condensed version of what you would find on [placeholder](https://www.google.com/).\nCreated by [hipji](https://github.com/hipjiOfficial)")

@bot.tree.command(name="missing", description="Sends the missing playercards")
async def missing_slash(interaction: discord.Interaction):
    await interaction.response.send_message(get_missing_pcs())

@bot.tree.command(name="hello", description="Says hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")

#playcard dropdown command

CARD_FOLDER = Path("BomblinePCS")
ALL_CARDS = {p.stem: p for p in list(CARD_FOLDER.glob("*.png")) + list(CARD_FOLDER.glob("*.gif"))}

CARD_NAMES = sorted(ALL_CARDS.keys())
PAGE_SIZE = 20
MAX_PAGE = max(0, (len(CARD_NAMES) - 1) // PAGE_SIZE)

class PlayercardDropdown(discord.ui.Select):
    def __init__(self, page: int):
        self.page = page
        start = page * PAGE_SIZE
        end = start + PAGE_SIZE

        options = [
            discord.SelectOption(label=name, value=name)
            for name in CARD_NAMES[start:end]
        ]

        if not options:
            options = [
                discord.SelectOption(
                    label="Debug: No playercards available?"
                    value="None"
                    default=True
                )
            ]

        super().__init__(
            placeholder=f"Choose a playercard (Page {page + 1}/{MAX_PAGE + 1})",
            min_values=1,
            max_values=1,
            options=options
        )
        
    async def callback(self, interaction: discord.Interaction):
        chosen = self.values[0]
        path = ALL_CARDS[chosen]
        file = discord.File(path, filename=path.name)

        result = get_pc_info(chosen)

        if result:
            rarity, chance = result
        else:
            rarity, chance = "Unknown", "N/A"

        await interaction.response.send_message(
            content=(
                f"**{chosen}**\n"
                f"Rarity: **[{rarity}]**\n"
                f"Drop Chance: **{chance}%**"
            ),
            file=file
        )


class PlayercardView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.page = 0
        self.dropdown = PlayercardDropdown(self.page)
        self.add_item(self.dropdown)

    def refresh_dropdown(self):
        self.remove_item(self.dropdown)
        self.dropdown = PlayercardDropdown(self.page)
        self.add_item(self.dropdown)

    @discord.ui.button(label="<- Prev", style=discord.ButtonStyle.secondary)
    async def prev_page(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        if self.page > 0:
            self.page -= 1
            self.refresh_dropdown()
            await interaction.response.edit_message(view=self)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="-> Next", style=discord.ButtonStyle.secondary)
    async def next_page(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        if self.page < MAX_PAGE:
            self.page += 1
            self.refresh_dropdown()
            await interaction.response.edit_message(view=self)
        else:
            await interaction.response.defer()


@bot.tree.command(
    name="getplayercard",
    description="Select a playercard from a dropdown"
)
async def getplayercard_slash(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Select a playercard:",
        view=PlayercardView()
    )

bot.run(bot_token)


