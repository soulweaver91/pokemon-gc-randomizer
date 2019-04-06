#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum, IntEnum


class PokemonSpecies(IntEnum):
    NONE = 0x000
    BULBASAUR = 0x001
    IVYSAUR = 0x002
    VENUSAUR = 0x003
    CHARMANDER = 0x004
    CHARMELEON = 0x005
    CHARIZARD = 0x006
    SQUIRTLE = 0x007
    WARTORTLE = 0x008
    BLASTOISE = 0x009
    CATERPIE = 0x00A
    METAPOD = 0x00B
    BUTTERFREE = 0x00C
    WEEDLE = 0x00D
    KAKUNA = 0x00E
    BEEDRILL = 0x00F
    PIDGEY = 0x010
    PIDGEOTTO = 0x011
    PIDGEOT = 0x012
    RATTATA = 0x013
    RATICATE = 0x014
    SPEAROW = 0x015
    FEAROW = 0x016
    EKANS = 0x017
    ARBOK = 0x018
    PIKACHU = 0x019
    RAICHU = 0x01A
    SANDSHREW = 0x01B
    SANDSLASH = 0x01C
    NIDORAN_F = 0x01D
    NIDORINA = 0x01E
    NIDOQUEEN = 0x01F
    NIDORAN_M = 0x020
    NIDORINO = 0x021
    NIDOKING = 0x022
    CLEFAIRY = 0x023
    CLEFABLE = 0x024
    VULPIX = 0x025
    NINETALES = 0x026
    JIGGLYPUFF = 0x027
    WIGGLYTUFF = 0x028
    ZUBAT = 0x029
    GOLBAT = 0x02A
    ODDISH = 0x02B
    GLOOM = 0x02C
    VILEPLUME = 0x02D
    PARAS = 0x02E
    PARASECT = 0x02F
    VENONAT = 0x030
    VENOMOTH = 0x031
    DIGLETT = 0x032
    DUGTRIO = 0x033
    MEOWTH = 0x034
    PERSIAN = 0x035
    PSYDUCK = 0x036
    GOLDUCK = 0x037
    MANKEY = 0x038
    PRIMEAPE = 0x039
    GROWLITHE = 0x03A
    ARCANINE = 0x03B
    POLIWAG = 0x03C
    POLIWHIRL = 0x03D
    POLIWRATH = 0x03E
    ABRA = 0x03F
    KADABRA = 0x040
    ALAKAZAM = 0x041
    MACHOP = 0x042
    MACHOKE = 0x043
    MACHAMP = 0x044
    BELLSPROUT = 0x045
    WEEPINBELL = 0x046
    VICTREEBEL = 0x047
    TENTACOOL = 0x048
    TENTACRUEL = 0x049
    GEODUDE = 0x04A
    GRAVELER = 0x04B
    GOLEM = 0x04C
    PONYTA = 0x04D
    RAPIDASH = 0x04E
    SLOWPOKE = 0x04F
    SLOWBRO = 0x050
    MAGNEMITE = 0x051
    MAGNETON = 0x052
    FARFETCH_D = 0x053
    DODUO = 0x054
    DODRIO = 0x055
    SEEL = 0x056
    DEWGONG = 0x057
    GRIMER = 0x058
    MUK = 0x059
    SHELLDER = 0x05A
    CLOYSTER = 0x05B
    GASTLY = 0x05C
    HAUNTER = 0x05D
    GENGAR = 0x05E
    ONIX = 0x05F
    DROWZEE = 0x060
    HYPNO = 0x061
    KRABBY = 0x062
    KINGLER = 0x063
    VOLTORB = 0x064
    ELECTRODE = 0x065
    EXEGGCUTE = 0x066
    EXEGGUTOR = 0x067
    CUBONE = 0x068
    MAROWAK = 0x069
    HITMONLEE = 0x06A
    HITMONCHAN = 0x06B
    LICKITUNG = 0x06C
    KOFFING = 0x06D
    WEEZING = 0x06E
    RHYHORN = 0x06F
    RHYDON = 0x070
    CHANSEY = 0x071
    TANGELA = 0x072
    KANGASKHAN = 0x073
    HORSEA = 0x074
    SEADRA = 0x075
    GOLDEEN = 0x076
    SEAKING = 0x077
    STARYU = 0x078
    STARMIE = 0x079
    MR_MIME = 0x07A
    SCYTHER = 0x07B
    JYNX = 0x07C
    ELECTABUZZ = 0x07D
    MAGMAR = 0x07E
    PINSIR = 0x07F
    TAUROS = 0x080
    MAGIKARP = 0x081
    GYARADOS = 0x082
    LAPRAS = 0x083
    DITTO = 0x084
    EEVEE = 0x085
    VAPOREON = 0x086
    JOLTEON = 0x087
    FLAREON = 0x088
    PORYGON = 0x089
    OMANYTE = 0x08A
    OMASTAR = 0x08B
    KABUTO = 0x08C
    KABUTOPS = 0x08D
    AERODACTYL = 0x08E
    SNORLAX = 0x08F
    ARTICUNO = 0x090
    ZAPDOS = 0x091
    MOLTRES = 0x092
    DRATINI = 0x093
    DRAGONAIR = 0x094
    DRAGONITE = 0x095
    MEWTWO = 0x096
    MEW = 0x097
    CHIKORITA = 0x098
    BAYLEEF = 0x099
    MEGANIUM = 0x09A
    CYNDAQUIL = 0x09B
    QUILAVA = 0x09C
    TYPHLOSION = 0x09D
    TOTODILE = 0x09E
    CROCONAW = 0x09F
    FERALIGATR = 0x0A0
    SENTRET = 0x0A1
    FURRET = 0x0A2
    HOOTHOOT = 0x0A3
    NOCTOWL = 0x0A4
    LEDYBA = 0x0A5
    LEDIAN = 0x0A6
    SPINARAK = 0x0A7
    ARIADOS = 0x0A8
    CROBAT = 0x0A9
    CHINCHOU = 0x0AA
    LANTURN = 0x0AB
    PICHU = 0x0AC
    CLEFFA = 0x0AD
    IGGLYBUFF = 0x0AE
    TOGEPI = 0x0AF
    TOGETIC = 0x0B0
    NATU = 0x0B1
    XATU = 0x0B2
    MAREEP = 0x0B3
    FLAAFFY = 0x0B4
    AMPHAROS = 0x0B5
    BELLOSSOM = 0x0B6
    MARILL = 0x0B7
    AZUMARILL = 0x0B8
    SUDOWOODO = 0x0B9
    POLITOED = 0x0BA
    HOPPIP = 0x0BB
    SKIPLOOM = 0x0BC
    JUMPLUFF = 0x0BD
    AIPOM = 0x0BE
    SUNKERN = 0x0BF
    SUNFLORA = 0x0C0
    YANMA = 0x0C1
    WOOPER = 0x0C2
    QUAGSIRE = 0x0C3
    ESPEON = 0x0C4
    UMBREON = 0x0C5
    MURKROW = 0x0C6
    SLOWKING = 0x0C7
    MISDREAVUS = 0x0C8
    UNOWN = 0x0C9
    WOBBUFFET = 0x0CA
    GIRAFARIG = 0x0CB
    PINECO = 0x0CC
    FORRETRESS = 0x0CD
    DUNSPARCE = 0x0CE
    GLIGAR = 0x0CF
    STEELIX = 0x0D0
    SNUBBULL = 0x0D1
    GRANBULL = 0x0D2
    QWILFISH = 0x0D3
    SCIZOR = 0x0D4
    SHUCKLE = 0x0D5
    HERACROSS = 0x0D6
    SNEASEL = 0x0D7
    TEDDIURSA = 0x0D8
    URSARING = 0x0D9
    SLUGMA = 0x0DA
    MAGCARGO = 0x0DB
    SWINUB = 0x0DC
    PILOSWINE = 0x0DD
    CORSOLA = 0x0DE
    REMORAID = 0x0DF
    OCTILLERY = 0x0E0
    DELIBIRD = 0x0E1
    MANTINE = 0x0E2
    SKARMORY = 0x0E3
    HOUNDOUR = 0x0E4
    HOUNDOOM = 0x0E5
    KINGDRA = 0x0E6
    PHANPY = 0x0E7
    DONPHAN = 0x0E8
    PORYGON2 = 0x0E9
    STANTLER = 0x0EA
    SMEARGLE = 0x0EB
    TYROGUE = 0x0EC
    HITMONTOP = 0x0ED
    SMOOCHUM = 0x0EE
    ELEKID = 0x0EF
    MAGBY = 0x0F0
    MILTANK = 0x0F1
    BLISSEY = 0x0F2
    RAIKOU = 0x0F3
    ENTEI = 0x0F4
    SUICUNE = 0x0F5
    LARVITAR = 0x0F6
    PUPITAR = 0x0F7
    TYRANITAR = 0x0F8
    LUGIA = 0x0F9
    HO_OH = 0x0FA
    CELEBI = 0x0FB
    UNUSED_252 = 0x0FC
    UNUSED_253 = 0x0FD
    UNUSED_254 = 0x0FE
    UNUSED_255 = 0x0FF
    UNUSED_256 = 0x100
    UNUSED_257 = 0x101
    UNUSED_258 = 0x102
    UNUSED_259 = 0x103
    UNUSED_260 = 0x104
    UNUSED_261 = 0x105
    UNUSED_262 = 0x106
    UNUSED_263 = 0x107
    UNUSED_264 = 0x108
    UNUSED_265 = 0x109
    UNUSED_266 = 0x10A
    UNUSED_267 = 0x10B
    UNUSED_268 = 0x10C
    UNUSED_269 = 0x10D
    UNUSED_270 = 0x10E
    UNUSED_271 = 0x10F
    UNUSED_272 = 0x110
    UNUSED_273 = 0x111
    UNUSED_274 = 0x112
    UNUSED_275 = 0x113
    UNUSED_276 = 0x114
    TREECKO = 0x115
    GROVYLE = 0x116
    SCEPTILE = 0x117
    TORCHIC = 0x118
    COMBUSKEN = 0x119
    BLAZIKEN = 0x11A
    MUDKIP = 0x11B
    MARSHTOMP = 0x11C
    SWAMPERT = 0x11D
    POOCHYENA = 0x11E
    MIGHTYENA = 0x11F
    ZIGZAGOON = 0x120
    LINOONE = 0x121
    WURMPLE = 0x122
    SILCOON = 0x123
    BEAUTIFLY = 0x124
    CASCOON = 0x125
    DUSTOX = 0x126
    LOTAD = 0x127
    LOMBRE = 0x128
    LUDICOLO = 0x129
    SEEDOT = 0x12A
    NUZLEAF = 0x12B
    SHIFTRY = 0x12C
    NINCADA = 0x12D
    NINJASK = 0x12E
    SHEDINJA = 0x12F
    TAILLOW = 0x130
    SWELLOW = 0x131
    SHROOMISH = 0x132
    BRELOOM = 0x133
    SPINDA = 0x134
    WINGULL = 0x135
    PELIPPER = 0x136
    SURSKIT = 0x137
    MASQUERAIN = 0x138
    WAILMER = 0x139
    WAILORD = 0x13A
    SKITTY = 0x13B
    DELCATTY = 0x13C
    KECLEON = 0x13D
    BALTOY = 0x13E
    CLAYDOL = 0x13F
    NOSEPASS = 0x140
    TORKOAL = 0x141
    SABLEYE = 0x142
    BARBOACH = 0x143
    WHISCASH = 0x144
    LUVDISC = 0x145
    CORPHISH = 0x146
    CRAWDAUNT = 0x147
    FEEBAS = 0x148
    MILOTIC = 0x149
    CARVANHA = 0x14A
    SHARPEDO = 0x14B
    TRAPINCH = 0x14C
    VIBRAVA = 0x14D
    FLYGON = 0x14E
    MAKUHITA = 0x14F
    HARIYAMA = 0x150
    ELECTRIKE = 0x151
    MANECTRIC = 0x152
    NUMEL = 0x153
    CAMERUPT = 0x154
    SPHEAL = 0x155
    SEALEO = 0x156
    WALREIN = 0x157
    CACNEA = 0x158
    CACTURNE = 0x159
    SNORUNT = 0x15A
    GLALIE = 0x15B
    LUNATONE = 0x15C
    SOLROCK = 0x15D
    AZURILL = 0x15E
    SPOINK = 0x15F
    GRUMPIG = 0x160
    PLUSLE = 0x161
    MINUN = 0x162
    MAWILE = 0x163
    MEDITITE = 0x164
    MEDICHAM = 0x165
    SWABLU = 0x166
    ALTARIA = 0x167
    WYNAUT = 0x168
    DUSKULL = 0x169
    DUSCLOPS = 0x16A
    ROSELIA = 0x16B
    SLAKOTH = 0x16C
    VIGOROTH = 0x16D
    SLAKING = 0x16E
    GULPIN = 0x16F
    SWALOT = 0x170
    TROPIUS = 0x171
    WHISMUR = 0x172
    LOUDRED = 0x173
    EXPLOUD = 0x174
    CLAMPERL = 0x175
    HUNTAIL = 0x176
    GOREBYSS = 0x177
    ABSOL = 0x178
    SHUPPET = 0x179
    BANETTE = 0x17A
    SEVIPER = 0x17B
    ZANGOOSE = 0x17C
    RELICANTH = 0x17D
    ARON = 0x17E
    LAIRON = 0x17F
    AGGRON = 0x180
    CASTFORM = 0x181
    VOLBEAT = 0x182
    ILLUMISE = 0x183
    LILEEP = 0x184
    CRADILY = 0x185
    ANORITH = 0x186
    ARMALDO = 0x187
    RALTS = 0x188
    KIRLIA = 0x189
    GARDEVOIR = 0x18A
    BAGON = 0x18B
    SHELGON = 0x18C
    SALAMENCE = 0x18D
    BELDUM = 0x18E
    METANG = 0x18F
    METAGROSS = 0x190
    REGIROCK = 0x191
    REGICE = 0x192
    REGISTEEL = 0x193
    KYOGRE = 0x194
    GROUDON = 0x195
    RAYQUAZA = 0x196
    LATIAS = 0x197
    LATIOS = 0x198
    JIRACHI = 0x199
    DEOXYS = 0x19A
    CHIMECHO = 0x19B
    EGG = 0x19C
    BONSLY = 0x19D
    MUNCHLAX = 0x19E


