
from flow.scenarios.loop.loop_scenario import LoopScenario
from flow.scenarios.loop.gen import CircleGenerator
from flow.core.vehicles import Vehicles
from flow.controllers.car_following_models import IDMController
from flow.controllers.routing_controllers import ContinuousRouter
from flow.scenarios.loop.loop_scenario import ADDITIONAL_NET_PARAMS
from flow.core.params import NetParams
from flow.core.params import InitialConfig
from flow.core.traffic_lights import TrafficLights
from flow.envs.loop.loop_accel import AccelEnv
from flow.core.params import SumoParams
from flow.envs.loop.loop_accel import ADDITIONAL_ENV_PARAMS
from flow.core.params import EnvParams
from flow.core.experiment import SumoExperiment

vehicles = Vehicles()
vehicles.add("human",
             acceleration_controller=(IDMController, {}),
             routing_controller=(ContinuousRouter, {}),
             num_vehicles=22)
net_params = NetParams(additional_params=ADDITIONAL_NET_PARAMS)
initial_config = InitialConfig(spacing="uniform", perturbation=1)
traffic_lights = TrafficLights()
sumo_params = SumoParams(sim_step=0.1, render=True)
env_params = EnvParams(additional_params=ADDITIONAL_ENV_PARAMS)
# create the scenario object
scenario = LoopScenario(name="ring_example",
                        generator_class=CircleGenerator,
                        vehicles=vehicles,
                        net_params=net_params,
                        initial_config=initial_config,
                        traffic_lights=traffic_lights)

# create the environment object
env = AccelEnv(env_params, sumo_params, scenario)

# create the experiment object
exp = SumoExperiment(env, scenario)

# run the experiment for a set number of rollouts / time steps
exp.run(1, 3000)