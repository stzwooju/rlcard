''' A toy example of playing Blackjack with random agents
'''

import rlcard
from rlcard.agents.random_agent import RandomAgent
from rlcard.utils.utils import set_global_seed

# Make environment
env = rlcard.make('badugi')
episode_num = 1

# Set a global seed
# set_global_seed(0)

# Set up agents
agent= RandomAgent(action_num=env.action_num)
env.set_agents([agent for _ in range(5)])

for episode in range(episode_num):

    # Generate data from the environment
    trajectories, _, _ = env.run(is_training=False)

    # Print out the trajectories
    print('\nEpisode {}'.format(episode))
    for ts in trajectories[0]:
        print('State: {}, Action: {}, Reward: {}, Next State: {}, Done: {}'.format(ts[0], ts[1], ts[2], ts[3], ts[4]))
