$(document).on('click', '.emotion', function(e){
    e.preventDefault();
    var emotion = $(this).data('emotion');
    window.location.href = `/select/emotion/${emotion}#home`;
})