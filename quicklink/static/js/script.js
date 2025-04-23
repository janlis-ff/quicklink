(function($, bs){

    const FORM = $("#shortenLinkForm");
    const RESULT_INPUT = $("#shortLinkURL");
    const MODAL = new bs.Modal($("#shortLinkModal")[0]);

    function handle_form_submit(){
        FORM.find("button")
            .prop("disabled", true)
            .text("Shortening...");
        let data = {
            url: FORM.find("[name=url]").val(),
            slug: FORM.find("[name=slug]").val() || null,
        };
        $.ajax({
            method: "POST",
            url: "/api/links/",
            data: JSON.stringify(data),
            contentType: "application/json",
            success: (response) => {
                RESULT_INPUT.val(response.short_url);
                FORM.find("input").val("");
                FORM.find("button")
                    .prop("disabled", false)
                    .text("Make it short!");
                MODAL.show();
                confetti({
                    particleCount: 80,
                    scalar: 1.8,
                    shapes: ['star'],
                    spread: 360,
                    ticks: 50,
                    gravity: 0.4,
                    decay: 0.92,
                    startVelocity: 20,
                    colors: ['0d6efd', '1254b5', '0d3b7f', '4b7abf', '7397cd']
                });
            },
            error: (response) => {
                FORM.find("button")
                    .prop("disabled", false)
                    .text("Make it short!");
                if(response.responseJSON){
                    let json = response.responseJSON;
                    if(json.detail){
                        return alert(detail);
                    }else if(json.slug){
                        return alert("Slug: " + json.slug[0]);
                    }else if(json.url){
                        return alert("URL: " + json.url[0]);
                    }
                }
                alert("Unknown error occured.");
                console.error(response);
            },
        });
        
    }

    FORM.on("submit", (e) => {
        e.preventDefault();
        handle_form_submit();
        return true;
    });

    // Handle "copy to clipboard" button 
    $(document).on("click", "#shortLinkCopyBtn", function(){
        let input = $("#shortLinkURL");
        navigator.clipboard.writeText(input[0].value).then(() => {
            $(this).text("Copied!");
            setTimeout(() => {
                $(this).text("⧉");
            }, 1200);
        }).catch(err => {
            console.error(err);
        });
    });

})(jQuery, bootstrap);