# Pokémon GameCube Randomizer

This tool randomizes Pokémon XD: Gale of Darkness ISOs, providing a fresh gameplay
experience with different trainer battles, Pokémon specifics and item placements
based on the given settings. It also partially randomizes Pokémon Colosseum ISOs
as well.

## Image support

These images have been tested to work correctly with this randomizer:

| Game                        | Game ID / Region | MD5 Checksum                       |
| --------------------------- | -----------------| ---------------------------------- |
| Colosseum                   | GC6P01 / EUR     | `2be2607ae4826cbc77efb4ef4ada6385` |
| Colosseum                   | GC6J01 / JPN     | `ec80218d9079ccae07350e42356748ce` |
| Colosseum                   | GC6E01 / USA     | `e3f389dc5662b9f941769e370195ec90` |
| XD: Gale of Darkness        | GXXP01 / EUR     | `f36d14bebf8fea6a046404bff6adb7e6` |
| XD: Yami no Kaze Dark Lugia | GXXJ01 / JPN     | `e92856cb965f8411e29ccfc818bd6d5b` |
| XD: Gale of Darkness        | GXXE01 / USA     | `3bc1671806cf763a8712a5d398f62ad3` |

Trainer, item box, starter and gift Pokémon related randomization is not yet supported for Colosseum.

Please consult other online sources regarding creating a supported backup image of your game disc.

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
