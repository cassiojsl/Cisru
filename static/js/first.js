$(document).ready(function() {
    $("#campo_data").mask("00/00/0000");

    //$(document).off('.datepicker.data-api');
    var minDate = new Date();
    $('#datepicker_folga, #datepicker_plantao_extra').datepicker({
        showOn: "button",
        // buttonImage: "{% static '../imgs/calendario.jpg'%}",
        // buttonImageOnly: true,
        // buttonText: "Clique para abrir o calendário",
        showOptions: { direction: "down" },
        showAnim: 'drop',
        // minDate: minDate,
        showOtherMonths: true,
        dateFormat: 'dd/mm/yy',
        dayNamesMin: ['D', 'S', 'T', 'Q', 'Q', 'S', 'S', 'D'],
        dayNamesShort: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
        dayNames: ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
        monthNamesShort: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
        monthNames: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        dateFormat: 'dd/mm/yy',
        nextText: 'Próximo',
        prevText: 'Anterior',
        changeMonth: false,
        // changeYear: true,
        showWeek: 'Sem',
        firstDay: 1
    });

});