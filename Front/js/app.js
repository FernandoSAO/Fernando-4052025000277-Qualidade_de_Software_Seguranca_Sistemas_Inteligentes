
// módulos Js
import { initializeClientForm } from './pages/insert_client.js';
import { initializeLoanForm } from './pages/loan_test.js';
import { initializeLoanHistory } from './pages/loan_history.js';

// Salva todos os inicializadores em um objeto
const pageInitializers = {
    'insert-client' : initializeClientForm,
    'loan-test': initializeLoanForm,
    'loan-history': initializeLoanHistory
};

// Cache para todos os elementos HTML
const componentCache = new Map();

async function loadComponent(componentName) {
    if (componentCache.has(componentName)) {
        return componentCache.get(componentName);
    }
    
    try {
        const response = await fetch(`components/${componentName}.html`);
        const html = await response.text();
        componentCache.set(componentName, html);
        return html;
    } catch (error) {
        console.error(`Error loading ${componentName}:`, error);
        return `<div>Error loading ${componentName}</div>`;
    }
}

// Inicializa o app
async function initApp() {
    console.log('🚀 Initializing app...');
    
    // Carrega o header e a sidebar
    const [headerHTML, sidebarHTML] = await Promise.all([
        loadComponent('header'),
        loadComponent('sidebar')
    ]);
    
    // Insere componente no DOM
    document.getElementById('header-container').innerHTML = headerHTML;
    document.getElementById('sidebar-container').innerHTML = sidebarHTML;
    
    console.log('✅ Components loaded');
    
    // DEBUG: Verifica os elementos do dropdown
    setTimeout(() => {
        console.log('🔍 Dropdown toggles found:', 
            document.querySelectorAll('.dropdown-toggle').length);
        console.log('🔍 Dropdown items found:', 
            document.querySelectorAll('.dropdown-nav-btn').length);
    }, 50);
    
    // Faz o setup das interações após a inserção dos componentes
    setupHamburgerToggle();
    setupSidebarNavigation();
    
    // Carrega página inicial
    loadPage('insert-client');
}

// função para abrir e fechar a sidebar usando apenas o hamburgerBtn
function setupHamburgerToggle() {
    const hamburgerBtn = document.getElementById('menu-toggle');
    const sidebar = document.querySelector('.left-sidebar');
    
    if (!hamburgerBtn || !sidebar) {
        console.error('❌ Button or sidebar not found');
        return;
    }
    
    hamburgerBtn.addEventListener('click', function() {
        sidebar.classList.toggle('active');
    });
    
    console.log('✅ Hamburger setup: Click hamburger to open/close');
}

function setupSidebarNavigation() {
    console.log('🔗 Setting up ALL sidebar interactions...');
    
    // A. Faz o setup dos toggles do dropdown (botões com classe .dropdown-toggle)
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    console.log(`📂 Found ${dropdownToggles.length} dropdown toggles`);
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.stopPropagation(); // Don't trigger parent clicks
            
            console.log('📂 Dropdown toggle clicked:', this.textContent.trim());
            
            // procura e aciona o container do dropdown
            const dropdown = this.closest('.sidebar-dropdown');
            if (dropdown) {
                dropdown.classList.toggle('expanded');
                console.log(`Dropdown ${dropdown.classList.contains('expanded') ? 'expanded' : 'collapsed'}`);
            }
        });
    });
    
    // B. Aciona a navegação da página (botões com atributo data-page)
    const navButtons = document.querySelectorAll('[data-page]');
    console.log(`📄 Found ${navButtons.length} navigation buttons`);
    
    navButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            
            const page = this.dataset.page;
            console.log(`📄 Navigating to: ${page}`);
            
            // Carrega a página
            loadPage(page);
            
            // Faz update nos itens de navegação
            updateActiveNavItem(page);

            // Fecha o sidebar ao navegar
            const sidebar = document.querySelector('.left-sidebar');
            if (sidebar?.classList.contains('active')) {
                sidebar.classList.remove('active');
            }
        });
    });
    
    console.log('✅ Sidebar navigation setup complete');
}

// Carrega a página para o content area
async function loadPage(pageName) {
    console.log(`📄 Loading page: ${pageName}`);
    
    const content = document.getElementById('app-content');
    
    // Mostra o indicador de loading
    content.innerHTML = '<div class="loading">⌛ Carregando...</div>';
    
    try {
        // converte nome da página para nome do arquivo
        const fileName = pageName.replace(/-/g, '_'); // insert-company → insert_company
        const filePath = `pages/${fileName}.html`;
        
        console.log(`📂 Fetching: ${filePath}`);
        
        // Faz o Fetch do arquivo de HTML
        const response = await fetch(filePath);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const pageHTML = await response.text();
        
        // Insere o HTML
        content.innerHTML = pageHTML;
        
        // Inicializa o JavaScript da página
        initializePage(pageName);
        
        console.log(`✅ Page loaded: ${pageName}`);
        
    } catch (error) {
        console.error(`❌ Failed to load page "${pageName}":`, error);
        content.innerHTML = `
            <div class="error">
                <h2>Erro ao carregar página</h2>
                <p>Não foi possível carregar "${pageName}"</p>
                <button onclick="loadPage('home')">Voltar para Início</button>
            </div>
        `;
    }
}

// Faz Update nos itens de navegação ativos
function updateActiveNavItem(activePage) {
    // Remove active de todos os botões
    document.querySelectorAll('.nav-btn, .dropdown-nav-btn').forEach(item => {
        item.classList.remove('active');
    });
    
    // Adiciona ativo
    document.querySelectorAll('[data-page]').forEach(item => {
        if (item.dataset.page === activePage) {
            item.classList.add('active');
        }
    });
}

// Inicializa as funcionalidades da página
function initializePage(pageName) {
    console.log(`⚙️ Initializing page: ${pageName}`);
    
    const initializer = pageInitializers[pageName];
    
    if (initializer) {
        console.log(`🔧 Calling initializer for: ${pageName}`);
        initializer();
    } else {
        console.log(`ℹ️ No initializer for: ${pageName}`);
    }
}

// Inicia o app quando o DOM esta pronto
document.addEventListener('DOMContentLoaded', initApp);