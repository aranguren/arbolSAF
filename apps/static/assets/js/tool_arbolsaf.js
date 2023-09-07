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
        $(".spinner-loading").css("visibility", "hidden");
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


$(document).on('click', '.js-btn-step', function () {
    let idPanelActive =  $('.multisteps-form__panel.js-active').prop("id");
    console.log('idPanelActive', idPanelActive);

    if (idPanelActive === "step-0") {
        $('.multisteps-form__progress').parent().parent().css('display', 'none');
    }
    else {
        console.log('ya no estoy en step0');
        $('.multisteps-form__progress').parent().parent().css('display', 'flex');
    }
});

$(document).on('click', '.js-btn-step-bar', function () {
    let idPanelActive =  $('.multisteps-form__panel.js-active').prop("id");
    console.log('idPanelActive', idPanelActive);

    if (idPanelActive === "step-0") {
        $('.multisteps-form__progress').parent().parent().css('display', 'none');
    }
    else {
        console.log('ya no estoy en step0');
        $('.multisteps-form__progress').parent().parent().css('display', 'flex');
    }
});

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

$('#table-species-selected').DataTable({
    lengthChange: false,
    searching: false,
    paging: false,
    columns: [
        { orderable: false },
        { orderable: false },
        { orderable: false },
        { orderable: false },
        { orderable: false },
        { orderable: false },
        { orderable: false },
        { orderable: false },
        { orderable: false },
        { orderable: true },
        { orderable: false },
    ],
    order: [[9, 'desc']],
    language: {
        "emptyTable": "No hay datos disponibles en la tabla",
        "info": "",
        "infoEmpty": "",        
    }
});

$('#table-conditions').DataTable({
    lengthChange: false,
    searching: false,
    paging: false,
    ordering: false,
    language: {
        "emptyTable": "No hay datos disponibles en la tabla",
        "info": "",
        "infoEmpty": "",        
    }
});

$('#table-conditions2').DataTable({
    lengthChange: false,
    searching: false,
    paging: false,
    ordering: false,
    language: {
        "emptyTable": "No hay datos disponibles en la tabla",
        "info": "",
        "infoEmpty": "",        
    }
});

