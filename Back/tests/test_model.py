import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.loan_predictor import get_predictor


class TestModelAccuracy:
    MIN_ACCURACY = 0.75

    @pytest.fixture(scope="class")
    def predictor(self):
        return get_predictor()

    def test_model_has_required_metrics(self, predictor):
        model_info = predictor.model_info

        assert 'score_cv' in model_info
        assert 'score_test' in model_info
        assert 'training_accuracy' in model_info

    def test_accuracy_thresholds(self, predictor):
        model_info = predictor.model_info

        assert model_info['score_cv'] >= self.MIN_ACCURACY
        assert model_info['score_test'] >= self.MIN_ACCURACY
        assert model_info['training_accuracy'] >= self.MIN_ACCURACY

    def test_no_extreme_overfitting(self, predictor):
        model_info = predictor.model_info

        assert model_info['training_accuracy'] < 0.99

    def test_accuracy_consistency(self, predictor):
        model_info = predictor.model_info

        diff_train_test = abs(model_info['training_accuracy'] - model_info['score_test'])
        diff_cv_test = abs(model_info['score_cv'] - model_info['score_test'])

        assert diff_train_test < 0.10
        assert diff_cv_test < 0.05