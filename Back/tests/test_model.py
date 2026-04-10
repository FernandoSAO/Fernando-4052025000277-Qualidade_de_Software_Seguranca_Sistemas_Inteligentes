# tests/test_model_accuracy.py
"""
Teste para verificar a acurácia registrada no modelo exportado
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.loan_predictor import get_predictor


class TestModelAccuracy:
    """Testes para verificar a acurácia do modelo exportado"""
    
    # Threshold mínimo aceitável (75%)
    MIN_ACCURACY = 0.75
    
    @pytest.fixture(scope="class")
    def predictor(self):
        """Carrega o modelo real"""
        return get_predictor()
    
    # ============================================
    # TESTES DE ACURÁCIA DO MODELO EXPORTADO
    # ============================================
    
    def test_model_has_accuracy_info(self, predictor):
        """Testa se o modelo exportado tem informações de acurácia"""
        model_info = predictor.model_info
        
        assert 'score_cv' in model_info, "Modelo não tem score_cv"
        assert 'score_test' in model_info, "Modelo não tem score_test"
        assert 'training_accuracy' in model_info, "Modelo não tem training_accuracy"
        
        print(f"\n📊 Informações de acurácia do modelo:")
        print(f"   Score CV (validação cruzada): {model_info['score_cv']:.4f}")
        print(f"   Score Teste: {model_info['score_test']:.4f}")
        print(f"   Acurácia no treino: {model_info['training_accuracy']:.4f}")
    
    def test_cv_accuracy_meets_threshold(self, predictor):
        """Testa se a acurácia da validação cruzada está acima do mínimo (75%)"""
        score_cv = predictor.model_info['score_cv']
        
        print(f"\n📊 Validação Cruzada: {score_cv:.4f} ({score_cv*100:.1f}%)")
        print(f"   Mínimo exigido: {self.MIN_ACCURACY:.0%}")
        
        assert score_cv >= self.MIN_ACCURACY, \
            f"Acurácia CV {score_cv:.4f} está abaixo do mínimo {self.MIN_ACCURACY:.0%}"
        
        print(f"   ✅ Acurácia CV dentro do esperado!")
    
    def test_test_accuracy_meets_threshold(self, predictor):
        """Testa se a acurácia do conjunto de teste está acima do mínimo (75%)"""
        score_test = predictor.model_info['score_test']
        
        print(f"\n📊 Conjunto de Teste: {score_test:.4f} ({score_test*100:.1f}%)")
        print(f"   Mínimo exigido: {self.MIN_ACCURACY:.0%}")
        
        assert score_test >= self.MIN_ACCURACY, \
            f"Acurácia Teste {score_test:.4f} está abaixo do mínimo {self.MIN_ACCURACY:.0%}"
        
        print(f"   ✅ Acurácia Teste dentro do esperado!")
    
    def test_training_accuracy_reasonable(self, predictor):
        """Testa se a acurácia do treino é razoável (não é 100% nem muito baixa)"""
        training_acc = predictor.model_info['training_accuracy']
        
        print(f"\n📊 Acurácia no Treino: {training_acc:.4f} ({training_acc*100:.1f}%)")
        
        # Verifica se não é 100% (overfitting extremo)
        assert training_acc < 0.99, f"Acurácia no treino muito alta ({training_acc:.4f}) - possível overfitting"
        
        # Verifica se não é muito baixa
        assert training_acc >= self.MIN_ACCURACY, \
            f"Acurácia no treino {training_acc:.4f} está abaixo do mínimo {self.MIN_ACCURACY:.0%}"
        
        print(f"   ✅ Acurácia no treino razoável!")
    
    def test_accuracy_consistency(self, predictor):
        """Testa se as acurácias são consistentes entre si (diferença não muito grande)"""
        score_cv = predictor.model_info['score_cv']
        score_test = predictor.model_info['score_test']
        training_acc = predictor.model_info['training_accuracy']
        
        print(f"\n📊 Consistência das acurácias:")
        print(f"   Treino: {training_acc:.4f}")
        print(f"   CV: {score_cv:.4f}")
        print(f"   Teste: {score_test:.4f}")
        
        # Diferença máxima aceitável entre treino e teste (10%)
        diff_train_test = abs(training_acc - score_test)
        assert diff_train_test < 0.10, \
            f"Diferença muito grande entre treino ({training_acc:.4f}) e teste ({score_test:.4f})"
        
        # Diferença máxima aceitável entre CV e teste (5%)
        diff_cv_test = abs(score_cv - score_test)
        assert diff_cv_test < 0.05, \
            f"Diferença muito grande entre CV ({score_cv:.4f}) e teste ({score_test:.4f})"
        
        print(f"   ✅ Acurácias consistentes!")
    
    def test_model_performance_summary(self, predictor):
        """Resumo completo da performance do modelo"""
        model_info = predictor.model_info
        
        print("\n" + "="*60)
        print("📊 RESUMO DA PERFORMANCE DO MODELO")
        print("="*60)
        print(f"\n🤖 Modelo: {model_info['algorithm']}")
        print(f"   Versão: {model_info['version']}")
        print(f"\n📈 Acurácias:")
        print(f"   Validação Cruzada (CV): {model_info['score_cv']:.4f} ({model_info['score_cv']*100:.2f}%)")
        print(f"   Conjunto de Teste: {model_info['score_test']:.4f} ({model_info['score_test']*100:.2f}%)")
        print(f"   Treino: {model_info['training_accuracy']:.4f} ({model_info['training_accuracy']*100:.2f}%)")
        
        print(f"\n🎯 Parâmetros do modelo:")
        for param, value in model_info['parameters'].items():
            print(f"   {param}: {value}")
        
        print(f"\n✅ Mínimo exigido: {self.MIN_ACCURACY:.0%}")
        
        if model_info['score_cv'] >= self.MIN_ACCURACY:
            print(f"\n🎉 MODELO APROVADO! Acurácia dentro do esperado.")
        else:
            print(f"\n⚠️ MODELO REPROVADO! Acurácia abaixo do esperado.")
        
        print("="*60)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])