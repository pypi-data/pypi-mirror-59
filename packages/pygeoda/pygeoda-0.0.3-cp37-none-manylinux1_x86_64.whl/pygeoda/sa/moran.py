from ..libgeoda import gda_localmoran
from .lisa import lisa

__author__ = "Xun Li <lixun910@gmail.com>"

def local_moran(w, data):
    """Apply local moran statistics.

    Args:
        w (Weight): An instance of Weight class.
        data (tuple): A 1d tuple of float type values of selected variable

    Returns:
        lisa: An instance of lisa class represents the results of local geary computations
    """
    if w == None:
        raise("Weights is None.")

    if w.num_obs != len(data):
        raise("The size of data doesnt not match the number of observations.")

    lisa_obj = gda_localmoran(w.gda_w, data)
    return lisa(lisa_obj)