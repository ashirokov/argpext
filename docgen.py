import os
import sys

from exdoc import *

os.chdir('examples')
sys.path += [os.path.abspath('.')]


for program,filename in [
        ('sheepgraze_daisies_cmd.py', 'sheepgraze_daisies_cmd.tmp')
        ,('sheepgraze_cmd.py', 'sheepgraze_cmd.tmp')
        ,('sheepactions_graze_daisies_cmd.py', 'sheepactions_graze_daisies_cmd.tmp')
        ,('sheepactions_jump_j5_cmd.py', 'sheepactions_jump_j5_cmd.tmp')
        ,('sheepgame_sheep_jump5_cmd.py', 'sheepgame_sheep_jump5_cmd.tmp')
        ,('sheepgame_sheep_graze_cmd.py', 'sheepgame_sheep_graze_cmd.tmp')
        ,('sheepgame_sheep_graze_daisies_cmd.py', 'sheepgame_sheep_graze_daisies_cmd.tmp')
        ,('sheepgame_wolf_feed_cmd.py', 'sheepgame_wolf_feed_cmd.tmp')
        ,('sheepgraze2_exe1_cmd.py', 'sheepgraze2_exe1_cmd.tmp')
        ,('sheepgraze2_exe2_cmd.py', 'sheepgraze2_exe2_cmd.tmp')
        ,('sheepgraze2_exe3_cmd.py', 'sheepgraze2_exe3_cmd.tmp')
        ,('categdate.py', 'categdate.tmp')
        ,('retval.py', 'retval.tmp')
]:
    interp(program,filename)


for script,attributes in [['sheepgraze.py', [(['-h'],'sheepgraze_help.tmp')
                                             ,(['-f', 'daisies'], 'sheepgraze_daisies.tmp')
                                             ,(['-f', 'money'], 'sheepgraze_money.tmp')
                                             ,([], 'sheepgraze.tmp')]],

                          ['sheepgraze3.py', [(['-h'], 'sheepgraze3_help.tmp')
                                              ,(['-f', 'hay'], 'sheepgraze3_hay.tmp')
                                              ,(['-f', 'daisies'], 'sheepgraze3_daisies.tmp')
                                              ,(['-f', 'money'], 'sheepgraze3_money.tmp')]],

                          ['sheepjump.py', [(['-h'], 'sheepjump_help.tmp')
                                            ,(['-n', '5'], 'sheepjump_j5.tmp')]],

                          ['sheepactions.py', [(['-h'], 'sheepactions_help.tmp')
                                               ,(['jump', '-h'], 'sheepactions_jump_help.tmp')
                                               ,(['graze', '-h'], 'sheepactions_graze_help.tmp')
                                               ,(['graze', '-f', 'daisies'], 'sheepactions_graze_daisies.tmp')
                                               ,(['jump', '-n', '5'], 'sheepactions_jump_j5.tmp')]],
                          
                          ['sheepgame.py', [(['-h'], 'sheepgame_help.tmp')
                                            ,(['sheep', '-h'], 'sheepgame_sheep_help.tmp')
                                            ,(['sheep', 'jump', '-h'], 'sheepgame_sheep_jump_help.tmp')
                                            ,(['sheep', 'graze', '-h'], 'sheepgame_sheep_graze_help.tmp')
                                            ,(['feed-wolf', '-h'], 'sheepgame_wolf_help.tmp')
                                            ,(['sheep', 'jump', '-n', '5'], 'sheepgame_sheep_jump5.tmp')
                                            ,(['sheep', 'graze'], 'sheepgame_sheep_graze.tmp')
                                            ,(['sheep', 'graze', '-f', 'daisies'], 'sheepgame_sheep_graze_daisies.tmp')
                                            ,(['feed-wolf'], 'sheepgame_wolf_feed.tmp')]],

                          ['sheepgraze2.py', [(['-h'],'sheepgraze2_help.tmp'),
                                              (['dosen'], 'sheepgraze2_exe1.tmp'),
                                              (['herd', '-t', '5'], 'sheepgraze2_exe2.tmp'),
                                              (['herd', '-f', 'hay'], 'sheepgraze2_exe3.tmp')]],

                          ['argpext.py', [(['-h'], 'argpext_help.tmp')]]
                       ]:
    for args,outputfile in attributes:
        print('Outputfile|:', outputfile )
        scriptrun(script,args,outputfile)






