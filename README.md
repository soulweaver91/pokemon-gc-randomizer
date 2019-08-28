# Pokémon Colosseum and XD Randomizer

This tool randomizes Pokémon XD: Gale of Darkness ISOs, providing a fresh gameplay
experience with different trainer battles, Pokémon specifics and item placements
based on the given settings. Eventually it will randomize Pokémon Colosseum ISOs
as well.

## Image support

These images have been tested to work correctly with this randomizer:

| Game                        | Game ID / Region | MD5 Checksum                       |
| --------------------------- | -----------------| ---------------------------------- |
| XD: Gale of Darkness        | GXXP01 / EUR     | `f36d14bebf8fea6a046404bff6adb7e6` |
| XD: Gale of Darkness        | GXXE01 / USA     | `3bc1671806cf763a8712a5d398f62ad3` |

Additionally, the following images exist but are currently not yet supported:

| Game                        | Game ID / Region | MD5 Checksum                       |
| --------------------------- | -----------------| ---------------------------------- |
| Colosseum                   | GC6P01 / EUR     | `2be2607ae4826cbc77efb4ef4ada6385` |
| Colosseum                   | GC6J01 / JPN     | `ec80218d9079ccae07350e42356748ce` |
| Colosseum                   | GC6E01 / USA     | `e3f389dc5662b9f941769e370195ec90` |
| XD: Yami no Kaze Dark Lugia | GXXJ01 / JPN     | `e92856cb965f8411e29ccfc818bd6d5b` |

The support for these versions will be explored later. Please consult other online
sources regarding creating a supported backup image of your game disc.

## Troubleshooting
If a randomized ISO crashes at the Nintendo logo or at the start of a Trainer battle, the randomizer
has managed to write a file into the ISO in such a manner that the game fails to uncompress it.
The ISO management routines should be rather stable by now, but this might still happen; please 
report which ISO you used (stating both the MD5 and the game/region is the best option) and 
with which options, and it will probably be looked into in due time.

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
