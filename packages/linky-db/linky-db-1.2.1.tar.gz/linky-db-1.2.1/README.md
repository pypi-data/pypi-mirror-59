linky ![build_status.svg] ![coverage.svg] ![avg_coverage.svg]

An databaseless file tagger using symlinks.

This allows for a file to have multiple tags without agonizing about folder structure.

# Quick start

If videos are your thing [here you go][video].

<iframe width="560" height="315" sandbox="allow-same-origin allow-scripts" src="https://video.ploud.fr/videos/embed/b404bb78-e1e6-4190-8517-ac222d015be4" frameborder="0" allowfullscreen></iframe>

This requires at least python 3.6 and pip.
Before files can be tagged, a directory first has to be initialized for use with `linky`.

## 1. Install the package

`pip install linky-db`

## 2. Configure the tag groups (categories)


**Navigate to directory for initialization**  
Can be your folder with videos, music, books, etc.

`cd my_link_root`

**Write a configuration file**  
You can modify it later of course.
See [categories.schema.yaml] for a description thereof and
 [categories.yaml] for an example

```bash
mkdir .linky
echo "
Tags:
  default: Untagged
  extensible: True
  exclusive_default: True
  tags:
    - Action
    - Fantasy
    - Romance
    - Sci-Fi
    - Zombie
" > .linky/categories.yaml
```

## 3. Initialize the folder

`linky init .`

A __.base__ directory will be created and everything previously in the directory,
 will be moved into the base directory.
 It will contain all the data.
The directory containing __.base__ and all other data is called the **linked root**.

See [How] and the [docs] for more information.

You can now start:

 - exploring commands: `linky help`, `linky help add`, `linky help ...`
 - tagging: `linky tag -t Category/Tag file_in_your_root`
 - adding more files `linky add fileOrDir_outside_your_root`
 - moving files: `linky move old/path/old_name new/path/new_name`  
   Moving files outside of the tag folders is restricted by `linky`!

# Why

Programs often use databases to keep meta information about files. These databases:
 
 - are often stored in places one might not expect
 - have a custom schema  
 - have incompatibilities with other databases  
   e.g postgres vs mariadb vs sqlite vs nosql vs etc.

All of which make migrations from program to program difficult. 
Now, of course this program will suffer from that particular problem (migration) too, however
 it will be possible to manually maintain the folder structure and links mentioned below. 

# How

Consider this existing directory. Lines prefixed by `#` are comments about the item below them!

```bash
# The linked root
.
### Base folder that contains the data
├── .base
####### Configuration folder
│   ├── .linky
│   │   └── categories.yaml
│   ├── Last Christmas (2019)
│   │   ├── Last.Christmas.2019.4k.HEVC.YIFY.mkv
│   │   └── subs
│   │       ├── cmn.srt
│   │       ├── de.srt
│   │       ├── eng.srt
│   │       └── nl.srt
│   └── The Hurt Locker (2008)
│       └── The.Hurt.Locker.2008.1080p.BRrip.mkv
### A category (or tag group) folder in the linked root
├── Actors
####### A tag folder
│   ├── Anthony Mackie
│   │   └── The Hurt Locker (2008)
│   │       └── The.Hurt.Locker.2008.1080p.BRrip.mkv -> ../../../.base/The Hurt Locker (2008)/The.Hurt.Locker.2008.1080p.BRrip.mkv
####### Another tag folder
│   ├── Emilia Clarke
│   │   └── Last Christmas (2019)
│   │       ├── Last.Christmas.2019.4k.HEVC.YIFY.mkv -> ../../../.base/Last Christmas (2019)/Last.Christmas.2019.4k.HEVC.YIFY.mkv
│   │       └── subs
│   │           ├── cmn.srt -> ../../../../.base/Last Christmas (2019)/subs/cmn.srt
│   │           ├── de.srt -> ../../../../.base/Last Christmas (2019)/subs/de.srt
│   │           ├── eng.srt -> ../../../../.base/Last Christmas (2019)/subs/eng.srt
│   │           └── nl.srt -> ../../../../.base/Last Christmas (2019)/subs/nl.srt
│   ├── Emma Thompson
│   │   └── Last Christmas (2019)
│   │       ├── Last.Christmas.2019.4k.HEVC.YIFY.mkv -> ../../../.base/Last Christmas (2019)/Last.Christmas.2019.4k.HEVC.YIFY.mkv
│   │       └── subs
│   │           ├── cmn.srt -> ../../../../.base/Last Christmas (2019)/subs/cmn.srt
│   │           ├── de.srt -> ../../../../.base/Last Christmas (2019)/subs/de.srt
│   │           ├── eng.srt -> ../../../../.base/Last Christmas (2019)/subs/eng.srt
│   │           └── nl.srt -> ../../../../.base/Last Christmas (2019)/subs/nl.srt
│   ├── Guy Pearce
│   │   └── The Hurt Locker (2008)
│   │       └── The.Hurt.Locker.2008.1080p.BRrip.mkv -> ../../../.base/The Hurt Locker (2008)/The.Hurt.Locker.2008.1080p.BRrip.mkv
│   ├── Jeremy Renner
│   │   └── The Hurt Locker (2008)
│   │       └── The.Hurt.Locker.2008.1080p.BRrip.mkv -> ../../../.base/The Hurt Locker (2008)/The.Hurt.Locker.2008.1080p.BRrip.mkv
│   └── Madison Ingoldsby
│       └── Last Christmas (2019)
│           ├── Last.Christmas.2019.4k.HEVC.YIFY.mkv -> ../../../.base/Last Christmas (2019)/Last.Christmas.2019.4k.HEVC.YIFY.mkv
│           └── subs
│               ├── cmn.srt -> ../../../../.base/Last Christmas (2019)/subs/cmn.srt
│               ├── de.srt -> ../../../../.base/Last Christmas (2019)/subs/de.srt
│               ├── eng.srt -> ../../../../.base/Last Christmas (2019)/subs/eng.srt
│               └── nl.srt -> ../../../../.base/Last Christmas (2019)/subs/nl.srt
└── Watched
    ├── Unwatched
    │   └── Last Christmas (2019)
    │       ├── Last.Christmas.2019.4k.HEVC.YIFY.mkv -> ../../../.base/Last Christmas (2019)/Last.Christmas.2019.4k.HEVC.YIFY.mkv
    │       └── subs
    │           ├── cmn.srt -> ../../../../.base/Last Christmas (2019)/subs/cmn.srt
    │           ├── de.srt -> ../../../../.base/Last Christmas (2019)/subs/de.srt
    │           ├── eng.srt -> ../../../../.base/Last Christmas (2019)/subs/eng.srt
    │           └── nl.srt -> ../../../../.base/Last Christmas (2019)/subs/nl.srt
    └── Watched
        └── The Hurt Locker (2008)
            └── The.Hurt.Locker.2008.1080p.BRrip.mkv -> ../../../.base/The Hurt Locker (2008)/The.Hurt.Locker.2008.1080p.BRrip.mkv
```

