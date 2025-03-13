# filepath: c:\Users\Admn\OneDrive\Escritorio\proyectos\GameBot\src\bot.py
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Asegúrate de que el bot tiene acceso a los miembros

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} ha iniciado sesión.')

vidas = {}

@bot.command(name='game')
async def start_game(ctx):
    reglas = '''
Reglas del juego:
- El juego funciona como una ruleta rusa.
- El bot elegirá a un jugador al azar para que inicie el juego.
- El jugador elegido deberá elegir entre escribir la palabra "!bang" en el chat.
- Al escribir "!bang", pueden pasar dos cosas:
  - El jugador sobrevive y el juego continúa.
  - El jugador pierde una vida y se debe quitar una prenda.
- En caso de perder una prenda debe enviar al canal de texto una prueba de que se quitó la prenda.
    - Puede ser una foto de la prenda en el suelo
    - o puede ser una selfie con la prenda en la mano.
- La probabilidad de perder una vida es del 45%.
- El jugador elegido también tiene otra opción. Puede escribir la palabra "!ratata" en el chat.
- Al escribir "!ratata", cambian los porcentajes de probabilidad de perder una vida.
    - La probabilidad de perder una vida es del 75%. 
    - Pero el otro 25% es la probabilidad de dispararle a otro jugador al azar.
    - Si le dispara a otro jugador, el otro jugador pierde una vida y se quita una prenda.
- El juego termina cuando solo queda un jugador con vida (prenda).
'''
    await ctx.send(reglas)
    
    global jugadores
    jugadores = [member.name for member in ctx.channel.members if member.name != 'ewe']
    
    if not jugadores:
        await ctx.send('No hay jugadores disponibles para iniciar el juego.')
        return
    
    jugador_inicial = random.choice(jugadores)
    await ctx.send(f'¡El juego ha comenzado! El primer turno es para {jugador_inicial}.')

@bot.command(name='turno')
async def turno(ctx):
    if not jugadores:
        await ctx.send('No hay jugadores disponibles para continuar el juego.')
        return
    
    jugador_siguiente = random.choice(jugadores)
    await ctx.send(f'El siguiente turno es para {jugador_siguiente}. ¡Buena suerte!')

@bot.command(name='setvidas')
async def set_vidas(ctx, n: int):
    if 1 <= n <= 5:
        global vidas
        for member in ctx.channel.members:
            if member.name != 'ewe':
                vidas[member.name] = n
        await ctx.send(f'Las vidas de los jugadores se han establecido en {n}.')
    else:
        await ctx.send('Por favor, ingrese un número entre 1 y 5.')

@bot.command(name='vidas')
async def get_vidas(ctx):
    vidas_text = "\n".join([f'{member}: {vidas[member]} vidas' for member in vidas])
    await ctx.send(f'Vidas de los jugadores:\n{vidas_text}')

@bot.command(name='comandos')
async def comandos(ctx): 
    #se deben listar los comandos disponibles
    comandos = '''
    Comandos disponibles: 
    !bang: disparar con 45% probabilidad de perder una vida.
    !ratata: disparar con 25% de probabilidad de herir a otro jugador, 
    !jugadores: lista de los jugadores en el canal,
    !vidas: lista de las vidas de los jugadores,
    -------------------------------------------
    Comandos de administrador:
    !setvidas: establecer el número de vidas de los jugadores.
    !game: iniciar el juego.
    !comandos: lista de los comandos disponibles.
    ''' 
    await ctx.send(comandos)


    @bot.command(name='bang')
    async def bang(ctx):
        jugador = ctx.author.name
        if random.random() < 0.45:
            vidas[jugador] -= 1
            if vidas[jugador] <= 0:
                await ctx.send(f'{jugador} ha perdido una vida y ha sido eliminado del juego. No olvide que se debe quedar desnudo y enviar pruebas.')
                jugadores.remove(jugador)
            else:
                await ctx.send(f'{jugador} ha perdido una vida. Le quedan {vidas[jugador]} vidas. No olvide que se debe quitarse una prenda y enviar pruebas.')
        else:
            await ctx.send(f'{jugador} se ha salvado.')

    @bot.command(name='ratata')
    async def ratata(ctx):
        jugador = ctx.author.name
        if random.random() < 0.75:
            vidas[jugador] -= 1
            if vidas[jugador] <= 0:
                await ctx.send(f'{jugador} ha perdido una vida y ha sido eliminado del juego. No olvide que se debe quedar desnudo y enviar pruebas.')
                jugadores.remove(jugador)
            else:
                await ctx.send(f'{jugador} ha perdido una vida. Le quedan {vidas[jugador]} vidas. No olvide que se debe quitarse una prenda y enviar pruebas.')
        else:
            otro_jugador = random.choice([j for j in jugadores if j != jugador])
            vidas[otro_jugador] -= 1
            if vidas[otro_jugador] <= 0:
                await ctx.send(f'{otro_jugador} ha perdido una vida y ha sido eliminado del juego. No olvide que se debe quedar desnudo y enviar pruebas.')
                jugadores.remove(otro_jugador)
            else:
                await ctx.send(f'{otro_jugador} ha perdido una vida por culpa de {jugador}. Le quedan {vidas[otro_jugador]} vidas. No olvide que se debe quitarse una prenda y enviar pruebas.')

@bot.command(name='members')
async def list_members(ctx):
    members = ctx.guild.members
    member_names = [member.name for member in members]
    await ctx.send(f'Miembros en el servidor: {", ".join(member_names)}')

@bot.command(name='jugadores')
async def list_members(ctx):
    members_in_canal = ctx.channel.members
    member_names = [member.name for member in members_in_canal]
    await ctx.send(f'Miembros en el canal: {", ".join(member_names)}')

@bot.command(name='actividad')
async def list_activities(ctx):
    activities = ["Foto desnudo en la cocina", "Foto desnudo en el baño", "Foto desnudo en la sala",
                  "Foto desnudo en la habitación", "Foto desnudo fuera de casa", "Foto desnudo en la playa",
                  "Foto poto desnudo","Foto teta desnuda","foto trabajando desnudo", "video saltando desnudo"]
    activity = random.choice(activities)
    await ctx.send(f'Actividad: {activity}')



bot.run(TOKEN)