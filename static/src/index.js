$("#content p").delay(1000).animate({ "opacity": "1" }, 700);


$('document').ready(function(){
    $( "textarea" ).each(function(){
        $(this).addClass('editable')
    })
    let editor = new MediumEditor('.editable');
    $('#conteudo').each(function(){
        $(this).html($(this).text())
    })
})