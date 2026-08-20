document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('[data-nav-toggle]');
    const navMenu = document.querySelector('[data-nav-menu]');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            const isOpen = navMenu.classList.toggle('is-open');
            navToggle.classList.toggle('is-open', isOpen);
            navToggle.setAttribute('aria-expanded', String(isOpen));
        });
    }

    const accordions = document.querySelectorAll('[data-accordion]');
    accordions.forEach((item) => {
        const trigger = item.querySelector('[data-accordion-trigger]');
        const panel = item.querySelector('[data-accordion-panel]');

        if (!trigger || !panel) {
            return;
        }

        trigger.addEventListener('click', () => {
            const isExpanded = trigger.getAttribute('aria-expanded') === 'true';
            trigger.setAttribute('aria-expanded', String(!isExpanded));
            panel.hidden = isExpanded;
            item.classList.toggle('is-open', !isExpanded);
        });
    });

    const revealItems = document.querySelectorAll('[data-reveal]');
    if (revealItems.length) {
        const revealObserver = new IntersectionObserver(
            (entries, observer) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.2 }
        );

        revealItems.forEach((item) => revealObserver.observe(item));
    }

    const counters = document.querySelectorAll('[data-counter]');
    if (counters.length) {
        const animateCount = (element) => {
            const targetValue = Number(element.dataset.counter || 0);
            const suffix = element.dataset.suffix || '';
            const startTime = performance.now();
            const duration = 1200;

            const step = (now) => {
                const progress = Math.min((now - startTime) / duration, 1);
                const value = Math.floor(progress * targetValue);
                element.textContent = `${value}${suffix}`;

                if (progress < 1) {
                    requestAnimationFrame(step);
                }
            };

            requestAnimationFrame(step);
        };

        const counterObserver = new IntersectionObserver(
            (entries, observer) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        animateCount(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.4 }
        );

        counters.forEach((counter) => counterObserver.observe(counter));
    }

    const filterGroups = document.querySelectorAll('[data-filter-group]');
    filterGroups.forEach((group) => {
        const targetSelector = group.dataset.filterTarget;
        if (!targetSelector) {
            return;
        }

        const target = document.querySelector(targetSelector);
        if (!target) {
            return;
        }

        const items = Array.from(target.querySelectorAll('[data-filter-item]'));
        const buttons = Array.from(group.querySelectorAll('[data-filter]'));
        if (!items.length || !buttons.length) {
            return;
        }

        group.addEventListener('click', (event) => {
            const button = event.target.closest('[data-filter]');
            if (!button) {
                return;
            }

            buttons.forEach((btn) => {
                btn.classList.remove('active');
                btn.setAttribute('aria-pressed', 'false');
            });

            button.classList.add('active');
            button.setAttribute('aria-pressed', 'true');

            const filter = button.dataset.filter;
            items.forEach((item) => {
                const categories = (item.dataset.category || '').split(' ');
                const isVisible = filter === 'all' || categories.includes(filter);
                item.style.display = isVisible ? '' : 'none';
            });
        });
    });
});