$('#table-asociations').DataTable({
    lengthChange: false,
    searching: false,
    paging: false,
    ordering: false,
    language: {
        "emptyTable": "No hay datos disponibles en la tabla",
        "info": "",
        "infoEmpty": "",        
    }
});


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
        ],
        language: {
            "info":           "Mostrando _START_ to _END_ de _TOTAL_ entradas",
            "infoEmpty":      "Mostrando 0 to 0 of 0 entradas",
            "search":         "Buscar:",
            "zeroRecords":    "No se encontraron registros coincidentes",
            "loadingRecords": "Please wait - loading...",
            "paginate": {
                "first":      "Primero",
                "last":       "Último",
                "next":       "Próximo",
                "previous":   "Anterior"
            },
        }
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

        // $("table#table-species-selected tbody").append(sel_rowtable);

        let table = $('#table-species-selected').DataTable();
        table.row.add($(sel_rowtable)).draw();

        species_selected.push(specie_selected[0]);
        species_selected = $.map(species_selected, function (item) {            
            item['SEMAFORO_PASO_2'] = "";
            item['SEMAFORO_PASO_3'] = "";
            item['NOTAS'] = "";
            return item;                     
        })
        console.log('species_selected', species_selected);

        conditionSpecies(specie_selected[0]);
        conditionSpeciesTwo(specie_selected[0]);
        asociationSpecies(specie_selected[0])

    } else {
        let specie_code = $(item).val();
        
        let tss = $('#table-species-selected').DataTable();
        tss.row($("#" + specie_code)).remove().draw(false);

        let tc = $('#table-conditions').DataTable();
        tc.row($("#" + specie_code)).remove().draw(false);

        let tctwo = $('#table-conditions2').DataTable();
        tctwo.row($("#" + specie_code)).remove().draw(false);

        let ta = $('#table-asociations').DataTable();
        ta.row($("#" + specie_code)).remove().draw(false);                             


        let indexForDelete = species_selected.findIndex(item => item['CODIGO'] === specie_code);
        species_selected.splice(indexForDelete, 1);
        console.log('species_selected_deleted', species_selected);
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

function removeSpecies(item=false) {

    let tr_id = $(item).closest("tr").prop('id');

    /* $("#tbody-species-selected tr[id='" + tr_id + "'").remove();
    $("#tbody-conditions tr[id='" + tr_id + "'").remove();
    $("#tbody-conditions2 tr[id='" + tr_id + "'").remove();
    $("#tbody-asociations tr[id='" + tr_id + "'").remove(); */

    $('#species-list input[value=' + tr_id).prop("checked", false);

    let indexForDelete = species_selected.findIndex(item => item['CODIGO'] === tr_id);
    species_selected.splice(indexForDelete, 1);

    let tss = $('#table-species-selected').DataTable();
    tss.row($("#tbody-species-selected tr[id='" + tr_id + "'")).remove().draw(false);

    let tc = $('#table-conditions').DataTable();
    tc.row($("#tbody-conditions tr[id='" + tr_id + "'")).remove().draw(false);

    let tctwo = $('#table-conditions2').DataTable();
    tctwo.row($("#tbody-conditions2 tr[id='" + tr_id + "'")).remove().draw(false);

    let ta = $('#table-asociations').DataTable();
    ta.row($("#tbody-asociations tr[id='" + tr_id + "'")).remove().draw(false);
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
                        '<span class="mb-0 text-sm cursor-pointer" id="specie_name" style="font-weight: 500 !important;">' + specie['NOMBRE COMUN'] + '<span class="tool-tip font-italic">' + specie['NOMBRE CIENTIFICO'] + '</span> </span>' +                        
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v101_temperatura_min'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v100_temperatura_max'] + '</span>' +
                    '</div>' +
                '</td>' +                
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v157_elevacion_min'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v158_elevacion_max'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v82_precipitacion_min'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v81_precipitacion_max'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v161_tolerancia_condiciones'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center text-xs font-weight-bold ">' +
                        '<div class="w-100 d-flex justify-content-between align-items-center">' +
                            '<div onclick="activeGreen(this)" id="green-light" style="border-radius: 0.5rem; padding: 0.75rem 0.75rem;" data-code="step_two">' +
                                '<span style="background: #00a44d;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center mx-auto" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                            '</div>' +
                            '<div onclick="activeRed(this)" id="red-light" style="border-radius: 0.5rem; padding: 0.75rem 0.75rem;" data-code="step_two">' +
                                '<span style="background: #ea4a4a;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center mx-auto" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                            '</div>' +
                            '<i onclick="removeSpecies(this)" class="fas fa-trash text-secondary cursor-pointer delete_item" style="font-size: 18px;" id="delete_item"></i>' +
                            
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
                        '<span class="mb-0 text-sm cursor-pointer" id="specie_name" style="font-weight: 500 !important;">' + specie['NOMBRE COMUN'] + '<span class="tool-tip font-italic">' + specie['NOMBRE CIENTIFICO'] + '</span> </span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v106_tipo_suelo_optimo'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v68_exigencia_suelos_fertiles'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v108_tolerancia_acidez'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v109_tolerancia_salinidad'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v83_preferencia_ph_suelo'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v160_ph_min'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v159_ph_max'] + '</span>' +
                    '</div>' +
                '</td>' +                
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v152_desarrollo_suelos_rocosos'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v153_desarrollo_suelos_drenados'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center text-xs font-weight-bold ">' +
                        '<div class="w-100 d-flex justify-content-between align-items-center">' +
                            '<div onclick="activeGreen(this)" id="green-light" style="border-radius: 0.5rem; padding: 0.75rem 0.75rem;" data-code="step_three">' +
                                '<span style="background: #00a44d;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center mx-auto" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                            '</div>' +
                            '<div onclick="activeRed(this)" id="red-light" style="border-radius: 0.5rem; padding: 0.75rem 0.75rem;" data-code="step_three">' +
                                '<span style="background: #ea4a4a;" class="btn btn-sm btn-icon-only btn-rounded btn-outline-secondary mb-0 d-flex align-items-center justify-content-center mx-auto" data-bs-toggle="tooltip" data-bs-placement="bottom" title="" data-bs-original-title="Refund rate is lower with 97% than other products"></span>' +
                            '</div>' +
                            '<i onclick="removeSpecies(this)" class="fas fa-trash text-secondary cursor-pointer delete_item" style="font-size: 18px;" id="delete_item"></i>' +
                    
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
                        '<span class="mb-0 text-sm cursor-pointer" id="specie_name" style="font-weight: 500 !important;">' + specie['NOMBRE COMUN'] + '<span class="tool-tip font-italic">' + specie['NOMBRE CIENTIFICO'] + '</span> </span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v73_gremio_ecologico'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v37_fenologia_hojas'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v118_tipo_raiz'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v143_forma_corteza'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v119_capacidad_regeneracion'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v7_forma_copa'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v4_densidad_promedio_copa'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v6_follage'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v1_altura_copa'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v2_ancho_potencial_copa'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<div class="d-flex justify-content-center align-items-center">' +
                        '<span class="text-sm" style="font-weight: 500 !important;">' + specie['v13_tipo_ramificacion_copa'] + '</span>' +
                    '</div>' +
                '</td>' +
                '<td>' +
                    '<input onchange="noteHandle(this)" class="multisteps-form__input form-control" type="text" placeholder="ej. centro" onfocus="focused(this)" onfocusout="defocused(this)">' +
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

function noteHandle (item) {  
    let id_item = $(item).closest('tr').attr('id');
    let item_val = $(item).val();
    console.log('NOTAAAAAAAAAA', $(item).val());
    $.each( species_selected, function( item, key ) {        
        key.CODIGO === id_item ? key.NOTAS = item_val: "";
    })

    console.log('species with note', species_selected);

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



    $( window ).on( "resize", function() {
        let w = $( "#table-species-selected thead tr th:first-child" ).css('width');
        console.log('w', w);

        $("#table-species-selected thead tr th:nth-child(2)").css('left', parseInt( w, 10 ) + 4 + "px");
    } );

    $("body").on( "click", '.circle-arbol, .options-arbol', function() {        
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
                console.log(blob.size);
                var link=document.createElement('a');
                link.href=window.URL.createObjectURL(blob);
                // link.target = "_blank";
                // link.download="PDFname_" + new Date() + ".pdf";
                link.click();
            },
            error: function( jqXHR, textStatus, errorThrown ) {
                console.log('error', errorThrown);
            }
        });
    })

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