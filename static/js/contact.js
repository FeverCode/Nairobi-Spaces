function getInputVal(id) {
    return document.getElementById(id).value;
}

function writeUserData(fName,subject, email, message) {
    const db = getDatabase();
    set(ref(db, 'users/' + fName), {
        subject: subject,
        email: email,
        message: message,
    });



    //Show alert
    document.querySelector('.alert').style.display = 'block';

    //Hide alert after 3 seconds
    setTimeout(function () {
        document.querySelector('.alert').style.display = 'none';
    }, 3000);

    document.getElementById('contact_form').reset();


}