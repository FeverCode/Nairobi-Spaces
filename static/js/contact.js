const contact = function(email, name,subject,message) {
    var formData = new FormData();
    formData.append('email', email);
    formData.append('name', name);
    formData.append('subject', subject);
    formData.append('message', message);
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });
    $.ajax({
        url: '/contact/',
        type: 'POST',
        dataType: 'json',
        cache: false,
        processData: false,
        contentType: false,
        data: formData,
        error: function (xhr) {
            console.error(xhr.statusText);
        },
        success: function (res) {
            $('.success').text(res.msg);
            $('#Email').val(' ');
            $('#Name').val(' ');
            $('#Subject').val(' ');
            $('#Message').val(' ');

        }
    });
};

(function ($) {
    $('#submit').on('click', () => {
        event.preventDefault();
        const Name = $('#userName').val();
        const Subject = $('#userSubject').val();
        const Email = $('#userEmail').val();
        const Message = $('#userMessage').val();
        if (Email && Name) {
            contact(Email, Name, Subject, Message);
        }
    });

    $('#Email').on('change', (event) => {
        event.preventDefault();
        const email = event.target.value;
        validateEmail(email);
    });
})(jQuery);