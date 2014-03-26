

import argpext

def sheep_graze(feed):
    print('Sheep grazes on %s' % feed)


class SheepGraze(argpext.Function):
    "Let sheep graze"
    hook = argpext.Hook(sheep_graze)
    def populate(self,parser):
        parser.add_argument('-f', dest='feed', default='grass'
                            , type=argpext.KeyWords(['hay',
                                                     'grass',
                                                     'daisies'])
                            , help='Specify the feed. '\
                                'Choose from:%(type)s. '\
                                'Default: %(default)s.')

if __name__ == '__main__':
    SheepGraze().digest()

