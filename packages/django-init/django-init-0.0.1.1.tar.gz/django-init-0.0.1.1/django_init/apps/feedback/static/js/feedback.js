function setToken() {
    $('.token').each(function (i, elem) {
        $(this).val(Math.floor(Math.random() * Math.pow(2, 64)).toString(36));
    });
}

function modalSuccess() {
    $(function () {
        $.magnificPopup.open({
            items: {src: '#thank-modal'},
            type: 'inline',
            // callbacks: {
            //     close: function () {
            //         // window.location.reload();
            //     }
            // }
        }, 0);
        $.magnificPopup.instance.close = function () {
            window.location.reload(true);
            $.magnificPopup.proto.close.call(this);
        }
    });
}

setToken();

$(function () {
    $(document).on('submit', 'form.send_ajax', function (event) {
        event.preventDefault();
        var form = $(this),
            form_container = $(this).parents('.updatable'),
            // form_data = form.serialize();
            form_data = new FormData(this);
        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            dataType: 'json',
            data: form_data,
            cache: false,
            processData: false,
            contentType: false,
            success: function (data) {
                // console.log(data);
                if (data.success) {
                    // setInputs();
                    // setToken();
                    modalSuccess();
                } else {
                    form_container.html(data.form_html);
                    setToken();
                }
            },
            error: function (data) {
                console.log('AJAX ERROR' + data.error);
            }
        });
    });
});