class Type(Enum):
    NORMAL = 0x00
    FIGHTING = 0x01
    FLYING = 0x02
    POISON = 0x03
    GROUND = 0x04
    ROCK = 0x05
    BUG = 0x06
    GHOST = 0x07
    STEEL = 0x08
    CURSE = 0x09
    FIRE = 0x0A
    WATER = 0x0B
    GRASS = 0x0C
    ELECTRIC = 0x0D
    PSYCHIC = 0x0E
    ICE = 0x0F
    DRAGON = 0x10
    DARK = 0x11

    # TODO: temp value
    SHADOW = 0xFF


class Ability(IntEnum):
    NONE = 0x00
    STENCH = 0x01
    DRIZZLE = 0x02
    SPEED_BOOST = 0x03
    BATTLE_ARMOR = 0x04
    STURDY = 0x05
    DAMP = 0x06
    LIMBER = 0x07
    SAND_VEIL = 0x08
    STATIC = 0x09
    VOLT_ABSORB = 0x0A
    WATER_ABSORB = 0x0B
    OBLIVIOUS = 0x0C
    CLOUD_NINE = 0x0D
    COMPOUND_EYES = 0x0E
    INSOMNIA = 0x0F
    COLOR_CHANGE = 0x10
    IMMUNITY = 0x11
    FLASH_FIRE = 0x12
    SHIELD_DUST = 0x13
    OWN_TEMPO = 0x14
    SUCTION_CUPS = 0x15
    INTIMIDATE = 0x16
    SHADOW_TAG = 0x17
    ROUGH_SKIN = 0x18
    WONDER_GUARD = 0x19
    LEVITATE = 0x1A
    EFFECT_SPORE = 0x1B
    SYNCHRONIZE = 0x1C
    CLEAR_BODY = 0x1D
    NATURAL_CURE = 0x1E
    LIGHTING_ROD = 0x1F
    SERENE_GRACE = 0x20
    SWIFT_SWIM = 0x21
    CHLOROPHYLL = 0x22
    ILLUMINATE = 0x23
    TRACE = 0x24
    HUGE_POWER = 0x25
    POISON_POINT = 0x26
    INNER_FOCUS = 0x27
    MAGMA_ARMOR = 0x28
    WATER_VEIL = 0x29
    MAGNET_PULL = 0x2A
    SOUNDPROOF = 0x2B
    RAIN_DISH = 0x2C
    SAND_STREAM = 0x2D
    PRESSURE = 0x2E
    THICK_FAT = 0x2F
    EARLY_BIRD = 0x30
    FLAME_BODY = 0x31
    RUN_AWAY = 0x32
    KEEN_EYE = 0x33
    HYPER_CUTTER = 0x34
    PICKUP = 0x35
    TRUANT = 0x36
    HUSTLE = 0x37
    CUTE_CHARM = 0x38
    PLUS = 0x39
    MINUS = 0x3A
    FORECAST = 0x3B
    STICKY_HOLD = 0x3C
    SHED_SKIN = 0x3D
    GUTS = 0x3E
    MARVEL_SCALE = 0x3F
    LIQUID_OOZE = 0x40
    OVERGROW = 0x41
    BLAZE = 0x42
    TORRENT = 0x43
    SWARM = 0x44
    ROCK_HEAD = 0x45
    DROUGHT = 0x46
    ARENA_TRAP = 0x47
    VITAL_SPIRIT = 0x48
    WHITE_SMOKE = 0x49
    PURE_POWER = 0x4A
    SHELL_ARMOR = 0x4B
    CACOPHONY = 0x4C
    AIR_LOCK = 0x4D


