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
        : '<i class="fas fa-tree"></i>';

    var cats = '';
    if ((sp['VALOR MADERA'] || 0) > 1) cats += '<span class="cat-badge cat-b-maderable">Maderable</span>';
    if ((sp['VALOR FRUTA']  || 0) > 0) cats += '<span class="cat-badge cat-b-fruta">Frutal</span>';
    if ((sp['VALOR SUELO']  || 0) > 0) cats += '<span class="cat-badge cat-b-suelo">Suelo</span>';
    if ((sp['VALOR MICROCLIMA']    || 0) > 0) cats += '<span class="cat-badge cat-b-microclima">Microclima</span>';
    if ((sp['VALOR BIODIVERSIDAD'] || 0) > 0) cats += '<span class="cat-badge cat-b-biodiv">Biodiversidad</span>';
    if ((sp['VALOR OTROS USOS']    || 0) > 0) cats += '<span class="cat-badge cat-b-otros">Otros usos</span>';

    var threatParts = [];
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
                '<tr><td>Nativa de Perú</td><td>' + (sp.nativa ? 'Sí' : 'No') + '</td></tr>' +
                '<tr><td>Endemismo para Perú</td><td>' + (sp.v64_endemismo ? 'Sí' : 'No') + '</td></tr>' +
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

// ── Círculo gris con valor (lista preliminar) ─────────────────────
function valueDot(value, type) {
    if (type === 'display') {
        return value > 0
            ? '<span class="cat-circle cat-circle--filled">' + value + '</span>'
            : '<span class="cat-circle cat-circle--empty"></span>';
    }
    return value > 0 ? 1 : 0;
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
        cols: [
            { title: 'Especie',              data: 'NOMBRE COMUN' },
            { title: 'Construcción',         data: 'v163_madera_construccion', render: boolDot },
            { title: 'Muebles',              data: 'v167_madera_muebles',      render: boolDot },
            { title: 'Postes/<br>cajonería', data: 'v168_madera_postes',       render: boolDot },
            { title: 'Valor<br>madera',      data: 'VALOR MADERA' },
            { title: 'Seleccione',           data: 'CODIGO',                   render: renderCheckbox, orderable: false },
        ]
    },
    frutales: {
        cols: [
            { title: 'Especie',         data: 'NOMBRE COMUN' },
            { title: 'Fruta',           data: 'v170_fruta',          render: boolDot },
            { title: 'Semilla',         data: 'v130_semilla_consumo', render: boolDot },
            { title: 'Valor<br>fruta',  data: 'VALOR FRUTA' },
            { title: 'Seleccione',      data: 'CODIGO',              render: renderCheckbox, orderable: false },
        ]
    },
    biodiversidad: {
        cols: [
            { title: 'Especie',                  data: 'NOMBRE COMUN' },
            { title: 'Aves',                     data: 'v89_aves',           render: boolDot },
            { title: 'Mamiferos<br>pequeños',    data: 'v90_micromamiferos', render: boolDot },
            { title: 'Abejas',                   data: 'v18_abejas',         render: boolDot },
            { title: 'Murciélagos',              data: 'v91_murcielagos',    render: boolDot },
            { title: 'Grado<br>amenaza',         data: 'v56_amenaza_iucn' },
            { title: 'Grado<br>protección',      data: 'v59_amenaza_nacional' },
            { title: 'Endemismo',                data: 'v64_endemismo',      render: boolDot },
            { title: 'Valor<br>biodiversidad',   data: 'VALOR BIODIVERSIDAD' },
            { title: 'Seleccione',               data: 'CODIGO',             render: renderCheckbox, orderable: false },
        ]
    },
    otrosusos: {
        cols: [
            { title: 'Especie',                  data: 'NOMBRE COMUN' },
            { title: 'Carbón',                   data: 'v142_carbon',    render: boolDot },
            { title: 'Leña',                     data: 'v162_lena',      render: boolDot },
            { title: 'Forraje<br>ganado',        data: 'v39_forraje',    render: boolDot },
            { title: 'Medicinal',                data: 'v113_medicinal', render: boolDot },
            { title: 'Artesanías',               data: 'v111_artesanias',render: boolDot },
            { title: 'Cosméticos/<br>repelente', data: 'v112_cosmeticos',render: boolDot },
            { title: 'Tintes/<br>pigmentos',     data: 'v102_tintes',    render: boolDot },
            { title: 'Fibra',                    data: 'v70_fibra',      render: boolDot },
            { title: 'Valor<br>otros usos',      data: 'VALOR OTROS USOS' },
            { title: 'Seleccione',               data: 'CODIGO',         render: renderCheckbox, orderable: false },
        ]
    },
    suelo: {
        cols: [
            { title: 'Especie',         data: 'NOMBRE COMUN' },
            { title: 'Valor<br>suelo',  data: 'VALOR SUELO' },
            { title: 'Seleccione',      data: 'CODIGO',       render: renderCheckbox, orderable: false },
        ]
    },
    microclima: {
        cols: [
            { title: 'Especie',              data: 'NOMBRE COMUN' },
            { title: 'Valor<br>microclima',  data: 'VALOR MICROCLIMA' },
            { title: 'Seleccione',           data: 'CODIGO',           render: renderCheckbox, orderable: false },
        ]
    },
    preliminar: {
        cols: [
            { title: 'Nombre común',      data: 'NOMBRE COMUN' },
            { title: 'Nombre científico', data: 'NOMBRE CIENTIFICO',
              render: function(d, t) { return t === 'display' ? '<em>' + d + '</em>' : d; } },
            { title: 'Imágenes',          data: 'imagenes',             render: renderImgDT,  orderable: false },
            { title: 'Madera',            data: 'VALOR MADERA',         render: valueDot },
            { title: 'Fruta',             data: 'VALOR FRUTA',          render: valueDot },
            { title: 'Suelo',             data: 'VALOR SUELO',          render: valueDot },
            { title: 'Microclima',        data: 'VALOR MICROCLIMA',     render: valueDot },
            { title: 'Biodiversidad',     data: 'VALOR BIODIVERSIDAD',  render: valueDot },
            { title: 'Otros usos',        data: 'VALOR OTROS USOS',     render: valueDot },
            { title: 'IVIM',              data: 'IVIM' },
            { title: 'Deseleccionar',     data: 'CODIGO',               render: renderTrash,  orderable: false },
        ]
    }
};

