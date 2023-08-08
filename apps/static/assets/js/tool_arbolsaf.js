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
    species_selected = [];

$.ajax({
    url: "/arbolsaf/especie/listado/json/",
    type: "GET",
    dataType: "json",
    success: function(data) {
        console.log('GET DATA', data);
        data_species = data;
        createTable(data_species);
    }
});

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


function createTable(data) {

    $('#species-list').DataTable( {
        data: data,
        lengthChange: false,
        pageLength: 8,
        columns: [
            { data: 'NOMBRE COMUN' },
            { data: 'CODIGO',
              render: function (data, type) {
                if (type === 'display') {
                    let rowtable = 
                        '<div class="d-flex align-items-center justify-content-center">' +
                            '<div class="form-check">' +
                                '<input ' + inputSelected(data) + ' class="form-check-input" type="checkbox" id="customCheck1" value=' + data + ' onclick="selectSpecies(this)">' +
                            '</div>' +
                        '</div>';

                    return rowtable;
                } 
                return data;
            }}
        ]
    } );


    /* let rowtable = "";
    data.forEach(especie => {        
        rowtable += 
            '<tr>' +
                '<td class="text-sm text-start font-weight-bold">' +
                    '<span class="my-2 text-sm">' +  especie['NOMBRE COMUN'] + '</span>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex align-items-center justify-content-center">' +
                        '<div class="form-check">' +
                            '<input ' + inputSelected(especie['CODIGO']) + ' class="form-check-input" type="checkbox" id="customCheck1" value=' + especie['CODIGO'] + ' onclick="selectSpecies(this)">' +
                        '</div>' +
                    '</div>' +
                '</td>' +
            '</tr>'
    });
    $(".table.table-flush").append(rowtable); */
}

function inputSelected(code) {
    let check = false;

    // let p = $( "#tbody-species-selected" ).find("tr").each(function (item, value) { 
    let p = $( "#tbody-species-selected tr" ).each(function (item, value) { 
         if ($(this).prop("id") === code) {
            check = true;
            console.log('checked');
        }else {
            console.log('unchecked');
        };
    });
   if (check) return "checked";
}

function selectedColor(val) {
    if (val > 0) {
        return 'style="background: #8392AB;"';
    }
    return "";
}


