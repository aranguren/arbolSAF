/* fetch("/static/assets/db/arbolsaf_especies.json")
    .then (response => {
        return response.json();
    })
    .then (
        especies => console.log(especies)

        // $('.dataTable-table tbody')
    ); */

/* $.ajax({
    url: "/static/assets/db/arbolsaf_especies.json",
    dataType: "json",
    success: function(data) {
        console.log(data);
        data_species = data;
        createTable(data_species);
    }
}); */

let data_species,
    species_selected = [],
    currentMode     = 'maderable',   // modo activo actual
    lastDataMode    = 'maderable',   // último modo con datos completos (≠ preliminar)
    portafolio_data = null,          // cache de todas las especies para el portafolio
    portafolio_rendered = false;     // para renderizar sólo una vez

// ── Carga de especies habilitadas para la herramienta ────────────
$.ajax({
    url: "/arbolsaf/especie/listado/json/",
    type: "GET",
    dataType: "json",
    success: function(data) {
        $('#step1-loading').hide();
        $('#step1-table-wrap').show();
        console.log('GET DATA', data);
        data_species = data;
        createTable(data_species, 'maderable');   // auto-carga Maderable
    }
});

// ── Pre-fetch de todas las especies para el portafolio ───────────
$.ajax({
    url: "/arbolsaf/especie/listado/json/?todos=1",
    type: "GET",
    dataType: "json",
    success: function(data) {
        portafolio_data = data;
        // Si el panel portafolio ya está visible, renderizarlo ahora
        if ($('#panel-portafolio').hasClass('js-active')) {
            renderPortafolio();
        }
    }
});

// ── Función para construir tarjeta del portafolio ────────────────
function buildCatCard(sp) {
    function v(x) { return (x !== null && x !== undefined && x !== '') ? x : '—'; }
    var code   = sp['CODIGO'];
    var cid    = 'cat-card-' + code;
    var search = ((sp['NOMBRE COMUN'] || '') + ' ' + (sp['NOMBRE CIENTIFICO'] || '')).toLowerCase();

    var imgHtml = (sp.imagenes && sp.imagenes.length > 0)
        ? '<img src="' + sp.imagenes[0] + '" alt="">'
        : '<img src="/static/assets/img/icon-tree.svg" alt="árbol" style="width:100%;height:100%;object-fit:contain;">';

    var cats = '';
    if ((sp['VALOR MADERA'] || 0) > 1) cats += '<span class="cat-badge cat-b-maderable">Maderable</span>';
    if ((sp['VALOR FRUTA']  || 0) > 0) cats += '<span class="cat-badge cat-b-fruta">Frutal</span>';
    if ((sp['VALOR SUELO']  || 0) > 1) cats += '<span class="cat-badge cat-b-suelo">Suelo</span>';
    // if ((sp['VALOR MICROCLIMA']    || 0) > 0) cats += '<span class="cat-badge cat-b-microclima">Microclima</span>';
    if ((sp['VALOR BIODIVERSIDAD'] || 0) > 0) cats += '<span class="cat-badge cat-b-biodiv">Biodiversidad</span>';
    if ((sp['VALOR OTROS USOS']    || 0) > 0) cats += '<span class="cat-badge cat-b-otros">Otros usos</span>';

    var threatParts = [];
    if ((sp.v175_amenaza_peru    || '').trim()) threatParts.push(sp.v175_amenaza_peru.trim());
    if ((sp.v56_amenaza_iucn     || '').trim()) threatParts.push(sp.v56_amenaza_iucn.trim());
    if ((sp.v59_amenaza_nacional || '').trim()) threatParts.push(sp.v59_amenaza_nacional.trim());
    var amenaza = threatParts.length ? threatParts.join(' / ') : '—';

    return (
        '<div class="species-cat-card" id="' + cid + '" data-search="' + search + '">' +
        '<div class="cat-header">' +
            '<div class="cat-icon">' + imgHtml + '</div>' +
            '<div class="cat-names">' +
                '<div class="cat-common">' + v(sp['NOMBRE COMUN']) + '</div>' +
                '<div class="cat-sci"><em>' + v(sp['NOMBRE CIENTIFICO']) + '</em></div>' +
            '</div>' +
        '</div>' +
        '<div class="cat-body">' +
            (cats ? '<div class="cat-cats">' + cats + '</div>' : '') +
            '<table class="cat-info-table">' +
                '<tr><td>Nativa/Endémica de Perú</td><td>' + (sp.nativa ? 'Sí' : 'No') + '/' + (sp.v64_endemismo ? 'Sí' : 'No') +'</td></tr>' +
                '<tr><td>Categoría amenaza</td><td>' + amenaza + '</td></tr>' +
            '</table>' +
        '</div>' +
        '<div class="cat-footer">' +
            '<span class="cat-ivim-label">IVIM</span>' +
            '<span class="cat-ivim-val">' + (sp['IVIM'] !== undefined ? sp['IVIM'] : '—') + '</span>' +
        '</div>' +
        '</div>'
    );
}

// ── Renderizar portafolio en su panel ────────────────────────────
function renderPortafolio() {
    if (!portafolio_data) return;   // aún cargando
    if (portafolio_rendered) return; // ya renderizado

    portafolio_rendered = true;
    $('#portafolio-loading').hide();
    var grid = $('#portafolio-grid');
    grid.empty();
    portafolio_data.forEach(function(sp) { grid.append(buildCatCard(sp)); });
    var n = portafolio_data.length;
    $('#portafolio-count').text(n + ' especie' + (n !== 1 ? 's' : '') + ' encontrada' + (n !== 1 ? 's' : ''));

    // Búsqueda cliente en portafolio
    $('#portafolio-search').off('input').on('input', function() {
        var q       = this.value.toLowerCase().trim();
        var cards   = document.querySelectorAll('#portafolio-grid .species-cat-card');
        var noRes   = document.getElementById('portafolio-no-results');
        var counter = document.getElementById('portafolio-count');
        var visible = 0;
        cards.forEach(function(card) {
            var match = !q || card.dataset.search.indexOf(q) !== -1;
            card.style.display = match ? '' : 'none';
            if (match) visible++;
        });
        counter.textContent = visible + ' especie' + (visible !== 1 ? 's' : '') + ' encontrada' + (visible !== 1 ? 's' : '');
        if (noRes) {
            noRes.style.display = (q && visible === 0) ? '' : 'none';
            var st = document.getElementById('portafolio-search-term');
            if (st) st.textContent = q;
        }
    });
}

var target = document.querySelector('#species-list tbody');
// var target = document.querySelector('.multisteps-form__panel');


// Crea una instancia de observer
var observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation['addedNodes'].length === 0) {
            checkRemoveSpecies();            
        }
    });
});

// Configura el observer:
var config = { attributes: false, childList: true, characterData: false };

// pasa al observer el nodo y la configuracion
observer.observe(target, config);

// Posteriormente, puede detener la observacion
// observer.disconnect();


// La barra de nav es siempre visible — la navegación es únicamente por tab

/* $(document).on('click', '.js-btn-step-bar', function () {
    let idPanelActive =  $('.multisteps-form__panel.js-active').prop("id");
    console.log('idPanelActive', idPanelActive);

    if (idPanelActive === "step-0") {
        $('.multisteps-form__progress').parent().parent().css('display', 'none');
    }
    else {
        console.log('ya no estoy en step0');
        $('.multisteps-form__progress').parent().parent().css('display', 'flex');
    }
}); */



// ── Círculo gris sin valor (sub-usos booleanos: sí/no) ───────────
function boolDot(value, type) {
    if (type === 'display') {
        return value
            ? '<span class="cat-circle cat-circle--filled"></span>'
            : '<span class="cat-circle cat-circle--empty"></span>';
    }
    return value ? 1 : 0;
}

// ── Nombre común con tooltip de nombre científico ─────────────────
function renderNombreComun(value, type, row) {
    if (type !== 'display') return value || '';
    var sci = row['NOMBRE CIENTIFICO'] || '';
    return '<span data-bs-toggle="tooltip" data-bs-placement="top" title="' + sci + '" style="cursor:default;">' + (value || '') + '</span>';
}

// ── Círculo sí/no basado en presencia de término en texto ─────────
function textContainsDot(terms) {
    return function(value, type) {
        if (type === 'display') {
            var txt = (value || '').toLowerCase();
            var match = terms.some(function(t) { return txt.indexOf(t.toLowerCase()) !== -1; });
            return match
                ? '<span class="cat-circle cat-circle--filled"></span>'
                : '<span class="cat-circle cat-circle--empty"></span>';
        }
        var txt = (value || '').toLowerCase();
        return terms.some(function(t) { return txt.indexOf(t.toLowerCase()) !== -1; }) ? 1 : 0;
    };
}

var renderFertilidad = textContainsDot(['fertilidad del suelo', 'recuperacion de suelo', 'recuperación de suelo']);
var renderSequia     = textContainsDot(['sequia', 'sequía']);

// ── Tipo de follaje (v37) — display tal cual, sort por ranking ─────
// Para que la flechita ordene caducifolio > semicaducifolio > perennifolio,
// devolvemos un puntaje numérico cuando DataTables pide 'sort'/'type'.
function renderFollaje(value, type) {
    if (type === 'display') return value || '—';
    var txt = (value || '').toLowerCase();
    if (txt.indexOf('semicaducifolio') !== -1) return 1;
    if (txt.indexOf('caducifolio')     !== -1) return 2;
    if (txt.indexOf('perennifolio')    !== -1) return 0;
    return -1;  // vacío al final
}

// ── Círculo gris con valor (lista preliminar) ─────────────────────
// Valor numérico sin adorno: 1 decimal o '—' si es cero/nulo
function valuePlain(value, type) {
    if (type !== 'display') return parseFloat(value) || 0;
    var n = parseFloat(value);
    return isNaN(n) || n === 0 ? '—' : n.toFixed(1);
}

