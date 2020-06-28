const text_to_html = (element) =>{
    $(element).each(function(){
        $(this).html($(this).text())
    })
}

async function activateMediumEditor(){
    let editor = await new MediumEditor('.editable');
}

$("#content p").delay(1000).animate({ "opacity": "1" }, 700);
$('document').ready(function(){
    $( "textarea" ).each(function(){
        $(this).addClass('editable')
    })
    activateMediumEditor()
    text_to_html('#conteudo')
    text_to_html('.html-inside')
})