$(document).ready(function(){
	$("code").map(function(){
        //alert('b'+ $(this).html() + 'e');
        //pattern = /^\$(.*)\$$/m
		//match = pattern.exec($(this).html());
		//if (match){
        inner_html = $(this).html();
        if(inner_html[0] == '$$' && inner_html.slice(-1) == '$$' && inner_html.length > 4){
			$(this).replaceWith("<span class=hpl_mathjax_display>" + $(this).html() + "</span>");
			MathJax.Hub.Queue(["Typeset",MathJax.Hub,$(this).get(0)]);
            return;
		}
        if(inner_html[0] == '$' && inner_html.slice(-1) == '$' && inner_html.length > 2){
			$(this).replaceWith("<span class=hpl_mathjax_inline>" + $(this).html() + "</span>");
			MathJax.Hub.Queue(["Typeset",MathJax.Hub,$(this).get(0)]);
            return;
		}
	});
});
