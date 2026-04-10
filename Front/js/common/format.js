/*
  --------------------------------------------------------------------------------------
  Garante formato correto para Valor
  --------------------------------------------------------------------------------------

*/

export function setupCurrencyMask(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.addEventListener('input', function () {
        // mantém apenas números
        let rawValue = this.value.replace(/\D/g, '');

        if (!rawValue) {
            this.value = 'R$ 0,00';
            return;
        }

        // remove zeros à esquerda
        rawValue = rawValue.replace(/^0+/, '') || '0';

        // garante pelo menos 3 dígitos (centavos)
        rawValue = rawValue.padStart(3, '0');

        // separa parte inteira e decimal
        let integerPart = rawValue.slice(0, -2);
        const decimalPart = rawValue.slice(-2);

        // adiciona separador de milhar
        integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');

        // monta valor final
        this.value = `R$ ${integerPart},${decimalPart}`;
    });

    // valor inicial
    input.value = 'R$ 0,00';
}

/*
  --------------------------------------------------------------------------------------
  Garante formato correto para telefone
  --------------------------------------------------------------------------------------

*/

export function setupPhoneMask(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.addEventListener('input', function () {
        // mantém só números
        let value = this.value.replace(/\D/g, '');

        // limita no máximo 11 dígitos (DDD + celular)
        value = value.slice(0, 11);

        // aplica máscara progressiva
        if (value.length <= 2) {
            this.value = `(${value}`;
        } 
        else if (value.length <= 6) {
            this.value = `(${value.slice(0,2)}) ${value.slice(2)}`;
        } 
        else if (value.length <= 10) {
            // telefone fixo: (21) 9999-9999
            this.value = `(${value.slice(0,2)}) ${value.slice(2,6)}-${value.slice(6)}`;
        } 
        else {
            // celular: (21) 99999-9999
            this.value = `(${value.slice(0,2)}) ${value.slice(2,7)}-${value.slice(7)}`;
        }
    });

}

/*
  --------------------------------------------------------------------------------------
  Garante formato correto para CPF
  --------------------------------------------------------------------------------------
*/

export function setupCpfMask(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.addEventListener('input', function () {
        // mantém apenas números
        let value = this.value.replace(/\D/g, '');

        // limita no máximo 11 dígitos
        value = value.slice(0, 11);

        // aplica máscara progressiva
        if (value.length <= 3) {
            this.value = value;
        } 
        else if (value.length <= 6) {
            this.value = `${value.slice(0,3)}.${value.slice(3)}`;
        } 
        else if (value.length <= 9) {
            this.value = `${value.slice(0,3)}.${value.slice(3,6)}.${value.slice(6)}`;
        } 
        else {
            this.value = `${value.slice(0,3)}.${value.slice(3,6)}.${value.slice(6,9)}-${value.slice(9,11)}`;
        }
    });
}

/*
  --------------------------------------------------------------------------------------
  Garante formato correto para Percentual (%)
  --------------------------------------------------------------------------------------
*/

export function setupPercentMask(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.addEventListener('input', function () {
        // Mantém apenas números e vírgula
        let rawValue = this.value.replace(/[^0-9,]/g, '');
        
        // Remove formatação anterior para processar
        let cleanValue = rawValue.replace(',', '');
        
        if (cleanValue === '') {
            this.value = '';
            return;
        }
        
        // Converte para número (sem vírgula)
        let numericValue = parseInt(cleanValue, 10);
        
        if (isNaN(numericValue)) {
            this.value = '';
            return;
        }
        
        // Limita entre 0 e 10000 (para permitir até 100,00)
        if (numericValue > 10000) numericValue = 10000;
        
        // Separa parte inteira e decimal
        let integerPart = Math.floor(numericValue / 100);
        let decimalPart = numericValue % 100;
        
        // Limita parte inteira a 100
        if (integerPart > 100) {
            integerPart = 100;
            decimalPart = 0;
        }
        
        // Formata o valor
        if (decimalPart === 0) {
            this.value = `${integerPart}%`;
        } else {
            this.value = `${integerPart},${decimalPart.toString().padStart(2, '0')}%`;
        }
    });
    
    // Formata ao perder o foco (blur)
    input.addEventListener('blur', function () {
        if (!this.value || this.value === '') return;
        
        // Extrai o valor numérico
        let value = this.value.replace(/[^0-9,]/g, '').replace(',', '.');
        let numericValue = parseFloat(value);
        
        if (isNaN(numericValue)) {
            this.value = '';
            return;
        }
        
        // Limita entre 0 e 100
        if (numericValue < 0) numericValue = 0;
        if (numericValue > 100) numericValue = 100;
        
        // Formata com 2 casas decimais
        this.value = numericValue.toFixed(2).replace('.', ',') + '%';
    });
}

/*
  --------------------------------------------------------------------------------------
  Garante formato correto para Percentual (versão alternativa com limite de 2 casas)
  --------------------------------------------------------------------------------------
*/

export function setupPercentMaskSimple(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.addEventListener('input', function () {
        // mantém apenas números
        let value = this.value.replace(/\D/g, '');
        
        if (!value) {
            this.value = '';
            return;
        }
        
        // limita entre 0 e 10000 (para permitir até 100.00)
        let numericValue = parseInt(value, 10);
        if (numericValue > 10000) numericValue = 10000;
        
        // separa parte inteira e decimal
        let integerPart = Math.floor(numericValue / 100);
        let decimalPart = numericValue % 100;
        
        // limita parte inteira a 100
        if (integerPart > 100) integerPart = 100;
        
        // formata
        this.value = `${integerPart}.${decimalPart.toString().padStart(2, '0')}%`;
    });
    
    input.addEventListener('blur', function () {
        if (!this.value || this.value === '') return;
        
        let cleanValue = this.value.replace(/[^0-9]/g, '');
        if (!cleanValue) {
            this.value = '';
            return;
        }
        
        let numericValue = parseInt(cleanValue, 10);
        let integerPart = Math.floor(numericValue / 100);
        let decimalPart = numericValue % 100;
        
        if (integerPart > 100) integerPart = 100;
        
        this.value = `${integerPart}.${decimalPart.toString().padStart(2, '0')}%`;
    });
}