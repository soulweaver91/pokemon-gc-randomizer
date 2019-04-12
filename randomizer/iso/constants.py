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


VALID_POKEMON_TYPES = [a for a in list(Type) if a not in [
    Type.CURSE
]]


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


class Move(Enum):
    NONE = 0x00
    POUND = 0x01
    KARATE_CHOP = 0x02
    DOUBLESLAP = 0x03
    DOUBLE_SLAP = DOUBLESLAP
    COMET_PUNCH = 0x04
    MEGA_PUNCH = 0x05
    PAY_DAY = 0x06
    FIRE_PUNCH = 0x07
    ICE_PUNCH = 0x08
    THUNDERPUNCH = 0x09
    THUNDER_PUNCH = THUNDERPUNCH
    SCRATCH = 0x0A
    VICEGRIP = 0x0B
    VICE_GRIP = VICEGRIP
    GUILLOTINE = 0x0C
    RAZOR_WIND = 0x0D
    SWORDS_DANCE = 0x0E
    CUT = 0x0F
    GUST = 0x10
    WING_ATTACK = 0x11
    WHIRLWIND = 0x12
    FLY = 0x13
    BIND = 0x14
    SLAM = 0x15
    VINE_WHIP = 0x16
    STOMP = 0x17
    DOUBLE_KICK = 0x18
    MEGA_KICK = 0x19
    JUMP_KICK = 0x1A
    ROLLING_KICK = 0x1B
    SAND_ATTACK = 0x1C
    HEADBUTT = 0x1D
    HORN_ATTACK = 0x1E
    FURY_ATTACK = 0x1F
    HORN_DRILL = 0x20
    TACKLE = 0x21
    BODY_SLAM = 0x22
    WRAP = 0x23
    TAKE_DOWN = 0x24
    THRASH = 0x25
    DOUBLE_EDGE = 0x26
    TAIL_WHIP = 0x27
    POISON_STING = 0x28
    TWINEEDLE = 0x29
    PIN_MISSILE = 0x2A
    LEER = 0x2B
    BITE = 0x2C
    GROWL = 0x2D
    ROAR = 0x2E
    SING = 0x2F
    SUPERSONIC = 0x30
    SONICBOOM = 0x31
    SONIC_BOOM = SONICBOOM
    DISABLE = 0x32
    ACID = 0x33
    EMBER = 0x34
    FLAMETHROWER = 0x35
    MIST = 0x36
    WATER_GUN = 0x37
    HYDRO_PUMP = 0x38
    SURF = 0x39
    ICE_BEAM = 0x3A
    BLIZZARD = 0x3B
    PSYBEAM = 0x3C
    BUBBLEBEAM = 0x3D
    BUBBLE_BEAM = BUBBLEBEAM
    AURORA_BEAM = 0x3E
    HYPER_BEAM = 0x3F
    PECK = 0x40
    DRILL_PECK = 0x41
    SUBMISSION = 0x42
    LOW_KICK = 0x43
    COUNTER = 0x44
    SEISMIC_TOSS = 0x45
    STRENGTH = 0x46
    ABSORB = 0x47
    MEGA_DRAIN = 0x48
    LEECH_SEED = 0x49
    GROWTH = 0x4A
    RAZOR_LEAF = 0x4B
    SOLARBEAM = 0x4C
    SOLAR_BEAM = SOLARBEAM
    POISONPOWDER = 0x4D
    POISON_POWDER = POISONPOWDER
    STUN_SPORE = 0x4E
    SLEEP_POWDER = 0x4F
    PETAL_DANCE = 0x50
    STRING_SHOT = 0x51
    DRAGON_RAGE = 0x52
    FIRE_SPIN = 0x53
    THUNDERSHOCK = 0x54
    THUNDER_SHOCK = THUNDERSHOCK
    THUNDERBOLT = 0x55
    THUNDER_BOLT = THUNDERBOLT
    THUNDER_WAVE = 0x56
    THUNDER = 0x57
    ROCK_THROW = 0x58
    EARTHQUAKE = 0x59
    FISSURE = 0x5A
    DIG = 0x5B
    TOXIC = 0x5C
    CONFUSION = 0x5D
    PSYCHIC = 0x5E
    HYPNOSIS = 0x5F
    MEDITATE = 0x60
    AGILITY = 0x61
    QUICK_ATTACK = 0x62
    RAGE = 0x63
    TELEPORT = 0x64
    NIGHT_SHADE = 0x65
    MIMIC = 0x66
    SCREECH = 0x67
    DOUBLE_TEAM = 0x68
    RECOVER = 0x69
    HARDEN = 0x6A
    MINIMIZE = 0x6B
    SMOKESCREEN = 0x6C
    SMOKE_SCREEN = SMOKESCREEN
    CONFUSE_RAY = 0x6D
    WITHDRAW = 0x6E
    DEFENSE_CURL = 0x6F
    BARRIER = 0x70
    LIGHT_SCREEN = 0x71
    HAZE = 0x72
    REFLECT = 0x73
    FOCUS_ENERGY = 0x74
    BIDE = 0x75
    METRONOME = 0x76
    MIRROR_MOVE = 0x77
    SELFDESTRUCT = 0x78
    SELF_DESTRUCT = SELFDESTRUCT
    EGG_BOMB = 0x79
    LICK = 0x7A
    SMOG = 0x7B
    SLUDGE = 0x7C
    BONE_CLUB = 0x7D
    FIRE_BLAST = 0x7E
    WATERFALL = 0x7F
    CLAMP = 0x80
    SWIFT = 0x81
    SKULL_BASH = 0x82
    SPIKE_CANNON = 0x83
    CONSTRICT = 0x84
    AMNESIA = 0x85
    KINESIS = 0x86
    SOFTBOILED = 0x87
    SOFT_BOILED = SOFTBOILED
    HI_JUMP_KICK = 0x88
    HIGH_JUMP_KICK = HI_JUMP_KICK
    GLARE = 0x89
    DREAM_EATER = 0x8A
    POISON_GAS = 0x8B
    BARRAGE = 0x8C
    LEECH_LIFE = 0x8D
    LOVELY_KISS = 0x8E
    SKY_ATTACK = 0x8F
    TRANSFORM = 0x90
    BUBBLE = 0x91
    DIZZY_PUNCH = 0x92
    SPORE = 0x93
    FLASH = 0x94
    PSYWAVE = 0x95
    SPLASH = 0x96
    ACID_ARMOR = 0x97
    CRABHAMMER = 0x98
    EXPLOSION = 0x99
    FURY_SWIPES = 0x9A
    BONEMERANG = 0x9B
    REST = 0x9C
    ROCK_SLIDE = 0x9D
    HYPER_FANG = 0x9E
    SHARPEN = 0x9F
    CONVERSION = 0xA0
    TRI_ATTACK = 0xA1
    SUPER_FANG = 0xA2
    SLASH = 0xA3
    SUBSTITUTE = 0xA4
    STRUGGLE = 0xA5
    SKETCH = 0xA6
    TRIPLE_KICK = 0xA7
    THIEF = 0xA8
    SPIDER_WEB = 0xA9
    MIND_READER = 0xAA
    NIGHTMARE = 0xAB
    FLAME_WHEEL = 0xAC
    SNORE = 0xAD
    CURSE = 0xAE
    FLAIL = 0xAF
    CONVERSION_2 = 0xB0
    AEROBLAST = 0xB1
    COTTON_SPORE = 0xB2
    REVERSAL = 0xB3
    SPITE = 0xB4
    POWDER_SNOW = 0xB5
    PROTECT = 0xB6
    MACH_PUNCH = 0xB7
    SCARY_FACE = 0xB8
    FAINT_ATTACK = 0xB9
    FEINT_ATTACK = FAINT_ATTACK
    SWEET_KISS = 0xBA
    BELLY_DRUM = 0xBB
    SLUDGE_BOMB = 0xBC
    MUD_SLAP = 0xBD
    OCTAZOOKA = 0xBE
    SPIKES = 0xBF
    ZAP_CANNON = 0xC0
    FORESIGHT = 0xC1
    DESTINY_BOND = 0xC2
    PERISH_SONG = 0xC3
    ICY_WIND = 0xC4
    DETECT = 0xC5
    BONE_RUSH = 0xC6
    LOCK_ON = 0xC7
    OUTRAGE = 0xC8
    SANDSTORM = 0xC9
    GIGA_DRAIN = 0xCA
    ENDURE = 0xCB
    CHARM = 0xCC
    ROLLOUT = 0xCD
    FALSE_SWIPE = 0xCE
    SWAGGER = 0xCF
    MILK_DRINK = 0xD0
    SPARK = 0xD1
    FURY_CUTTER = 0xD2
    STEEL_WING = 0xD3
    MEAN_LOOK = 0xD4
    ATTRACT = 0xD5
    SLEEP_TALK = 0xD6
    HEAL_BELL = 0xD7
    RETURN = 0xD8
    PRESENT = 0xD9
    FRUSTRATION = 0xDA
    SAFEGUARD = 0xDB
    PAIN_SPLIT = 0xDC
    SACRED_FIRE = 0xDD
    MAGNITUDE = 0xDE
    DYNAMICPUNCH = 0xDF
    DYNAMIC_PUNCH = DYNAMICPUNCH
    MEGAHORN = 0xE0
    DRAGONBREATH = 0xE1
    DRAGON_BREATH = DRAGONBREATH
    BATON_PASS = 0xE2
    ENCORE = 0xE3
    PURSUIT = 0xE4
    RAPID_SPIN = 0xE5
    SWEET_SCENT = 0xE6
    IRON_TAIL = 0xE7
    METAL_CLAW = 0xE8
    VITAL_THROW = 0xE9
    MORNING_SUN = 0xEA
    SYNTHESIS = 0xEB
    MOONLIGHT = 0xEC
    HIDDEN_POWER = 0xED
    CROSS_CHOP = 0xEE
    TWISTER = 0xEF
    RAIN_DANCE = 0xF0
    SUNNY_DAY = 0xF1
    CRUNCH = 0xF2
    MIRROR_COAT = 0xF3
    PSYCH_UP = 0xF4
    EXTREMESPEED = 0xF5
    EXTREME_SPEED = EXTREMESPEED
    ANCIENTPOWER = 0xF6
    ANCIENT_POWER = ANCIENTPOWER
    SHADOW_BALL = 0xF7
    FUTURE_SIGHT = 0xF8
    ROCK_SMASH = 0xF9
    WHIRLPOOL = 0xFA
    BEAT_UP = 0xFB
    FAKE_OUT = 0xFC
    UPROAR = 0xFD
    STOCKPILE = 0xFE
    SPIT_UP = 0xFF
    SWALLOW = 0x100
    HEAT_WAVE = 0x101
    HAIL = 0x102
    TORMENT = 0x103
    FLATTER = 0x104
    WILL_O_WISP = 0x105
    MEMENTO = 0x106
    FACADE = 0x107
    FOCUS_PUNCH = 0x108
    SMELLINGSALT = 0x109
    SMELLING_SALTS = SMELLINGSALT
    FOLLOW_ME = 0x10A
    NATURE_POWER = 0x10B
    CHARGE = 0x10C
    TAUNT = 0x10D
    HELPING_HAND = 0x10E
    TRICK = 0x10F
    ROLE_PLAY = 0x110
    WISH = 0x111
    ASSIST = 0x112
    INGRAIN = 0x113
    SUPERPOWER = 0x114
    MAGIC_COAT = 0x115
    RECYCLE = 0x116
    REVENGE = 0x117
    BRICK_BREAK = 0x118
    YAWN = 0x119
    KNOCK_OFF = 0x11A
    ENDEAVOR = 0x11B
    ERUPTION = 0x11C
    SKILL_SWAP = 0x11D
    IMPRISON = 0x11E
    REFRESH = 0x11F
    GRUDGE = 0x120
    SNATCH = 0x121
    SECRET_POWER = 0x122
    DIVE = 0x123
    ARM_THRUST = 0x124
    CAMOUFLAGE = 0x125
    TAIL_GLOW = 0x126
    LUSTER_PURGE = 0x127
    MIST_BALL = 0x128
    FEATHERDANCE = 0x129
    FEATHER_DANCE = FEATHERDANCE
    TEETER_DANCE = 0x12A
    BLAZE_KICK = 0x12B
    MUD_SPORT = 0x12C
    ICE_BALL = 0x12D
    NEEDLE_ARM = 0x12E
    SLACK_OFF = 0x12F
    HYPER_VOICE = 0x130
    POISON_FANG = 0x131
    CRUSH_CLAW = 0x132
    BLAST_BURN = 0x133
    HYDRO_CANNON = 0x134
    METEOR_MASH = 0x135
    ASTONISH = 0x136
    WEATHER_BALL = 0x137
    AROMATHERAPY = 0x138
    FAKE_TEARS = 0x139
    AIR_CUTTER = 0x13A
    OVERHEAT = 0x13B
    ODOR_SLEUTH = 0x13C
    ROCK_TOMB = 0x13D
    SILVER_WIND = 0x13E
    METAL_SOUND = 0x13F
    GRASSWHISTLE = 0x140
    GRASS_WHISTLE = GRASSWHISTLE
    TICKLE = 0x141
    COSMIC_POWER = 0x142
    WATER_SPOUT = 0x143
    SIGNAL_BEAM = 0x144
    SHADOW_PUNCH = 0x145
    EXTRASENSORY = 0x146
    SKY_UPPERCUT = 0x147
    SAND_TOMB = 0x148
    SHEER_COLD = 0x149
    MUDDY_WATER = 0x14A
    BULLET_SEED = 0x14B
    AERIAL_ACE = 0x14C
    ICICLE_SPEAR = 0x14D
    IRON_DEFENSE = 0x14E
    BLOCK = 0x14F
    HOWL = 0x150
    DRAGON_CLAW = 0x151
    FRENZY_PLANT = 0x152
    BULK_UP = 0x153
    BOUNCE = 0x154
    MUD_SHOT = 0x155
    POISON_TAIL = 0x156
    COVET = 0x157
    VOLT_TACKLE = 0x158
    MAGICAL_LEAF = 0x159
    WATER_SPORT = 0x15A
    CALM_MIND = 0x15B
    LEAF_BLADE = 0x15C
    DRAGON_DANCE = 0x15D
    ROCK_BLAST = 0x15E
    SHOCK_WAVE = 0x15F
    WATER_PULSE = 0x160
    DOOM_DESIRE = 0x161
    PSYCHO_BOOST = 0x162
    UNUSED_0x163 = 0x163
    SHADOW_BLITZ = 0x164
    SHADOW_RUSH_COLO = 0x164
    SHADOW_RUSH_XD = 0x165
    SHADOW_BREAK = 0x166
    SHADOW_END = 0x167
    SHADOW_WAVE = 0x168
    SHADOW_RAVE = 0x169
    SHADOW_STORM = 0x16A
    SHADOW_FIRE = 0x16B
    SHADOW_BOLT = 0x16C
    SHADOW_CHILL = 0x16D
    SHADOW_BLAST = 0x16E
    SHADOW_SKY = 0x16F
    SHADOW_HOLD = 0x170
    SHADOW_MIST = 0x171
    SHADOW_PANIC = 0x172
    SHADOW_DOWN = 0x173
    SHADOW_SHED = 0x174
    SHADOW_HALF = 0x175

    @classmethod
    def _missing_(cls, value):
        return Move.NONE


