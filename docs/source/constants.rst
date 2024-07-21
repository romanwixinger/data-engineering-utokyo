Constants
=========

Physical constants and parameters of the experiments. These are mainly used in the ImageAnalysis.

.. automodule:: data_eng_utokyo.constants
   :members:
   :imported-members:
   :show-inheritance:
   :undoc-members:

In the following, we demonstrate the use of the CameraConstants class with a simplified implementation.


.. code:: python

    import numpy as np

    class Constants:

        def __init__(self, x_power: float, beam_diam: float):
            self.x_power = x_power
            self.beam_diam = beam_diam

        @property
        def x_intens(self) -> float:
            return self.x_power/(np.pi * ((self.beam_diam/2)**2))


Without the property decorator, the x_intens attribute would have to be set in the constructor.
This has the problem, that updating the other attributes is not possible without causing
inconsistencies between the attributes, as some attributes are calculated from the other. However,
using the properties decorator, we can now easily do update like


.. code:: python

    from data_engineering_utokyo import Constants

    c = Constants(x_power=100, beam_diam=1)

    for x_power in range(100):
        c.x_power = x_power
        print("The derived value is x_intens = {c.x_intens}.")


We see that we can access the method x_intens() like an attribute and it always gives us the value
based on the most up-to-date value of the other attributes. This is especially important when we want
to vary parameters in an experiment.
