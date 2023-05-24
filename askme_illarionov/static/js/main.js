function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(".like-btn").on('click', function (ev) {
    const request = new Request(
        "http://127.0.0.1/question_like/",
        {
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            method: 'POST',
            body: 'question_id=' + $(this).data('id'),
        }
    );
//    fetch(request).then(function (response) {
//        console.log('like')
//    });
    fetch(request).then(
        response_raw => response_raw.json().then(
            response_json => $(this).attr("data-count", response_json.likes)
        )
    );
});

$(".answer-like-btn").on('click', function (ev) {
    const request = new Request(
        "http://127.0.0.1/answer_like/",
        {
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            method: 'POST',
            body: 'answer_id=' + $(this).data('id'),
        }
    );
//    fetch(request).then(function (response) {
//        console.log('like')
//    });
    fetch(request).then(
        response_raw => response_raw.json().then(
            response_json => $(this).attr("data-count", response_json.likes)
        )
    );
});
//:8000!!!!!
$(".correct-btn").on('click', function (ev) {
    const request = new Request(
        "http://127.0.0.1/mark_as_correct/",
        {
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            method: 'POST',
            body: 'answer_id=' + $(this).data('id'),
        }
    );
//    fetch(request).then(function (response) {
//        console.log('like')
//    });
    fetch(request).then(
        response_raw => response_raw.json().then(
            response_json => $(this).attr("data-status", response_json.status)
        )
    );
});

