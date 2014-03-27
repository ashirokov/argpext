

# File: sheepgraze.py
import argpext

def sheep_graze(feed):
    print('Sheep grazes on %s' % feed)

class SheepGraze(argpext.Function):
    "Let sheep graze"
    hook = argpext.hook(sheep_graze)
    def populate(self,parser):
        parser.add_argument('-f', dest='feed', default='grass', 
                            help='Specify the feed. Default: %(default)s.')

if __name__ == '__main__':
    SheepGraze().digest()