UNIQUE_DAMAGING_MOVE = -1
STATUS_MOVE = 0
OHKO_MOVE = 1000


# TODO: these should be read from the ISO
class Move(Enum):
    NONE = (0x00, "-", Type.NORMAL, STATUS_MOVE)
    POUND = (0x01, "Pound", Type.NORMAL, 40)
    KARATE_CHOP = (0x02, "Karate Chop", Type.FIGHTING, 50)
    DOUBLESLAP = (0x03, "DoubleSlap", Type.NORMAL, 15)
    DOUBLE_SLAP = DOUBLESLAP
    COMET_PUNCH = (0x04, "Comet Punch", Type.NORMAL, 18)
    MEGA_PUNCH = (0x05, "Mega Punch", Type.NORMAL, 80)
    PAY_DAY = (0x06, "Pay Day", Type.NORMAL, 40)
    FIRE_PUNCH = (0x07, "Fire Punch", Type.FIRE, 75)
    ICE_PUNCH = (0x08, "Ice Punch", Type.ICE, 75)
    THUNDERPUNCH = (0x09, "ThunderPunch", Type.ELECTRIC, 75)
    THUNDER_PUNCH = THUNDERPUNCH
    SCRATCH = (0x0A, "Scratch", Type.NORMAL, 40)
    VICEGRIP = (0x0B, "ViceGrip", Type.NORMAL, 55)
    VICE_GRIP = VICEGRIP
    GUILLOTINE = (0x0C, "Guillotine", Type.NORMAL, OHKO_MOVE)
    RAZOR_WIND = (0x0D, "Razor Wind", Type.NORMAL, 80)
    SWORDS_DANCE = (0x0E, "Swords Dance", Type.NORMAL, STATUS_MOVE)
    CUT = (0x0F, "Cut", Type.NORMAL, 50)
    GUST = (0x10, "Gust", Type.FLYING, 40)
    WING_ATTACK = (0x11, "Wing Attack", Type.FLYING, 60)
    WHIRLWIND = (0x12, "Whirlwind", Type.NORMAL, STATUS_MOVE)
    FLY = (0x13, "Fly", Type.FLYING, 90)
    BIND = (0x14, "Bind", Type.NORMAL, 15)
    SLAM = (0x15, "Slam", Type.NORMAL, 80)
    VINE_WHIP = (0x16, "Vine Whip", Type.GRASS, 35)
    STOMP = (0x17, "Stomp", Type.NORMAL, 65)
    DOUBLE_KICK = (0x18, "Double Kick", Type.FIGHTING, 30)
    MEGA_KICK = (0x19, "Mega Kick", Type.NORMAL, 120)
    JUMP_KICK = (0x1A, "Jump Kick", Type.FIGHTING, 70)
    ROLLING_KICK = (0x1B, "Rolling Kick", Type.FIGHTING, 60)
    SAND_ATTACK = (0x1C, "Sand-Attack", Type.GROUND, STATUS_MOVE)
    HEADBUTT = (0x1D, "Headbutt", Type.NORMAL, 70)
    HORN_ATTACK = (0x1E, "Horn Attack", Type.NORMAL, 65)
    FURY_ATTACK = (0x1F, "Fury Attack", Type.NORMAL, 15)
    HORN_DRILL = (0x20, "Horn Drill", Type.NORMAL, OHKO_MOVE)
    TACKLE = (0x21, "Tackle", Type.NORMAL, 35)
    BODY_SLAM = (0x22, "Body Slam", Type.NORMAL, 85)
    WRAP = (0x23, "Wrap", Type.NORMAL, 15)
    TAKE_DOWN = (0x24, "Take Down", Type.NORMAL, 90)
    THRASH = (0x25, "Thrash", Type.NORMAL, 90)
    DOUBLE_EDGE = (0x26, "Double-Edge", Type.NORMAL, 120)
    TAIL_WHIP = (0x27, "Tail Whip", Type.NORMAL, STATUS_MOVE)
    POISON_STING = (0x28, "Poison Sting", Type.POISON, 15)
    TWINEEDLE = (0x29, "Twineedle", Type.BUG, 25)
    PIN_MISSILE = (0x2A, "Pin Missile", Type.BUG, 14)
    LEER = (0x2B, "Leer", Type.NORMAL, STATUS_MOVE)
    BITE = (0x2C, "Bite", Type.DARK, 60)
    GROWL = (0x2D, "Growl", Type.NORMAL, STATUS_MOVE)
    ROAR = (0x2E, "Roar", Type.NORMAL, STATUS_MOVE)
    SING = (0x2F, "Sing", Type.NORMAL, STATUS_MOVE)
    SUPERSONIC = (0x30, "Supersonic", Type.NORMAL, STATUS_MOVE)
    SONICBOOM = (0x31, "SonicBoom", Type.NORMAL, UNIQUE_DAMAGING_MOVE)
    SONIC_BOOM = SONICBOOM
    DISABLE = (0x32, "Disable", Type.NORMAL, STATUS_MOVE)
    ACID = (0x33, "Acid", Type.POISON, 40)
    EMBER = (0x34, "Ember", Type.FIRE, 40)
    FLAMETHROWER = (0x35, "Flamethrower", Type.FIRE, 95)
    MIST = (0x36, "Mist", Type.ICE, STATUS_MOVE)
    WATER_GUN = (0x37, "Water Gun", Type.WATER, 40)
    HYDRO_PUMP = (0x38, "Hydro Pump", Type.WATER, 120)
    SURF = (0x39, "Surf", Type.WATER, 95)
    ICE_BEAM = (0x3A, "Ice Beam", Type.ICE, 95)
    BLIZZARD = (0x3B, "Blizzard", Type.ICE, 120)
    PSYBEAM = (0x3C, "Psybeam", Type.PSYCHIC, 65)
    BUBBLEBEAM = (0x3D, "BubbleBeam", Type.WATER, 65)
    BUBBLE_BEAM = BUBBLEBEAM
    AURORA_BEAM = (0x3E, "Aurora Beam", Type.ICE, 65)
    HYPER_BEAM = (0x3F, "Hyper Beam", Type.NORMAL, 150)
    PECK = (0x40, "Peck", Type.FLYING, 35)
    DRILL_PECK = (0x41, "Drill Peck", Type.FLYING, 80)
    SUBMISSION = (0x42, "Submission", Type.FIGHTING, 80)
    LOW_KICK = (0x43, "Low Kick", Type.FIGHTING, UNIQUE_DAMAGING_MOVE)
    COUNTER = (0x44, "Counter", Type.FIGHTING, UNIQUE_DAMAGING_MOVE)
    SEISMIC_TOSS = (0x45, "Seismic Toss", Type.FIGHTING, UNIQUE_DAMAGING_MOVE)
    STRENGTH = (0x46, "Strength", Type.NORMAL, 80)
    ABSORB = (0x47, "Absorb", Type.GRASS, 20)
    MEGA_DRAIN = (0x48, "Mega Drain", Type.GRASS, 40)
    LEECH_SEED = (0x49, "Leech Seed", Type.GRASS, STATUS_MOVE)
    GROWTH = (0x4A, "Growth", Type.NORMAL, STATUS_MOVE)
    RAZOR_LEAF = (0x4B, "Razor Leaf", Type.GRASS, 55)
    SOLARBEAM = (0x4C, "SolarBeam", Type.GRASS, 120)
    SOLAR_BEAM = SOLARBEAM
    POISONPOWDER = (0x4D, "PoisonPowder", Type.POISON, STATUS_MOVE)
    POISON_POWDER = POISONPOWDER
    STUN_SPORE = (0x4E, "Stun Spore", Type.GRASS, STATUS_MOVE)
    SLEEP_POWDER = (0x4F, "Sleep Powder", Type.GRASS, STATUS_MOVE)
    PETAL_DANCE = (0x50, "Petal Dance", Type.GRASS, 70)
    STRING_SHOT = (0x51, "String Shot", Type.BUG, STATUS_MOVE)
    DRAGON_RAGE = (0x52, "Dragon Rage", Type.DRAGON, UNIQUE_DAMAGING_MOVE)
    FIRE_SPIN = (0x53, "Fire Spin", Type.FIRE, 15)
    THUNDERSHOCK = (0x54, "ThunderShock", Type.ELECTRIC, 40)
    THUNDER_SHOCK = THUNDERSHOCK
    THUNDERBOLT = (0x55, "ThunderBolt", Type.ELECTRIC, 95)
    THUNDER_BOLT = THUNDERBOLT
    THUNDER_WAVE = (0x56, "Thunder Wave", Type.ELECTRIC, STATUS_MOVE)
    THUNDER = (0x57, "Thunder", Type.ELECTRIC, 120)
    ROCK_THROW = (0x58, "Rock Throw", Type.ROCK, 50)
    EARTHQUAKE = (0x59, "Earthquake", Type.GROUND, 100)
    FISSURE = (0x5A, "Fissure", Type.GROUND, OHKO_MOVE)
    DIG = (0x5B, "Dig", Type.GROUND, 80)
    TOXIC = (0x5C, "Toxic", Type.POISON, STATUS_MOVE)
    CONFUSION = (0x5D, "Confusion", Type.PSYCHIC, 50)
    PSYCHIC = (0x5E, "Psychic", Type.PSYCHIC, 90)
    HYPNOSIS = (0x5F, "Hypnosis", Type.PSYCHIC, STATUS_MOVE)
    MEDITATE = (0x60, "Meditate", Type.PSYCHIC, STATUS_MOVE)
    AGILITY = (0x61, "Agility", Type.PSYCHIC, STATUS_MOVE)
    QUICK_ATTACK = (0x62, "Quick Attack", Type.NORMAL, 40)
    RAGE = (0x63, "Rage", Type.NORMAL, 20)
    TELEPORT = (0x64, "Teleport", Type.PSYCHIC, STATUS_MOVE)
    NIGHT_SHADE = (0x65, "Night Shade", Type.GHOST, UNIQUE_DAMAGING_MOVE)
    MIMIC = (0x66, "Mimic", Type.NORMAL, STATUS_MOVE)
    SCREECH = (0x67, "Screech", Type.NORMAL, STATUS_MOVE)
    DOUBLE_TEAM = (0x68, "Double Team", Type.NORMAL, STATUS_MOVE)
    RECOVER = (0x69, "Recover", Type.NORMAL, STATUS_MOVE)
    HARDEN = (0x6A, "Harden", Type.NORMAL, STATUS_MOVE)
    MINIMIZE = (0x6B, "Minimize", Type.NORMAL, STATUS_MOVE)
    SMOKESCREEN = (0x6C, "SmokeScreen", Type.NORMAL, STATUS_MOVE)
    SMOKE_SCREEN = SMOKESCREEN
    CONFUSE_RAY = (0x6D, "Confuse Ray", Type.GHOST, STATUS_MOVE)
    WITHDRAW = (0x6E, "Withdraw", Type.WATER, STATUS_MOVE)
    DEFENSE_CURL = (0x6F, "Defense Curl", Type.NORMAL, STATUS_MOVE)
    BARRIER = (0x70, "Barrier", Type.PSYCHIC, STATUS_MOVE)
    LIGHT_SCREEN = (0x71, "Light Screen", Type.PSYCHIC, STATUS_MOVE)
    HAZE = (0x72, "Haze", Type.ICE, STATUS_MOVE)
    REFLECT = (0x73, "Reflect", Type.PSYCHIC, STATUS_MOVE)
    FOCUS_ENERGY = (0x74, "Focus Energy", Type.NORMAL, STATUS_MOVE)
    BIDE = (0x75, "Bide", Type.NORMAL, UNIQUE_DAMAGING_MOVE)
    METRONOME = (0x76, "Metronome", Type.NORMAL, UNIQUE_DAMAGING_MOVE)
    MIRROR_MOVE = (0x77, "Mirror Move", Type.FLYING, UNIQUE_DAMAGING_MOVE)
    SELFDESTRUCT = (0x78, "SelfDestruct", Type.NORMAL, 200)
    SELF_DESTRUCT = SELFDESTRUCT
    EGG_BOMB = (0x79, "Egg Bomb", Type.NORMAL, 100)
    LICK = (0x7A, "Lick", Type.GHOST, 20)
    SMOG = (0x7B, "Smog", Type.POISON, 20)
    SLUDGE = (0x7C, "Sludge", Type.POISON, 65)
    BONE_CLUB = (0x7D, "Bone Club", Type.GROUND, 65)
    FIRE_BLAST = (0x7E, "Fire Blast", Type.FIRE, 120)
    WATERFALL = (0x7F, "Waterfall", Type.WATER, 80)
    CLAMP = (0x80, "Clamp", Type.WATER, 35)
    SWIFT = (0x81, "Swift", Type.NORMAL, 60)
    SKULL_BASH = (0x82, "Skull Bash", Type.NORMAL, 100)
    SPIKE_CANNON = (0x83, "Spike Cannon", Type.NORMAL, 20)
    CONSTRICT = (0x84, "Constrict", Type.NORMAL, 10)
    AMNESIA = (0x85, "Amnesia", Type.PSYCHIC, STATUS_MOVE)
    KINESIS = (0x86, "Kinesis", Type.PSYCHIC, STATUS_MOVE)
    SOFTBOILED = (0x87, "Softboiled", Type.NORMAL, STATUS_MOVE)
    SOFT_BOILED = SOFTBOILED
    HI_JUMP_KICK = (0x88, "Hi Jump Kick", Type.FIGHTING, 100)
    HIGH_JUMP_KICK = HI_JUMP_KICK
    GLARE = (0x89, "Glare", Type.NORMAL, STATUS_MOVE)
    DREAM_EATER = (0x8A, "Dream Eater", Type.PSYCHIC, 100)
    POISON_GAS = (0x8B, "Poison Gas", Type.POISON, STATUS_MOVE)
    BARRAGE = (0x8C, "Barrage", Type.NORMAL, 15)
    LEECH_LIFE = (0x8D, "Leech Life", Type.BUG, 20)
    LOVELY_KISS = (0x8E, "Lovely Kiss", Type.NORMAL, STATUS_MOVE)
    SKY_ATTACK = (0x8F, "Sky Attack", Type.FLYING, 140)
    TRANSFORM = (0x90, "Transform", Type.NORMAL, STATUS_MOVE)
    BUBBLE = (0x91, "Bubble", Type.WATER, 20)
    DIZZY_PUNCH = (0x92, "Dizzy Punch", Type.NORMAL, 70)
    SPORE = (0x93, "Spore", Type.GRASS, STATUS_MOVE)
    FLASH = (0x94, "Flash", Type.NORMAL, STATUS_MOVE)
    PSYWAVE = (0x95, "Psywave", Type.PSYCHIC, UNIQUE_DAMAGING_MOVE)
    SPLASH = (0x96, "Splash", Type.NORMAL, STATUS_MOVE)
    ACID_ARMOR = (0x97, "Acid Armor", Type.POISON, STATUS_MOVE)
    CRABHAMMER = (0x98, "Crabhammer", Type.WATER, 90)
    EXPLOSION = (0x99, "Explosion", Type.NORMAL, 250)
    FURY_SWIPES = (0x9A, "Fury Swipes", Type.NORMAL, 18)
    BONEMERANG = (0x9B, "Bonemerang", Type.GROUND, 50)
    REST = (0x9C, "Rest", Type.PSYCHIC, STATUS_MOVE)
    ROCK_SLIDE = (0x9D, "Rock Slide", Type.ROCK, 75)
    HYPER_FANG = (0x9E, "Hyper Fang", Type.NORMAL, 80)
    SHARPEN = (0x9F, "Sharpen", Type.NORMAL, STATUS_MOVE)
    CONVERSION = (0xA0, "Conversion", Type.NORMAL, STATUS_MOVE)
    TRI_ATTACK = (0xA1, "Tri Attack", Type.NORMAL, 80)
    SUPER_FANG = (0xA2, "Super Fang", Type.NORMAL, UNIQUE_DAMAGING_MOVE)
    SLASH = (0xA3, "Slash", Type.NORMAL, 70)
    SUBSTITUTE = (0xA4, "Substitute", Type.NORMAL, STATUS_MOVE)
    STRUGGLE = (0xA5, "Struggle", Type.NORMAL, 50)
    SKETCH = (0xA6, "Sketch", Type.NORMAL, STATUS_MOVE)
    TRIPLE_KICK = (0xA7, "Triple Kick", Type.FIGHTING, 10)
    THIEF = (0xA8, "Thief", Type.DARK, 40)
    SPIDER_WEB = (0xA9, "Spider Web", Type.BUG, STATUS_MOVE)
    MIND_READER = (0xAA, "Mind Reader", Type.NORMAL, STATUS_MOVE)
    NIGHTMARE = (0xAB, "Nightmare", Type.GHOST, STATUS_MOVE)
    FLAME_WHEEL = (0xAC, "Flame Wheel", Type.FIRE, 60)
    SNORE = (0xAD, "Snore", Type.NORMAL, 40)
    CURSE = (0xAE, "Curse", Type.CURSE, STATUS_MOVE)
    FLAIL = (0xAF, "Flail", Type.NORMAL, UNIQUE_DAMAGING_MOVE)
    CONVERSION_2 = (0xB0, "Conversion 2", Type.NORMAL, STATUS_MOVE)
    AEROBLAST = (0xB1, "Aeroblast", Type.FLYING, 100)
    COTTON_SPORE = (0xB2, "Cotton Spore", Type.GRASS, STATUS_MOVE)
    REVERSAL = (0xB3, "Reversal", Type.FIGHTING, UNIQUE_DAMAGING_MOVE)
    SPITE = (0xB4, "Spite", Type.GHOST, STATUS_MOVE)
    POWDER_SNOW = (0xB5, "Powder Snow", Type.ICE, 40)
    PROTECT = (0xB6, "Protect", Type.NORMAL, STATUS_MOVE)
    MACH_PUNCH = (0xB7, "Mach Punch", Type.FIGHTING, 40)
    SCARY_FACE = (0xB8, "Scary Face", Type.NORMAL, STATUS_MOVE)
    FAINT_ATTACK = (0xB9, "Faint Attack", Type.DARK, 60)
    FEINT_ATTACK = FAINT_ATTACK
    SWEET_KISS = (0xBA, "Sweet Kiss", Type.NORMAL, STATUS_MOVE)
    BELLY_DRUM = (0xBB, "Belly Drum", Type.NORMAL, STATUS_MOVE)
    SLUDGE_BOMB = (0xBC, "Sludge Bomb", Type.POISON, 90)
    MUD_SLAP = (0xBD, "Mud-Slap", Type.GROUND, 20)
    OCTAZOOKA = (0xBE, "Octazooka", Type.WATER, 65)
    SPIKES = (0xBF, "Spikes", Type.GROUND, STATUS_MOVE)
    ZAP_CANNON = (0xC0, "Zap Cannon", Type.ELECTRIC, 120)
    FORESIGHT = (0xC1, "Foresight", Type.NORMAL, STATUS_MOVE)
    DESTINY_BOND = (0xC2, "Destiny Bond", Type.GHOST, STATUS_MOVE)
    PERISH_SONG = (0xC3, "Perish Song", Type.NORMAL, STATUS_MOVE)
    ICY_WIND = (0xC4, "Icy Wind", Type.ICE, 55)
    DETECT = (0xC5, "Detect", Type.NORMAL, STATUS_MOVE)
    BONE_RUSH = (0xC6, "Bone Rush", Type.GROUND, 25)
    LOCK_ON = (0xC7, "Lock-On", Type.NORMAL, STATUS_MOVE)
    OUTRAGE = (0xC8, "Outrage", Type.DRAGON, 120)
    SANDSTORM = (0xC9, "Sandstorm", Type.ROCK, STATUS_MOVE)
    GIGA_DRAIN = (0xCA, "Giga Drain", Type.GRASS, 60)
    ENDURE = (0xCB, "Endure", Type.NORMAL, STATUS_MOVE)
    CHARM = (0xCC, "Charm", Type.NORMAL, STATUS_MOVE)
    ROLLOUT = (0xCD, "Rollout", Type.ROCK, 30)
    FALSE_SWIPE = (0xCE, "False Swipe", Type.NORMAL, 40)
    SWAGGER = (0xCF, "Swagger", Type.NORMAL, STATUS_MOVE)
    MILK_DRINK = (0xD0, "Milk Drink", Type.NORMAL, STATUS_MOVE)
    SPARK = (0xD1, "Spark", Type.ELECTRIC, 65)
    FURY_CUTTER = (0xD2, "Fury Cutter", Type.BUG, 10)
    STEEL_WING = (0xD3, "Steel Wing", Type.STEEL, 70)
    MEAN_LOOK = (0xD4, "Mean Look", Type.NORMAL, STATUS_MOVE)
    ATTRACT = (0xD5, "Attract", Type.NORMAL, STATUS_MOVE)
    SLEEP_TALK = (0xD6, "Sleep Talk", Type.NORMAL, STATUS_MOVE)
    HEAL_BELL = (0xD7, "Heal Bell", Type.NORMAL, STATUS_MOVE)
    RETURN = (0xD8, "Return", Type.NORMAL, UNIQUE_DAMAGING_MOVE)
    PRESENT = (0xD9, "Present", Type.NORMAL, UNIQUE_DAMAGING_MOVE)
    FRUSTRATION = (0xDA, "Frustration", Type.NORMAL, UNIQUE_DAMAGING_MOVE)
    SAFEGUARD = (0xDB, "Safeguard", Type.NORMAL, STATUS_MOVE)
    PAIN_SPLIT = (0xDC, "Pain Split", Type.NORMAL, STATUS_MOVE)
    SACRED_FIRE = (0xDD, "Sacred Fire", Type.FIRE, 100)
    MAGNITUDE = (0xDE, "Magnitude", Type.GROUND, UNIQUE_DAMAGING_MOVE)
    DYNAMICPUNCH = (0xDF, "DynamicPunch", Type.FIGHTING, 100)
    DYNAMIC_PUNCH = DYNAMICPUNCH
    MEGAHORN = (0xE0, "Megahorn", Type.BUG, 120)
    DRAGONBREATH = (0xE1, "DragonBreath", Type.DRAGON, 60)
    DRAGON_BREATH = DRAGONBREATH
    BATON_PASS = (0xE2, "Baton Pass", Type.NORMAL, STATUS_MOVE)
    ENCORE = (0xE3, "Encore", Type.NORMAL, STATUS_MOVE)
    PURSUIT = (0xE4, "Pursuit", Type.DARK, 40)
    RAPID_SPIN = (0xE5, "Rapid Spin", Type.NORMAL, 20)
    SWEET_SCENT = (0xE6, "Sweet Scent", Type.NORMAL, STATUS_MOVE)
    IRON_TAIL = (0xE7, "Iron Tail", Type.STEEL, 100)
    METAL_CLAW = (0xE8, "Metal Claw", Type.STEEL, 50)
    VITAL_THROW = (0xE9, "Vital Throw", Type.FIGHTING, 70)
    MORNING_SUN = (0xEA, "Morning Sun", Type.NORMAL, STATUS_MOVE)
    SYNTHESIS = (0xEB, "Synthesis", Type.GRASS, STATUS_MOVE)
    MOONLIGHT = (0xEC, "Moonlight", Type.NORMAL, STATUS_MOVE)
    HIDDEN_POWER = (0xED, "Hidden Power", Type.NORMAL, UNIQUE_DAMAGING_MOVE)
    CROSS_CHOP = (0xEE, "Cross Chop", Type.FIGHTING, 100)
    TWISTER = (0xEF, "Twister", Type.DRAGON, 40)
    RAIN_DANCE = (0xF0, "Rain Dance", Type.WATER, STATUS_MOVE)
    SUNNY_DAY = (0xF1, "Sunny Day", Type.FIRE, STATUS_MOVE)
    CRUNCH = (0xF2, "Crunch", Type.DARK, 80)
    MIRROR_COAT = (0xF3, "Mirror Coat", Type.PSYCHIC, UNIQUE_DAMAGING_MOVE)
    PSYCH_UP = (0xF4, "Psych Up", Type.NORMAL, STATUS_MOVE)
    EXTREMESPEED = (0xF5, "ExtremeSpeed", Type.NORMAL, 80)
    EXTREME_SPEED = EXTREMESPEED
    ANCIENTPOWER = (0xF6, "AncientPower", Type.ROCK, 60)
    ANCIENT_POWER = ANCIENTPOWER
    SHADOW_BALL = (0xF7, "Shadow Ball", Type.GHOST, 80)
    FUTURE_SIGHT = (0xF8, "Future Sight", Type.PSYCHIC, 80)
    ROCK_SMASH = (0xF9, "Rock Smash", Type.FIGHTING, 40)
    WHIRLPOOL = (0xFA, "Whirlpool", Type.WATER, 15)
    BEAT_UP = (0xFB, "Beat Up", Type.DARK, UNIQUE_DAMAGING_MOVE)
    FAKE_OUT = (0xFC, "Fake Out", Type.NORMAL, 40)
    UPROAR = (0xFD, "Uproar", Type.NORMAL, 50)
    STOCKPILE = (0xFE, "Stockpile", Type.NORMAL, STATUS_MOVE)
    SPIT_UP = (0xFF, "Spit Up", Type.NORMAL, 100)
    SWALLOW = (0x100, "Swallow", Type.NORMAL, STATUS_MOVE)
    HEAT_WAVE = (0x101, "Heat Wave", Type.FIRE, 100)
    HAIL = (0x102, "Hail", Type.ICE, STATUS_MOVE)
    TORMENT = (0x103, "Torment", Type.DARK, STATUS_MOVE)
    FLATTER = (0x104, "Flatter", Type.DARK, STATUS_MOVE)
    WILL_O_WISP = (0x105, "Will-O-Wisp", Type.FIRE, STATUS_MOVE)
    MEMENTO = (0x106, "Memento", Type.DARK, STATUS_MOVE)
    FACADE = (0x107, "Facade", Type.NORMAL, 70)
    FOCUS_PUNCH = (0x108, "Focus Punch", Type.FIGHTING, 150)
    SMELLINGSALT = (0x109, "SmellingSalt", Type.NORMAL, 60)
    SMELLING_SALTS = SMELLINGSALT
    FOLLOW_ME = (0x10A, "Follow Me", Type.NORMAL, STATUS_MOVE)
    NATURE_POWER = (0x10B, "Nature Power", Type.NORMAL, STATUS_MOVE)
    CHARGE = (0x10C, "Charge", Type.ELECTRIC, STATUS_MOVE)
    TAUNT = (0x10D, "Taunt", Type.DARK, STATUS_MOVE)
    HELPING_HAND = (0x10E, "Helping Hand", Type.NORMAL, STATUS_MOVE)
    TRICK = (0x10F, "Trick", Type.PSYCHIC, STATUS_MOVE)
    ROLE_PLAY = (0x110, "Role Play", Type.PSYCHIC, STATUS_MOVE)
    WISH = (0x111, "Wish", Type.NORMAL, STATUS_MOVE)
    ASSIST = (0x112, "Assist", Type.NORMAL, STATUS_MOVE)
    INGRAIN = (0x113, "Ingrain", Type.GRASS, STATUS_MOVE)
    SUPERPOWER = (0x114, "Superpower", Type.FIGHTING, 120)
    MAGIC_COAT = (0x115, "Magic Coat", Type.PSYCHIC, STATUS_MOVE)
    RECYCLE = (0x116, "Recycle", Type.NORMAL, STATUS_MOVE)
    REVENGE = (0x117, "Revenge", Type.FIGHTING, 60)
    BRICK_BREAK = (0x118, "Brick Break", Type.FIGHTING, 75)
    YAWN = (0x119, "Yawn", Type.NORMAL, STATUS_MOVE)
    KNOCK_OFF = (0x11A, "Knock Off", Type.DARK, 20)
    ENDEAVOR = (0x11B, "Endeavor", Type.NORMAL, UNIQUE_DAMAGING_MOVE)
    ERUPTION = (0x11C, "Eruption", Type.FIRE, UNIQUE_DAMAGING_MOVE)
    SKILL_SWAP = (0x11D, "Skill Swap", Type.PSYCHIC, STATUS_MOVE)
    IMPRISON = (0x11E, "Imprison", Type.PSYCHIC, STATUS_MOVE)
    REFRESH = (0x11F, "Refresh", Type.NORMAL, STATUS_MOVE)
    GRUDGE = (0x120, "Grudge", Type.GHOST, STATUS_MOVE)
    SNATCH = (0x121, "Snatch", Type.DARK, STATUS_MOVE)
    SECRET_POWER = (0x122, "Secret Power", Type.NORMAL, 70)
    DIVE = (0x123, "Dive", Type.WATER, 80)
    ARM_THRUST = (0x124, "Arm Thrust", Type.FIGHTING, 15)
    CAMOUFLAGE = (0x125, "Camouflage", Type.NORMAL, STATUS_MOVE)
    TAIL_GLOW = (0x126, "Tail Glow", Type.BUG, STATUS_MOVE)
    LUSTER_PURGE = (0x127, "Luster Purge", Type.PSYCHIC, 70)
    MIST_BALL = (0x128, "Mist Ball", Type.PSYCHIC, 70)
    FEATHERDANCE = (0x129, "FeatherDance", Type.FLYING, STATUS_MOVE)
    FEATHER_DANCE = FEATHERDANCE
    TEETER_DANCE = (0x12A, "Teeter Dance", Type.NORMAL, STATUS_MOVE)
    BLAZE_KICK = (0x12B, "Blaze Kick", Type.FIRE, 85)
    MUD_SPORT = (0x12C, "Mud Sport", Type.GROUND, STATUS_MOVE)
    ICE_BALL = (0x12D, "Ice Ball", Type.ICE, 30)
    NEEDLE_ARM = (0x12E, "Needle Arm", Type.GRASS, 60)
    SLACK_OFF = (0x12F, "Slack Off", Type.NORMAL, STATUS_MOVE)
    HYPER_VOICE = (0x130, "Hyper Voice", Type.NORMAL, 90)
    POISON_FANG = (0x131, "Poison Fang", Type.POISON, 50)
    CRUSH_CLAW = (0x132, "Crush Claw", Type.NORMAL, 75)
    BLAST_BURN = (0x133, "Blast Burn", Type.FIRE, 150)
    HYDRO_CANNON = (0x134, "Hydro Cannon", Type.WATER, 150)
    METEOR_MASH = (0x135, "Meteor Mash", Type.STEEL, 100)
    ASTONISH = (0x136, "Astonish", Type.GHOST, 30)
    WEATHER_BALL = (0x137, "Weather Ball", Type.NORMAL, 50)
    AROMATHERAPY = (0x138, "Aromatherapy", Type.GRASS, STATUS_MOVE)
    FAKE_TEARS = (0x139, "Fake Tears", Type.DARK, STATUS_MOVE)
    AIR_CUTTER = (0x13A, "Air Cutter", Type.FLYING, 55)
    OVERHEAT = (0x13B, "Overheat", Type.FIRE, 140)
    ODOR_SLEUTH = (0x13C, "Odor Sleuth", Type.NORMAL, STATUS_MOVE)
    ROCK_TOMB = (0x13D, "Rock Tomb", Type.ROCK, 50)
    SILVER_WIND = (0x13E, "Silver Wind", Type.BUG, 60)
    METAL_SOUND = (0x13F, "Metal Sound", Type.STEEL, STATUS_MOVE)
    GRASSWHISTLE = (0x140, "GrassWhistle", Type.GRASS, STATUS_MOVE)
    GRASS_WHISTLE = GRASSWHISTLE
    TICKLE = (0x141, "Tickle", Type.NORMAL, STATUS_MOVE)
    COSMIC_POWER = (0x142, "Cosmic Power", Type.PSYCHIC, STATUS_MOVE)
    WATER_SPOUT = (0x143, "Water Spout", Type.WATER, UNIQUE_DAMAGING_MOVE)
    SIGNAL_BEAM = (0x144, "Signal Beam", Type.BUG, 75)
    SHADOW_PUNCH = (0x145, "Shadow Punch", Type.GHOST, 60)
    EXTRASENSORY = (0x146, "Extrasensory", Type.PSYCHIC, 80)
    SKY_UPPERCUT = (0x147, "Sky Uppercut", Type.FIGHTING, 85)
    SAND_TOMB = (0x148, "Sand Tomb", Type.GROUND, 15)
    SHEER_COLD = (0x149, "Sheer Cold", Type.ICE, OHKO_MOVE)
    MUDDY_WATER = (0x14A, "Muddy Water", Type.WATER, 95)
    BULLET_SEED = (0x14B, "Bullet Seed", Type.GRASS, 10)
    AERIAL_ACE = (0x14C, "Aerial Ace", Type.FLYING, 60)
    ICICLE_SPEAR = (0x14D, "Icicle Spear", Type.ICE, 10)
    IRON_DEFENSE = (0x14E, "Iron Defense", Type.STEEL, STATUS_MOVE)
    BLOCK = (0x14F, "Block", Type.NORMAL, STATUS_MOVE)
    HOWL = (0x150, "Howl", Type.NORMAL, STATUS_MOVE)
    DRAGON_CLAW = (0x151, "Dragon Claw", Type.DRAGON, 80)
    FRENZY_PLANT = (0x152, "Frenzy Plant", Type.GRASS, 150)
    BULK_UP = (0x153, "Bulk Up", Type.FIGHTING, STATUS_MOVE)
    BOUNCE = (0x154, "Bounce", Type.FLYING, 85)
    MUD_SHOT = (0x155, "Mud Shot", Type.GROUND, 55)
    POISON_TAIL = (0x156, "Poison Tail", Type.POISON, 50)
    COVET = (0x157, "Covet", Type.NORMAL, 40)
    VOLT_TACKLE = (0x158, "Volt Tackle", Type.ELECTRIC, 120)
    MAGICAL_LEAF = (0x159, "Magical Leaf", Type.GRASS, 60)
    WATER_SPORT = (0x15A, "Water Sport", Type.WATER, STATUS_MOVE)
    CALM_MIND = (0x15B, "Calm Mind", Type.PSYCHIC, STATUS_MOVE)
    LEAF_BLADE = (0x15C, "Leaf Blade", Type.GRASS, 90)
    DRAGON_DANCE = (0x15D, "Dragon Dance", Type.DRAGON, STATUS_MOVE)
    ROCK_BLAST = (0x15E, "Rock Blast", Type.ROCK, 25)
    SHOCK_WAVE = (0x15F, "Shock Wave", Type.ELECTRIC, 60)
    WATER_PULSE = (0x160, "Water Pulse", Type.WATER, 60)
    DOOM_DESIRE = (0x161, "Doom Desire", Type.STEEL, 120)
    PSYCHO_BOOST = (0x162, "Psycho Boost", Type.PSYCHIC, 140)
    SHADOW_BLITZ = (0x164, "Shadow Blitz", Type.SHADOW, 40)
    SHADOW_RUSH_COLO = (0x164, "Shadow Rush", Type.SHADOW, 90)
    SHADOW_RUSH_XD = (0x165, "Shadow Rush", Type.SHADOW, 55)
    SHADOW_BREAK = (0x166, "Shadow Break", Type.SHADOW, 75)
    SHADOW_END = (0x167, "Shadow End", Type.SHADOW, 120)
    SHADOW_WAVE = (0x168, "Shadow Wave", Type.SHADOW, 50)
    SHADOW_RAVE = (0x169, "Shadow Rave", Type.SHADOW, 70)
    SHADOW_STORM = (0x16A, "Shadow Storm", Type.SHADOW, 95)
    SHADOW_FIRE = (0x16B, "Shadow Fire", Type.SHADOW, 75)
    SHADOW_BOLT = (0x16C, "Shadow Bolt", Type.SHADOW, 75)
    SHADOW_CHILL = (0x16D, "Shadow Chill", Type.SHADOW, 75)
    SHADOW_BLAST = (0x16E, "Shadow Blast", Type.SHADOW, 80)
    SHADOW_SKY = (0x16F, "Shadow Sky", Type.SHADOW, STATUS_MOVE)
    SHADOW_HOLD = (0x170, "Shadow Hold", Type.SHADOW, STATUS_MOVE)
    SHADOW_MIST = (0x171, "Shadow Mist", Type.SHADOW, STATUS_MOVE)
    SHADOW_PANIC = (0x172, "Shadow Panic", Type.SHADOW, STATUS_MOVE)
    SHADOW_DOWN = (0x173, "Shadow Down", Type.SHADOW, STATUS_MOVE)
    SHADOW_SHED = (0x174, "Shadow Shed", Type.SHADOW, STATUS_MOVE)
    SHADOW_HALF = (0x175, "Shadow Half", Type.SHADOW, STATUS_MOVE)

    def __init__(self, idx, friendly_name, m_type, power):
        self.idx = idx
        self.friendly_name = friendly_name
        self.type = m_type
        self.power = power

    @classmethod
    def from_idx(cls, idx):
        for item in cls:
            if item.value[0] == idx:
                return item
        raise KeyError