// Las tablas de condiciones y asociaciones fueron reemplazadas por tarjetas (createEvalCard).


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
        tableData    = data;
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

    // Aplicar color de cabecera según modo
    $('#species-list')
        .removeClass('table-mode-maderable table-mode-frutales table-mode-biodiversidad table-mode-suelo table-mode-microclima table-mode-otrosusos table-mode-preliminar')
        .addClass('table-mode-' + mode);

    // Inicializar DataTable con nuevas columnas
    $('#species-list').DataTable({
        data: tableData,
        lengthChange: false,
        pageLength: 8,
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
        }
    });
}

// ── Cambio de modo al hacer clic en pestaña de categoría ─────────
$(document).on('click', '.btn-category', function() {
    if ($(this).is(':disabled')) return;
    if (!data_species) return;
    createTable(data_species, $(this).data('mode'));
});

// ── Step-2: Clima / Suelo ─────────────────────────────────────────
var currentCSMode   = 'clima';

// ── Step-3: Forma / Ecología ─────────────────────────────────────
var currentMorfoMode = 'forma';

function renderMinMax(minKey, maxKey) {
    return function(data, type, row) {
        var lo = row[minKey] !== '' && row[minKey] !== null && row[minKey] !== undefined ? row[minKey] : null;
        var hi = row[maxKey] !== '' && row[maxKey] !== null && row[maxKey] !== undefined ? row[maxKey] : null;
        if (!lo && !hi) return '—';
        return (lo || '—') + ' – ' + (hi || '—');
    };
}

