#!/usr/bin/env python3
"""Part 2: a11y, image attrs, JS behaviours. Run after fix-landing.py."""
P = "index.html"
s = open(P, encoding="utf-8").read()
orig = s


def sub(old, new, count=1, label=""):
    global s
    n = s.count(old)
    assert n == count, f"[{label}] expected {count}, found {n}: {old[:70]!r}"
    s = s.replace(old, new)
    print(f"  ok  {label}")


print("8) modal a11y")
sub('<div id="bookingModal" class="modal-overlay" onclick="closeModalOnOverlay(event)">',
    '<div id="bookingModal" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="bookingModalTitle" onclick="closeModalOnOverlay(event)">',
    1, "booking dialog role")
sub('<button class="modal-close" onclick="closeModal()">✕</button>',
    '<button class="modal-close" onclick="closeModal()" aria-label="Close booking form">✕</button>',
    1, "booking close label")
sub('<h3 style="font-size:1.5rem;">Book Your Appointment</h3>',
    '<h3 id="bookingModalTitle" style="font-size:1.5rem;">Book Your Appointment</h3>',
    1, "booking title id")
sub('<div id="testimonialLightbox" class="modal-overlay" onclick="closeTestimonialLightboxOnOverlay(event)">',
    '<div id="testimonialLightbox" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="lightboxName" onclick="closeTestimonialLightboxOnOverlay(event)">',
    1, "lightbox dialog role")
sub('<button class="mobile-toggle" onclick="toggleMobileNav()" aria-label="Toggle menu">',
    '<button class="mobile-toggle" onclick="toggleMobileNav()" aria-label="Toggle menu" aria-expanded="false" aria-controls="navLinks">',
    1, "mobile toggle aria")
sub("""        html {
            scroll-behavior: smooth;
            font-size: 16px;
        }""",
    """        html {
            scroll-behavior: smooth;
            font-size: 16px;
            scroll-padding-top: 92px;
        }""", 1, "scroll-padding-top")

# tap targets >= 44px on mobile
sub("""            .btn-sm.nav-book-btn {
                width: 32px;
                height: 32px;
                padding: 0.3rem 0.4rem;
            }""",
    """            .btn-sm.nav-book-btn {
                width: 44px;
                height: 44px;
                padding: 0.3rem 0.4rem;
            }""", 1, "nav book tap target")

sub("""        .mobile-toggle {
            display: none;
            background: var(--surface-white);
            border: 2px solid var(--border-dark);
            border-radius: var(--radius-sm);
            padding: 0.4rem 0.5rem;""",
    """        .mobile-toggle {
            display: none;
            background: var(--surface-white);
            border: 2px solid var(--border-dark);
            border-radius: var(--radius-sm);
            min-width: 44px;
            min-height: 44px;
            padding: 0.4rem 0.5rem;""", 1, "hamburger 44px")

print("9) image attrs")
sub('<img id="lightboxImg" src="" alt="" style="display:none;">',
    '<img id="lightboxImg" src="" alt="" decoding="async" style="display:none;">', 1, "lightbox img decoding")
sub('mediaContent = `<img src="${data.media}" alt="${data.name}" style="width:100%;height:100%;object-fit:cover;">`;',
    'mediaContent = `<img src="${data.media}" alt="${data.name} livestream setup" loading="lazy" decoding="async" width="640" height="1330" style="width:100%;height:100%;object-fit:cover;">`;',
    1, "testimonial img lazy+dims")
sub('iconContent = `<img src="${brand.image}" alt="${brand.name} logo">`;',
    'iconContent = `<img src="${brand.image}" alt="${brand.name} logo" loading="lazy" decoding="async" width="96" height="96">`;',
    1, "brand img lazy+dims")
sub('<img src="img-logo/KW-icon.webp" alt="Kotak Wayang Studio Logo" />',
    '<img src="img-logo/KW-icon.webp" alt="Kotak Wayang Studio Logo" width="128" height="128" fetchpriority="high" decoding="async" />',
    1, "nav logo dims")
sub('<img src="img-logo/KW-3D.webp" alt="Kotak Wayang Studio Logo" />',
    '<img src="img-logo/KW-3D.webp" alt="Kotak Wayang Studio Logo" width="160" height="160" loading="lazy" decoding="async" />',
    1, "footer logo dims")
