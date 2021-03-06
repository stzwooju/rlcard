''' An example of learning a Deep-Q Agent on Texas Limit Holdem
'''

import os
import tensorflow as tf

import rlcard
from rlcard.agents.dqn_agent import DQNAgent
from rlcard.agents.random_agent import RandomAgent
from rlcard.utils.utils import set_global_seed
from rlcard.utils.logger import Logger

# Make environment
env = rlcard.make('badugi')
eval_env = rlcard.make('badugi')

# Set the iterations numbers and how frequently we evaluate/save plot
evaluate_every = 1000
save_plot_every = 10000
checkpoint_every = 10000
evaluate_num = 1000
episode_num = 1000000

# Set the the number of steps for collecting normalization statistics
# and intial memory size
memory_init_size = 1000
norm_step = 100

# The paths for saving the logs and learning curves
root_path = './experiments/badugi_bet_dqn_result/'
log_path = root_path + 'log.txt'
csv_path = root_path + 'performance.csv'
figure_path = root_path + 'figures/'
checkpoint_path = root_path + 'ckpt/'

# Set a global seed
# set_global_seed(0)

with tf.Session() as sess:
    # Set agents
    global_step = tf.Variable(0, name='global_step', trainable=False)
    agent = DQNAgent(sess,
                     scope='dqn',
                     action_num=env.action_num,
                     replay_memory_size=int(1e5),
                     replay_memory_init_size=memory_init_size,
                     norm_step=norm_step,
                     state_shape=env.state_shape,
                     mlp_layers=[512, 512])

    random_agent = RandomAgent(action_num=eval_env.action_num)

    sess.run(tf.global_variables_initializer())

    env.set_agents([agent, random_agent, random_agent, random_agent, random_agent])
    eval_env.set_agents([agent, random_agent, random_agent, random_agent, random_agent])

    # Count the number of steps
    step_counter = 0

    # Init a Logger to plot the learning curve
    logger = Logger(xlabel='timestep', ylabel='bet reward', legend='DQN on Badugi', log_path=log_path, csv_path=csv_path)
    if not os.path.exists(checkpoint_path):
        os.makedirs(checkpoint_path)

    for episode in range(episode_num):

        # Generate data from the environment
        trajectories, _, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent
        for ts in trajectories[0]:
            agent.feed(ts)
            step_counter += 1

            # Train the agent
            train_count = step_counter - (memory_init_size + norm_step)
            if train_count > 0:
                loss = agent.train()
                print('\rINFO - Step {}, bet loss: {}'.format(step_counter, loss), end='')

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            print('Episode {}'.format(episode))
            reward = 0
            for eval_episode in range(evaluate_num):
                _, reward_sum, _ = eval_env.run(is_training=False)

                reward += reward_sum

            logger.log('\n########## Evaluation ##########')
            logger.log('Timestep: {} Average bet reward is {}'.format(env.timestep, float(reward)/evaluate_num))

            # Add point to logger
            logger.add_point(x=env.timestep, y=float(reward)/evaluate_num)

        # Make plot
        if episode % save_plot_every == 0 and episode > 0:
            logger.make_plot(save_path=figure_path+str(episode)+'.png')
        
        if episode % checkpoint_every == 0 and episode > 0:
            ckpt = agent.save(checkpoint_path, episode)
            print('Saved to {}'.format(ckpt))

    # Make the final plot
    logger.make_plot(save_path=figure_path+str(episode)+'.png')