function selectSpecies(item) {

    //     $("table#table-species-selected tbody").append(sel_rowtable);

    /* let specie_code =  $(item).val(), sel_rowtable = "";
    let specie_selected = $.grep(data_species, function (item) {
        return item['CODIGO'] === specie_code;            
    })  */

    if( $(item).is(':checked') ) {

        let specie_code = $(item).val(), sel_rowtable = "", cond_rowtable = "";
        let specie_selected = $.grep(data_species, function (i) {
            return i['CODIGO'] === specie_code;            
        })

        sel_rowtable +=            
            '<tr id=' + specie_selected[0]['CODIGO'] + '>' + 
                '<td>' + 
                    '<div class="d-flex justify-content-start text-start">' +
                        '<span class="mb-0 text-sm">' + specie_selected[0]['NOMBRE COMUN'] + '</span>' +
                        /* '<button type="button" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 ms-2 btn-sm d-flex align-items-center justify-content-center ms-3" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products">' +
                            '<i class="fas fa-info" aria-hidden="true"></i>' +
                          '</button>' + */
                    '</div>' +
                '</td>' +
                '<td>' + 
                    '<div class="d-flex justify-content-start text-start">' +
                        '<span class="mb-0 text-sm">' + specie_selected[0]['NOMBRE CIENTIFICO'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span style="font-size: 14px;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center ms-3" data-bs-placement="bottom" title="">' +   /* selectedColor(specie_selected[0]['VALOR MADERA']) */
                            specie_selected[0]['VALOR MADERA'] +
                        '</span>' +    
                        
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span style="font-size: 14px;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center ms-3" data-bs-placement="bottom" title="">' +
                            specie_selected[0]['VALOR FRUTA'] +
                        '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span style="font-size: 14px;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center ms-3" data-bs-placement="bottom" title="">' +
                            specie_selected[0]['VALOR SUELO'] +
                        '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span style="font-size: 14px;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center ms-3" data-bs-placement="bottom" title="">' +
                            specie_selected[0]['VALOR MICROCLIMA'] +
                        '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span style="font-size: 14px;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center ms-3" data-bs-placement="bottom" title="">' +
                            specie_selected[0]['VALOR BIODIVERSIDAD'] +
                        '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span style="font-size: 14px;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center ms-3" data-bs-placement="bottom" title="">' +
                            specie_selected[0]['VALOR OTROS USOS'] +
                        '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center text-sm font-weight-bold">' +
                        '<span style="font-size: 14px;" class="my-2 text-sm">' + Number(specie_selected[0]['IVIM'].toFixed(2)) + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<i onclick="removeSpecies(this)" class="fas fa-trash text-secondary delete_item" style="font-size: 18px;" id="delete_item"></i>' +
                    '</div>' +
                '</td>' +                    
            '</tr>' 

        // $("table#table-species-selected tbody").append(sel_rowtable);

        let table = $('#table-species-selected').DataTable();
        table.row.add($(sel_rowtable)).draw();

        species_selected.push(specie_selected[0]);

        conditionSpecies(specie_selected[0]);
        conditionSpeciesTwo(specie_selected[0]);
        asociationSpecies(specie_selected[0])

    } else {
        let specie_code = $(item).val();
        $("#" + specie_code).remove();

        let indexForDelete = species_selected.findIndex(item => item['CODIGO'] === specie_code);
        species_selected.splice(indexForDelete, 1);
        console.log('species_selected_deleted', species_selected);
    }

    let w = $("#table-species-selected th").css('width');
    $("#table-species-selected thead tr th:nth-child(2)").css('left', w);
    $("#table-species-selected tbody tr td:nth-child(2)").css('left', w);
}


function checkRemoveSpecies() {
    
    $('#species-list input').prop("checked", false);
    let tb_row = $('#species-list');
    species_selected.forEach((species) => {
        // let CODE = tb_row.find('input[value="' + species['CODIGO'] + '"');
        tb_row.find('input[value="' + species['CODIGO'] + '"').prop("checked", true);
    })
}

function removeSpecies(item=false) {

    let tr_id = $(item).closest("tr").prop('id');

    /* $("#tbody-species-selected tr[id='" + tr_id + "'").remove();
    $("#tbody-conditions tr[id='" + tr_id + "'").remove();
    $("#tbody-conditions2 tr[id='" + tr_id + "'").remove();
    $("#tbody-asociations tr[id='" + tr_id + "'").remove(); */

    $('#species-list input[value=' + tr_id).prop("checked", false);

    let indexForDelete = species_selected.findIndex(item => item['CODIGO'] === tr_id);
    species_selected.splice(indexForDelete, 1);

    let table = $('#table-species-selected').DataTable();
    table.row($("#tbody-species-selected tr[id='" + tr_id + "'")).remove().draw(false);
    table.row($("#tbody-conditions tr[id='" + tr_id + "'")).remove().draw(false);
    table.row($("#tbody-conditions2 tr[id='" + tr_id + "'")).remove().draw(false);
    table.row($("#tbody-asociations tr[id='" + tr_id + "'")).remove().draw(false);
}

function conditionSpecies(specie) {
    let cond_rowtable = "";
    
    // species_selected.forEach((specie) => {
        cond_rowtable += 
            '<tr id=' + specie['CODIGO'] + '>' + 
                /* '<td>' + 
                    '<div class="d-flex px-3 py-1 justify-content-center">' +
                        '<h6 class="mb-0 text-sm">' + specie_selected[0]['NOMBRE COMUN'] + '</h6>' +
                    '</div>' +
                '</td>' + */
                '<td>' +       /* class="position-relative" */ 
                    '<div class="d-flex justify-content-start text-start">' +
                        '<span class="mb-0 text-sm cursor-pointer" id="specie_name">' + specie['NOMBRE COMUN'] + '<span class="tool-tip">' + specie['NOMBRE CIENTIFICO'] + '</span> </span>' +                        
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v100_temperatura_max'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v101_temperatura_min'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v157_elevacion_min'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v158_elevacion_max'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v81_precipitacion_max'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v82_precipitacion_min'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v161_tolerancia_condiciones'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center text-xs font-weight-bold ">' +
                        '<div class="w-100 d-flex justify-content-between align-items-center">' +
                            '<div onclick="activeGreen(this)" id="green-light" style="border-radius: 0.5rem; padding: 0.75rem;">' +
                                '<span style="background: #00a44d;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center mx-auto" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                            '</div>' +
                            '<div onclick="activeRed(this)" id="red-light" style="border-radius: 0.5rem; padding: 0.75rem;">' +
                                '<span style="background: #ea4a4a;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center mx-auto" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                            '</div>' +
                            '<i onclick="removeSpecies(this)" class="fas fa-trash text-secondary delete_item" style="font-size: 18px;" id="delete_item"></i>' +
                            
                        '</div>' +
                    
                    /* '<div class="dropdown">' +
                            '<button class="dropbtn"><span></span> Seleccione </span></button>' +
                            '<div class="dropdown-content" id="dropdown-content-select">' +
                                '<a onclick="selectLights(this)" href="#">' +
                                    '<span style="background: #00a44d;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center mx-auto" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                                '</a>' +
                                '<a onclick="selectLights(this)" href="#">' +
                                    '<span style="background: #fdc00d;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center mx-auto" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                                '</a>' +
                                '<a onclick="selectLights(this)" href="#">' +
                                    '<span style="background: #f4dc40;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center mx-auto" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                                '</a>' +
                            '</div>'
                       ' </div>'
                    '</div>' + */
                '</td>' +
                /* '<td>' +
                    '<div class="d-flex px-3 py-1 justify-content-center align-items-center">' +
                        '<i class="fas fa-trash text-secondary delete_item" style="font-size: 18px;" id="delete_item"></i>' +
                    '</div>' +
                '</td>' +  */                   
            '</tr>'

    // })
    

    // $("table#table-conditions tbody").append(cond_rowtable);
    let table = $('#table-conditions').DataTable();
    table.row.add($(cond_rowtable)).draw();   
}

function conditionSpeciesTwo(specie) {
    let cond_rowtable = "";
    
    // species_selected.forEach((specie) => {
        cond_rowtable += 
            '<tr id=' + specie['CODIGO'] + '>' + 
                /* '<td>' + 
                    '<div class="d-flex px-3 py-1 justify-content-center">' +
                        '<h6 class="mb-0 text-sm">' + specie_selected[0]['NOMBRE COMUN'] + '</h6>' +
                    '</div>' +
                '</td>' + */
                '<td>' + 
                    '<div class="d-flex justify-content-start text-start">' +
                        '<span class="mb-0 text-sm cursor-pointer" id="specie_name">' + specie['NOMBRE COMUN'] + '<span class="tool-tip">' + specie['NOMBRE CIENTIFICO'] + '</span> </span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v106_tipo_suelo_optimo'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v68_exigencia_suelos_fertiles'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v108_tolerancia_acidez'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v109_tolerancia_salinidad'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v83_preferencia_ph_suelo'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v159_ph_max'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v160_ph_min'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v152_desarrollo_suelos_rocosos'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v153_desarrollo_suelos_drenados'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center text-xs font-weight-bold ">' +
                        '<div class="w-100 d-flex justify-content-between align-items-center">' +
                            '<div onclick="activeGreen(this)" id="green-light" style="border-radius: 0.5rem; padding: 0.75rem;">' +
                                '<span style="background: #00a44d;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center mx-auto" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                            '</div>' +
                            '<div onclick="activeRed(this)" id="red-light" style="border-radius: 0.5rem; padding: 0.75rem;">' +
                                '<span style="background: #ea4a4a;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center mx-auto" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                            '</div>' +
                            '<i onclick="removeSpecies(this)" class="fas fa-trash text-secondary delete_item" style="font-size: 18px;" id="delete_item"></i>' +
                    
                '       </div>' +
                    '</div>' +
                '</td>' +
                /* '<td>' +
                    '<div class="d-flex px-3 py-1 justify-content-center align-items-center">' +
                        '<i class="fas fa-trash text-secondary delete_item" style="font-size: 18px;" id="delete_item"></i>' +
                    '</div>' +
                '</td>' +  */                   
            '</tr>'

    // })
    

    // $("table#table-conditions2 tbody").append(cond_rowtable);
    let table = $('#table-conditions2').DataTable();
    table.row.add($(cond_rowtable)).draw();   
}


function asociationSpecies(specie) {
    let cond_rowtable = "";
    
    // species_selected.forEach((specie) => {
        cond_rowtable += 
            '<tr id=' + specie['CODIGO'] + '>' + 
                /* '<td>' + 
                    '<div class="d-flex px-3 py-1 justify-content-center">' +
                        '<h6 class="mb-0 text-sm">' + specie_selected[0]['NOMBRE COMUN'] + '</h6>' +
                    '</div>' +
                '</td>' + */
                '<td>' + 
                    '<div class="d-flex justify-content-start text-start">' +
                        '<span class="mb-0 text-sm cursor-pointer" id="specie_name">' + specie['NOMBRE COMUN'] + '<span class="tool-tip">' + specie['NOMBRE CIENTIFICO'] + '</span> </span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v73_gremio_ecologico'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v37_fenologia_hojas'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v118_tipo_raiz'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v143_forma_corteza'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v119_capacidad_regeneracion'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v7_forma_copa'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v4_densidad_promedio_copa'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v6_follage'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v1_altura_copa'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v2_ancho_potencial_copa'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="my-2 text-sm">' + specie['v13_tipo_ramificacion_copa'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<input class="multisteps-form__input form-control" type="text" placeholder="ej. centro" onfocus="focused(this)" onfocusout="defocused(this)">' +
                '</td>' +

                /* '<td>' +
                    '<div class="d-flex px-3 py-1 justify-content-center align-items-center text-xs font-weight-bold ">' +
                        '<div class="w-100 d-flex justify-content-between align-items-center">' +
                            '<div onclick="selectLights(this)" >' +
                                '<span style="background: #00a44d;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center mx-auto" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                            '</div>' +
                            '<div onclick="selectLights(this)" >' +
                                '<span style="background: #ea4a4a;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center mx-auto" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                            '</div>' +
                            '<i onclick="removeSpecies(this)" class="fas fa-trash text-secondary delete_item" style="font-size: 18px;" id="delete_item"></i>' +
                    
                        '</div>' +
                    '</div>' +
                '</td>' + */
                /* '<td>' +
                    '<div class="d-flex px-3 py-1 justify-content-center align-items-center">' +
                        '<i class="fas fa-trash text-secondary delete_item" style="font-size: 18px;" id="delete_item"></i>' +
                    '</div>' +
                '</td>' +  */                   
            '</tr>'

    // })
    

    // $("table#table-asociations tbody").append(cond_rowtable);
    let table = $('#table-asociations').DataTable();
    table.row.add($(cond_rowtable)).draw();   
}




function selectLights (item) {
    // console.log('SELECTED', $(item).closest('.dropbtn'));
    let child = $(item).clone();
    console.log('SELECTED', $(item).closest('.dropdown').find('.dropbtn'));

    $(item).closest('.dropdown').find('.dropbtn').html(child);

    
};

function activeGreen (item) {
    $(item).toggleClass( "active-green" );
    // $(".active-red").toggleClass( "active-red" );

    $(item).parent("div").find("#red-light").removeClass( "active-red" );

    console.log('SELECTED', $(item).parent("div").find(".active-red"));

};

function activeRed (item) {
    // console.log('SELECTED', $(item).closest('.dropbtn'));
    $(item).toggleClass( "active-red" );
    // $(".active-green").toggleClass( "active-green" );

    $(item).parent("div").find("#green-light").removeClass( "active-green" );

};



function treeTop() {
    $("#container-treetrunk-asociations").css("visibility", "hidden");
    $("#container-treetop-asociations").css("visibility", "visible");
    console.log('treeTop');
}

function treeTrunk() {
    $("#container-treetrunk-asociations").css("visibility", "visible");
    $("#container-treetop-asociations").css("visibility", "hidden");
    console.log('treeTrunk');

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
species_selected.push(register_form);

function handleForm (e) {
    // Object.defineProperty(register_form, "FORM DATA", {value: ""});
    register_form["FORM DATA"][e.name] = e.value;   
    console.log('species_selected >>>>>>>', species_selected);
}

function regionSelected (e) {
    region_selected = e.value;
    let provincia = $("select[name=PROVINCIA]")
    provincia.empty();

    regions[region_selected].forEach((value, key) => {
        let element = Object.keys(value)[0];
        provincia.append('<option value="' + element + '">' + element + '</option>');
    });

    register_form["FORM DATA"][e.name] = region_selected;
    console.log('species_selected >>>>>>>', species_selected);
}

function provinciaSelected (e) {
    provincia_selected = e.value;
    let district = $("select[name=DISTRITO]")
    district.empty();

    let p = regions[region_selected].filter((item) => {
        return item[provincia_selected];
    })

    p[0][provincia_selected].forEach((value, key) => {
        // console.log(`${key}: ${value}`);
        district.append('<option value="' + value + '">' + value + '</option>');
    })

    register_form["FORM DATA"][e.name] = provincia_selected;
    console.log('species_selected >>>>>>>', species_selected);
}

function sendForm() {
    $.ajax({
        url: "/arbolsaf/herramienta/pdf/",
        type: "GET",
        data: species_selected,
        dataType: "native",
        xhrFields: {
            responseType: 'blob'
        },
        success: function(blob) {
            console.log(blob.size);
            var link=document.createElement('a');
            link.href=window.URL.createObjectURL(blob);
            link.download="PDFname_" + new Date() + ".pdf";
            link.click();
        }
    });
}






$(document).ready(function() {

    let w = $("#table-species-selected th").css('width');
    $("#table-species-selected thead tr th:nth-child(2)").css('left', w);
    $("#table-species-selected tbody tr td:nth-child(2)").css('left', w);
    console.log('w', w);

    $("body").on( "click", '.circle-arbol', function() {
        
        console.log('$(this)', $(this));
        let bc = $(this).css("background-color").replace(')', ', 0.3)').replace('rgb', 'rgba');
        $("#table-card").css("background-color", bc);

        let text_sel = $(this).text().toUpperCase();
        /* $(".dataTable-wrapper").remove();

        let new_table = 
            '<table class="table table-flush" id="datatable-search">' +
                '<thead class="thead-light">' +
                    '<tr>' +
                        '<th> Especies </th>' +
                        '<th> Seleccione </th>' +
                    '</tr>' +
                '</thead>' +
                '<tbody></tbody>' +
            '</table>'
        
        $("#table-card .table-responsive").append(new_table); */

        let specie_selected = $.grep(data_species, function (item) {
            let sel = 'VALOR ' + text_sel;
            return item[sel] > 0;            
        }) 

        var datatable = $( "#species-list" ).DataTable();
        datatable.destroy();
        // datatable.rows.add(newDataArray);
        // datatable.draw();

        createTable(specie_selected);

        $.getScript("/static/assets/js/plugins/datatables.js");

        const dataTableSearch = new simpleDatatables.DataTable("#datatable-search", {
            searchable: true,
            fixedHeight: true,
            perPageSelect: false,
            perPage: 5
            });

        document.querySelectorAll(".export").forEach(function(el) {
            el.addEventListener("click", function(e) {
                var type = el.dataset.type;

                var data = {
                type: type,
                filename: "soft-ui-" + type,
                };

                if (type === "csv") {
                data.columnDelimiter = "|";
                }

                dataTableSearch.export(data);
            });
        });


        
    
    });   
});