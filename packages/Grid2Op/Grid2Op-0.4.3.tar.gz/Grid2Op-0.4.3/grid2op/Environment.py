"""
This module defines the :class:`Environment` the higher level representation of the world with which an
:class:`grid2op.Agent` will interact.

The environment receive an :class:`grid2op.Action.Action` from the :class:`grid2op.Agent.Agent` in the
:func:`Environment.step`
and returns an
:class:`grid2op.Observation.Observation` that the :class:`grid2op.Agent.Agent` will use to perform the next action.

An environment is better used inside a :class:`grid2op.Runner.Runner`, mainly because runners abstract the interaction
between environment and agent, and ensure the environment are properly reset after each episode.

It is however totally possible to use as any gym Environment.

Example (adapted from gym documentation available at
`gym random_agent.py <https://github.com/openai/gym/blob/master/examples/agents/random_agent.py>`_ ):

>>> import grid2op
>>> from grid2op.Agent import DoNothingAgent
>>> env = grid2op.make()
>>> agent = DoNothingAgent(env.action_space)
>>> env.seed(0)
>>> episode_count = 100
>>> reward = 0
>>> done = False
>>> total_reward = 0
>>> for i in range(episode_count):
>>>        ob = env.reset()
>>>        while True:
>>>            action = agent.act(ob, reward, done)
>>>            ob, reward, done, _ = env.step(action)
>>>            total_reward += reward
>>>            if done:
>>>                # in this case the episode is over
>>>                break
>>>
>>>    # Close the env and write monitor result info to disk
>>>    env.close()
>>> print("The total reward was {:.2f}".format(total_reward))

"""

import numpy as np
import time
import os

try:
    from .Action import HelperAction, Action, TopologyAction
    from .Exceptions import *
    from .Observation import CompleteObservation, ObservationHelper, Observation
    from .Reward import FlatReward, RewardHelper, Reward
    from .GameRules import GameRules, AllwaysLegal, LegalAction
    from .Parameters import Parameters
    from .Backend import Backend
    from .ChronicsHandler import ChronicsHandler
except (ModuleNotFoundError, ImportError):
    from Action import HelperAction, Action, TopologyAction
    from Exceptions import *
    from Observation import CompleteObservation, ObservationHelper, Observation
    from Reward import FlatReward, RewardHelper, Reward
    from GameRules import GameRules, AllwaysLegal, LegalAction
    from Parameters import Parameters
    from Backend import Backend
    from ChronicsHandler import ChronicsHandler

import pdb


