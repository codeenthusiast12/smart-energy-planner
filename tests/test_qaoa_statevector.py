"""Independent small dense-matrix checks of the QAOA evolution."""
import sys
import unittest
from pathlib import Path
import numpy as np
from scipy.linalg import expm

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from qaoa_statevector import qaoa_state, apply_x_mixer, state_probabilities, sample_metrics


class TestQAOAStatevector(unittest.TestCase):
    def test_two_layers_against_dense_exponentials(self):
        e=np.array([.1,.3,.7,.2,.9,.4,.6,.8])
        x=np.array([[0,1],[1,0]])
        identity=np.eye(2)
        mixer=sum(np.kron(np.kron(x if q==2 else identity,x if q==1 else identity),x if q==0 else identity) for q in range(3))
        parameters=[.37,.23,-.49,.81]
        reference=np.ones(8,dtype=complex)/np.sqrt(8)
        for gamma,beta in np.array(parameters).reshape(-1,2):
            reference=expm(-1j*beta*mixer) @ expm(-1j*gamma*np.diag(e)) @ reference
        np.testing.assert_allclose(qaoa_state(e,parameters),reference,atol=1e-12)

    def test_qubit_zero_is_least_significant(self):
        state=np.zeros(8,dtype=complex);state[0]=1
        evolved=apply_x_mixer(state,np.pi/2,0)
        self.assertAlmostEqual(abs(evolved[1]),1)
        self.assertAlmostEqual(abs(evolved[4]),0)

    def test_zero_gamma_is_uniform(self):
        np.testing.assert_allclose(state_probabilities(np.arange(8),[0,.7]),np.ones(8)/8,atol=1e-12)

    def test_zero_beta_cost_phase(self):
        e=np.array([.1,.4,.8,.2])
        np.testing.assert_allclose(qaoa_state(e,[.83,0]),np.exp(-1j*.83*e)/2,atol=1e-12)

    def test_twelve_qubit_norm(self):
        e=np.linspace(0,1,4096)
        self.assertAlmostEqual(float(np.linalg.norm(qaoa_state(e,[.4,.2,.8,.1]))),1.0,places=12)

    def test_invalid_shape_rejected(self):
        with self.assertRaises(ValueError):qaoa_state([1,2,3],[.1,.2])
        with self.assertRaises(ValueError):qaoa_state([1,2],[.1])

    def test_no_feasible_sample_has_no_fallback(self):
        result=sample_metrics([0,1],[.2,3],[True,False],10,np.random.default_rng(42))
        self.assertEqual(result['feasible_samples'],0)
        self.assertIsNone(result['best_feasible_cost_cu'])
        self.assertIsNone(result['gap_cu'])


if __name__=='__main__':unittest.main()
