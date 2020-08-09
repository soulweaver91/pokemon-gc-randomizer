# Pokémon GameCube Randomizer

This tool randomizes Pokémon Colosseum and Pokémon XD: Gale of Darkness ISOs, providing a
fresh gameplay experience with different trainer battles, Pokémon specifics and item placements
based on the given settings.

## Usage
Pokémon GameCube Randomizer requires Python 3. You can install it by downloading an installer from
[the official website](https://www.python.org/downloads/) or from a package manager for your operating
system.

The randomizer is currently only available as a command line tool; a graphical user interface might be added
at a later date. The only required parameters to invoke the randomizer are the path to a clean, unmodified
input ISO as well as either the target filename or the `--in-place` switch, which will randomize the ISO
without leaving the original behind. Thus in order to randomize an ISO with the default settings, something
like this does the job:

```
python pkrgc.py --output GXXP01_randomized.iso GXXP01.iso
```

The default settings are designed to strike a good balance between complete randomness and vanilla experience:
Pokémon rosters, learnsets, abilities and such are altered, while Pokémon evolutions and types, move details
and such are kept as is. However, the randomization process is highly customizable through a variety of
extra command line options. You can find out the list of available options by using the `--help` switch:

```
python pkrgc.py --help
```

For example, if you are craving for something more like the so-called "über randomizer", you can try something
akin to:

```
python pkrgc.py --rng-pktypes --rng-pkstats --rng-move-power --rng-move-types --rng-move-accuracy --rng-move-pp --rng-pkevo --no-rng-pkevo-samestage --no-rng-pkevo-shuffle --no-rng-pokespot-bst-based -o GXXE01_randomized.iso GXXE01.iso
```

If you are curious about the specifics of the randomization, you might be interested in using the `-l DEBUG`
switch to see more detailed output while the program is working on your ISO.

## Image support

This randomizer supports randomizing the following disc images:

| Game                        | Game ID | Region | MD5 Checksum                       |
| --------------------------- | --------|--------| ---------------------------------- |
| Colosseum                   | GC6P01  | EUR    | `2be2607ae4826cbc77efb4ef4ada6385` |
| Colosseum                   | GC6J01  | JPN    | `ec80218d9079ccae07350e42356748ce` |
| Colosseum                   | GC6E01  | USA    | `e3f389dc5662b9f941769e370195ec90` |
| XD: Gale of Darkness        | GXXP01  | EUR    | `f36d14bebf8fea6a046404bff6adb7e6` |
| XD: Yami no Kaze Dark Lugia | GXXJ01  | JPN    | `e92856cb965f8411e29ccfc818bd6d5b` |
| XD: Gale of Darkness        | GXXE01  | USA    | `3bc1671806cf763a8712a5d398f62ad3` |

Please consult other online sources regarding creating a supported backup image of your game disc.

## Known caveats
- The randomization process is very slow due to the currently not very well optimized implementation of
  the compression algorithm used to recompress the altered data files.
- Many cosmetic changes are yet to be done. This includes details like adjusting TM descriptions to reflect
  the newly assigned moves, trade related NPC dialogue to refer to the correct Pokémon and such.
- P★DA Snag List and Shadow Monitor entries are partially baked into the save files when the save
  file is first created. If you load a save started with a clean ISO, these lists will not be using the
  Pokémon that are actually available to you post-randomization. (The same obviously goes for already
  modified/randomized ISOs, though note that randomizing them is not formally supported in any case.)
- It is currently not feasible to randomize Colosseum trainers with Shadow Pokémon in such a way that
  their with-Shadow and without-Shadow roster variations match, since there is no easy way to find
  out which rosters should be paired up. This should hardly be an issue, though.

## Troubleshooting
If a randomized ISO crashes at the Nintendo logo or at the start of a Trainer battle, the randomizer
has managed to write a file into the ISO in such a manner that the game fails to uncompress it. The
game is pretty strict when it comes to this, and the randomizer occasionally compresses some corner
cases in a slightly different way that *should* still be interchangeable. If this does happen, please
file a bug report including at least the following information:

* The ISO type and its MD5 hash
* The options used for randomization
* Where and how exactly the ISO hung or crashed

## Acknowledgements

* [StarsMmd's comprehensive guide on where to find things in the ISO over at Project Pokémon](https://projectpokemon.org/tutorials/rom/stars-pok%C3%A9mon-colosseum-and-xd-hacking-tutorial/).
  Having so much already documented by others has saved a lot of time.
* [gciso by Joel Schumacher](https://github.com/pfirsich/gciso) for the basis for the high-level 
  ISO handling code of this tool. gciso code is licensed under the MIT license.
* [This LZSS algorithm in Python by nucular](https://gist.github.com/nucular/258d544bbd1ba401232ae83a11bd8857)
  which was amended to work with the particular flavor of LZSS that the ISOs use. Presumably in
  public domain, like the original C implementation by Okumura Haruhiko.

## License

MIT
