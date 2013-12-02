#!/bin/bash

export PATH=".:$PATH"



PY=/usr/bin/python




$PY -m excode sheepgraze_daisies_cmd.py > sheepgraze_daisies_cmd.tmp

$PY -m exprog sheepgraze.py -h > sheepgraze_help.tmp

$PY ./pyversion.py > pyversion.tmp
$PY -m exprog sheepgraze.py -f daisies > sheepgraze_daisies.tmp
$PY -m exprog sheepgraze.py -f money > sheepgraze_money.tmp
$PY -m exprog sheepgraze.py > sheepgraze.tmp
$PY -m excode sheepgraze_cmd.py > sheepgraze_cmd.tmp
$PY -m exprog sheepgraze3.py -h > sheepgraze3_help.tmp
$PY -m exprog sheepgraze3.py -f hay > sheepgraze3_hay.tmp
$PY -m exprog sheepgraze3.py -f daisies > sheepgraze3_daisies.tmp
$PY -m exprog sheepgraze3.py -f money > sheepgraze3_money.tmp
$PY -m exprog sheepjump.py -h > sheepjump_help.tmp
$PY -m exprog sheepjump.py -n 5 > sheepjump_j5.tmp
$PY -m exprog sheepactions.py -h > sheepactions_help.tmp
$PY -m exprog sheepactions.py jump -h > sheepactions_jump_help.tmp
$PY -m exprog sheepactions.py graze -h > sheepactions_graze_help.tmp
$PY -m exprog sheepactions.py graze -f daisies > sheepactions_graze_daisies.tmp
$PY -m excode sheepactions_graze_daisies_cmd.py > sheepactions_graze_daisies_cmd.tmp
$PY -m exprog sheepactions.py jump -n 5 > sheepactions_jump_j5.tmp
$PY -m excode sheepactions_jump_j5_cmd.py > sheepactions_jump_j5_cmd.tmp
$PY -m exprog sheepgame.py -h             > sheepgame_help.tmp
$PY -m exprog sheepgame.py sheep -h       > sheepgame_sheep_help.tmp
$PY -m exprog sheepgame.py sheep jump -h  > sheepgame_sheep_jump_help.tmp
$PY -m exprog sheepgame.py sheep graze -h > sheepgame_sheep_graze_help.tmp
$PY -m exprog sheepgame.py feed-wolf -h   > sheepgame_wolf_help.tmp
$PY -m exprog sheepgame.py sheep jump -n 5          > sheepgame_sheep_jump5.tmp
$PY -m excode sheepgame_sheep_jump5_cmd.py          > sheepgame_sheep_jump5_cmd.tmp
$PY -m exprog sheepgame.py sheep graze              > sheepgame_sheep_graze.tmp
$PY -m excode sheepgame_sheep_graze_cmd.py          > sheepgame_sheep_graze_cmd.tmp
$PY -m exprog sheepgame.py sheep graze -f daisies   > sheepgame_sheep_graze_daisies.tmp
$PY -m excode sheepgame_sheep_graze_daisies_cmd.py  > sheepgame_sheep_graze_daisies_cmd.tmp
$PY -m exprog sheepgame.py feed-wolf                > sheepgame_wolf_feed.tmp
$PY -m excode sheepgame_wolf_feed_cmd.py > sheepgame_wolf_feed_cmd.tmp
$PY -m exprog sheepgraze2.py -h             > sheepgraze2_help.tmp
$PY -m exprog sheepgraze2.py dosen          > sheepgraze2_exe1.tmp
$PY -m exprog sheepgraze2.py herd -t 5      > sheepgraze2_exe2.tmp
$PY -m exprog sheepgraze2.py herd -f hay    > sheepgraze2_exe3.tmp
$PY -m excode sheepgraze2_exe1_cmd.py       > sheepgraze2_exe1_cmd.tmp
$PY -m excode sheepgraze2_exe2_cmd.py       > sheepgraze2_exe2_cmd.tmp
$PY -m excode sheepgraze2_exe3_cmd.py       > sheepgraze2_exe3_cmd.tmp
$PY -m exprog argpext.py -h > argpext_help.tmp
$PY -m excode categdate.py > categdate.tmp
$PY -m excode retval.py > retval.tmp

