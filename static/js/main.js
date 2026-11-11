document.addEventListener('DOMContentLoaded', () => {
    const burger = document.querySelector('.header__burger');
    const nav = document.querySelector('.header__nav');

    if (!burger || !nav) {
        return;
    }

    // Dynamic backdrop overlay
    let backdrop = document.querySelector('.menu-backdrop');
    if (!backdrop) {
        backdrop = document.createElement('div');
        backdrop.className = 'menu-backdrop';
        document.body.appendChild(backdrop);
    }

    const setMenuState = (isOpen) => {
        document.body.classList.toggle('menu-open', isOpen);
        burger.setAttribute('aria-expanded', String(isOpen));
    };

    const toggleMenu = () => {
        const willOpen = !document.body.classList.contains('menu-open');
        setMenuState(willOpen);
    };

    burger.addEventListener('click', (event) => {
        event.stopPropagation();
        toggleMenu();
    });

    backdrop.addEventListener('click', () => {
        setMenuState(false);
    });

    // Close menu when clicking on any navigation link
    nav.querySelectorAll('.header__link').forEach((link) => {
        link.addEventListener('click', () => {
            setMenuState(false);
        });
    });

    // Close menu on Escape key press
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && document.body.classList.contains('menu-open')) {
            setMenuState(false);
        }
    });

    // Automatically close on resize back to desktop width
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768 && document.body.classList.contains('menu-open')) {
            setMenuState(false);
        }
    });
});