function valueDot(value, type) {
    if (type === 'display') {
        var n = parseFloat(value);
        return n > 0
            ? '<span class="cat-circle cat-circle--filled">' + n.toFixed(1) + '</span>'
            : '<span class="cat-circle cat-circle--empty"></span>';
    }
    // Para sort/filter/type devolver la magnitud real (no 0/1) para que
    // DataTables ordene 3 > 2 > 1 > 0 correctamente.
    var n = parseFloat(value);
    return isNaN(n) ? 0 : n;
}

// ── Ícono de imagen para DataTable (modo Lista preliminar) ────────
function renderImgDT(imgs, type, row) {
    if (type !== 'display') return '';
    if (!imgs || imgs.length === 0) {
        return '<i class="fas fa-eye-slash text-secondary" style="font-size:15px;"></i>';
    }
    return '<i class="fas fa-eye text-secondary cursor-pointer dt-eye" style="font-size:15px;" data-code="' + row['CODIGO'] + '"></i>';
}

// ── Ícono de papelera para deseleccionar en Lista preliminar ──────
function renderTrash(code, type) {
    if (type === 'display') {
        return '<div class="d-flex justify-content-center">' +
               '<i class="fas fa-trash text-secondary cursor-pointer dt-trash" style="font-size:15px;" data-code="' + code + '"></i>' +
               '</div>';
    }
    return code;
}

// ── Función para renderizar checkbox de selección ─────────────────
function renderCheckbox(code, type) {
    if (type === 'display') {
        return '<div class="d-flex align-items-center justify-content-center">' +
                   '<div class="form-check">' +
                       '<input ' + inputSelected(code) + ' class="form-check-input" type="checkbox" value="' + code + '" onclick="selectSpecies(this)">' +
                   '</div>' +
               '</div>';
    }
    return code;
}

// ── Definición de columnas por modo ──────────────────────────────
var MODES = {
    maderable: {
        valueField: 'VALOR MADERA',
        cols: [
            { title: 'Especie',              data: 'NOMBRE COMUN', render: renderNombreComun },
            { title: 'Construcción',         data: 'v163_madera_construccion', render: boolDot },
            { title: 'Muebles',              data: 'v167_madera_muebles',      render: boolDot },
            { title: 'Postes/<br>cajonería', data: 'v168_madera_postes',       render: boolDot },
            { title: 'Valor<br>madera',      data: 'VALOR MADERA',         render: valuePlain },
            { title: 'Seleccione',           data: 'CODIGO',                   render: renderCheckbox, orderable: false },
        ]
    },
    frutales: {
        valueField: 'VALOR FRUTA',
        cols: [
            { title: 'Especie',         data: 'NOMBRE COMUN', render: renderNombreComun },
            { title: 'Fruta',           data: 'v23_frutas_consumo_humano', render: boolDot },
            { title: 'Semilla',         data: 'v130_semilla_consumo', render: boolDot },
            { title: 'Valor<br>fruta',  data: 'VALOR FRUTA',           render: valuePlain },
            { title: 'Seleccione',      data: 'CODIGO',              render: renderCheckbox, orderable: false },
        ]
    },
    biodiversidad: {
        valueField: 'VALOR BIODIVERSIDAD',
        cols: [
            { title: 'Especie',                  data: 'NOMBRE COMUN', render: renderNombreComun },
            { title: 'Abejas',                   data: 'v18_abejas',              render: boolDot },
            { title: 'Aves',                     data: 'v89_aves',                render: boolDot },
            { title: 'Mamíferos<br>pequeños',    data: 'v90_micromamiferos',      render: boolDot },
            { title: 'Mamíferos<br>mayores',     data: 'v176_mamiferos_mayores',  render: boolDot },
            { title: 'Murciélagos',              data: 'v91_murcielagos',         render: boolDot },
            { title: 'Primates',                 data: 'v177_primates',           render: boolDot },
            { title: 'Amenaza/<br>protección',   data: 'v56_amenaza_iucn',        render: withRefs(['v56','v59'], renderAmenazaCombinada) },
            { title: 'Valor<br>biodiversidad',   data: 'VALOR BIODIVERSIDAD',  render: valuePlain },
            { title: 'Seleccione',               data: 'CODIGO',                  render: renderCheckbox, orderable: false },
        ]
    },
    otrosusos: {
        valueField: 'VALOR OTROS USOS',
        cols: [
            { title: 'Especie',                  data: 'NOMBRE COMUN', render: renderNombreComun },
            { title: 'Artesanías',               data: 'v111_artesanias',render: boolDot },
            { title: 'Carbón',                   data: 'v142_carbon',    render: boolDot },
            { title: 'Cosméticos/<br>repelente', data: 'v112_cosmeticos',render: boolDot },
            { title: 'Fibra',                    data: 'v70_fibra',      render: boolDot },
            { title: 'Forraje<br>ganado',        data: 'v39_forraje',    render: boolDot },
            { title: 'Leña',                     data: 'v162_lena',      render: boolDot },
            { title: 'Medicinal',                data: 'v113_medicinal', render: boolDot },
            { title: 'Tintes/<br>pigmentos',     data: 'v102_tintes',    render: boolDot },
            { title: 'Valor<br>otros usos',      data: 'VALOR OTROS USOS',     render: valuePlain },
            { title: 'Seleccione',               data: 'CODIGO',         render: renderCheckbox, orderable: false },
        ]
    },
    suelo: {
        valueField: 'VALOR SUELO',
        cols: [
            { title: 'Especie',                               data: 'NOMBRE COMUN', render: renderNombreComun },
            { title: 'Aporta fertilidad/<br>recuperación',    data: 'v95_fertilidad',             render: renderFertilidad },
            { title: 'Asociación con<br>microorganismos',     data: 'v115_microorganismos' },
            { title: 'Mejora la<br>estructura',               data: 'v116_mejora_estructura', render: boolDot },
            { title: 'Presencia<br>de nódulos',               data: 'v171_nodulos',           render: boolDot },
            { title: 'Tipo de<br>follaje',                    data: 'v37_fenologia_hojas',         render: renderFollaje },
            { title: 'Tolera<br>sequía',                      data: 'v161_tolerancia_condiciones', render: renderSequia },
            { title: 'Valor<br>suelo',                        data: 'VALOR SUELO',         render: valuePlain },
            { title: 'Seleccione',                            data: 'CODIGO',                 render: renderCheckbox, orderable: false },
        ]
    },
    preliminar: {
        cols: [
            { title: 'Nombre común',      data: 'NOMBRE COMUN', render: renderNombreComun },
            { title: 'Nombre científico', data: 'NOMBRE CIENTIFICO',
              render: function(d, t) { return t === 'display' ? '<em>' + d + '</em>' : d; } },
            { title: 'Imágenes',          data: 'imagenes',             render: renderImgDT,  orderable: false },
            { title: 'Madera',            data: 'VALOR MADERA',         render: valueDot },
            { title: 'Fruta',             data: 'VALOR FRUTA',          render: valueDot },
            { title: 'Biodiversidad',     data: 'VALOR BIODIVERSIDAD',  render: valueDot },
            { title: 'Suelo',             data: 'VALOR SUELO',          render: valueDot },
            { title: 'Otros usos',        data: 'VALOR OTROS USOS',     render: valueDot },
            { title: '<span data-bs-toggle="tooltip" data-bs-placement="top" title="Índice de Valor de Importancia Multifuncional" style="cursor:help;border-bottom:1px dotted rgba(255,255,255,0.5);color:inherit !important;">IVIM</span>',
              data: 'IVIM',
              render: function(v, t) { if (t !== 'display') return parseFloat(v) || 0; var n = parseFloat(v); return isNaN(n) ? '—' : n.toFixed(1); } },
            { title: 'Deseleccionar',     data: 'CODIGO',               render: renderTrash,  orderable: false },
        ]
    }
};



function createTable(data, mode) {
    mode = mode || currentMode;
    currentMode = mode;

    // Actualizar botón activo
    $('.btn-category').removeClass('btn-category-active');
    $('.btn-category[data-mode="' + mode + '"]').addClass('btn-category-active');

    // Determinar columnas y datos según el modo
    var colDefs, tableData;

    if (mode === 'preliminar') {
        colDefs   = MODES.preliminar.cols;
        tableData = data.filter(function(s) {
            return species_selected.some(function(sel) { return sel['CODIGO'] === s['CODIGO']; });
        });
    } else {
        colDefs      = MODES[mode].cols;
        var vf       = MODES[mode].valueField;
        tableData    = vf ? data.filter(function(s) { return (s[vf] || 0) > 0; }) : data;
        lastDataMode = mode;
    }

    // Destruir DataTable existente
    if ($.fn.DataTable.isDataTable('#species-list')) {
        $('#species-list').DataTable().destroy();
    }

    // Limpiar tbody (fix error tn/18: columnas no coinciden)
    $('#species-list tbody').empty();

    // Reconstruir encabezados
    var theadHtml = '<tr>';
    colDefs.forEach(function(col) {
        theadHtml += '<th class="text-lg">' + col.title + '</th>';
    });
    theadHtml += '</tr>';
    $('#species-list thead').html(theadHtml);

    // Aplicar color de cabecera según modo y altura automática en preliminar
    $('#species-list')
        .removeClass('table-mode-maderable table-mode-frutales table-mode-biodiversidad table-mode-suelo table-mode-otrosusos table-mode-preliminar')
        .addClass('table-mode-' + mode);
    if (mode === 'preliminar') {
        $('#table-card').addClass('table-card--preliminar');
    } else {
        $('#table-card').removeClass('table-card--preliminar');
    }

    // Inicializar DataTable con nuevas columnas
    $('#species-list').DataTable({
        data: tableData,
        lengthChange: false,
        pageLength: 10,
        deferRender: true,
        autoWidth: false,
        columns: colDefs.map(function(col) {
            var def = { data: col.data };
            if (col.render)    def.render    = col.render;
            if (col.orderable === false) def.orderable = false;
            return def;
        }),
        language: {
            "info":           "Mostrando _START_ a _END_ de _TOTAL_ entradas",
            "infoEmpty":      "Mostrando 0 a 0 de 0 entradas",
            "search":         "Buscar:",
            "zeroRecords":    "No se encontraron registros coincidentes",
            "loadingRecords": "Cargando...",
            "emptyTable":     "No hay datos disponibles",
            "paginate": {
                "first":      "Primero",
                "last":       "Último",
                "next":       "Próximo",
                "previous":   "Anterior"
            },
        },
        drawCallback: function() {
            initRefTooltips();
            this.api().columns().header().each(function(th) {
                $(th).find('[data-bs-toggle="tooltip"]').each(function() {
                    if (!bootstrap.Tooltip.getInstance(this)) {
                        new bootstrap.Tooltip(this, { trigger: 'hover', boundary: 'window' });
                    }
                });
            });
        }
    });
}

