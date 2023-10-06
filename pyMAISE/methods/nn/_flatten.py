import copy

from keras.layers import Flatten

from pyMAISE.utils.hyperparameters import HyperParameters


# Dense layer keras neural networks
class FlattenLayer:
    def __init__(self, layer_name, parameters: dict):
        self._layer_name = layer_name
        self.reset()

        for key, value in parameters.items():
            if key == "num_layers":
                self._num_layers = value
                continue

            self._data[key] = value

        # Assert keras non-default variables are defined
        # assert self._data["data_format"] != None

    # ==========================================================================
    # Methods
    def build(self, hp):
        # Set pyMAISE hyperparameter to keras-tuner hyperparameter
        sampled_data = copy.deepcopy(self._data)
        for key, value in self._data.items():
            if isinstance(value, HyperParameters):
                assert self._data[key]
                sampled_data[key] = value.hp(
                    hp, "_".join([self._layer_name + str(self._current_layer), key])
                )
            else:
                sampled_data[key] = value

        return Flatten(**sampled_data)

    def reset(self):
        self._current_layer = 0
        self._num_layers = 1
        self._data = {
            "data_format": None,
        }

    def increment_layer(self):
        self._current_layer = self._current_layer + 1

    # ==========================================================================
    # Getters
    def num_layers(self, hp):
        if isinstance(self._num_layers, HyperParameters):
            return self._num_layers.hp(hp, self._layer_name + "_num_layers")
        else:
            return self._num_layers
