const text_to_html = (element) =>{
    $(element).each(function(){
        $(this).html($(this).text())
    })
}

async function activateMediumEditor(){
    let editor = await new MediumEditor('.editable');
}

const alter_checkbox_form = (element_selector,label_element_selector,new_text) =>{
    if($(element_selector).length == 0){
        return
    }
    let element = $(element_selector)
    element.css('width','auto')
    $(label_element_selector).text(new_text)
    $(label_element_selector).before(element)
}

$("#content p").delay(1000).animate({ "opacity": "1" }, 700);
$('document').ready(function(){
    $( "textarea" ).each(function(){
        $(this).addClass('editable')
    })
    activateMediumEditor()
    text_to_html('#conteudo')
    text_to_html('.html-inside')
    alter_checkbox_form("#id_is_published","label[for='id_is_published']","Publish")
    $('.alert').delay(2000).slideUp(200,function(){
        $(this).alert('close')
    })
})