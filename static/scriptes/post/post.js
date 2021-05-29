function getPosts(){
    //console.log(dataform)
    $.ajax({
        url:URL_POST_DATA,
        type:'GET',
        success: function(data){
            console.log("success get_posts")
            $('#post_list').html(data);
        },
        error: function(e, x, r){
            console.log('error get posts')
            $('#post_list').html("Something went wrong");
            console.log(e.responseText)
        }
    });
}


function createComment(data){
    //getImage, getFullName, date, comment
    comment = `
    <div class="box-comment">
        <img class="img-circle img-sm" src="${ data.getImage }" alt="User Image">
        <div class="comment-text">
        <span class="username">
        ${ data.getFullName }
            <span class="text-muted pull-right">
            ${ data.date }
            </span>
        </span>
        ${ data.comment }
        </div>
    </div>
    `
    return comment
}

function postComment(e){
    form = $(e.target)
    $.ajax({
        url: form.attr('action'),
        type: form.attr('method'),
        data: form.serialize(),
        success: function(data) {
            console.log("success post comment");
            post = form[0].parentElement.parentElement
            comments = $(post).find('#post_comments')[0]
            console.log(post)
            console.log(comments)
            console.log(data)
            console.log(createComment(data))
            comments.innerHTML += (createComment(data))
            $(form)[0].reset();
        },
        error: function(e, x, r) {
            showError(e)
            $(form)[0].reset();
        }
    });
    
    e.preventDefault();
}


$(document).ready(function() {
    //to init
    getPosts()
});