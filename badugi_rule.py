''' A toy example of playing Blackjack with random agents
'''

import rlcard
from rlcard.models.badugi_rule_models import BadugiRuleAgentV1
from rlcard.utils.utils import set_global_seed, send_slack

# Make environment
env = rlcard.make('badugi')
episode_num = 1

# Set a global seed
# set_global_seed(0)

# Set up agents
agent = BadugiRuleAgentV1()
env.set_agents([agent for _ in range(5)])

for episode in range(episode_num):

    # Generate data from the environment
    trajectories, _, _ = env.run(is_training=False)

    # Print out the trajectories
    send_slack('\nEpisode {}'.format(episode))
    for ts in trajectories[0]:
        print('State: {}\nAction: {}\nReward: {}\nNext State: {}\nDone: {}\n'.format(ts[0], env.decode_action(ts[1]), ts[2], ts[3], ts[4]))