function renderRaw(minKey, maxKey) {
    return function(data, type, row) {
        var lo = row[minKey] !== '' && row[minKey] !== null && row[minKey] !== undefined ? row[minKey] : null;
        var hi = row[maxKey] !== '' && row[maxKey] !== null && row[maxKey] !== undefined ? row[maxKey] : null;
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

var CS_MODES = {
    clima: {
        cols: [
            { title: 'Especie',                              data: 'NOMBRE COMUN' },
            { title: 'Temperatura<br>(min–max; °C)',         data: 'v101_temperatura_min', render: renderMinMax('v101_temperatura_min', 'v100_temperatura_max') },
            { title: 'Elevación<br>(min–max; m.s.n.m)',      data: 'v157_elevacion_min',   render: renderMinMax('v157_elevacion_min',   'v158_elevacion_max')   },
            { title: 'Precipitación<br>(min–max; mm/año)',   data: 'v82_precipitacion_min', render: renderMinMax('v82_precipitacion_min', 'v81_precipitacion_max') },
            { title: 'pH suelo<br>(min–max)',                 data: 'v160_ph_min', render: renderMinMax('v160_ph_min', 'v159_ph_max') },
            { title: 'Pluviosidad<br>zona distribución',    data: 'v281_pluviosidad' },
            { title: 'Tolerancia<br>condiciones<br>extremas', data: 'v161_tolerancia_condiciones' },
            { title: 'Semáforo',                             data: 'CODIGO', render: renderSemDot('clima'), orderable: false },
        ]
    },
    suelo: {
        cols: [
            { title: 'Especie',                      data: 'NOMBRE COMUN' },
            { title: 'Tipo de<br>suelo óptimo',      data: 'v106_tipo_suelo_optimo' },
            { title: 'Exigencia<br>suelos fértiles', data: 'v68_exigencia_suelos_fertiles' },
            { title: 'Preferencia<br>pH suelo',      data: 'v83_preferencia_ph_suelo' },
            { title: 'Desarrollo en<br>suelos bien drenados',      data: 'v153_desarrollo_suelos_drenados', render: renderSINO },
            { title: 'Desarrollo en<br>suelos rocosos',            data: 'v152_desarrollo_suelos_rocosos',  render: renderSINO },
            { title: 'Tolerancia<br>acidez del suelo',         data: 'v108_tolerancia_acidez',          render: renderSINO },
            { title: 'Tolerancia<br>salinidad del suelo',      data: 'v109_tolerancia_salinidad',       render: renderSINO },
            { title: 'Semáforo',                     data: 'CODIGO', render: renderSemDot('suelo'), orderable: false },
        ]
    }
};

var MORFO_MODES = {
    forma: {
        cols: [
            { title: 'Especie',                  data: 'NOMBRE COMUN' },
            { title: 'Altura<br>potencial de copa (m)',   data: 'v1_altura_copa' },
            { title: 'Ancho<br>potencial decopa (m)',         data: 'v2_ancho_potencial_copa' },
            { title: 'Tipo<br>ramificación de copa',      data: 'v13_tipo_ramificacion_copa' },
            { title: 'Forma<br>de copa',          data: 'v7_forma_copa' },
            { title: 'Forma<br>de fuste',         data: 'v144_forma_fuste' },
            { title: 'Follaje de copa',                   data: 'v6_follage' },
            { title: 'Frecuencia<br>de poda',          data: 'v9_frecuencia_poda' },
            { title: 'Semáforo',                  data: 'CODIGO', render: renderSemDot('forma'),      orderable: false },
            { title: 'Notas',                     data: 'CODIGO', render: renderNotes('NOTAS_FORMA'), orderable: false },
        ]
    },
    ecologia: {
        cols: [
            { title: 'Especie',                          data: 'NOMBRE COMUN' },
            { title: 'Gremio<br>ecológico',              data: 'v73_gremio_ecologico' },
            { title: 'Grupo<br>funcional',               data: 'v80_grupo_funcional' },
            { title: 'Fenología<br>de las hojas',            data: 'v37_fenologia_hojas' },
            { title: 'Época de<br>caída de hojas',             data: 'v35_epoca_caida_hojas', render: renderMonths },
            { title: 'Tipo de<br>ramificación de copa',             data: 'v13_tipo_ramificacion_copa' },
            { title: 'Frecuencia<br>de poda',                 data: 'v9_frecuencia_poda' },
            { title: 'Semáforo',                         data: 'CODIGO', render: renderSemDot('ecologia'),      orderable: false },
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
        }
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
            return def;
        }),
        language: {
            search: 'Buscar:', info: 'Mostrando _START_ a _END_ de _TOTAL_',
            infoEmpty: 'Sin especies seleccionadas', zeroRecords: 'Sin coincidencias',
            paginate: { next: 'Próximo', previous: 'Anterior' }
        }
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
    $('#eval-card-' + code).remove();
    updateEvalEmptyMsg();
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
                        '<span style="opacity:1; cursor:inherit; ' + selectedColor(specie_selected[0]['VALOR MICROCLIMA']) + '" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center" data-bs-placement="bottom" title="">' +
                            // specie_selected[0]['VALOR MICROCLIMA'] +
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

        createEvalCard(specie_selected[0]);
        createCSTable(currentCSMode);
        createMorfoTable(currentMorfoMode);
    
    } else {
        let specie_code = $(item).val();

        // Quitar tarjeta de evaluación
        $('#eval-card-' + specie_code).remove();
        updateEvalEmptyMsg();

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

function removeEvalCard(btn) {
    var card = $(btn).closest('.species-eval-card');
    var code = card.data('code');

    $('#species-list input[value="' + code + '"]').prop('checked', false);
    var idx = species_selected.findIndex(function(s) { return s['CODIGO'] === code; });
    if (idx > -1) species_selected.splice(idx, 1);

    card.remove();
    updateEvalEmptyMsg();
    createCSTable(currentCSMode);
    createMorfoTable(currentMorfoMode);

    if (currentMode === 'preliminar') {
        createTable(data_species, 'preliminar');
    }
}

// ── Tarjeta de evaluación por especie (Clima / Suelo / Morfología) ──
function createEvalCard(specie) {
    var code = specie['CODIGO'];

    function v(x) { return (x !== null && x !== undefined && x !== '') ? x : '—'; }
    function rng(a, b, unit) { return v(a) + ' – ' + v(b) + (unit ? ' ' + unit : ''); }

    var html =
        '<div class="species-eval-card" id="eval-card-' + code + '" data-code="' + code + '">' +

        // Header
        '<div class="sec-header">' +
            '<div class="sec-icon"><i class="fas fa-tree"></i></div>' +
            '<div class="sec-names">' +
                '<div class="sec-common">' + v(specie['NOMBRE COMUN']) + '</div>' +
                '<div class="sec-sci"><em>' + v(specie['NOMBRE CIENTIFICO']) + '</em></div>' +
            '</div>' +
            '<div class="sec-semaphores">' +
                '<div class="sec-sem-row">' +
                    '<span class="sec-sem-label">Clima</span>' +
                    '<span class="sec-sem-dot" data-state="none" data-code="' + code + '" data-type="clima" onclick="toggleSemaphore(this)"></span>' +
                '</div>' +
                '<div class="sec-sem-row">' +
                    '<span class="sec-sem-label">Suelo</span>' +
                    '<span class="sec-sem-dot" data-state="none" data-code="' + code + '" data-type="suelo" onclick="toggleSemaphore(this)"></span>' +
                '</div>' +
            '</div>' +
        '</div>' +

        // Tabs
        '<div class="sec-tabs">' +
            '<button type="button" class="sec-tab sec-tab-active" data-card="eval-card-' + code + '" data-panel="clima" onclick="switchCardTab(this)">🌡 CLIMA</button>' +
            '<button type="button" class="sec-tab" data-card="eval-card-' + code + '" data-panel="suelo" onclick="switchCardTab(this)">🌱 SUELO</button>' +
            '<button type="button" class="sec-tab" data-card="eval-card-' + code + '" data-panel="morfologia" onclick="switchCardTab(this)">🌿 MORFOLOGÍA</button>' +
        '</div>' +

        // Panel Clima
        '<div class="sec-panel sec-panel-clima sec-panel-active">' +
            '<table class="sec-data-table">' +
                '<tr><td>Temp. min / max</td><td><strong>' + rng(specie['v101_temperatura_min'], specie['v100_temperatura_max'], '°C') + '</strong></td></tr>' +
                '<tr><td>Elevación</td><td><strong>' + rng(specie['v157_elevacion_min'], specie['v158_elevacion_max'], 'msnm') + '</strong></td></tr>' +
                '<tr><td>Precipitación</td><td><strong>' + rng(specie['v82_precipitacion_min'], specie['v81_precipitacion_max'], 'mm/año') + '</strong></td></tr>' +
                '<tr><td>Tolerancia condiciones</td><td><strong>' + v(specie['v161_tolerancia_condiciones']) + '</strong></td></tr>' +
            '</table>' +
        '</div>' +

        // Panel Suelo
        '<div class="sec-panel sec-panel-suelo">' +
            '<table class="sec-data-table">' +
                '<tr><td>Tipo de suelo óptimo</td><td><strong>' + v(specie['v106_tipo_suelo_optimo']) + '</strong></td></tr>' +
                '<tr><td>Exigencia fertilidad</td><td><strong>' + v(specie['v68_exigencia_suelos_fertiles']) + '</strong></td></tr>' +
                '<tr><td>Tolerancia acidez</td><td><strong>' + v(specie['v108_tolerancia_acidez']) + '</strong></td></tr>' +
                '<tr><td>pH min / max</td><td><strong>' + rng(specie['v160_ph_min'], specie['v159_ph_max'], '') + '</strong></td></tr>' +
                '<tr><td>Drenaje preferido</td><td><strong>' + v(specie['v153_desarrollo_suelos_drenados']) + '</strong></td></tr>' +
            '</table>' +
        '</div>' +

        // Panel Morfología
        '<div class="sec-panel sec-panel-morfologia">' +
            '<table class="sec-data-table">' +
                '<tr><td>Gremio ecológico</td><td><strong>' + v(specie['v73_gremio_ecologico']) + '</strong></td></tr>' +
                '<tr><td>Fenología</td><td><strong>' + v(specie['v37_fenologia_hojas']) + '</strong></td></tr>' +
                '<tr><td>Tipo de raíz</td><td><strong>' + v(specie['v118_tipo_raiz']) + '</strong></td></tr>' +
                '<tr><td>Forma copa</td><td><strong>' + v(specie['v7_forma_copa']) + '</strong></td></tr>' +
                '<tr><td>Densidad copa</td><td><strong>' + v(specie['v4_densidad_promedio_copa']) + '%</strong></td></tr>' +
                '<tr><td>Altura / ancho copa</td><td><strong>' + v(specie['v1_altura_copa']) + ' / ' + v(specie['v2_ancho_potencial_copa']) + ' m</strong></td></tr>' +
            '</table>' +
        '</div>' +

        // Notas
        '<div class="sec-notes-wrap">' +
            '<textarea class="sec-notes" placeholder="Notas para esta especie..." data-code="' + code + '" onchange="noteHandle(this)"></textarea>' +
        '</div>' +

        // Footer
        '<div class="sec-footer">' +
            '<span class="sec-ivim">IVIM: <strong>' + Number(specie['IVIM'].toFixed(2)) + '</strong></span>' +
            '<button type="button" class="sec-remove-btn" onclick="removeEvalCard(this)">✕ Eliminar</button>' +
        '</div>' +

        '</div>';

    $('#eval-cards-grid').append(html);
    updateEvalEmptyMsg();
}

function switchCardTab(btn) {
    var cardId = btn.getAttribute('data-card');
    var panel  = btn.getAttribute('data-panel');
    var card   = document.getElementById(cardId);
    card.querySelectorAll('.sec-tab').forEach(function(t) { t.classList.remove('sec-tab-active'); });
    btn.classList.add('sec-tab-active');
    card.querySelectorAll('.sec-panel').forEach(function(p) { p.classList.remove('sec-panel-active'); });
    card.querySelector('.sec-panel-' + panel).classList.add('sec-panel-active');
}

function toggleSemaphore(dot) {
    var states = ['none', 'green', 'red'];
    var current = dot.getAttribute('data-state') || 'none';
    var next = states[(states.indexOf(current) + 1) % states.length];
    dot.setAttribute('data-state', next);
    var code  = dot.getAttribute('data-code');
    var type  = dot.getAttribute('data-type');
    var field = type === 'clima' ? 'SEMAFORO_PASO_2' : 'SEMAFORO_PASO_3';
    var val   = next === 'green' ? 'active_green' : (next === 'red' ? 'active_red' : '');
    species_selected.forEach(function(s) {
        if (s['CODIGO'] === code) { s[field] = val; }
    });
}

function updateEvalEmptyMsg() {
    var isEmpty = $('#eval-cards-grid').children().length === 0;
    $('#eval-empty-msg').toggle(isEmpty);
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
    var code = $(item).data('code') || $(item).closest('.species-eval-card').data('code');
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
                            '<span ' + selectedColor(specie_selected[0]['VALOR MICROCLIMA']) + ' class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center ms-3" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
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