// ── Cambio de modo al hacer clic en pestaña de categoría ─────────
$(document).on('click', '.btn-category', function() {
    if ($(this).is(':disabled')) return;
    if (!data_species) return;
    createTable(data_species, $(this).data('mode'));
});

// ── Paso 4 — Síntesis ecológica ──────────────────────────────────
var _chartMainCats   = null;
var _chartOtrosUsos  = null;
var _chartFaunaGrups = null;

function renderSintesis() {
    var sp = species_selected;
    var n  = sp.length;

    var emptyMsg = document.getElementById('sint-empty-msg');
    var content  = document.getElementById('sint-content');
    if (emptyMsg) emptyMsg.style.display = n === 0 ? '' : 'none';
    if (content)  content.style.display  = n === 0 ? 'none' : '';

    // ── a) Estadísticas de composición ────────────────────────────
    var nativas   = sp.filter(function(s) { return s.nativa; }).length;
    var endemicas = sp.filter(function(s) { return s.v64_endemismo; }).length;
    var amenaza   = sp.filter(function(s) {
        return (s.v56_amenaza_iucn     || '').trim() ||
               (s.v59_amenaza_nacional || '').trim() ||
               (s.v175_amenaza_peru    || '').trim();
    }).length;
    var ivimVals = sp.map(function(s) { return parseFloat(s['IVIM']); })
                     .filter(function(v) { return !isNaN(v); });
    var ivimAvg  = ivimVals.length
        ? (ivimVals.reduce(function(a, b) { return a + b; }, 0) / ivimVals.length).toFixed(1)
        : '—';

    document.getElementById('sint-n-especies').textContent = n;
    document.getElementById('sint-nativas').textContent    = nativas;
    document.getElementById('sint-endemicas').textContent  = endemicas;
    document.getElementById('sint-amenaza').textContent    = amenaza;
    document.getElementById('sint-ivim').textContent       = ivimAvg;

    if (n === 0) return;

    // ── b) Gráficos de servicios y productos ──────────────────────
    function pct(count) { return n ? Math.round(count / n * 100) : 0; }

    // Gráfico izquierdo — categorías principales
    var mainLabels = ['Maderables', 'Frutales', 'Suelos', 'Biodiversidad'];
    var mainData   = [
        pct(sp.filter(function(s) { return (s['VALOR MADERA']        || 0) > 1; }).length),
        pct(sp.filter(function(s) { return (s['VALOR FRUTA']         || 0) > 0; }).length),
        pct(sp.filter(function(s) { return (s['VALOR SUELO']         || 0) > 0; }).length),
        pct(sp.filter(function(s) { return (s['VALOR BIODIVERSIDAD'] || 0) > 0; }).length),
    ];
    var mainColors = ['#85604b', '#806377', '#aa4207', '#00a44d'];

    if (_chartMainCats) _chartMainCats.destroy();
    _chartMainCats = new Chart(document.getElementById('chart-main-cats'), {
        type: 'bar',
        data: {
            labels: mainLabels,
            datasets: [{
                data: mainData,
                backgroundColor: mainColors,
                borderRadius: 4,
                barThickness: 28,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(ctx) { return ' ' + ctx.parsed.x + '%'; }
                    }
                }
            },
            scales: {
                x: {
                    min: 0, max: 100,
                    ticks: { callback: function(v) { return v + '%'; }, stepSize: 25 },
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                y: { grid: { display: false } }
            }
        }
    });

    // Gráfico derecho — otros usos
    var otrosLabels = ['Artesanías', 'Carbón', 'Cosméticos', 'Fibra', 'Forraje', 'Leña', 'Medicinal', 'Tintes'];
    var otrosData   = [
        pct(sp.filter(function(s) { return s.v111_artesanias;  }).length),
        pct(sp.filter(function(s) { return s.v142_carbon;      }).length),
        pct(sp.filter(function(s) { return s.v112_cosmeticos;  }).length),
        pct(sp.filter(function(s) { return s.v70_fibra;        }).length),
        pct(sp.filter(function(s) { return s.v39_forraje;      }).length),
        pct(sp.filter(function(s) { return s.v162_lena;        }).length),
        pct(sp.filter(function(s) { return s.v113_medicinal;   }).length),
        pct(sp.filter(function(s) { return s.v102_tintes;      }).length),
    ];

    if (_chartOtrosUsos) _chartOtrosUsos.destroy();
    _chartOtrosUsos = new Chart(document.getElementById('chart-otros-usos'), {
        type: 'bar',
        data: {
            labels: otrosLabels,
            datasets: [{
                data: otrosData,
                backgroundColor: '#c8a951',
                borderRadius: 4,
                barThickness: 18,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(ctx) { return ' ' + ctx.parsed.x + '%'; }
                    }
                }
            },
            scales: {
                x: {
                    min: 0, max: 100,
                    ticks: { callback: function(v) { return v + '%'; }, stepSize: 25 },
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                y: { grid: { display: false } }
            }
        }
    });

    // ── c) Fauna y polinizadores ──────────────────────────────────
    renderFauna(sp);
}

function renderFauna(sp) {
    // — Grupos de fauna: gráfico de pastel —
    var faunaGroups = [
        { label: 'Abejas',         short: 'Abejas',      key: 'v18_abejas'            },
        { label: 'Aves',           short: 'Aves',         key: 'v89_aves'              },
        { label: 'Mamífero pequeños',  short: 'Mamífero\npequeños',key: 'v90_micromamiferos'    },
        { label: 'Mamífero mayores',  short: 'Mamífero\nmayores',key: 'v176_mamiferos_mayores'},
        { label: 'Murciélagos',    short: 'Murciélagos', key: 'v91_murcielagos'       },
        { label: 'Primates',       short: 'Primates',    key: 'v177_primates'         },
    ];

    var GREEN_PRESENT = '#21ac8d';
    var GRAY_ABSENT   = '#d8d8d8';

    var labels = faunaGroups.map(function(g) { return g.label; });
    var colors = faunaGroups.map(function(g) {
        return sp.some(function(s) { return s[g.key]; }) ? GREEN_PRESENT : GRAY_ABSENT;
    });

    // Plugin inline para dibujar labels dentro de cada segmento
    var sliceLabelPlugin = {
        id: 'sliceLabels',
        afterDraw: function(chart) {
            var ctx = chart.ctx;
            var meta = chart.getDatasetMeta(0);
            meta.data.forEach(function(arc, i) {
                var midAngle = (arc.startAngle + arc.endAngle) / 2;
                var r = arc.outerRadius * 0.65;
                var x = arc.x + Math.cos(midAngle) * r;
                var y = arc.y + Math.sin(midAngle) * r;
                var lines = faunaGroups[i].short.split('\n');
                var lineH = 11;
                ctx.save();
                ctx.fillStyle = colors[i] === GRAY_ABSENT ? '#666' : '#fff';
                ctx.font = 'bold 12px sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                var startY = y - ((lines.length - 1) * lineH) / 2;
                lines.forEach(function(line, li) {
                    ctx.fillText(line, x, startY + li * lineH);
                });
                ctx.restore();
            });
        }
    };

    if (_chartFaunaGrups) _chartFaunaGrups.destroy();
    _chartFaunaGrups = new Chart(document.getElementById('chart-fauna-groups'), {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: [1, 1, 1, 1, 1, 1],
                backgroundColor: colors,
                borderColor: '#fff',
                borderWidth: 2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(ctx) {
                            var present = colors[ctx.dataIndex] === GREEN_PRESENT;
                            return ' ' + ctx.label + ': ' + (present ? 'Presente' : 'No detectado');
                        }
                    }
                }
            }
        },
        plugins: [sliceLabelPlugin]
    });

    // — Polinizadores (v14) — grid de 12 imágenes —
    var polinizadores = [
        { label: 'Abejas',      key: 'abejas',      img: '/static/assets/img/fauna/abeja.png'      },
        { label: 'Abejorros',   key: 'abejorros',   img: '/static/assets/img/fauna/abejorro.png'   },
        { label: 'Avispas',     key: 'avispas',     img: '/static/assets/img/fauna/avispa.png'     },
        { label: 'Chinches',    key: 'chinches',    img: '/static/assets/img/fauna/chinche.png'    },
        { label: 'Colibríes',   key: 'colibries',   img: '/static/assets/img/fauna/colibri.png'    },
        { label: 'Escarabajos', key: 'escarabajos', img: '/static/assets/img/fauna/escarabajo.png' },
        { label: 'Gorgojos',    key: 'gorgojos',    img: '/static/assets/img/fauna/gorgojo.png'    },
        { label: 'Hormigas',    key: 'hormigas',    img: '/static/assets/img/fauna/hormiga.png'    },
        { label: 'Mariposas',   key: 'mariposas',   img: '/static/assets/img/fauna/mariposa.png'   },
        { label: 'Moscas',      key: 'moscas',      img: '/static/assets/img/fauna/mosca.png'      },
        { label: 'Murciélagos', key: 'murcielagos', img: '/static/assets/img/fauna/murcielago.png' },
        { label: 'Polillas',    key: 'polillas',    img: '/static/assets/img/fauna/polilla.png'    },
    ];

    var polEl = document.getElementById('sint-polinizadores-grid');
    if (!polEl) return;

    // Normalizador: lowercase + strip acentos (NFD). En la BD las opciones de v14
    // están sin acentos ('colibries', 'murcielagos'), pero antes el JS comparaba
    // con tilde ('colibríes', 'murciélagos') y nunca matcheaban.
    function _norm(s) {
        return (s || '').toString().toLowerCase()
            .normalize('NFD').replace(/[̀-ͯ]/g, '')
            .trim();
    }

    // Build set of all pollinator keys present in selected species
    var presentKeys = {};
    sp.forEach(function(s) {
        var arr = s.v14_polinizadores || [];
        arr.forEach(function(val) { presentKeys[_norm(val)] = true; });
    });

    var polHtml = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.65rem;">';
    polinizadores.forEach(function(p) {
        var present = presentKeys[p.key];
        var opacity = present ? '1' : '0.2';
        var border  = present ? '2px solid #21ac8d' : '2px solid transparent';
        var bg      = present ? '#e8f7f3' : '#f5f5f5';
        polHtml +=
            '<div style="display:flex;flex-direction:column;align-items:center;gap:0.3rem;' +
            'padding:0.45rem;border-radius:10px;background:' + bg + ';border:' + border + ';opacity:' + opacity + ';">' +
            '<img src="' + p.img + '" alt="' + p.label + '" style="width:60px;height:60px;object-fit:contain;">' +
            '<span style="font-size:0.75rem;text-align:center;color:#333;font-weight:' + (present ? '700' : '400') + ';line-height:1.2;">' + p.label + '</span>' +
            '</div>';
    });
    polHtml += '</div>';
    polEl.innerHTML = polHtml;
}