linky works by keeping all files in a common, hidden folder called `.base`.
All siblings of in the folder tree will link their files to the base folder.
It is thus possible to have a file in multiple categories like 
 Watched, Rating, Size, Actors etc.

# [Docs][]

For more information on the nomenclature and inner workings.

# Development

See [HACKING.md](./HACKING.md)

# Alternatives

The following are [semantic filesystems] that fulfill very similar functions.
Most use separate database files, which is why I don't use them, but they
 might very well be useful to you!

 - [dhtfs] - Tagging based filesystem, providing dynamic directory hierarchies
    based on tags associated with files.
 - [Tagsistant] - a tag-based filesystem for Linux 
    that turns directories into tags and search your files for you.
 - [TMSU] - TMSU is a tool for tagging your files. 
   It provides a simple command-line tool for applying tags 
    and a virtual filesystem so that you can get a tag-based 
    view of your files from within any other program. 
 - [xtagfs] - A tag-based filesystem for Mac OS X
 
[dhtfs]: https://code.google.com/archive/p/dhtfs/
[semantic filesystems]: https://en.wikipedia.org/wiki/Semantic_file_system
[Tagsistant]: https://tagsistant.net/
[TMSU]: https://tmsu.org/
[xtagfs]: https://code.google.com/archive/p/xtagfs/

# Thanks

First and formost to all the open source devs who made this possible.

 - the packages on pypi like cliff, yamale ando ther
 - `pip` for the package hosting
 - `gitlab` for the code hosting and CI
 - Jetbrains for the Pycharm IDE
 - Inkscape for the icon editor
 - My partner for the icon (a link is 66% of a foot. Source: [wikipedia][link-wiki])


[categories.yaml]: /presentation/data/1.movies/.linky/categories.yaml
[categories.schema.yaml]: /linky/schemas/categories.schema.yaml
[Docs]: ./docs/index.md
[How]: #how
[link-wiki]: https://en.wikipedia.org/wiki/Link_(unit)
[video]: https://video.ploud.fr/videos/watch/b404bb78-e1e6-4190-8517-ac222d015be4


[build_status.svg]: https://gitlab.com/NamingThingsIsHard/linky/-/jobs/artifacts/master/raw/images/build_status.svg?job=test
[coverage.svg]: https://gitlab.com/NamingThingsIsHard/linky/-/jobs/artifacts/master/raw/images/coverage.svg?job=test
[avg_coverage.svg]: https://gitlab.com/NamingThingsIsHard/linky/-/jobs/artifacts/master/raw/images/avg_coverage.svg?job=test