class Item(Enum):
    NONE = 0x0000
    MASTER_BALL = 0x0001
    ULTRA_BALL = 0x0002
    GREAT_BALL = 0x0003
    POKE_BALL = 0x0004
    SAFARI_BALL = 0x0005
    NET_BALL = 0x0006
    DIVE_BALL = 0x0007
    NEST_BALL = 0x0008
    REPEAT_BALL = 0x0009
    TIMER_BALL = 0x000A
    LUXURY_BALL = 0x000B
    PREMIER_BALL = 0x000C
    POTION = 0x000D
    ANTIDOTE = 0x000E
    BURN_HEAL = 0x000F
    ICE_HEAL = 0x0010
    AWAKENING = 0x0011
    PARLYZ_HEAL = 0x0012
    FULL_RESTORE = 0x0013
    MAX_POTION = 0x0014
    HYPER_POTION = 0x0015
    SUPER_POTION = 0x0016
    FULL_HEAL = 0x0017
    REVIVE = 0x0018
    MAX_REVIVE = 0x0019
    FRESH_WATER = 0x001A
    SODA_POP = 0x001B
    LEMONADE = 0x001C
    MOOMOO_MILK = 0x001D
    ENERGYPOWDER = 0x001E
    ENERGY_ROOT = 0x001F
    HEAL_POWDER = 0x0020
    REVIVAL_HERB = 0x0021
    ETHER = 0x0022
    MAX_ETHER = 0x0023
    ELIXIR = 0x0024
    MAX_ELIXIR = 0x0025
    LAVA_COOKIE = 0x0026
    BLUE_FLUTE = 0x0027
    YELLOW_FLUTE = 0x0028
    RED_FLUTE = 0x0029
    BLACK_FLUTE = 0x002A
    WHITE_FLUTE = 0x002B
    BERRY_JUICE = 0x002C
    SACRED_ASH = 0x002D
    SHOAL_SALT = 0x002E
    SHOAL_SHELL = 0x002F
    RED_SHARD = 0x0030
    BLUE_SHARD = 0x0031
    YELLOW_SHARD = 0x0032
    GREEN_SHARD = 0x0033

    HP_UP = 0x003F
    PROTEIN = 0x0040
    IRON = 0x0041
    CARBOS = 0x0042
    CALCIUM = 0x0043
    RARE_CANDY = 0x0044
    PP_UP = 0x0045
    ZINC = 0x0046
    PP_MAX = 0x0047

    GUARD_SPEC_ = 0x0049
    DIRE_HIT = 0x004A
    X_ATTACK = 0x004B
    X_DEFEND = 0x004C
    X_SPEED = 0x004D
    X_ACCURACY = 0x004E
    X_SPECIAL = 0x004F
    POKE_DOLL = 0x0050
    FLUFFY_TAIL = 0x0051

    SUPER_REPEL = 0x0053
    MAX_REPEL = 0x0054
    ESCAPE_ROPE = 0x0055
    REPEL = 0x0056

    SUN_STONE = 0x005D
    MOON_STONE = 0x005E
    FIRE_STONE = 0x005F
    THUNDERSTONE = 0x0060
    WATER_STONE = 0x0061
    LEAF_STONE = 0x0062

    TINYMUSHROOM = 0x0067
    BIG_MUSHROOM = 0x0068

    PEARL = 0x006A
    BIG_PEARL = 0x006B
    STARDUST = 0x006C
    STAR_PIECE = 0x006D
    NUGGET = 0x006E
    HEART_SCALE = 0x006F

    CHERI_BERRY = 0x0085
    CHESTO_BERRY = 0x0086
    PECHA_BERRY = 0x0087
    RAWST_BERRY = 0x0088
    ASPEAR_BERRY = 0x0089
    LEPPA_BERRY = 0x008A
    ORAN_BERRY = 0x008B
    PERSIM_BERRY = 0x008C
    LUM_BERRY = 0x008D
    SITRUS_BERRY = 0x008E
    FIGY_BERRY = 0x008F
    WIKI_BERRY = 0x0090
    MAGO_BERRY = 0x0091
    AGUAV_BERRY = 0x0092
    IAPAPA_BERRY = 0x0093
    RAZZ_BERRY = 0x0094
    BLUK_BERRY = 0x0095
    NANAB_BERRY = 0x0096
    WEPEAR_BERRY = 0x0097
    PINAP_BERRY = 0x0098
    POMEG_BERRY = 0x0099
    KELPSY_BERRY = 0x009A
    QUALOT_BERRY = 0x009B
    HONDEW_BERRY = 0x009C
    GREPA_BERRY = 0x009D
    TAMATO_BERRY = 0x009E
    CORNN_BERRY = 0x009F
    MAGOST_BERRY = 0x00A0
    RABUTA_BERRY = 0x00A1
    NOMEL_BERRY = 0x00A2
    SPELON_BERRY = 0x00A3
    PAMTRE_BERRY = 0x00A4
    WATMEL_BERRY = 0x00A5
    DURIN_BERRY = 0x00A6
    BELUE_BERRY = 0x00A7
    LIECHI_BERRY = 0x00A8
    GANLON_BERRY = 0x00A9
    SALAC_BERRY = 0x00AA
    PETAYA_BERRY = 0x00AB
    APICOT_BERRY = 0x00AC
    LANSAT_BERRY = 0x00AD
    STARF_BERRY = 0x00AE

    BRIGHTPOWDER = 0x00B3
    WHITE_HERB = 0x00B4
    MACHO_BRACE = 0x00B5
    EXP_SHARE = 0x00B6
    QUICK_CLAW = 0x00B7
    SOOTHE_BELL = 0x00B8
    MENTAL_HERB = 0x00B9
    CHOICE_BAND = 0x00BA
    KINGS_ROCK = 0x00BB
    SILVERPOWDER = 0x00BC
    AMULET_COIN = 0x00BD
    CLEANSE_TAG = 0x00BE
    SOUL_DEW = 0x00BF
    DEEPSEATOOTH = 0x00C0
    DEEPSEASCALE = 0x00C1
    SMOKE_BALL = 0x00C2
    EVERSTONE = 0x00C3
    FOCUS_BAND = 0x00C4
    LUCKY_EGG = 0x00C5
    SCOPE_LENS = 0x00C6
    METAL_COAT = 0x00C7
    LEFTOVERS = 0x00C8
    DRAGON_SCALE = 0x00C9
    LIGHT_BALL = 0x00CA
    SOFT_SAND = 0x00CB
    HARD_STONE = 0x00CC
    MIRACLE_SEED = 0x00CD
    BLACKGLASSES = 0x00CE
    BLACK_BELT = 0x00CF
    MAGNET = 0x00D0
    MYSTIC_WATER = 0x00D1
    SHARP_BEAK = 0x00D2
    POISON_BARB = 0x00D3
    NEVERMELTICE = 0x00D4
    SPELL_TAG = 0x00D5
    TWISTEDSPOON = 0x00D6
    CHARCOAL = 0x00D7
    DRAGON_FANG = 0x00D8
    SILK_SCARF = 0x00D9
    UP_GRADE = 0x00DA
    SHELL_BELL = 0x00DB
    SEA_INCENSE = 0x00DC
    LAX_INCENSE = 0x00DD
    LUCKY_PUNCH = 0x00DE
    METAL_POWDER = 0x00DF
    THICK_CLUB = 0x00E0
    STICK = 0x00E1

    RED_SCARF = 0x00FE
    BLUE_SCARF = 0x00FF
    PINK_SCARF = 0x0100
    GREEN_SCARF = 0x0101
    YELLOW_SCARF = 0x0102

    TM01 = 0x0121
    TM02 = 0x0122
    TM03 = 0x0123
    TM04 = 0x0124
    TM05 = 0x0125
    TM06 = 0x0126
    TM07 = 0x0127
    TM08 = 0x0128
    TM09 = 0x0129
    TM10 = 0x012A
    TM11 = 0x012B
    TM12 = 0x012C
    TM13 = 0x012D
    TM14 = 0x012E
    TM15 = 0x012F
    TM16 = 0x0130
    TM17 = 0x0131
    TM18 = 0x0132
    TM19 = 0x0133
    TM20 = 0x0134
    TM21 = 0x0135
    TM22 = 0x0136
    TM23 = 0x0137
    TM24 = 0x0138
    TM25 = 0x0139
    TM26 = 0x013A
    TM27 = 0x013B
    TM28 = 0x013C
    TM29 = 0x013D
    TM30 = 0x013E
    TM31 = 0x013F
    TM32 = 0x0140
    TM33 = 0x0141
    TM34 = 0x0142
    TM35 = 0x0143
    TM36 = 0x0144
    TM37 = 0x0145
    TM38 = 0x0146
    TM39 = 0x0147
    TM40 = 0x0148
    TM41 = 0x0149
    TM42 = 0x014A
    TM43 = 0x014B
    TM44 = 0x014C
    TM45 = 0x014D
    TM46 = 0x014E
    TM47 = 0x014F
    TM48 = 0x0150
    TM49 = 0x0151
    TM50 = 0x0152

    # Colosseum key items
    JAIL_KEY = 0x01F4
    ELEVATOR_KEY_COLO = 0x01F5
    SMALL_TABLET = 0x01F6
    F_DISK = 0x01F7
    R_DISK = 0x01F8
    L_DISK = 0x01F9
    D_DISK = 0x01FA
    U_DISK = 0x01FB
    SUBWAY_KEY = 0x01FC
    MAINGATE_KEY = 0x01FD
    CARD_KEY = 0x01FE
    DOWN_ST_KEY = 0x01FF
    DNA_SAMPLE_1 = 0x0200
    DNA_SAMPLE_2 = 0x0201
    DNA_SAMPLE_3 = 0x0202
    DNA_SAMPLE_4 = 0x0203
    DNA_SAMPLE_5 = 0x0204
    DNA_SAMPLE_6 = 0x0205
    DNA_SAMPLE_7 = 0x0206
    DNA_SAMPLE_8 = 0x0207
    DNA_SAMPLE_9 = 0x0208
    DNA_SAMPLE_10 = 0x0209
    DNA_SAMPLE_11 = 0x020A
    DNA_SAMPLE_12 = 0x020B
    DNA_SAMPLE_13 = 0x020C
    DNA_SAMPLE_14 = 0x020D
    DNA_SAMPLE_15 = 0x020E
    DNA_SAMPLE_16 = 0x020F
    DNA_SAMPLE_17 = 0x0210
    DNA_SAMPLE_18 = 0x0211
    DATA_ROM_COLO = 0x0212
    STEEL_TEETH = 0x0213
    GEAR = 0x0214
    RED_ID_BADGE = 0x0215
    GRN_ID_BADGE = 0x0216
    BLU_ID_BADGE = 0x0217
    YLW_ID_BADGE = 0x0218
    TIME_FLUTE = 0x0219
    EIN_FILE_S = 0x021A
    EIN_FILE_H = 0x021B
    EIN_FILE_C = 0x021C
    EIN_FILE_P = 0x021D
    COLOGNE_CASE_COLO = 0x021E
    JOY_SCENT_COLO = 0x021F
    EXCITE_SCENT_COLO = 0x0220
    VIVID_SCENT_COLO = 0x0221
    POWERUP_PART = 0x0222
    EIN_FILE_F = 0x0223

    # XD key items
    SAFE_KEY = 0x01F4
    ELEVATOR_KEY_XD = 0x01F5
    BONSLY_CARD = 0x01F6
    MACHINE_PART = 0x01F7
    GONZAPS_KEY = 0x01F8
    DATA_ROM_XD = 0x01F9
    ID_CARD = 0x01FA
    MUSIC_DISC = 0x01FB
    SYSTEM_LEVER = 0x01FC
    MAYORS_NOTE = 0x01FD
    MIROR_RADAR = 0x01FE
    POKE_SNACK = 0x01FF
    COLOGNE_CASE_XD = 0x0200
    JOY_SCENT_XD = 0x0201
    EXCITE_SCENT_XD = 0x0202
    VIVID_SCENT_XD = 0x0203
    SUN_SHARD = 0x0204
    MOON_SHARD = 0x0205
    BONSLY_PHOTO = 0x0206
    CRY_ANALYZER = 0x0207

    KRANE_MEMO_1 = 0x020B
    KRANE_MEMO_2 = 0x020C
    KRANE_MEMO_3 = 0x020D
    KRANE_MEMO_4 = 0x020E
    KRANE_MEMO_5 = 0x020F
    VOICE_CASE_1 = 0x0210
    VOICE_CASE_2 = 0x0211
    VOICE_CASE_3 = 0x0212
    VOICE_CASE_4 = 0x0213
    VOICE_CASE_5 = 0x0214
    DISC_CASE = 0x0215
    BATTLE_CD_01 = 0x0216
    BATTLE_CD_02 = 0x0217
    BATTLE_CD_03 = 0x0218
    BATTLE_CD_04 = 0x0219
    BATTLE_CD_05 = 0x021A
    BATTLE_CD_06 = 0x021B
    BATTLE_CD_07 = 0x021C
    BATTLE_CD_08 = 0x021D
    BATTLE_CD_09 = 0x021E
    BATTLE_CD_10 = 0x021F
    BATTLE_CD_11 = 0x0220
    BATTLE_CD_12 = 0x0221
    BATTLE_CD_13 = 0x0222
    BATTLE_CD_14 = 0x0223
    BATTLE_CD_15 = 0x0224
    BATTLE_CD_16 = 0x0225
    BATTLE_CD_17 = 0x0226
    BATTLE_CD_18 = 0x0227
    BATTLE_CD_19 = 0x0228
    BATTLE_CD_20 = 0x0229
    BATTLE_CD_21 = 0x022A
    BATTLE_CD_22 = 0x022B
    BATTLE_CD_23 = 0x022C
    BATTLE_CD_24 = 0x022D
    BATTLE_CD_25 = 0x022E
    BATTLE_CD_26 = 0x022F
    BATTLE_CD_27 = 0x0230
    BATTLE_CD_28 = 0x0231
    BATTLE_CD_29 = 0x0232
    BATTLE_CD_30 = 0x0233
    BATTLE_CD_31 = 0x0234
    BATTLE_CD_32 = 0x0235
    BATTLE_CD_33 = 0x0236
    BATTLE_CD_34 = 0x0237
    BATTLE_CD_35 = 0x0238
    BATTLE_CD_36 = 0x0239
    BATTLE_CD_37 = 0x023A
    BATTLE_CD_38 = 0x023B
    BATTLE_CD_39 = 0x023C
    BATTLE_CD_40 = 0x023D
    BATTLE_CD_41 = 0x023E
    BATTLE_CD_42 = 0x023F
    BATTLE_CD_43 = 0x0240
    BATTLE_CD_44 = 0x0241
    BATTLE_CD_45 = 0x0242
    BATTLE_CD_46 = 0x0243
    BATTLE_CD_47 = 0x0244
    BATTLE_CD_48 = 0x0245
    BATTLE_CD_49 = 0x0246
    BATTLE_CD_50 = 0x0247
    BATTLE_CD_51 = 0x0248
    BATTLE_CD_52 = 0x0249
    BATTLE_CD_53 = 0x024A
    BATTLE_CD_54 = 0x024B
    BATTLE_CD_55 = 0x024C
    BATTLE_CD_56 = 0x024D
    BATTLE_CD_57 = 0x024E
    BATTLE_CD_58 = 0x024F
    BATTLE_CD_59 = 0x0250
    BATTLE_CD_60 = 0x0251

    @classmethod
    def _missing_(cls, value):
        return Item.NONE


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