// Activa renderSintesis() cada vez que step-4 se hace visible
(function() {
    var el = document.getElementById('step-4');
    if (!el) return;
    new MutationObserver(function(mutations) {
        mutations.forEach(function(m) {
            if (m.attributeName === 'class' && el.classList.contains('js-active')) {
                renderSintesis();
            }
        });
    }).observe(el, { attributes: true });
})();

// ── Step-2: Clima / Suelo ─────────────────────────────────────────
var currentCSMode   = 'clima';

// ── Step-3: Forma / Ecología ─────────────────────────────────────
var currentMorfoMode = 'forma';

function renderMinMax(minKey, maxKey) {
    return function(data, type, row) {
        var lo = row[minKey] !== '' && row[minKey] !== null && row[minKey] !== undefined ? row[minKey] : null;
        var hi = row[maxKey] !== '' && row[maxKey] !== null && row[maxKey] !== undefined ? row[maxKey] : null;
        if (type !== 'display') {
            // Ordenar numéricamente por el valor mínimo (vacíos al final)
            if (lo !== null) return parseFloat(lo);
            if (hi !== null) return parseFloat(hi);
            return 1e9;
        }
        if (!lo && !hi) return '—';
        return (lo || '—') + ' – ' + (hi || '—');
    };
}

function renderRaw(minKey, maxKey) {
    return function(data, type, row) {
        var lo = row[minKey] !== '' && row[minKey] !== null && row[minKey] !== undefined ? row[minKey] : null;
        var hi = row[maxKey] !== '' && row[maxKey] !== null && row[maxKey] !== undefined ? row[maxKey] : null;
        if (type !== 'display') {
            if (lo !== null) return parseFloat(lo);
            if (hi !== null) return parseFloat(hi);
            return 1e9;
        }
        if (!lo && !hi) return '—';
        if (String(lo) === String(hi)) return lo;
        return (lo || '—') + ' – ' + (hi || '—');
    };
}

function semField(semType) {
    return { clima: 'SEMAFORO_PASO_2', suelo: 'SEMAFORO_PASO_3', forma: 'SEMAFORO_PASO_4', ecologia: 'SEMAFORO_PASO_5' }[semType] || 'SEMAFORO_PASO_2';
}

function renderSemDot(semType) {
    return function(data, type, row) {
        if (type !== 'display') return '';
        var field = semField(semType);
        var stored = species_selected.find(function(s) { return s['CODIGO'] === row['CODIGO']; });
        var val = stored ? (stored[field] || '') : '';
        var gOn = val === 'active_green';
        var rOn = val === 'active_red';
        var code = row['CODIGO'];
        var dot = 'width:20px;height:20px;border-radius:50%;cursor:pointer;display:inline-block;border:2px solid;transition:opacity .15s,box-shadow .15s;';
        return '<div style="display:flex;gap:10px;justify-content:center;align-items:center;">' +
            '<span class="cs-light" data-code="' + code + '" data-type="' + semType + '" data-color="green" data-active="' + gOn + '" onclick="toggleCSLight(this)" ' +
                'style="' + dot + 'background:#00a44d;border-color:#00a44d;opacity:' + (gOn ? '1' : '0.22') + ';box-shadow:' + (gOn ? '0 0 7px rgba(0,164,77,.65)' : 'none') + ';"></span>' +
            '<span class="cs-light" data-code="' + code + '" data-type="' + semType + '" data-color="red"   data-active="' + rOn + '" onclick="toggleCSLight(this)" ' +
                'style="' + dot + 'background:#ea4a4a;border-color:#ea4a4a;opacity:' + (rOn ? '1' : '0.22') + ';box-shadow:' + (rOn ? '0 0 7px rgba(234,74,74,.65)' : 'none') + ';"></span>' +
        '</div>';
    };
}

function toggleCSLight(btn) {
    var code  = btn.getAttribute('data-code');
    var type  = btn.getAttribute('data-type');
    var color = btn.getAttribute('data-color');
    var field = semField(type);
    var isActive = btn.getAttribute('data-active') === 'true';

    // Reset both lights in this cell
    btn.parentElement.querySelectorAll('.cs-light').forEach(function(b) {
        b.setAttribute('data-active', 'false');
        b.style.opacity = '0.22';
        b.style.boxShadow = 'none';
    });

    var val = '';
    if (!isActive) {
        btn.setAttribute('data-active', 'true');
        btn.style.opacity = '1';
        btn.style.boxShadow = color === 'green'
            ? '0 0 7px rgba(0,164,77,.65)'
            : '0 0 7px rgba(234,74,74,.65)';
        val = color === 'green' ? 'active_green' : 'active_red';
    }

    species_selected.forEach(function(s) {
        if (s['CODIGO'] === code) s[field] = val;
    });
}

// ── Tamaño de copa: combina altura (v1) y ancho (v2) con " / " ──────────
function renderTamanoCopa(data, type, row) {
    if (type !== 'display') return data || '';
    function rngStr(min, max) {
        var lo = (min !== '' && min !== null && min !== undefined) ? parseFloat(min) : null;
        var hi = (max !== '' && max !== null && max !== undefined) ? parseFloat(max) : null;
        if (lo === null && hi === null) return null;
        if (lo !== null && hi !== null && lo === hi) return lo;
        return (lo !== null ? lo : '—') + '–' + (hi !== null ? hi : '—');
    }
    var alt   = rngStr(row['v1_altura_min'], row['v1_altura_max']);
    var ancho = rngStr(row['v2_ancho_min'],  row['v2_ancho_max']);
    if (alt && ancho) return alt + ' / ' + ancho;
    return alt || ancho || '—';
}

// ── Tipo de suelo óptimo: si hay más de 5 clases → "Amplia preferencia" ──
function renderTipoSuelo(data, type) {
    if (!data || data === '') return '—';
    var clases = data.split(',').map(function(s) { return s.trim(); }).filter(Boolean);
    if (clases.length > 5) return 'amplia preferencia';
    return data;
}

function renderAmenazaCombinada(data, type, row) {
    var v56 = (row.v56_amenaza_iucn     || '').trim();
    var v59 = (row.v59_amenaza_nacional || '').trim();

    // Texto combinado v56 / v59 (o '' si ambos están vacíos).
    // Se usa tanto para mostrar como para ordenar — DataTables hará
    // sort alfabético natural sobre este string.
    var parts = [];
    if (v56) parts.push(v56);
    if (v59) parts.push(v59);
    var combined = parts.join(' / ');

    if (type !== 'display') return combined;  // sort/filter/type
    return combined || '—';
}

function renderSINO(data, type) {
    if (type !== 'display') return data;
    if (data === 'SI') return '<span style="color:#00a44d;font-weight:600">Sí</span>';
    if (data === 'NO') return '<span style="color:#ea4a4a;">No</span>';
    return data || '—';
}

var MESES_ES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];
function renderMonths(data, type) {
    if (type !== 'display') return data;
    if (!data || data === '') return '—';
    return data.split(',').map(function(m) {
        var n = parseInt(m.trim(), 10);
        return (n >= 1 && n <= 12) ? MESES_ES[n - 1] : m.trim();
    }).join(', ');
}

function renderNotes(notesKey) {
    return function(code, type) {
        if (type !== 'display') return '';
        var stored = species_selected.find(function(s) { return s['CODIGO'] === code; });
        var note = stored ? (stored[notesKey] || '') : '';
        return '<textarea class="dt-note" data-code="' + code + '" data-field="' + notesKey + '" rows="2" ' +
               'style="width:100%;min-width:120px;font-size:0.73rem;border:1px solid #dee2e6;border-radius:4px;padding:3px 5px;resize:vertical;" ' +
               'onchange="noteDTHandle(this)">' + note + '</textarea>';
    };
}

function noteDTHandle(textarea) {
    var code  = textarea.getAttribute('data-code');
    var field = textarea.getAttribute('data-field');
    species_selected.forEach(function(s) {
        if (s['CODIGO'] === code) { s[field] = textarea.value; }
    });
}

// ── Inicializar Bootstrap tooltips en celdas con fuente ──────────
function initRefTooltips() {
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function(el) {
        if (!bootstrap.Tooltip.getInstance(el)) {
            new bootstrap.Tooltip(el, { trigger: 'hover', boundary: 'window' });
        }
    });
}