sub('<img src="images-testimoni/C1.webp" alt="Amateur livestream setup before">',
    '<img src="images-testimoni/C1.webp" alt="Amateur livestream setup before" width="640" height="1138" decoding="async" fetchpriority="high">',
    1, "comp C1 dims")
sub('<img src="images-testimoni/C2.webp">',
    '<img src="images-testimoni/C2.webp" alt="Professional Kotak Wayang studio setup after" width="640" height="1138" loading="lazy" decoding="async">',
    1, "comp C2 alt+dims")

print("10) js behaviours")
sub("""        function openModal() {
            document.getElementById('bookingModal').classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeModal() {
            document.getElementById('bookingModal').classList.remove('active');
            document.body.style.overflow = '';
        }""",
    """        let lastFocused = null;

        function trapFocus(container, e) {
            const f = container.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])');
            if (!f.length) return;
            const first = f[0], last = f[f.length - 1];
            if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
            else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
        }

        function openModal() {
            lastFocused = document.activeElement;
            const m = document.getElementById('bookingModal');
            m.classList.add('active');
            document.body.style.overflow = 'hidden';
            setTimeout(() => document.getElementById('fullName').focus(), 60);
        }

        function closeModal() {
            document.getElementById('bookingModal').classList.remove('active');
            document.body.style.overflow = '';
            if (lastFocused) { lastFocused.focus(); lastFocused = null; }
        }""", 1, "modal open/close focus")

sub("""        function toggleMobileNav() {
            const links = document.getElementById('navLinks');
            links.classList.toggle('mobile-open');
        }""",
    """        function toggleMobileNav() {
            const links = document.getElementById('navLinks');
            const open = links.classList.toggle('mobile-open');
            document.querySelector('.mobile-toggle').setAttribute('aria-expanded', String(open));
        }""", 1, "mobile toggle aria state")

sub("""            document.getElementById('testimonialLightbox').classList.add('active');
            document.body.style.overflow = 'hidden';""",
    """            lastFocused = document.activeElement;
            document.getElementById('testimonialLightbox').classList.add('active');
            document.body.style.overflow = 'hidden';
            document.querySelector('#testimonialLightbox .modal-close').focus();""",
    1, "lightbox focus in")

sub("""        function closeTestimonialLightbox() {
            document.getElementById('testimonialLightbox').classList.remove('active');
            document.body.style.overflow = '';
            document.getElementById('lightboxVideo').pause();
        }""",
    """        function closeTestimonialLightbox() {
            document.getElementById('testimonialLightbox').classList.remove('active');
            document.body.style.overflow = '';
            document.getElementById('lightboxVideo').pause();
            if (lastFocused) { lastFocused.focus(); lastFocused = null; }
        }""", 1, "lightbox focus out")

sub("""        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeTestimonialLightbox();
                closeModal();
            }
        });""",
    """        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeTestimonialLightbox();
                closeModal();
                return;
            }
            if (e.key !== 'Tab') return;
            const open = document.querySelector('.modal-overlay.active');
            if (open) trapFocus(open, e);
        });""", 1, "esc + focus trap wiring")

sub("""            } else if (mediaSrc) {
                img.src = mediaSrc;
                img.style.display = 'block';""",
    """            } else if (mediaSrc) {
                img.src = mediaSrc;
                img.alt = name + ' livestream setup';
                img.style.display = 'block';""", 1, "lightbox img alt")

# lightbox media inset so children aren't flush against the border
sub("""        .lightbox-media {
            flex: 0 0 260px;
            max-width: 260px;
            width: 100%;
            aspect-ratio: 9 / 18;""",
    """        .lightbox-media {
            flex: 0 0 260px;
            max-width: 260px;
            width: 100%;
            padding: 10px;
            aspect-ratio: 9 / 18;""", 1, "lightbox media inset")

sub("""        document.addEventListener('DOMContentLoaded', function() {
            initSliders();
        });""",
    """        document.addEventListener('DOMContentLoaded', function() {
            initSliders();
        });

        window.addEventListener('pagehide', () => sliders.forEach(s => s.stop()));""",
    1, "slider cleanup")

open(P, "w", encoding="utf-8").write(s)
print(f"\ndone. {len(orig)} -> {len(s)} bytes")
