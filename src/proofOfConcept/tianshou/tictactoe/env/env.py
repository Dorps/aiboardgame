import gymnasium
import numpy as np
from gymnasium import spaces
from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers
from .board import Board


def env(render_mode=None):
    internal_render_mode = render_mode if render_mode != "ansi" else "human"
    env = raw_env(render_mode=internal_render_mode)
    if render_mode == "ansi":
        env = wrappers.CaptureStdoutWrapper(env)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env


class raw_env(AECEnv):
    metadata = {
        "render_modes": ["human"],
        "name": "tictactoe_v0",
        "is_parallelizable": False,
        "render_fps": 1,
    }

    def __init__(self, render_mode=None):
        super().__init__()
        self.board = Board()
        self.agents = ["player_1", "player_2"]
        self.possible_agents = self.agents[:]
        self.action_spaces = {i: spaces.Discrete(32) for i in self.agents}
        self.observation_spaces = {
            i: spaces.Dict(
                {
                    "observation": spaces.Box(
                        low=0, high=1, shape=(4, 4, 2), dtype=np.int8
                    ),
                    "action_mask": spaces.Box(low=0, high=1, shape=(32,), dtype=np.int8),
                }
            )
            for i in self.agents
        }
        self.rewards = {i: 0 for i in self.agents}
        self.terminations = {i: False for i in self.agents}
        self.truncations = {i: False for i in self.agents}
        self.infos = {i: {"legal_moves": list(
            range(0, 9))} for i in self.agents}
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.reset()
        self.render_mode = render_mode

    def observe(self, agent):
        board_vals = np.array(self.board.squares).reshape(4, 4)
        cur_player = self.possible_agents.index(agent)
        opp_player = (cur_player + 1) % 2

        cur_p_board = np.equal(board_vals, cur_player + 1)
        opp_p_board = np.equal(board_vals, opp_player + 1)

        observation = np.stack(
            [cur_p_board, opp_p_board], axis=2).astype(np.int8)
        legal_moves = self._legal_moves() if agent == self.agent_selection else []

        action_mask = np.zeros(32, "int8")
        for i in legal_moves:
            action_mask[i] = 1
        if(self.board.specialMovesLeft[cur_player] > 0):
            for i in range(16, 32):
                if(self.board.squares[i-16] == (cur_player+1) or self.board.squares[i-16] == 0):
                    action_mask[i] = 0
                else:
                    action_mask[i] = 1
        else:
            for i in range(16, 32):
                action_mask[i] = 0
        return {"observation": observation, "action_mask": action_mask}

    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def action_space(self, agent):
        return self.action_spaces[agent]

    def _legal_moves(self):
        return [i for i in range(len(self.board.squares)) if self.board.squares[i] == 0]

    def step(self, action):
        if (
            self.terminations[self.agent_selection]
            or self.truncations[self.agent_selection]
        ):
            return self._was_dead_step(action)
        # check if input action is a valid move (0 == empty spot)
        if(action <= 15):
            assert self.board.squares[action] == 0, "played illegal move"
        elif(action > 15):
            agentIndex = self.agents.index(self.agent_selection)
            assert self.board.specialMovesLeft[agentIndex] > 0

        # play turn
        print(self.agent_selection)
        self.board.play_turn(self.agents.index(self.agent_selection), action)
        # self.rewards[self.agents[self.agents.index(self.agent_selection)]] -= 1

        # update infos
        # list of valid actions (indexes in board)
        # next_agent = self.agents[(self.agents.index(self.agent_selection) + 1) % len(self.agents)]

        if self.board.check_game_over():
            winner = self.board.check_for_winner()

            if winner == -1:
                # tie
                self.rewards[self.agents[0]] -= 1  # tie is bad for X player
                self.rewards[self.agents[1]] += 1  # tie is good for O player
            elif winner == 1:
                # agent 0 won
                self.rewards[self.agents[0]] += 2
                self.rewards[self.agents[1]] -= 1
            else:
                # agent 1 won
                self.rewards[self.agents[1]] += 2
                self.rewards[self.agents[0]] -= 1

            # once either play wins or there is a draw, game over, both players are done
            self.terminations = {i: True for i in self.agents}

        # Switch selection to next agents
        self._cumulative_rewards[self.agent_selection] = 0

        self.agent_selection = self.agents[self.board.getPlayer()]

        self._accumulate_rewards()
        if self.render_mode == "human":
            self.render()

    def reset(self, seed=None, return_info=False, options=None):
        # reset environment
        self.board = Board()

        self.agents = self.possible_agents[:]
        self.rewards = {i: 0 for i in self.agents}
        self._cumulative_rewards = {i: 0 for i in self.agents}
        self.terminations = {i: False for i in self.agents}
        self.truncations = {i: False for i in self.agents}
        self.infos = {i: {} for i in self.agents}
        # selects the first agent
        self._agent_selector.reinit(self.agents)
        self._agent_selector.reset()
        self.agent_selection = self._agent_selector.reset()

    def render(self):
        if self.render_mode is None:
            gymnasium.logger.warn(
                "You are calling render method without specifying any render mode."
            )
            return

        def getSymbol(input):
            if input == 0:
                return "-"
            elif input == 1:
                return "X"
            else:
                return "O"

        board = list(map(getSymbol, self.board.squares))
        print("#" * 22)
        print(" " * 5 + "|" + " " * 5 + "|" + " " * 5 + "|" + " " * 5)
        print(f"  {board[0]}  " + "|" + f"  {board[4]}  " +
              "|" + f"  {board[8]} " + " |" + f"  {board[12]} ")
        print(" " * 5 + "|" + " " * 5 + "|" + " " * 5 + "|" + " " * 5)

        print(" " * 5 + "|" + " " * 5 + "|" + " " * 5 + "|" + " " * 5)
        print(f"  {board[1]}  " + "|" + f"  {board[5]}  " +
              "|" + f"  {board[9]} " + " |" + f"  {board[13]} ")
        print(" " * 5 + "|" + " " * 5 + "|" + " " * 5 + "|" + " " * 5)

        print(" " * 5 + "|" + " " * 5 + "|" + " " * 5 + "|" + " " * 5)
        print(f"  {board[2]}  " + "|" + f"  {board[6]}  " +
              "|" + f"  {board[10]} " + " |" + f"  {board[14]} ")
        print(" " * 5 + "|" + " " * 5 + "|" + " " * 5 + "|" + " " * 5)

        print(" " * 5 + "|" + " " * 5 + "|" + " " * 5 + "|" + " " * 5)
        print(f"  {board[3]}  " + "|" + f"  {board[7]}  " +
              "|" + f"  {board[11]} " + " |" + f"  {board[15]} ")
        print(" " * 5 + "|" + " " * 5 + "|" + " " * 5 + "|" + " " * 5)
        print("Special Moves Left", self.board.specialMovesLeft)

        winner = self.board.check_for_winner()
        if(winner > 0):
            print("Winner is", winner)

    def close(self):
        pass