# TODO code "start from a given time step"
class Environment:
    """

    Attributes
    ----------
    logger: ``logger``
        Use to store some information (currently in beta status)

    time_stamp: ``datetime.time``
        Current time of the chronics

    nb_time_step: ``int``
        Number of time steps played this episode

    parameters: :class:`grid2op.Parameters.Parameters`
        Parameters used for the game

    rewardClass: ``type``
        Type of reward used. Should be a subclass of :class:`grid2op.Reward.Reward`

    init_grid_path: ``str``
        The path where the description of the powergrid is located.

    backend: :class:`grid2op.Backend.Backend`
        The backend used to compute powerflows and cascading failures.

    game_rules: :class:`grid2op.GameRules.GameRules`
        The rules of the game (define which actions are legal and which are not)

    helper_action_player: :class:`grid2op.Action.HelperAction`
        Helper used to manipulate more easily the actions given to / provided by the :class:`grid2op.Agent` (player)

    helper_action_env: :class:`grid2op.Action.HelperAction`
        Helper used to manipulate more easily the actions given to / provided by the environment to the backend.

    helper_observation: :class:`grid2op.Observation.ObservationHelper`
        Helper used to generate the observation that will be given to the :class:`grid2op.Agent`

    current_obs: :class:`grid2op.Observation.Observation`
        The current observation (or None if it's not intialized)

    no_overflow_disconnection: ``bool``
        Whether or not cascading failures are computed or not (TRUE = the powerlines above their thermal limits will
        not be disconnected). This is initialized based on the attribute
        :attr:`grid2op.Parameters.Parameters.NO_OVERFLOW_DISCONNECTION`.

    timestep_overflow: ``numpy.ndarray``, dtype: int
        Number of consecutive timesteps each powerline has been on overflow.

    nb_timestep_overflow_allowed: ``numpy.ndarray``, dtype: int
        Number of consecutive timestep each powerline can be on overflow. It is usually read from
        :attr:`grid2op.Parameters.Parameters.NB_TIMESTEP_POWERFLOW_ALLOWED`.

    hard_overflow_threshold: ``float``
        Number of timestep before an :class:`grid2op.Agent.Agent` can reconnet a powerline that has been disconnected
        by the environment due to an overflow.

    env_dc: ``bool``
        Whether the environment computes the powerflow using the DC approximation or not. It is usually read from
        :attr:`grid2op.Parameters.Parameters.ENV_DC`.

    chronics_handler: :class:`grid2op.ChronicsHandler.ChronicsHandler`
        Helper to get the modification of each time step during the episode.

    names_chronics_to_backend: ``dict``
        Configuration file used to associated the name of the objects in the backend
        (both extremities of powerlines, load or production for
        example) with the same object in the data (:attr:`Environment.chronics_handler`). The idea is that, usually
        data generation comes from a different software that does not take into account the powergrid infrastructure.
        Hence, the same "object" can have a different name. This mapping is present to avoid the need to rename
        the "object" when providing data. A more detailed description is available at
        :func:`grid2op.ChronicsHandler.GridValue.initialize`.

    reward_helper: :class:`grid2p.Reward.RewardHelper`
        Helper that is called to compute the reward at each time step.

    action_space: :class:`grid2op.Action.HelperAction`
        Another name for :attr:`Environment.helper_action_player` for gym compatibility.

    observation_space:  :class:`grid2op.Observation.ObservationHelper`
        Another name for :attr:`Environment.helper_observation` for gym compatibility.

    reward_range: ``(float, float)``
        The range of the reward function

    metadata: ``dict``
        For gym compatibility, do not use

    spec: ``None``
        For Gym compatibility, do not use

    viewer: ``object``
        Used to display the powergrid. Currently not supported.

    env_modification: :class:`grid2op.Action.Action`
        Representation of the actions of the environment for the modification of the powergrid.

    TODO update with maintenance, hazards etc. see below
    # store actions "cooldown"
    times_before_line_status_actionable
    max_timestep_line_status_deactivated
    times_before_topology_actionable
    max_timestep_topology_deactivated
    time_next_maintenance
    duration_next_maintenance
    hard_overflow_threshold
    time_remaining_before_reconnection

    """
    def __init__(self,
                 init_grid_path: str,
                 chronics_handler,
                 backend,
                 parameters,
                 names_chronics_to_backend=None,
                 actionClass=TopologyAction,
                 observationClass=CompleteObservation,
                 rewardClass=FlatReward,
                 legalActClass=AllwaysLegal):
        """
        Initialize the environment. See the descirption of :class:`grid2op.Environment.Environment` for more information.

        Parameters
        ----------
        init_grid_path: ``str``
            Used to initailize :attr:`Environment.init_grid_path`

        chronics_handler
        backend
        parameters
        names_chronics_to_backend
        actionClass
        observationClass
        rewardClass
        legalActClass
        """
        # TODO documentation!!

        # some timers
        self._time_apply_act = 0
        self._time_powerflow = 0
        self._time_extract_obs = 0

        # define logger
        self.logger = None

        # and calendar data
        self.time_stamp = None
        self.nb_time_step = 0

        # specific to power system
        if not isinstance(parameters, Parameters):
            raise Grid2OpException("Parameter \"parameters\" used to build the Environment should derived form the "
                                   "grid2op.Parameters class, type provided is \"{}\"".format(type(parameters)))
        self.parameters = parameters

        if not isinstance(rewardClass, type):
            raise Grid2OpException("Parameter \"rewardClass\" used to build the Environment should be a type (a class) "
                                   "and not an object (an instance of a class). "
                                   "It is currently \"{}\"".format(type(rewardClass)))
        if not issubclass(rewardClass, Reward):
            raise Grid2OpException(
                "Parameter \"rewardClass\" used to build the Environment should derived form the grid2op.Reward class, "
                "type provided is \"{}\"".format(
                    type(rewardClass)))
        self.rewardClass = rewardClass

        # backend
        self.init_grid_path = os.path.abspath(init_grid_path)

        if not isinstance(backend, Backend):
            raise Grid2OpException(
                "Parameter \"backend\" used to build the Environment should derived form the grid2op.Backend class, "
                "type provided is \"{}\"".format(
                    type(backend)))
        self.backend = backend
        self.backend.load_grid(self.init_grid_path)  # the real powergrid of the environment
        self.backend.assert_grid_correct()
        *_, tmp = self.backend.generators_info()

        # rules of the game
        if not isinstance(legalActClass, type):
            raise Grid2OpException("Parameter \"legalActClass\" used to build the Environment should be a type "
                                   "(a class) and not an object (an instance of a class). "
                                   "It is currently \"{}\"".format(type(legalActClass)))
        if not issubclass(legalActClass, LegalAction):
            raise Grid2OpException(
                "Parameter \"legalActClass\" used to build the Environment should derived form the "
                "grid2op.LegalAction class, type provided is \"{}\"".format(
                    type(legalActClass)))
        self.game_rules = GameRules(legalActClass=legalActClass)

        # action helper
        if not isinstance(actionClass, type):
            raise Grid2OpException("Parameter \"actionClass\" used to build the Environment should be a type (a class) "
                                   "and not an object (an instance of a class). "
                                   "It is currently \"{}\"".format(type(legalActClass)))
        if not issubclass(actionClass, Action):
            raise Grid2OpException(
                "Parameter \"actionClass\" used to build the Environment should derived form the "
                "grid2op.Action class, type provided is \"{}\"".format(
                    type(actionClass)))

        if not isinstance(observationClass, type):
            raise Grid2OpException("Parameter \"actionClass\" used to build the Environment should be a type (a class) "
                                   "and not an object (an instance of a class). "
                                   "It is currently \"{}\"".format(type(legalActClass)))
        if not issubclass(observationClass, Observation):
            raise Grid2OpException(
                "Parameter \"observationClass\" used to build the Environment should derived form the "
                "grid2op.Observation class, type provided is \"{}\"".format(
                    type(observationClass)))

        # action affecting the _grid that will be made by the agent
        self.helper_action_player = HelperAction(gridobj=self.backend,
                                                 actionClass=actionClass,
                                                 game_rules=self.game_rules)

        # action that affect the _grid made by the environment.
        self.helper_action_env = HelperAction(gridobj=self.backend,
                                              actionClass=Action,
                                              game_rules=self.game_rules)

        self.helper_observation = ObservationHelper(gridobj=self.backend,
                                                    observationClass=observationClass,
                                                    rewardClass=rewardClass,
                                                    env=self)
        # observation
        self.current_obs = None

        # type of power flow to play
        # if True, then it will not disconnect lines above their thermal limits
        self.no_overflow_disconnection = self.parameters.NO_OVERFLOW_DISCONNECTION
        self.timestep_overflow = np.zeros(shape=(self.backend.n_line,), dtype=np.int)
        self.nb_timestep_overflow_allowed = np.full(shape=(self.backend.n_line,),
                                                    fill_value=self.parameters.NB_TIMESTEP_POWERFLOW_ALLOWED)
        # store actions "cooldown"
        self.times_before_line_status_actionable = np.zeros(shape=(self.backend.n_line,), dtype=np.int)
        self.max_timestep_line_status_deactivated = self.parameters.NB_TIMESTEP_LINE_STATUS_REMODIF

        self.times_before_topology_actionable = np.zeros(shape=(self.backend.n_sub,), dtype=np.int)
        self.max_timestep_topology_deactivated = self.parameters.NB_TIMESTEP_TOPOLOGY_REMODIF

        # for maintenance operation
        self.time_next_maintenance = np.zeros(shape=(self.backend.n_line,), dtype=np.int) - 1
        self.duration_next_maintenance = np.zeros(shape=(self.backend.n_line,), dtype=np.int)

        # hazard (not used outside of this class, information is given in `time_remaining_before_line_reconnection`
        self._hazard_duration = np.zeros(shape=(self.backend.n_line,), dtype=np.int)

        # hard overflow part
        self.hard_overflow_threshold = self.parameters.HARD_OVERFLOW_THRESHOLD
        self.time_remaining_before_line_reconnection = np.full(shape=(self.backend.n_line,),
                                                               fill_value=0, dtype=np.int)
        self.env_dc = self.parameters.ENV_DC

        # handles input data
        if not isinstance(chronics_handler, ChronicsHandler):
            raise Grid2OpException(
                "Parameter \"chronics_handler\" used to build the Environment should derived form the "
                "grid2op.ChronicsHandler class, type provided is \"{}\"".format(
                    type(chronics_handler)))
        self.chronics_handler = chronics_handler
        self.chronics_handler.initialize(self.backend.name_load, self.backend.name_gen,
                                         self.backend.name_line, self.backend.name_sub,
                                         names_chronics_to_backend=names_chronics_to_backend)
        self.names_chronics_to_backend = names_chronics_to_backend

        # test to make sure the backend is consistent with the chronics generator
        self.chronics_handler.check_validity(self.backend)

        # store environment modifications
        self._injection = None
        self._maintenance = None
        self._hazards = None
        self.env_modification = None

        # reward
        self.reward_helper = RewardHelper(rewardClass=rewardClass)
        self.reward_helper.initialize(self)

        # performs one step to load the environment properly (first action need to be taken at first time step after
        # first injections given)
        self._reset_maintenance()
        do_nothing = self.helper_action_env({})
        *_, fail_to_start, _ = self.step(do_nothing)
        if fail_to_start:
            raise Grid2OpException("Impossible to initialize the powergrid, the powerflow diverge at iteration 0.")

        # test the backend returns object of the proper size
        self.backend.assert_grid_correct_after_powerflow()

        # for gym compatibility
        self.action_space = self.helper_action_player  # this should be an action !!!
        self.observation_space = self.helper_observation  # this return an observation.
        self.reward_range = self.reward_helper.range()
        self.viewer = None

        self.metadata = {'render.modes': []}
        self.spec = None

        self._reset_vectors_and_timings()

    def __str__(self):
        return '<{} instance>'.format(type(self).__name__)
        # TODO be closer to original gym implementation
        # if self.spec is None:
        #     return '<{} instance>'.format(type(self).__name__)
        # else:
        #     return '<{}<{}>>'.format(type(self).__name__, self.spec.id)

    def __enter__(self):
        """
        Support *with-statement* for the environment.

        Examples
        --------
        >>> import grid2op
        >>> import grid2op.Agent
        >>> with grid2op.make() as env:
        >>>     agent = grid2op.Agent.DoNothingAgent(env.action_space)
        >>>     act = env.action_space()
        >>>     obs, r, done, info = env.step(act)
        >>>     act = agent.act(obs, r, info)
        >>>     obs, r, done, info = env.step(act)
        """
        return self

    def __exit__(self, *args):
        """
        Support *with-statement* for the environment.
        """
        self.close()
        # propagate exception
        return False

    def _reset_maintenance(self):
        self.time_next_maintenance = np.zeros(shape=(self.backend.n_line,), dtype=np.int) - 1
        self.duration_next_maintenance = np.zeros(shape=(self.backend.n_line,), dtype=np.int)
        self.time_remaining_before_reconnection = np.full(shape=(self.backend.n_line,), fill_value=0, dtype=np.int)

    def reset_grid(self):
        """
        Reset the backend to a clean state by reloading the powergrid from the hard drive. This might takes some time.

        """
        self.backend.load_grid(self.init_grid_path)  # the real powergrid of the environment
        self.backend.assert_grid_correct()

        do_nothing = self.helper_action_env({})
        self.step(do_nothing)
        # test the backend returns object of the proper size
        self.backend.assert_grid_correct_after_powerflow()

    def add_text_logger(self, logger=None):
        """
        Add a text logger to this  :class:`Environment`

        Logging is for now an incomplete feature. It will get improved
        Parameters
        ----------
            seed:
               The logger to use

        """
        self.logger = logger
        return self

    def seed(self, seed=None):
        """
        Set the seed of this :class:`Environment` for a better control and to ease reproducible experiments.

        This is not supported yet;
        Parameters
        ----------
            seed: ``int``
               The seed to set.

        """
        # example from gym
        # self.np_random, seed = seeding.np_random(seed)
        # TODO make that more clean, see example of seeding @ https://github.com/openai/gym/tree/master/gym/utils
        self.chronics_handler.seed(seed)
        self.helper_observation.seed(seed)
        return [seed]

    def _update_actions(self):
        """
        Retrieve the actions to perform the update of the underlying powergrid represented by
         the :class:`grid2op.Backend`in the next time step.
        A call to this function will also read the next state of :attr:`chronics_handler`, so it must be called only
        once per time step.

        Returns
        --------
        res: :class:`grid2op.Action.Action`
            The action representing the modification of the powergrid induced by the Backend.
        """
        timestamp, tmp, maintenance_time, maintenance_duration, hazard_duration = self.chronics_handler.next_time_step()
        if "injection" in tmp:
            self._injection = tmp["injection"]
        else:
            self._injection = None
        if 'maintenance' in tmp:
            self._maintenance = tmp['maintenance']
        else:
            self._maintenance = None
        if "hazards" in tmp:
            self._hazards = tmp["hazards"]
        else:
            self._hazards = None
        self.time_stamp = timestamp
        self.duration_next_maintenance = maintenance_duration
        self.time_next_maintenance = maintenance_time
        self._hazard_duration = hazard_duration
        return self.helper_action_env({"injection": self._injection, "maintenance": self._maintenance,
                                       "hazards": self._hazards})

    def get_obs(self):
        """
        Return the observations of the current environment made by the :class:`grid2op.Agent.Agent`.

        Returns
        -------
        res: :class:`grid2op.Observation.Observation`
            The current Observation given to the :class:`grid2op.Agent.Agent` / bot / controler.
        """
        res = self.helper_observation(env=self)
        return res

    def _get_reward(self, action, has_error, is_done, is_illegal, is_ambiguous):
        return self.reward_helper(action, self, has_error, is_done, is_illegal, is_ambiguous)

    def _is_done(self, has_error, is_done):
        no_more_data = self.chronics_handler.done()
        return has_error or is_done or no_more_data

    def _update_time_reconnection_hazards_maintenance(self):
        """
        This supposes that :attr:`Environment.time_remaining_before_line_reconnection` is already updated
        with the cascading failure, soft overflow and hard overflow.

        It also supposes that :func:`Environment._update_actions` has been called, so that the vectors
        :attr:`Environment.duration_next_maintenance`, :attr:`Environment.time_next_maintenance` and
        :attr:`Environment._hazard_duration` are updated with the most recent values.

        Finally the Environment supposes that this method is called before calling :func:`Environment.get_obs`

        This function integrates the hazards and maintenance in the
        :attr:`Environment.time_remaining_before_line_reconnection` vector.
        For example, if a powerline `i` has no problem
        of overflow, but is affected by a hazard, :attr:`Environment.time_remaining_before_line_reconnection`
        should be updated with the duration of this hazard (stored in one of the three vector mentionned in the
        above paragraph)

        For this Environment, we suppose that the maximum of the 3 values are taken into account. The reality would
        be more complicated.

        Returns
        -------

        """
        self.time_remaining_before_line_reconnection = np.maximum(self.time_remaining_before_line_reconnection,
                                                                  self.duration_next_maintenance)
        self.time_remaining_before_line_reconnection = np.maximum(self.time_remaining_before_line_reconnection,
                                                                  self._hazard_duration)

    def step(self, action):
        """
        Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.
        Accepts an action and returns a tuple (observation, reward, done, info).

        If the :class:`grid2op.Action.Action` is illegal or ambiguous, the step is performed, but the action is
        replaced with a "do nothing" action.

        Parameters
        ----------
            action: :class:`grid2op.Action.Action`
                an action provided by the agent that is applied on the underlying through the backend.

        Returns
        -------
            observation: :class:`grid2op.Observation.Observation`
                agent's observation of the current environment

            reward: ``float``
                amount of reward returned after previous action

            done: ``bool``
                whether the episode has ended, in which case further step() calls will return undefined results

            info: ``dict``
                contains auxiliary diagnostic information (helpful for debugging, and sometimes learning). It is a
                dicitonnary with keys:

                    - "disc_lines": a numpy array (or ``None``) saying, for each powerline if it has been disconnected
                        due to overflow
                    - "is_illegal" (``bool``) whether the action given as input was illegal
                    - "is_ambiguous" (``bool``) whether the action given as input was ambiguous.

        """
        has_error = True
        is_done = False
        disc_lines = None
        is_illegal = False
        is_ambiguous = False
        try:
            beg_ = time.time()
            is_illegal = not self.game_rules(action=action, env=self)
            if is_illegal:
                # action is replace by do nothing
                action = self.helper_action_player({})

            try:
                self.backend.apply_action(action)
            except AmbiguousAction:
                # action has not been implemented on the powergrid because it's ambiguous, it's equivalent to
                # "do nothing"
                is_ambiguous = True

            self.env_modification = self._update_actions()
            self.backend.apply_action(self.env_modification)
            self._time_apply_act += time.time() - beg_

            self.nb_time_step += 1
            try:
                # compute the next _grid state
                beg_ = time.time()
                disc_lines, infos = self.backend.next_grid_state(env=self, is_dc=self.env_dc)
                self._time_powerflow += time.time() - beg_

                beg_ = time.time()
                self.backend.update_thermal_limit(self)  # update the thermal limit, for DLR for example
                overflow_lines = self.backend.get_line_overflow()

                # one timestep passed, i can maybe reconnect some lines
                self.time_remaining_before_line_reconnection[self.time_remaining_before_line_reconnection > 0] -= 1
                # update the vector for lines that have been disconnected
                self.time_remaining_before_line_reconnection[disc_lines] = int(self.parameters.NB_TIMESTEP_RECONNECTION)
                self._update_time_reconnection_hazards_maintenance()

                # for the powerline that are on overflow, increase this time step
                self.timestep_overflow[overflow_lines] += 1

                # set to 0 the number of timestep for lines that are not on overflow
                self.timestep_overflow[~overflow_lines] = 0

                # build the topological action "cooldown"
                aff_lines, aff_subs = action.get_topological_impact()
                if self.max_timestep_line_status_deactivated > 0:
                    # this is a feature I want to consider in the parameters
                    self.times_before_line_status_actionable[self.times_before_line_status_actionable > 0] -= 1
                    self.times_before_line_status_actionable[aff_lines] = self.max_timestep_line_status_deactivated
                if self.max_timestep_topology_deactivated > 0:
                    # this is a feature I want to consider in the parameters
                    self.times_before_topology_actionable[self.times_before_topology_actionable > 0] -= 1
                    self.times_before_topology_actionable[aff_subs] = self.max_timestep_topology_deactivated

                # build the observation
                self.current_obs = self.get_obs()
                self._time_extract_obs += time.time() - beg_

                has_error = False
            except Grid2OpException as e:
                if self.logger is not None:
                    self.logger.error("Impossible to compute next _grid state with error \"{}\"".format(e))
        except StopIteration:
            # episode is over
            is_done = True
        infos = {"disc_lines": disc_lines, "is_illegal": is_illegal, "is_ambiguous": is_ambiguous}
        return self.current_obs, self._get_reward(action, has_error, is_done, is_illegal, is_ambiguous),\
               self._is_done(has_error, is_done),\
               infos

    def _reset_vectors_and_timings(self):
        """
        Maintenance are not reset, otherwise the data are not read properly (skip the first time step)
        Returns
        -------

        """
        self.no_overflow_disconnection = self.parameters.NO_OVERFLOW_DISCONNECTION
        self.timestep_overflow = np.zeros(shape=(self.backend.n_line,), dtype=np.int)
        self.nb_timestep_overflow_allowed = np.full(shape=(self.backend.n_line,),
                                                    fill_value=self.parameters.NB_TIMESTEP_POWERFLOW_ALLOWED)
        self.nb_time_step = 0
        self.hard_overflow_threshold = self.parameters.HARD_OVERFLOW_THRESHOLD
        self.env_dc = self.parameters.ENV_DC

        self.times_before_line_status_actionable = np.zeros(shape=(self.backend.n_line,), dtype=np.int)
        self.max_timestep_line_status_deactivated = self.parameters.NB_TIMESTEP_LINE_STATUS_REMODIF

        self.times_before_topology_actionable = np.zeros(shape=(self.backend.n_sub,), dtype=np.int)
        self.max_timestep_topology_deactivated = self.parameters.NB_TIMESTEP_TOPOLOGY_REMODIF

        self._time_apply_act = 0
        self._time_powerflow = 0
        self._time_extract_obs = 0

    def reset(self):
        """
        Reset the environment to a clean state.
        It will reload the next chronics if any. And reset the grid to a clean state.

        This triggers a full reloading of both the chronics (if they are stored as files) and of the powergrid,
        to ensure the episode is fully over.

        This method should be called only at the end of an episode.
        """
        self.chronics_handler.next_chronics()
        self.chronics_handler.initialize(self.backend.name_load, self.backend.name_gen,
                                         self.backend.name_line, self.backend.name_sub,
                                         names_chronics_to_backend=self.names_chronics_to_backend)
        self.current_obs = None
        self._reset_maintenance()
        self.reset_grid()

        # if True, then it will not disconnect lines above their thermal limits
        self._reset_vectors_and_timings()
        return self.get_obs()

    def render(self, mode='human'):
        # TODO here, and reuse pypownet
        pass

    def close(self):
        # todo there might be some side effect
        if self.viewer:
            self.viewer.close()
            self.viewer = None
        self.backend.close()