// ── Tooltip wrapper — muestra fuente(s) de la variable al hacer hover ──
// refKeys: array de cod_var (ej. ['v101','v100'])
// innerRender: función render original, o null para texto plano
function withRefs(refKeys, innerRender) {
    return function(data, type, row) {
        var val = innerRender ? innerRender(data, type, row) : (data != null && data !== '' ? data : '—');
        if (type !== 'display') return val;
        var parts = [];
        refKeys.forEach(function(k) {
            var r = row.refs && row.refs[k.toLowerCase()];
            if (r && parts.indexOf(r) === -1) parts.push(r);
        });
        if (!parts.length) return val;
        var tip = ('Fuente: ' + parts.join(' / ')).replace(/"/g, '&quot;');
        return '<span data-bs-toggle="tooltip" data-bs-placement="top" title="' + tip + '" style="cursor:help;">' + val + '</span>';
    };
}

var CS_MODES = {
    clima: {
        cols: [
            { title: 'Especie',                              data: 'NOMBRE COMUN', render: renderNombreComun },
            { title: 'Elevación<br>(min–max; m.s.n.m)',      data: 'v157_elevacion_min',    render: withRefs(['v157','v158'], renderMinMax('v157_elevacion_min',   'v158_elevacion_max'))   },
            { title: 'Pluviosidad<br>zona distribución',    data: 'v281_pluviosidad',        render: withRefs(['v281'], null) },
            { title: 'Precipitación<br>(min–max; mm/año)',  data: 'v82_precipitacion_min',   render: withRefs(['v82','v81'],   renderMinMax('v82_precipitacion_min', 'v81_precipitacion_max')) },
            { title: 'Temperatura<br>(min–max; °C)',        data: 'v101_temperatura_min',    render: withRefs(['v101','v100'], renderMinMax('v101_temperatura_min', 'v100_temperatura_max')) },
            { title: 'Tolerancia<br>condiciones<br>extremas', data: 'v161_tolerancia_condiciones', render: withRefs(['v161'], null) },
            { title: 'Semáforo',                             data: 'CODIGO', render: renderSemDot('clima'), orderable: false },
            { title: 'Eliminar',                             data: 'CODIGO', render: renderTrash,           orderable: false },
        ]
    },
    suelo: {
        cols: [
            { title: 'Especie',                               data: 'NOMBRE COMUN', render: renderNombreComun },
            { title: 'Desarrollo en<br>suelos bien drenados', data: 'v153_desarrollo_suelos_drenados', render: withRefs(['v153'], renderSINO) },
            { title: 'Desarrollo en<br>suelos rocosos',       data: 'v152_desarrollo_suelos_rocosos',  render: withRefs(['v152'], renderSINO) },
            { title: 'Exigencia<br>suelos fértiles',          data: 'v68_exigencia_suelos_fertiles',   render: withRefs(['v68'],  null) },
            { title: 'Preferencia<br>pH suelo',               data: 'v83_preferencia_ph_suelo',        render: withRefs(['v83'],  null) },
            { title: 'Tipo de<br>suelo óptimo',               data: 'v106_tipo_suelo_optimo',          render: withRefs(['v106'], renderTipoSuelo) },
            { title: 'Tolerancia<br>acidez del suelo',        data: 'v108_tolerancia_acidez',          render: withRefs(['v108'], renderSINO) },
            { title: 'Semáforo',                     data: 'CODIGO', render: renderSemDot('suelo'), orderable: false },
            { title: 'Eliminar',                     data: 'CODIGO', render: renderTrash,           orderable: false },
        ]
    }
};

var MORFO_MODES = {
    forma: {
        cols: [
            { title: 'Especie',                          data: 'NOMBRE COMUN', render: renderNombreComun },
            { title: 'Follaje de copa',                  data: 'v6_follage',                 render: withRefs(['v6'],       null) },
            { title: 'Forma<br>de copa',                 data: 'v7_forma_copa',              render: withRefs(['v7'],       null) },
            { title: 'Forma<br>de fuste',                data: 'v144_forma_fuste',           render: withRefs(['v144'],     null) },
            { title: 'Frecuencia<br>de poda',            data: 'v9_frecuencia_poda',         render: withRefs(['v9'],       null) },
            { title: 'Tamaño copa<br>(altura / ancho, m)',  data: 'v1_altura_min',              render: withRefs(['v1','v2'],  renderTamanoCopa) },
            { title: 'Tipo<br>ramificación de copa',     data: 'v13_tipo_ramificacion_copa', render: withRefs(['v13'],      null) },
            { title: 'Notas',                            data: 'CODIGO', render: renderNotes('NOTAS_FORMA'), orderable: false },
        ]
    },
    ecologia: {
        cols: [
            { title: 'Especie',                          data: 'NOMBRE COMUN', render: renderNombreComun },
            { title: 'Época de<br>caída de hojas',       data: 'v35_epoca_caida_hojas',        render: withRefs(['v35'],  renderMonths) },
            { title: 'Fenología<br>de las hojas',        data: 'v37_fenologia_hojas',           render: withRefs(['v37'],  null) },
            { title: 'Frecuencia<br>de poda',            data: 'v9_frecuencia_poda',            render: withRefs(['v9'],   null) },
            { title: 'Gremio<br>ecológico',              data: 'v73_gremio_ecologico',          render: withRefs(['v73'],  null) },
            { title: 'Grupo<br>funcional',               data: 'v80_grupo_funcional',           render: withRefs(['v80'],  null) },
            { title: 'Tipo de<br>ramificación de copa',  data: 'v13_tipo_ramificacion_copa',    render: withRefs(['v13'],  null) },
            { title: 'Notas',                            data: 'CODIGO', render: renderNotes('NOTAS_ECOLOGIA'), orderable: false },
        ]
    }
};

function createMorfoTable(mode) {
    mode = mode || currentMorfoMode;
    currentMorfoMode = mode;

    $('#morfo-tabs .btn-category').removeClass('btn-category-active');
    $('#morfo-tabs .btn-category[data-morfomode="' + mode + '"]').addClass('btn-category-active');

    var tableData = data_species ? data_species.filter(function(s) {
        return species_selected.some(function(sel) { return sel['CODIGO'] === s['CODIGO']; });
    }) : [];

    var isEmpty = tableData.length === 0;
    $('#morfo-empty-msg').toggle(isEmpty);
    $('#morfo-table').closest('.table-responsive').toggle(!isEmpty);

    if (isEmpty) {
        if ($.fn.DataTable.isDataTable('#morfo-table')) { $('#morfo-table').DataTable().destroy(); }
        return;
    }

    var colDefs = MORFO_MODES[mode].cols;

    if ($.fn.DataTable.isDataTable('#morfo-table')) { $('#morfo-table').DataTable().destroy(); }
    $('#morfo-table tbody').empty();

    var theadHtml = '<tr>';
    colDefs.forEach(function(col) { theadHtml += '<th class="text-lg">' + col.title + '</th>'; });
    theadHtml += '</tr>';
    $('#morfo-table thead').html(theadHtml);

    $('#morfo-table').removeClass('morfo-mode-forma morfo-mode-ecologia').addClass('morfo-mode-' + mode);

    $('#morfo-table').DataTable({
        data: tableData,
        lengthChange: false,
        pageLength: 10,
        deferRender: true,
        autoWidth: false,
        columns: colDefs.map(function(col) {
            var def = { data: col.data };
            if (col.render)           def.render    = col.render;
            if (col.orderable === false) def.orderable = false;
            return def;
        }),
        language: {
            search: 'Buscar:', info: 'Mostrando _START_ a _END_ de _TOTAL_',
            infoEmpty: 'Sin especies seleccionadas', zeroRecords: 'Sin coincidencias',
            paginate: { next: 'Próximo', previous: 'Anterior' }
        },
        drawCallback: function() { initRefTooltips(); }
    });
}

$(document).on('click', '#morfo-tabs .btn-category', function() {
    if (!data_species) return;
    createMorfoTable($(this).data('morfomode'));
});

function createCSTable(mode) {
    mode = mode || currentCSMode;
    currentCSMode = mode;

    $('#cs-tabs .btn-category').removeClass('btn-category-active');
    $('#cs-tabs .btn-category[data-csmode="' + mode + '"]').addClass('btn-category-active');

    var tableData = data_species ? data_species.filter(function(s) {
        return species_selected.some(function(sel) { return sel['CODIGO'] === s['CODIGO']; });
    }) : [];

    var isEmpty = tableData.length === 0;
    $('#cs-empty-msg').toggle(isEmpty);
    $('#cs-table').closest('.table-responsive').toggle(!isEmpty);

    if (isEmpty) {
        if ($.fn.DataTable.isDataTable('#cs-table')) { $('#cs-table').DataTable().destroy(); }
        return;
    }

    var colDefs = CS_MODES[mode].cols;

    if ($.fn.DataTable.isDataTable('#cs-table')) { $('#cs-table').DataTable().destroy(); }
    $('#cs-table tbody').empty();

    var theadHtml = '<tr>';
    colDefs.forEach(function(col) { theadHtml += '<th class="text-lg">' + col.title + '</th>'; });
    theadHtml += '</tr>';
    $('#cs-table thead').html(theadHtml);

    $('#cs-table').removeClass('cs-mode-clima cs-mode-suelo').addClass('cs-mode-' + mode);

    $('#cs-table').DataTable({
        data: tableData,
        lengthChange: false,
        pageLength: 10,
        deferRender: true,
        autoWidth: false,
        columns: colDefs.map(function(col) {
            var def = { data: col.data };
            if (col.render) def.render = col.render;
            if (col.orderable === false) def.orderable = false;
            return def;
        }),
        language: {
            search: 'Buscar:', info: 'Mostrando _START_ a _END_ de _TOTAL_',
            infoEmpty: 'Sin especies seleccionadas', zeroRecords: 'Sin coincidencias',
            paginate: { next: 'Próximo', previous: 'Anterior' }
        },
        drawCallback: function() { initRefTooltips(); }
    });
}

$(document).on('click', '#cs-tabs .btn-category', function() {
    if (!data_species) return;
    createCSTable($(this).data('csmode'));
});

// ── Deseleccionar especie desde la lista preliminar (papelera) ────
$(document).on('click', '.dt-trash', function() {
    var code = $(this).data('code');
    $('#species-list input[value="' + code + '"]').prop('checked', false);
    var idx = species_selected.findIndex(function(s) { return s['CODIGO'] === code; });
    if (idx > -1) species_selected.splice(idx, 1);
    createCSTable(currentCSMode);
    createMorfoTable(currentMorfoMode);
    createTable(data_species, 'preliminar');
});

// ── Ver imágenes desde la lista preliminar (ojo) ──────────────────
$(document).on('click', '.dt-eye', function() {
    var code = $(this).data('code');
    var specie = data_species.find(function(s) { return s['CODIGO'] === code; });
    if (!specie || !specie.imagenes || specie.imagenes.length === 0) return;
    var id_carrousel = 'carousel' + code;
    $('#modal' + id_carrousel).remove();
    $('body').append(slideCarrousel(specie.imagenes, id_carrousel));
    $('#modal' + id_carrousel).modal('show');
});

function inputSelected(code) {
    // Comprueba si la especie ya está en la lista de seleccionados
    var isSelected = species_selected.some(function(s) { return s['CODIGO'] === code; });
    return isSelected ? 'checked' : '';
}

function selectedColor(val) {
    if (val > 0) {
        return 'background: #8392AB;';
    }
    return "";
}

function slideCarrousel (item, id_carrousel ) {
    let i;
        // id_carrousel = 'carousel' + code;
    
    // console.log('id_carrousel', id_carrousel);

    i =  '<div class="modal fade" id="modal' + id_carrousel + '" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">' +
            '<div class="modal-dialog modal-dialog-centered" style="max-width: 80%; max-height: 80%;" role="document">' +
                '<div class="modal-content">' +
                    '<div class="modal-header">' +
                        '<h5 class="modal-title" id="exampleModalLongTitle"> Imágenes </h5>' +
                        '<button type="button" class="close" data-dismiss="modal" aria-label="Close">' +
                            '<span aria-hidden="true">&times;</span>' +
                        '</button>' +
                    '</div>' +
                    '<div class="modal-body">' + 
                        '<div id="' + id_carrousel + '" class="carousel slide" data-ride="carousel">' +
                            '<ol class="carousel-indicators">'    
    
    $.each(item, function (index, value) {
        if (index === 0) {
            i += '<li data-target="#' + id_carrousel + '" data-slide-to="' + index + '" class="active"></li>'
            // return i;
        } else {
            i += '<li data-target="#' + id_carrousel + '" data-slide-to="' + index + '"></li>'
            // return i;
        }
    }); 

    i += '</ol><div class="carousel-inner">';

    $.each(item, function (index, value) {
        if (index === 0) {
            i += '<div class="carousel-item active" style="height: 60vh;">' +
                    '<img class="d-block w-auto h-100 m-auto" src="' + value + '" alt="First slide">' +
                '</div>'            
        } else {
            i += '<div class="carousel-item" style="height: 60vh;">' +
                    '<img class="d-block w-auto h-100 m-auto" style="margin: auto;" src="' + value + '" alt="First slide">' +
                '</div>'
        }
        // return images;
    });

    i += '</div>';
    i += '<a class="carousel-control-prev" href="#' + id_carrousel + '" role="button" data-slide="prev">' +
            '<span class="carousel-control-prev-icon" aria-hidden="true"></span>' +
            '<span class="sr-only">Previous</span>' +
        '</a>' +
        '<a class="carousel-control-next" href="#' + id_carrousel + '" role="button" data-slide="next">' +
            '<span class="carousel-control-next-icon" aria-hidden="true"></span>' +
            '<span class="sr-only">Next</span>' +
        '</a>';
    i += '</div>' +
            '</div>' +
                '<div class="modal-footer">' +
                    '<button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>' +
                    // <button type="button" class="btn btn-primary">Save changes</button>
                '</div>' +
            '</div>' +
        '</div>';
    return i;
}


function selectSpecies(item) {

    //     $("table#table-species-selected tbody").append(sel_rowtable);

    /* let specie_code =  $(item).val(), sel_rowtable = "";
    let specie_selected = $.grep(data_species, function (item) {
        return item['CODIGO'] === specie_code;            
    })  */



    if( $(item).is(':checked') ) {

        let specie_code = $(item).val(), 
            id_carrousel = 'carousel' + specie_code;
            sel_rowtable = "", 
            cond_rowtable = "";
        let specie_selected = $.grep(data_species, function (i) {
            return i['CODIGO'] === specie_code;            
        })

        sel_rowtable =            
            '<tr id=' + specie_selected[0]['CODIGO'] + '>' + 
                '<td>' + 
                    '<div class="d-flex justify-content-start text-start">' +
                        '<span class="mb-0 text-sm" style="font-weight: 500 !important;">' + specie_selected[0]['NOMBRE COMUN'] + '</span>' +
                        /* '<button type="button" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 ms-2 btn-sm d-flex align-items-center justify-content-center ms-3" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products">' +
                            '<i class="fas fa-info" aria-hidden="true"></i>' +
                          '</button>' + */
                    '</div>' +
                '</td>' +
                '<td>' + 
                    '<div class="d-flex justify-content-start text-start">' +
                        '<span class="mb-0 text-sm font-italic" style="font-weight: 500 !important;">' + specie_selected[0]['NOMBRE CIENTIFICO'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +                        
                        function () {
                            // console.log('id_carrousel >>>>>>>>>>>', id_carrousel);
                            let i;
                            $.isEmptyObject(specie_selected[0]['imagenes'])
                            ?
                            i = '<i class="fas fa-eye-slash text-secondary cursor-pointer" style="font-size: 18px;" id="see_item"></i>'
                            :
                            i = '<span data-toggle="modal" data-target="#modal' + id_carrousel + '">' +
                                    '<i class="fas fa-eye text-secondary cursor-pointer" style="font-size: 18px;" id="see_item"></i>';
                                '</span>'
                            return i;
                        }()
                        +
                        
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span style="opacity:1; cursor:inherit; ' + selectedColor(specie_selected[0]['VALOR MADERA']) + '" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center cursor-inherit" data-bs-placement="bottom" title="">' +   /* selectedColor(specie_selected[0]['VALOR MADERA']) */
                            // specie_selected[0]['VALOR MADERA'] +
                        '</span>' +    
                        
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span style="opacity:1; cursor:inherit; ' + selectedColor(specie_selected[0]['VALOR FRUTA']) + '" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center" data-bs-placement="bottom" title="">' +
                            // specie_selected[0]['VALOR FRUTA'] +
                        '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span style="opacity:1; cursor:inherit; ' + selectedColor(specie_selected[0]['VALOR SUELO']) + '" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center" data-bs-placement="bottom" title="">' +
                            // specie_selected[0]['VALOR SUELO'] +
                        '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span style="opacity:1; cursor:inherit; ' + selectedColor(specie_selected[0]['VALOR BIODIVERSIDAD']) + '" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center" data-bs-placement="bottom" title="">' +
                            // specie_selected[0]['VALOR BIODIVERSIDAD'] +
                        '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span style="opacity:1; cursor:inherit; ' + selectedColor(specie_selected[0]['VALOR OTROS USOS']) + '" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center" data-bs-placement="bottom" title="">' +
                            // specie_selected[0]['VALOR OTROS USOS'] +
                        '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center text-sm font-weight-bold">' +
                        '<span style="font-size: 14px; font-weight: 500 !important;" class="my-2 text-sm">' + Number(specie_selected[0]['IVIM'].toFixed(2)) + '</span>' +
                    '</div>' +
                '</td>' +
                
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<i onclick="removeSpecies(this)" class="fas fa-trash text-secondary cursor-pointer delete_item" style="font-size: 18px;" id="delete_item"></i>' +
                    '</div>' +  
                        slideCarrousel (specie_selected[0]['imagenes'], id_carrousel) +
                    '</div>' +  
                '</td>' +                                  
            '</tr>' 

        // La tabla #table-species-selected fue eliminada; solo se gestiona el array
        species_selected.push(specie_selected[0]);
        species_selected = $.map(species_selected, function (item) {
            item['SEMAFORO_PASO_2']  = item['SEMAFORO_PASO_2']  || "";
            item['SEMAFORO_PASO_3']  = item['SEMAFORO_PASO_3']  || "";
            item['SEMAFORO_PASO_4']  = item['SEMAFORO_PASO_4']  || "";
            item['SEMAFORO_PASO_5']  = item['SEMAFORO_PASO_5']  || "";
            item['NOTAS']            = item['NOTAS']            || "";
            item['NOTAS_CLIMA']      = item['NOTAS_CLIMA']      || "";
            item['NOTAS_SUELO']      = item['NOTAS_SUELO']      || "";
            item['NOTAS_FORMA']      = item['NOTAS_FORMA']      || "";
            item['NOTAS_ECOLOGIA']   = item['NOTAS_ECOLOGIA']   || "";
            return item;
        })
        console.log('species_selected', species_selected);

        createCSTable(currentCSMode);
        createMorfoTable(currentMorfoMode);
    
    } else {
        let specie_code = $(item).val();

        let indexForDelete = species_selected.findIndex(item => item['CODIGO'] === specie_code);
        species_selected.splice(indexForDelete, 1);
        console.log('species_selected_deleted', species_selected);

        createCSTable(currentCSMode);
        createMorfoTable(currentMorfoMode);
    
        // En modo Lista preliminar, refrescar tabla para quitar la especie deseleccionada
        if (currentMode === 'preliminar') {
            createTable(data_species, 'preliminar');
        }
    }
}

// $('#myModal').on('shown.bs.modal', function () {
//     $('#myInput').trigger('focus')
// })

// $('#myModal').modal('toggle')

function checkRemoveSpecies() {
    
    $('#species-list input').prop("checked", false);
    let tb_row = $('#species-list');
    species_selected.forEach((species) => {
        // let CODE = tb_row.find('input[value="' + species['CODIGO'] + '"');
        tb_row.find('input[value="' + species['CODIGO'] + '"').prop("checked", true);
    })
}

function selectLights (item) {
    let child = $(item).clone();
    console.log('SELECTED', $(item).closest('.dropdown').find('.dropbtn'));

    $(item).closest('.dropdown').find('.dropbtn').html(child);    
};

function activeGreen (item) {
    $(item).toggleClass( "active-green" );
    $(item).parent("div").find("#red-light").removeClass( "active-red" );
    let id_item = $(item).closest('tr').attr('id');
    let data_item = $(item).data('code');

    if ($(item).data('code') === 'step_two') {
        $.each( species_selected, function( item, key ) {        
            key.CODIGO === id_item ? key.SEMAFORO_PASO_2 = 'active_green' : "";
        })
    } else if($(item).data('code') === 'step_three') {
        $.each( species_selected, function( item, key ) {        
            key.CODIGO === id_item ? key.SEMAFORO_PASO_3 = 'active_green' : "";
        })
    }
        // ($(item).data('code') === 'step_two') key.CODIGO === id_item ? key.SEMAFORO = 'active_green' : "";
    
    // console.log('species with color ligth', species_selected);
};

function activeRed (item) {
    $(item).toggleClass( "active-red" );
    $(item).parent("div").find("#green-light").removeClass( "active-green" );
    let id_item = $(item).closest('tr').attr('id');

    if ($(item).data('code') === 'step_two') {
        $.each( species_selected, function( item, key ) {        
            key.CODIGO === id_item ? key.SEMAFORO_PASO_2 = 'active_red' : "";
        })
    } else if($(item).data('code') === 'step_three') {
        $.each( species_selected, function( item, key ) {        
            key.CODIGO === id_item ? key.SEMAFORO_PASO_3 = 'active_red' : "";
        })
    }
    // console.log('species with color ligth', species_selected);
};

function noteHandle(item) {
    var code = $(item).data('code');
    var itemVal = $(item).val();
    $.each(species_selected, function(i, s) {
        if (s['CODIGO'] === code) { s['NOTAS'] = itemVal; }
    });
}

/* function selectSpecies() {

    $('input').on( 'change', function() {
        if( $(this).is(':checked') ) {

            let specie_code = $(this).val(),
                sel_rowtable = "";
            let specie_selected = $.grep(data_species, function (item) {
                return item['CODIGO'] === specie_code;            
            })  
            
            sel_rowtable += 
                '<tr id=' + specie_selected[0]['CODIGO'] + '>' + 
                    '<td>' + 
                        '<div class="d-flex px-3 py-1 justify-content-center">' +
                            '<h6 class="mb-0 text-sm">' + specie_selected[0]['NOMBRE COMUN'] + '</h6>' +
                        '</div>' +
                    '</td>' +
                    '<td>' + 
                        '<div class="d-flex px-3 py-1 justify-content-center">' +
                            '<h6 class="mb-0 text-sm">' + specie_selected[0]['NOMBRE CIENTIFICO'] + '</h6>' +
                        '</div>' +
                    '</td>' +
                    '<td>' +
                        '<div class="d-flex px-3 py-1 justify-content-center align-items-center">' +
                            '<span ' + selectedColor(specie_selected[0]['VALOR MADERA']) + ' class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center ms-3" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                        '</div>' +
                    '</td>' +
                    '<td>' +
                        '<div class="d-flex px-3 py-1 justify-content-center align-items-center">' +
                            '<span ' + selectedColor(specie_selected[0]['VALOR FRUTA']) + ' class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center ms-3" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                        '</div>' +
                    '</td>' +
                    '<td>' +
                        '<div class="d-flex px-3 py-1 justify-content-center align-items-center">' +
                            '<span ' + selectedColor(specie_selected[0]['VALOR SUELO']) + ' class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center ms-3" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                        '</div>' +
                    '</td>' +
                    '<td>' +
                        '<div class="d-flex px-3 py-1 justify-content-center align-items-center">' +
                            '<span ' + selectedColor(specie_selected[0]['VALOR BIODIVERSIDAD']) + ' class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center ms-3" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                        '</div>' +
                    '</td>' +
                    '<td>' +
                        '<div class="d-flex px-3 py-1 justify-content-center align-items-center">' +
                            '<span ' + selectedColor(specie_selected[0]['VALOR OTROS USOS']) + ' class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center ms-3" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                        '</div>' +
                    '</td>' +
                    '<td>' +
                        '<div class="d-flex px-3 py-1 justify-content-center align-items-center text-xs font-weight-bold ">' +
                            '<span class="my-2 text-xs">' + specie_selected[0]['IVIM'] + '</span>' +
                        '</div>' +
                    '</td>' +
                    '<td>' +
                        '<div class="d-flex px-3 py-1 justify-content-center align-items-center">' +
                            '<i class="fas fa-trash text-secondary delete_item" style="font-size: 18px;" id="delete_item"></i>' +
                        '</div>' +
                    '</td>' +                    
                '</tr>'

            $("table#table-species-selected tbody").append(sel_rowtable);

            species_selected.push(specie_selected[0]);

            console.log('species_selected', species_selected);


        } else {
            let specie_code = $(this).val();
            $("#" + specie_code).remove();

            let indexForDelete = species_selected.findIndex(item => item['CODIGO'] === specie_code);
            species_selected.splice(indexForDelete, 1);
            console.log('species_selected_deleted', species_selected);
        }

        
    });

    let table_species_selected = $("#table-species-selected")

    table_species_selected.on( "click", 'i[id = "delete_item"]', function() {
        let tr_id = $(this).closest("tr").prop('id');
        $(this).closest("tr").remove();
        $('.table.table-flush input[value=' + tr_id).prop("checked", false);

        let indexForDelete = species_selected.findIndex(item => item['CODIGO'] === tr_id);
        console.log('indexForDelete', indexForDelete);
        species_selected.splice(indexForDelete, 1);

        console.log('species_selected_deleted', species_selected);
    });
} */

let regions = {
    "Loreto": [
        {"Dátem del Maranón": ["Barranca", "Cahuapanas", "Manseriche", "Morona", "Pastaza", "Andoas"]},
        {"Loreto": ["Nauta", "Parinari", "Trompeteros", "Tigre", "Urarinas"]},
        {"Maynas": ["Alto Nanay", "Las Amazonas", "Mazán", "Napo", "Putumayo", "Torres Causana", "Yaquerana"]},
        {"Putumayo": ["Putumayo", "Rosa Panduro", "Yaguas", "Teniente Manuel Clavero"]},
        {"Mariscal Ramón Castilla": ["Ramón Castilla", "Pebas", "Yavarí", "San Pablo"]},
        {"Requena": ["Alto Tapiche", "Capelo", "Emilio San Martin", "Jenaro Herrera", "Maquia", "Puinahua", "Requena", "Saquena", "Soplin", "Tapiche", "Yaquerana"]},
        {"Ucayali": ["Contamana", "Inahuaya", "Padre Marquez", "Pampa Hermosa", "Sarayacu", "Vargas Guerra"]}
    ],
    "Amazonas": [
        {"Condorcanqui": ["El Cenepa", "Nieva", "Río Santiago"]},
        {"Bagua": ["Bagua", "La Peca", "Aramango", "Copallín", "El Parco", "Imaza"]},
        {"Utcubamba": ["Bagua Grande", "Cajaruro", "Cumba", "El Milagro", "Yamón"]}
    ],
    "Cajamarca": [
        {"Jaén": ["Jaén", "Bellavista", "Pucará"]},
        {"San Ignacio": ["Huarango", "Namballe"]}
    ],
    "Ucayali": [
        {"Coronel Portillo": ["Callería", "Campoverde", "Iparía", "Masisea", "Yarinacocha", "Nueva Requena", "Manantay"]},
        {"Padre Abad":	["Padre Abad", "Huipoca", "Boquerón", "Irázola", "Curimaná", "Alexander von Humboldt", "Neshuya"]},
        {"Atalaya":	["Raimondi", "Sepahua", "Tahuanía", "Yurúa"]},
        {"Purús":	["Purús"]}
    ],
    "San Martín": [
        {"San Martín": ["Tarapoto", "Alberto Leveau", "Cacatachi", "Chazuta", "Chipurana", "El Porvenir", "Huimbayoc", "Juan Guerra", "La Banda de Shilcayo", "Morales", "Papaplaya", "San Antonio", "Sauce", "Shapaja"]},
        {"Moyobamba": ["Moyobamba", "Calzada", "Habana", "Jepelacio", "Soritor", "Yantaló"]},
        {"Rioja": ["Awajun", "Elias Soplin Vargas", "Nueva Cajamarca", "Pardo Miguel", "Posic", "Rioja", "San Fernando", "Yorongos", "Yuracyacu"]},
        {"Lamas": ["Alonso de Alvarado", "Barranquita", "Caynarachi", "Cuñumbuqui", "Lamas", "Pinto Recodo", "Rumisapa", "San Roque de Cumbaza", "Shanao", "Tabalosos", "Zapatero"]},
        {"Tocache": ["Nuevo Progreso", "Pólvora", "Shunté", "Tocache", "Uchiza", "Santa Lucía"]},
        {"Bellavista": ["Bellavista", "Alto Biavo", "Bajo Biavo", "Huallaga", "San Pablo", "San Rafael"]},
        {"Mariscal Cáceres": ["Juanjuí", "Pachiza", "Huicungo", "Campanilla", "Pajarillo"]},
        {"Picota": ["Picota", "Buenos Aires", "Caspizapa", "Pilluana", "Pucacaca", "San Cristóbal", "San Hilarión", "Shamboyacu", "Tingo de Ponasa", "Tres Unidos"]},
        {"El Dorado": ["San José de Sisa", "Agua Blanca", "San Martín", "Santa Rosa", "Shatoja"]},
        {"Huallaga": ["Alto Saposoa", "Saposoa", "Piscoyacu", "Eslabón", "Sacanche", "Tingo de Saposoa"]}
    ],
    "Huánuco": [
        {"Leoncio Prado": ["Rupa Rupa", "José Crespo y Castillo", "Mariano Dámaso Beraún", "Padre Felipe Luyando", "Daniel Alomía Robles", "Hermilio Valdizán"]},
        {"Puerto Inca": ["Puerto Inca", "Codo del Pozuzo", "Honoria", "Tournavista", "Yuyapichis"]},
        {"Marañón":	["La Morada"]},
        {"Huamalíes": ["Monzón"]},
    ],
    "Madre de Dios": [
        {"Tambopata": ["Tambopata", "Inambari", "Las Piedras", "Laberinto"]},
        {"Manu": ["Manu", "Fitzcarrald", "Madre de Dios", "Huepetue"]},
        {"Tahuamanu": ["Iñapari", "Iberia", "Tahuamanu"]}
    ]
}

let region_selected, 
    provincia_selected, 
    register_form = {
        "FORM DATA": {
            "NOMBRE" : "",
            "REGION": "",
            "PROVINCIA": "",
            "DISTRITO": "",
            "TIPO DE INTERVENCION": "",
            "TAMANO DE FINCA": "",
            "TAMANO DE PARCELA": "",
            "TIPO DE USUARIO": "",
            "IDENTIDAD DE GENERO": "",
            "EDAD DEL USUARIO": ""
        }
    };
// species_selected.push(register_form);

function handleForm (e) {
    // Object.defineProperty(register_form, "FORM DATA", {value: ""});
    register_form["FORM DATA"][e.name] = e.value;   
    console.log('species_selected >>>>>>>', species_selected);
}

function regionSelected (e) {
    region_selected = e.value;
    let provincia = $("select[name=PROVINCIA]");
    provincia.empty();
    let district = $("select[name=DISTRITO]")
    district.empty();      
    register_form["FORM DATA"][e.name] = region_selected;

    if (region_selected) {
        console.log("region_selected >>>>>>", region_selected);
        provincia.append('<option value=""> -- Seleccione -- </option>');
        
        regions[region_selected].forEach((value, key) => {
            let item = Object.keys(value)[0];
            provincia.append('<option value="' + item + '">' + item + '</option>');
        });
        
    }
    else {
        register_form["FORM DATA"]['PROVINCIA'] = "";
        register_form["FORM DATA"]['DISTRITO'] = "";
    }    
    console.log('species_selected >>>>>>>', species_selected);

}

function provinciaSelected (e) {
    provincia_selected = e.value;
    let district = $("select[name=DISTRITO]");
    district.empty();
    register_form["FORM DATA"][e.name] = provincia_selected;

    if (provincia_selected) {
        district.append('<option value=""> -- Seleccione -- </option>');
    
        let p = regions[region_selected].filter((item) => {
            return item[provincia_selected];
        })
    
        p[0][provincia_selected].forEach((value, key) => {
            // console.log(`${key}: ${value}`);
            district.append('<option value="' + value + '">' + value + '</option>');
        })

    }
    else {
        register_form["FORM DATA"]['DISTRITO'] = "";
    }
    console.log('species_selected >>>>>>>', species_selected);    
}

// ── Reajuste de paneles/tablas al cambiar de pestaña ────────────
$(document).on('click', '#arbol-navtab .arbol-navtab-item', function() {
    var panel = $(this).data('panel');
    if (!panel) return;
    // Pequeño delay para que el panel sea visible antes de ajustar
    setTimeout(function() {
        if (panel === 'panel-portafolio') {
            renderPortafolio();
        }
        if (panel === 'step-1' && $.fn.DataTable.isDataTable('#species-list')) {
            $('#species-list').DataTable().columns.adjust();
        }
        if (panel === 'step-2') {
            createCSTable(currentCSMode);
        }
        if (panel === 'step-3') {
            createMorfoTable(currentMorfoMode);
        }
    }, 50);
});

$(document).ready(function() {

    // Inicializar tooltips en botones de categoría (Maderable → Otros usos)
    initRefTooltips();

    // $( window ).on( "resize", function() {
        /* function myFunction(x) {
            if (x.matches) { // If media query matches
                $(".col-one .circle-arbol").each(function(index) {
                    console.log('THIS', $(this));
                    let rcss =  $(this).css('right');
                    
                    console.log('rcss', rcss);
                    console.log('rcss plus',  parseInt(rcss.replace(/px/,""))+4);

                    $(this).css('right', (parseInt(rcss.replace(/px/,"")) - 50) + "px");
                })

                $(".col-two .circle-arbol").each(function(index) {
                    console.log('THIS', $(this));
                    let rcss =  $(this).css('right');
                    
                    console.log('rcss', rcss);
                    console.log('rcss plus',  parseInt(rcss.replace(/px/,""))+4);

                    $(this).css('right', (parseInt(rcss.replace(/px/,"")) + 50) + "px");
                })


            //   $(".circle-arbol").css('right', parseInt(rcss.replace(/px/,""))+4)+"px";
            } else {
            //   document.body.style.backgroundColor = "pink";
            }
        } */
          
        /* var x = window.matchMedia("(min-width: 1024px)")
        myFunction(x) */
    // } );



    /* $( window ).on( "resize", function() {
        let w = $( "#table-species-selected thead tr th:first-child" ).css('width');
        console.log('w', w);

        $("#table-species-selected thead tr th:nth-child(2)").css('left', parseInt( w, 10 ) + 4 + "px");
    } ); */

    $("body").on( "click", '.options-arbol', function() {        
        let bc = $(this).css("background-color").replace(')', ', 0.3)').replace('rgb', 'rgba');
        $("#table-card").css("background-color", bc);
        let text_sel = $(this).data('products');

        let specie_selected = $.grep(data_species, function (item) {
            let sel = 'VALOR ' + text_sel;
            return item[sel] > 0;            
        }) 

        var datatable = $( "#species-list" ).DataTable();
        datatable.destroy();

        createTable(specie_selected);  
    });   


    $('#form-tool').on('submit', function(e){
        e.preventDefault();

        console.log(species_selected);
        var element = $("form[name='form-herramienta'] input[name='csrfmiddlewaretoken']");
        console.log(element[0]);
        var token = element[0].value
        console.log(token)
        
        $.ajax({
            url: "/arbolsaf/herramienta/pdf/",
            type: "POST",
            headers: {"X-CSRFToken": token},
            data: {
                'especies': JSON.stringify(species_selected),
                "nombre": register_form["FORM DATA"]["NOMBRE"],
                "region": register_form["FORM DATA"]["REGION"],
                "provincia": register_form["FORM DATA"]["PROVINCIA"],
                "distrito": register_form["FORM DATA"]["DISTRITO"],
                "tipo_de_intervencion": register_form["FORM DATA"]["TIPO DE INTERVENCION"],
                "tamano_de_finca": register_form["FORM DATA"]["TAMANO DE FINCA"],
                "tamano_de_parcela": register_form["FORM DATA"]["TAMANO DE PARCELA"],
                "tipo_de_usuario": register_form["FORM DATA"]["TIPO DE USUARIO"],
                "identidad_de_genero": register_form["FORM DATA"]["IDENTIDAD DE GENERO"],
                "edad_del_usuario": register_form["FORM DATA"]["EDAD DEL USUARIO"]
            },
            /* dataType:'json',
            contentType:'application/pdf', */
            
            xhrFields: {
                responseType: 'blob'
            },
            success: function(blob) {
                var link = downloadBlob(blob, "Reporte-ArbolSAF.pdf");
                console.log("generando link con nombre")
                //console.log(blob.size);
                //var link=document.createElement('a');
                //link.href=window.URL.createObjectURL(blob);
                //link.target = "_blank";
                //link.download="Reporte_" + new Date() + ".pdf";
                link.click();
            },
            error: function( jqXHR, textStatus, errorThrown ) {
                console.log('error', errorThrown);
            }
        });
    })

    function downloadBlob(blob, filename) {
        // Create an object URL for the blob object
        const url = URL.createObjectURL(blob);
      
        // Create a new anchor element
        const a = document.createElement('a');
      
        // Set the href and download attributes for the anchor element
        // You can optionally set other attributes like `title`, etc
        // Especially, if the anchor element will be attached to the DOM
        a.href = url;
        a.download = filename || 'download';
        a.target = "_blank"
      
        // Click handler that releases the object URL after the element has been clicked
        // This is required for one-off downloads of the blob content
        const clickHandler = () => {
          setTimeout(() => {
            URL.revokeObjectURL(url);
            removeEventListener('click', clickHandler);
          }, 150);
        };
      
        // Add the click event listener on the anchor element
        // Comment out this line if you don't want a one-off download of the blob content
        a.addEventListener('click', clickHandler, false);
      
        // Programmatically trigger a click on the anchor element
        // Useful if you want the download to happen automatically
        // Without attaching the anchor element to the DOM
        // Comment out this line if you don't want an automatic download of the blob content
        //a.click();
      
        // Return the anchor element
        // Useful if you want a reference to the element
        // in order to attach it to the DOM or use it in some other way
        return a;
      }

    $(document).on("click", "#next-button", function () {
        // $("body").scrollTop();

        $("html, body").animate({ scrollTop: 0 }, "slow");

        console.log("scrooll", $(document).scrollTop());
    });

    $(document).on("click", "#prev-button", function () {
        // $("body").scrollTop();

        $("html, body").animate({ scrollTop: 0 }, "slow");

        console.log("scrooll", $(document).scrollTop());
    });
});