$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        const csrfToken = $('meta[name="csrf-token"]').attr('content');
        if (!(/^GET|HEAD|OPTIONS|TRACE$/i.test(settings.type))) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        }
    }
});


(function($, bs){

    const FORM = $("#shortenLinkForm");
    const RESULT_INPUT = $("#shortLinkURL");
    const MODAL = new bs.Modal($("#shortLinkModal")[0]);
    const USER_LINKS_TABLE = $("#userLinksTable");

    function print_user_link(link){
        let row = $("<tr></tr>");
        let url = ((link.url.length > 40) ? link.url.slice(0, 40) + "..." : link.url);
        row.append($("<td><a href='" + link.short_url + "' target='_blank'>" + link.short_url + "</a></td>"));
        row.append($("<td><a href='" + link.url + "' target='_blank'>" + url + "</a></td>"));
        row.append($("<td>" + link.clicks_count + "</td>"));
        return row;
    }

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
                // Reset the form
                FORM.find("input").val("");
                FORM.find("button")
                    .prop("disabled", false)
                    .text("Make it short!");
                // Show the modal
                RESULT_INPUT.val(response.short_url);
                MODAL.show();
                // Append the new link to the user links table
                if(USER_LINKS_TABLE.length){
                    let tbody = USER_LINKS_TABLE.find("tbody");
                    let row = print_user_link(response);
                    tbody.prepend(row);
                }
                // Confetti animation
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

    if(USER_LINKS_TABLE.length){
        $.ajax({
            method: "GET",
            url: "/api/links/user-links/",
            success: (response) => {
                let tbody = USER_LINKS_TABLE.find("tbody");
                tbody.empty();
                response.reverse();
                for(let i = 0; i < response.length; i++){
                    let link = response[i];
                    let row = print_user_link(link);
                    tbody.prepend(row);
                }
            },
            error: (error) => {
                console.error(error);
            },
        });
    }

})(jQuery, bootstrap);
