function loadCategory(category) {
    $.ajax({
        url: `/load-category/${category}`,
        type: 'GET',
        success: function(data) {
            $('#content-area').html(data);
        },
        error: function(error) {
            console.log('Error loading category: ', error);
        }
    });
}

function postComment() {
    const comment = $('textarea').val();
    // AJAX Post to Flask
    $.post('/post-comment', {comment: comment}, function(data) {
        $('textarea').val(''); // Clear textarea
        alert('Comment posted!');
    }).fail(function() {
        alert('Error posting comment');
    });
}

// Example Websocket connection (requires further backend setup)
var socket = new WebSocket('ws://localhost:5000/updates');
socket.onmessage = function(event) {
    $('#live-updates').append(`<p>${event.data}</p>`);
};
