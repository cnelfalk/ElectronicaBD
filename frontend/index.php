<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechMatch — Comparador Inteligente de Hardware</title>
    <meta name="description" content="Compará laptops, procesadores y componentes con datos reales de fabricantes. TechMatch te ayuda a encontrar el hardware perfecto para tu perfil de uso.">
    <link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">
    <link rel="stylesheet" href="assets/css/style.css?v=<?php echo time(); ?>">
</head>
<body class="index-page">

    <?php include 'componentes/navbar.php'; ?>

    <!-- ═══════════════════════════════════════════════════════ -->
    <!--  HERO                                                   -->
    <!-- ═══════════════════════════════════════════════════════ -->
    <section class="lp-hero">
        <!-- Orbes de fondo decorativos -->
        <div class="lp-orb lp-orb-1"></div>
        <div class="lp-orb lp-orb-2"></div>
        <div class="lp-grid-overlay"></div>

        <div class="lp-hero-inner">
            <div class="lp-hero-badge">
                <span class="lp-badge-dot"></span>
                Datos reales de fabricantes · Actualizado en tiempo real
            </div>

            <h1 class="lp-hero-title">
                El comparador de hardware<br>
                que <span class="lp-gradient-text">realmente importa</span>
            </h1>

            <p class="lp-hero-subtitle">
                Specs extraídas directamente de ASUS, Lenovo, Intel y AMD.
                Sin marketing, sin suposiciones — solo datos duros y precios reales.
            </p>

            <div class="lp-hero-ctas">
                <a href="catalogo.php" class="lp-btn-primary">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                    Explorar Catálogo
                </a>
                <a href="#como-funciona" class="lp-btn-ghost">
                    ¿Cómo funciona?
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
                </a>
            </div>

            <!-- Stats -->
            <div class="lp-hero-stats">
                <div class="lp-stat">
                    <span class="lp-stat-value">5</span>
                    <span class="lp-stat-label">Categorías</span>
                </div>
                <div class="lp-stat-divider"></div>
                <div class="lp-stat">
                    <span class="lp-stat-value">Real</span>
                    <span class="lp-stat-label">Specs de fabricante</span>
                </div>
                <div class="lp-stat-divider"></div>
                <div class="lp-stat">
                    <span class="lp-stat-value">100%</span>
                    <span class="lp-stat-label">Gratis</span>
                </div>
            </div>
        </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════ -->
    <!--  BANDAS DE MARCAS (Social proof visual)                -->
    <!-- ═══════════════════════════════════════════════════════ -->
    <div class="lp-brands-bar">
    <p class="lp-brands-label">Datos extraídos directamente de</p>
    <div class="lp-brands-list">
        <a href="https://www.asus.com/ar/" target="_blank" rel="noopener noreferrer">
            <img src="assets/img/asus-whitelg.png" alt="ASUS" class="lp-brand-logo">
        </a>
        
        <a href="https://www.lenovo.com/ar/es/" target="_blank" rel="noopener noreferrer">
            <img src="assets/img/lenovo-whitelg.png" alt="Lenovo" class="lp-brand-logo">
        </a>
        
        <a href="https://www.intel.la/content/www/xl/es/products/overview.html" target="_blank" rel="noopener noreferrer">
            <img src="assets/img/intel-whitelg.png" alt="Intel" class="lp-brand-logo">
        </a>
        
        <a href="https://www.amd.com/es" target="_blank" rel="noopener noreferrer">
            <img src="assets/img/amd-whitelg.png" alt="AMD" class="lp-brand-logo">
        </a>
        
        <a href="https://www.nvidia.com/es-la/" target="_blank" rel="noopener noreferrer">
            <img src="assets/img/nvidia-whitelg.png" alt="NVIDIA" class="lp-brand-logo">
        </a>
        
        <a href="https://listado.mercadolibre.com.ar/computacion/" target="_blank" rel="noopener noreferrer">
            <img src="assets/img/mercadolibre-whitelg.png" alt="MercadoLibre" class="lp-brand-logo">
        </a>

        <a href="https://www.compragamer.com/" target="_blank" rel="noopener noreferrer">
            <img src="assets/img/compragamer-whitelg.png" alt="CompraGamer" class="lp-brand-logo">
        </a>
    </div>
