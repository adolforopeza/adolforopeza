document.addEventListener('alpine:init', () => {
    Alpine.data('portfolio', () => ({
        section: 'home',
        lang: 'es',
        mobileOpen: false,
        scrolled: false,
        modalExp: null,
        isLoaded: false,
        langCache: {},
        // Estructura inicial para evitar errores de "undefined"
        data: {
            core: {},
            expData: [],
            projectsData: [],
            skillsCategories: [],
            t: { nav: {}, home: {}, about: {}, exp: {}, proj: {}, contact: {}, footer: {} }
        },

        dataBasePath: './',

        // Getters protegidos para evitar errores de consola
        get role () {
            return this.data.core?.role || '';
        },
        get location () {
            return this.data.core?.location || '';
        },
        get specialty () {
            return this.data.core?.specialty || '';
        },
        getYearsSince: function(startYear) {
            if (!startYear) return 0;
            const currentYear = new Date().getFullYear();
            return currentYear - parseInt(startYear);
        },
        get totalyearsexpinphp() {
            // Si tienes el año en devphpsince, calcula la diferencia
            const startYear = this.data.core?.dev_php_since;
            return startYear ? this.getYearsSince(startYear) + " yrs." : "";
        },
        get totalyearsexpinmage() {
            // Si tienes el año en devmagesince, calcula la diferencia
            const startYear = this.data.core?.dev_mage_since;
            return startYear ? this.getYearsSince(startYear) +" yrs." : '';
        },
        get devphpsince() { return this.data.core?.dev_php_since || ''; },
        get devmagesince() { return this.data.core?.dev_mage_since || ''; },
        get summary () {
            return this.data.core?.summary || '';
        },
        get profile () {
            return this.data.core?.profile || '';
        },
        get email () {
            return this.data.core?.email || '';
        },
        get phone () {
            return this.data.core?.phone || '';
        },
        get linkedin () {
            return this.data.core?.linkedin || '';
        },
        get github () {
            return this.data.core?.github || '';
        },
        get education () {
            return this.data.core?.education || '';
        },
        get languages () {
            return this.data.core?.languages || '';
        },
        get experiences () {
            return this.data.expData || [];
        },
        get projects () {
            return this.data.projectsData || [];
        },
        get skills () {
            return this.data.skillsCategories || [];
        },
        get t () {
            return this.data.t || {};
        },

        init: async function() {
            const saved = localStorage.getItem('portfolio-lang');
            if (saved === 'es' || saved === 'en') this.lang = saved;
            await this.loadLang(this.lang);
            const hash = window.location.hash.replace('#', '');
            if (['home','about','experience','projects','contact'].includes(hash)) {
                this.section = hash;
            }
        },

        loadLang: async function(lang) {
            try {
                this.isLoaded = false;
                if (!this.langCache[lang]) {
                    // Asegúrate de que la carpeta /data/ existe en la raíz
                    const response = await fetch(`${this.dataBasePath}data/${lang}.json`);
                    if (!response.ok) throw new Error(`HTTP ${response.status}`);
                    this.langCache[lang] = await response.json();
                }
                this.data = this.langCache[lang];
                this.lang = lang;
                document.documentElement.lang = lang;
                this.isLoaded = true;
            } catch (error) {
                console.error(`[portfolio] Error loading ${lang}.json:`, error);
                this.isLoaded = true;
            }
        },

        setLang: async function(lang) {
            if (lang === this.lang) return;
            localStorage.setItem('portfolio-lang', lang);
            await this.loadLang(lang);
        },

        navigate: function(sec) {
            this.section = sec;
            this.mobileOpen = false;
            window.history.pushState(null, '', `#${sec}`);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        },

        openModal: function(exp) {
            this.modalExp = exp;
            document.body.style.overflow = 'hidden';
        },

        closeModal: function() {
            this.modalExp = null;
            document.body.style.overflow = '';
        }
    }));
});

// Cerrar modal con ESC
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && window.Alpine) {
        const body = document.querySelector('body[x-data="portfolio"]');
        if (body && Alpine.$data(body).modalExp) {
            Alpine.$data(body).closeModal();
        }
    }
});