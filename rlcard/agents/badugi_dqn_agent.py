import os

from rlcard.agents.dqn_agent import DQNAgent


class BadugiDQNAgent(object):
    
    def __init__(self,
                 sess,
                 scope,
                 replay_memory_size=20000,
                 replay_memory_init_size=100,
                 update_target_estimator_every=1000,
                 discount_factor=0.99,
                 epsilon_start=1.0,
                 epsilon_end=0.1,
                 epsilon_decay_steps=20000,
                 batch_size=32,
                 action_num=2,
                 state_shape=None,
                 norm_step=100,
                 mlp_layers=None,
                 learning_rate=0.00005,
                 ckpt_path=None):
        self.bet_agent = DQNAgent(sess,
                                  scope=scope+'_bet',
                                  replay_memory_size=replay_memory_size,
                                  replay_memory_init_size=replay_memory_init_size,
                                  update_target_estimator_every=update_target_estimator_every,
                                  discount_factor=discount_factor,
                                  epsilon_start=epsilon_start,
                                  epsilon_end=epsilon_end,
                                  epsilon_decay_steps=epsilon_decay_steps,
                                  batch_size=batch_size,
                                  action_num=action_num,
                                  state_shape=state_shape,
                                  norm_step=norm_step,
                                  mlp_layers=mlp_layers,
                                  learning_rate=learning_rate)
        self.change_agent = DQNAgent(sess,
                                     scope=scope+'_change',
                                     replay_memory_size=replay_memory_size,
                                     replay_memory_init_size=replay_memory_init_size,
                                     update_target_estimator_every=update_target_estimator_every,
                                     discount_factor=discount_factor,
                                     epsilon_start=epsilon_start,
                                     epsilon_end=epsilon_end,
                                     epsilon_decay_steps=epsilon_decay_steps,
                                     batch_size=batch_size,
                                     action_num=action_num,
                                     state_shape=state_shape,
                                     norm_step=norm_step,
                                     mlp_layers=mlp_layers,
                                     learning_rate=learning_rate)

        if ckpt_path is not None:
            ckpt_dir = os.path.dirname(ckpt_path+'bet/')
            if not os.path.exists(ckpt_dir):
                os.makedirs(ckpt_dir)
            ckpt_dir = os.path.dirname(ckpt_path+'change/')
            if not os.path.exists(ckpt_dir):
                os.makedirs(ckpt_dir)
    
    def feed(self, ts):
        # print('State: {}, Action: {}, Reward: {}, Next State: {}, Done: {}'.format(ts[0], ts[1], ts[2], ts[3], ts[4]))
        if ts[0]['is_bet'] or ts[4]:
            self.bet_agent.feed(ts)
        else:
            self.change_agent.feed(ts)
        
    def step(self, state):
        if state['is_bet']:
            return self.bet_agent.step(state)
        else:
            return self.change_agent.step(state)
        
    def eval_step(self, state):
        if state['is_bet']:
            return self.bet_agent.eval_step(state)
        else:
            return self.change_agent.eval_step(state)

    def predict(self, state):
        if state['is_bet']:
            return self.bet_agent.predict(state)
        else:
            return self.change_agent.predict(state)
    
    def train(self):
        bet_loss = self.bet_agent.train()
        change_loss = self.change_agent.train()
        return bet_loss, change_loss

    def save(self, path, step):
        bet_path = self.bet_agent.save(path+'bet/', step)
        change_path = self.change_agent.save(path+'change/', step)
        return bet_path, change_path