</div>

    <!-- ═══════════════════════════════════════════════════════ -->
    <!--  CÓMO FUNCIONA                                          -->
    <!-- ═══════════════════════════════════════════════════════ -->
    <section class="lp-section" id="como-funciona">
        <div class="lp-section-inner">
            <div class="lp-section-header">
                <div class="lp-section-tag">Proceso</div>
                <h2 class="lp-section-title">Tres pasos, resultado claro</h2>
                <p class="lp-section-subtitle">Sin curva de aprendizaje. Entrás, comparás y salís con una decisión informada.</p>
            </div>

            <div class="lp-steps">
                <div class="lp-step">
                    <div class="lp-step-head">
                        <div class="lp-step-num">01</div>
                        <div class="lp-step-icon-wrap">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                        </div>
                    </div>
                    <h3>Encontrá los productos</h3>
                    <p>Navegá el catálogo con filtros por categoría, marca o perfil de uso. Cada tarjeta muestra specs reales, sin relleno.</p>
                    <a href="catalogo.php" class="lp-step-link">Ir al catálogo →</a>
                </div>

                <div class="lp-step-connector">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3"><polyline points="9 18 15 12 9 6"/></svg>
                </div>

                <div class="lp-step">
                    <div class="lp-step-head">
                        <div class="lp-step-num">02</div>
                        <div class="lp-step-icon-wrap">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                        </div>
                    </div>
                    <h3>Elegí tu perfil de uso</h3>
                    <p>Gaming, desarrollo, diseño u ofimática. Nuestro algoritmo ajusta el peso de cada spec según lo que realmente necesitás.</p>
                    <a href="comparar.php" class="lp-step-link" onclick="return irACompararDesdeNav(event)">Ir a comparar →</a>
                </div>

                <div class="lp-step-connector">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3"><polyline points="9 18 15 12 9 6"/></svg>
                </div>

                <div class="lp-step">
                    <div class="lp-step-head">
                        <div class="lp-step-num">03</div>
                        <div class="lp-step-icon-wrap">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                        </div>
                    </div>
                    <h3>Obtenés la recomendación</h3>
                    <p>Un ganador claro, con los motivos técnicos explicados en lenguaje simple y links directos a las mejores tiendas.</p>
                    <a href="registro.php" class="lp-step-link" id="stepCta">Crear cuenta →</a>
                </div>
            </div>
        </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════ -->
    <!--  CATEGORÍAS                                             -->
    <!-- ═══════════════════════════════════════════════════════ -->
    <section class="lp-section lp-section-alt">
        <div class="lp-section-inner">
            <div class="lp-section-header">
                <div class="lp-section-tag">Catálogo</div>
                <h2 class="lp-section-title">¿Qué querés comparar?</h2>
                <p class="lp-section-subtitle">Cobertura completa de hardware para cualquier setup.</p>
            </div>

            <div class="lp-cats">
                <a href="catalogo.php?categoria=Laptop" class="lp-cat">
                    <div class="lp-cat-icon">💻</div>
                    <div class="lp-cat-info">
                        <h3>Laptops</h3>
                        <p>ASUS, Lenovo, HP y más</p>
                    </div>
                    <svg class="lp-cat-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
                </a>
                <a href="catalogo.php?categoria=CPU" class="lp-cat">
                    <div class="lp-cat-icon">⚙️</div>
                    <div class="lp-cat-info">
                        <h3>Procesadores</h3>
                        <p>Intel Core & AMD Ryzen</p>
                    </div>
                    <svg class="lp-cat-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
                </a>
                <a href="catalogo.php?categoria=GPU" class="lp-cat">
                    <div class="lp-cat-icon">🎮</div>
                    <div class="lp-cat-info">
                        <h3>Placas de Video</h3>
                        <p>NVIDIA GeForce & AMD Radeon</p>
                    </div>
                    <svg class="lp-cat-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
                </a>
                <a href="catalogo.php?categoria=RAM" class="lp-cat">
                    <div class="lp-cat-icon">🧠</div>
                    <div class="lp-cat-info">
                        <h3>Memoria RAM</h3>
                        <p>DDR4 & DDR5 de alta velocidad</p>
                    </div>
                    <svg class="lp-cat-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
                </a>
                <a href="catalogo.php?categoria=Almacenamiento" class="lp-cat">
                    <div class="lp-cat-icon">💾</div>
                    <div class="lp-cat-info">
                        <h3>Almacenamiento</h3>
                        <p>SSD NVMe, SATA y HDD</p>
                    </div>
                    <svg class="lp-cat-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
                </a>
            </div>
        </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════ -->
    <!--  FEATURE CARDS (por qué TechMatch)                     -->
    <!-- ═══════════════════════════════════════════════════════ -->
    <section class="lp-section">
        <div class="lp-section-inner">
            <div class="lp-section-header">
                <div class="lp-section-tag">Diferencial</div>
                <h2 class="lp-section-title">Sin datos inventados</h2>
                <p class="lp-section-subtitle">Cada spec viene de la fuente oficial. Comparás con información real.</p>
            </div>

            <div class="lp-features">
                <div class="lp-feature-card lp-feature-accent">
                    <div class="lp-feature-icon-box">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                    </div>
                    <h3>Specs de fabricante</h3>
                    <p>Scrapeamos directamente los sitios oficiales de Intel, AMD, ASUS y Lenovo para tener datos 100% verificados.</p>
                </div>
                <div class="lp-feature-card">
                    <div class="lp-feature-icon-box">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/></svg>
                    </div>
                    <h3>Precios en tiempo real</h3>
                    <p>Conectamos con MercadoLibre y retailers locales para mostrarte los mejores precios disponibles hoy.</p>
                </div>
                <div class="lp-feature-card">
                    <div class="lp-feature-icon-box">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                    </div>
                    <h3>Algoritmo por perfil</h3>
                    <p>No es una comparación genérica. Cada perfil de uso pondera las specs que realmente importan para tu actividad.</p>
                </div>
                <div class="lp-feature-card">
                    <div class="lp-feature-icon-box">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
                    </div>
                    <h3>Guardá tus favoritos</h3>
                    <p>Creá tu cuenta gratis y guardá comparaciones, armá listas de favoritos y accedé desde cualquier dispositivo.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════ -->
    <!--  CTA FINAL                                              -->
    <!-- ═══════════════════════════════════════════════════════ -->
    <section class="lp-cta-final">
        <div class="lp-orb lp-orb-cta"></div>
        <div class="lp-cta-final-inner">
            <h2>¿Listo para comparar?</h2>
            <p>Gratis. Sin publicidad. Sin afiliados que distorsionen el resultado.</p>
            <div class="lp-cta-actions">
                <a href="catalogo.php" class="lp-btn-primary">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                    Explorar Catálogo
                </a>
                <a href="registro.php" class="lp-btn-outline" id="ctaRegistroFinal">
                    Crear cuenta gratis
                </a>
            </div>
        </div>
    </section>

    <?php include 'componentes/footer.php'; ?>

    <script src="assets/js/api.js"></script>
    <script>
        // Adaptar CTAs según sesión activa
        if (localStorage.getItem('techmatch_usuario')) {
            const stepCta = document.getElementById('stepCta');
            if (stepCta) { stepCta.href = 'favoritos.php'; stepCta.textContent = 'Mis favoritos →'; }

            const ctaFinal = document.getElementById('ctaRegistroFinal');
            if (ctaFinal) { ctaFinal.href = 'favoritos.php'; ctaFinal.textContent = '❤️ Mis favoritos'; }
        }
    </script>

</body>
</html>
