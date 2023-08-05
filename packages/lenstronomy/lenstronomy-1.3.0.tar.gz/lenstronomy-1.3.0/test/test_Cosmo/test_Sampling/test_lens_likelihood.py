import numpy as np
import pytest
import numpy.testing as npt
from lenstronomy.Cosmo.lens_cosmo import LensCosmo
from lenstronomy.Cosmo.Sampling.lens_likelihood import LensSampleLikelihood
from astropy.cosmology import FlatLambdaCDM


class TestLensLikelihood(object):

    def setup(self):
        np.random.seed(seed=41)
        self.z_L = 0.8
        self.z_S = 3.0

        self.H0_true = 70
        self.omega_m_true = 0.3
        self.cosmo = FlatLambdaCDM(H0=self.H0_true, Om0=self.omega_m_true, Ob0=0.05)
        lensCosmo = LensCosmo(self.z_L, self.z_S, cosmo=self.cosmo)
        self.Dd_true = lensCosmo.D_d
        self.D_dt_true = lensCosmo.D_dt

        self.sigma_Dd = 100
        self.sigma_Ddt = 100
        num_samples = 10000
        self.D_dt_samples = np.random.normal(self.D_dt_true, self.sigma_Ddt, num_samples)
        self.D_d_samples = np.random.normal(self.Dd_true, self.sigma_Dd, num_samples)

        self.kwargs_lens_list = [{'z_lens': self.z_L, 'z_source': self.z_S, 'D_d_sample': self.D_d_samples,
                         'D_delta_t_sample': self.D_dt_samples, 'kde_type': 'scipy_gaussian', 'bandwidth': 1}]

    def test_log_likelihood(self):
        lens = LensSampleLikelihood(kwargs_lens_list=self.kwargs_lens_list)
        logl = lens.log_likelihood(self.cosmo, gamma_ppn=1, kappa_ext=0)
        cosmo = FlatLambdaCDM(H0=self.H0_true*0.99, Om0=self.omega_m_true, Ob0=0.05)
        logl_sigma = lens.log_likelihood(cosmo, gamma_ppn=1, kappa_ext=0)
        npt.assert_almost_equal(logl - logl_sigma, 0.12, decimal=2)


if __name__ == '__main__':
    pytest.main()
