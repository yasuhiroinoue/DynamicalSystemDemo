import numpy as np
from scipy.integrate import odeint

class DynamicalSystem:
    def __init__(self, name, default_params, param_ranges, initial_state, t_max=50.0, dt=0.01):
        self.name = name
        self.default_params = default_params
        self.param_ranges = param_ranges
        self.initial_state = initial_state
        self.t_max = t_max
        self.dt = dt

    def equations(self, state, t, **params):
        raise NotImplementedError

    @property
    def latex_equations(self):
        raise NotImplementedError

    def solve(self, params):
        t = np.arange(0, self.t_max, self.dt)
        # Unpack params to match signature
        args = tuple(params[k] for k in self.default_params.keys())
        
        # Wrapper to unpack args for odeint which expects f(y, t, *args)
        def func(state, t, *args):
            # Reconstruct kwargs for the equations method
            kwargs = {k: v for k, v in zip(self.default_params.keys(), args)}
            return self.equations(state, t, **kwargs)

        states = odeint(func, self.initial_state, t, args=args)
        return t, states

class LorenzSystem(DynamicalSystem):
    def __init__(self):
        super().__init__(
            name="Lorenz Attractor",
            default_params={"sigma": 10.0, "rho": 28.0, "beta": 8.0/3.0},
            param_ranges={
                "sigma": (0.1, 50.0),
                "rho": (0.1, 100.0),
                "beta": (0.1, 20.0)
            },
            initial_state=[1.0, 1.0, 1.0]
        )

    @property
    def latex_equations(self):
        return r"""
        \begin{aligned}
        \frac{dx}{dt} &= \sigma(y - x) \\
        \frac{dy}{dt} &= x(\rho - z) - y \\
        \frac{dz}{dt} &= xy - \beta z
        \end{aligned}
        """

    def equations(self, state, t, sigma, rho, beta):
        x, y, z = state
        dxdt = sigma * (y - x)
        dydt = x * (rho - z) - y
        dzdt = x * y - beta * z
        return [dxdt, dydt, dzdt]

class RosslerSystem(DynamicalSystem):
    def __init__(self):
        super().__init__(
            name="Rössler Attractor",
            default_params={"a": 0.2, "b": 0.2, "c": 5.7},
            param_ranges={
                "a": (0.0, 1.0),
                "b": (0.0, 2.0),
                "c": (0.0, 20.0)
            },
            initial_state=[1.0, 1.0, 1.0],
            t_max=100.0
        )

    @property
    def latex_equations(self):
        return r"""
        \begin{aligned}
        \frac{dx}{dt} &= -y - z \\
        \frac{dy}{dt} &= x + ay \\
        \frac{dz}{dt} &= b + z(x - c)
        \end{aligned}
        """

    def equations(self, state, t, a, b, c):
        x, y, z = state
        dxdt = -y - z
        dydt = x + a * y
        dzdt = b + z * (x - c)
        return [dxdt, dydt, dzdt]

class ThomasSystem(DynamicalSystem):
    def __init__(self):
        super().__init__(
            name="Thomas Cyclically Symmetric Attractor",
            default_params={"b": 0.208186},
            param_ranges={
                "b": (0.0, 1.0)
            },
            initial_state=[1.1, 1.1, -0.01],
            t_max=500.0,
            dt=0.05
        )

    @property
    def latex_equations(self):
        return r"""
        \begin{aligned}
        \frac{dx}{dt} &= \sin(y) - bx \\
        \frac{dy}{dt} &= \sin(z) - by \\
        \frac{dz}{dt} &= \sin(x) - bz
        \end{aligned}
        """

    def equations(self, state, t, b):
        x, y, z = state
        dxdt = np.sin(y) - b * x
        dydt = np.sin(z) - b * y
        dzdt = np.sin(x) - b * z
        return [dxdt, dydt, dzdt]

SYSTEMS = {
    "Lorenz": LorenzSystem(),
    "Rössler": RosslerSystem(),
    "Thomas": ThomasSystem()
}