class ExpClass(Enum):
    ERRATIC = 0x01
    FAST = 0x04
    MEDIUM_FAST = 0x00
    MEDIUM_SLOW = 0x03
    SLOW = 0x05
    FLUCTUATING = 0x02


class EvolutionType(Enum):
    NONE = 0x00
    HAPPINESS = 0x01
    UNUSED_2 = 0x02
    UNUSED_3 = 0x03
    LEVEL_UP = 0x04
    TRADE_ALWAYS = 0x05
    TRADE_WITH_ITEM = 0x06
    STONE_EVOLUTION = 0x07
    ATTACK_GT_DEFENSE = 0x08
    ATTACK_EQ_DEFENSE = 0x09
    ATTACK_LT_DEFENSE = 0x0A
    PERSONALITY_VALUE_MODULO_LOW = 0x0B
    PERSONALITY_VALUE_MODULO_HIGH = 0x0C
    UNUSED_13 = 0x0D
    SHEDINJA = 0x0E
    HIGH_BEAUTY = 0x0F
    HAPPINESS_WITH_ITEM_IN_BAG = 0x10

    @property
    def param_is_level(self):
        return self in [self.LEVEL_UP, self.ATTACK_EQ_DEFENSE, self.ATTACK_GT_DEFENSE, self.ATTACK_LT_DEFENSE,
                        self.PERSONALITY_VALUE_MODULO_LOW, self.PERSONALITY_VALUE_MODULO_HIGH, self.SHEDINJA]

    @property
    def param_is_item(self):
        return self in [self.TRADE_WITH_ITEM, self.STONE_EVOLUTION, self.HAPPINESS_WITH_ITEM_IN_BAG]
