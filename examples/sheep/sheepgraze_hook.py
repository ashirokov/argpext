

import argpext

class SheepGraze(argpext.Task):
    "Let sheep graze"

    def hook(self,feed):
        print('Sheep grazes on %s' % feed)

    def populate(self,parser):
        parser.add_argument('-f', dest='feed', default='grass', 
                            help='Specify the feed. Default: %(default)s.')

if __name__ == '__main__':
    SheepGraze().digest()

