class State:
    '''
    this class would hold the game snapshot, used by the
    q learner to index it's table, as well as reward function
    to determine the reward of that particular state.
    '''

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
