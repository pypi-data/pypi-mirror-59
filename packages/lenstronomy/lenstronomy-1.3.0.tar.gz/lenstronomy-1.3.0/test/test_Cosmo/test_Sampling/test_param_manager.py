import unittest
import pytest
import numpy.testing as npt
from lenstronomy.Cosmo.Sampling.param_manager import CosmoParam


class TestParamManager(object):

    def setup(self):
        cosmology_list = ['FLCDM', "FwCDM", "w0waCDM", "oLCDM"]
        kwargs_lower = {'h0': 10, 'om': 0., 'ok': -0.5, 'w': -2, 'wa': -1, 'w0': -2, 'gamma_ppn': 0}
        kwargs_upper = {'h0': 200, 'om': 1, 'ok': 0.5, 'w': 0, 'wa': 1, 'w0': 1, 'gamma_ppn': 5}
        kwargs_fixed = {'h0': 70, 'om': 0.3, 'ok': 0., 'w': -1, 'wa': -0, 'w0': -0, 'gamma_ppn': 1}
        param_list = []
        for cosmology in cosmology_list:
            param_list.append(CosmoParam(cosmology, kwargs_lower, kwargs_upper, kwargs_fixed, ppn_sampling=True))
            param_list.append(CosmoParam(cosmology, kwargs_lower, kwargs_upper, kwargs_fixed={}, ppn_sampling=True))
        self.param_list = param_list

    def test_num_param(self):
        num, list = self.param_list[0].num_param
        assert num == 0
        num, list = self.param_list[1].num_param
        assert num == 3
        for param in self.param_list:
            num, list = param.num_param

    def test_kwargs2args(self):
        kwargs = {'h0': 70, 'om': 0.3, 'ok': 0., 'w': -1, 'wa': -0, 'w0': -0, 'gamma_ppn': 1}
        for param in self.param_list:
            args = param.kwargs2args(kwargs)
            kwargs_new = param.args2kwargs(args)
            args_new = param.kwargs2args(kwargs_new)
            npt.assert_almost_equal(args_new, args)

    def test_cosmo(self):
        kwargs = {'h0': 70, 'om': 0.3, 'ok': 0., 'w': -1, 'wa': -0, 'w0': -0, 'gamma_ppn': 1}
        for param in self.param_list:
            cosmo = param.cosmo(kwargs)
            assert hasattr(cosmo, 'H0')

    def test_param_bounds(self):
        lower_limit, upper_limit = self.param_list[0].param_bounds
        assert len(lower_limit) == 0
        lower_limit, upper_limit = self.param_list[1].param_bounds
        assert len(lower_limit) == 3


class TestRaise(unittest.TestCase):

    def test_raise(self):

        with self.assertRaises(ValueError):
            CosmoParam(cosmology='wrong', kwargs_lower={}, kwargs_upper={}, kwargs_fixed={}, ppn_sampling=True)
        with self.assertRaises(ValueError):
            param = CosmoParam(cosmology='FLCDM', kwargs_lower={}, kwargs_upper={}, kwargs_fixed={}, ppn_sampling=True)
            param._cosmology = 'wrong'
            param.cosmo(kwargs={})


if __name__ == '__main__':
    pytest.main()
