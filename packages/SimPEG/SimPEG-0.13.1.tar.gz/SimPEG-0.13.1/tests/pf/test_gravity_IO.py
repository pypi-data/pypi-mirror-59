from __future__ import print_function
import unittest
import numpy as np
from SimPEG import Mesh, PF
from SimPEG.Utils import io_utils
from scipy.constants import mu_0
import shutil
import os


class GravSensProblemTests(unittest.TestCase):

    def setUp(self):
        url = 'https://storage.googleapis.com/simpeg/tests/potential_fields/'
        cloudfiles = ['GravData.obs', 'Gaussian.topo', 'Mesh_10m.msh',
                      'ModelStart.sus', 'SimPEG_Grav_Input.inp']

        self.basePath = os.path.expanduser('~/Downloads/simpegtemp')
        self.files = io_utils.download(
            [url + f for f in cloudfiles],
            folder=self.basePath,
            overwrite=True
        )

    def test_gravity_inversion(self):

        inp_file = os.path.sep.join([self.basePath, 'SimPEG_Grav_Input.inp'])

        driver = PF.GravityDriver.GravityDriver_Inv(inp_file)

        print(driver.mesh)
        print(driver.survey)
        print(driver.m0)
        print(driver.mref)
        print(driver.activeCells)
        print(driver.staticCells)
        print(driver.dynamicCells)
        print(driver.chi)
        print(driver.nC)
        print(driver.alphas)
        print(driver.bounds)
        print(driver.lpnorms)
        print(driver.eps)

        # Write obs to file
        io_utils.writeUBCgravityObservations(
            os.path.sep.join(
                [self.basePath, 'FWR_data.dat']
            ),
            driver.survey, driver.survey.dobs
        )
        # Read it back
        data = io_utils.readUBCgravityObservations(
                os.path.sep.join(
                    [self.basePath, 'FWR_data.dat']
                )
        )
        # Check similarity
        passed = np.all(data.dobs == driver.survey.dobs)
        self.assertTrue(passed, True)

        # Clean up the working directory
        shutil.rmtree(self.basePath)

if __name__ == '__main__':
    unittest.main()
