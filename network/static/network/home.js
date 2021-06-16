document.addEventListener("DOMContentLoaded", () => {

    document.querySelector('#next').onclick = () => {
        changePage("next")
    }

    document.querySelector('#previous').onclick = () => {
        changePage("prev")
    }
})

async function loadPost(mode, page) {
    if (mode == "all") {
        var posts = await fetch(`/posts?page=${page}`)
        .then(response => response.json())

    } else {
        var posts = await fetch(`/posts/${mode}?page=${page}`)
        .then(response => response.json())

    }
    posts.forEach(function(post) {
        console.log(post)
        const div = document.createElement('div')
        const content = document.createElement('h6')
        const poster = document.createElement('h4')
        const likes = document.createElement('h6')
        const postTime = document.createElement('h6')

        content.innerHTML = `${post.content}`
        poster.innerHTML = `${post.poster}`
        likes.innerHTML = `Likes: ${post.likes}`
        postTime.innerHTML = `Time: ${post.postTime}`

        div.append(poster)
        div.append(content)
        div.append(likes)
        div.append(postTime)
        document.querySelector("#posts").append(div)
    })
}

async function Follow(profile) {
    // profile is person to be followed, current user is following
    // mode determines whether to follow (true) or unfollow (false)

    var mode = document.querySelector("#follow").dataset.state

    let follow = await fetch("/follow", {
        method: "PUT",
        body: JSON.stringify({
        following: profile,
        follow: mode
        })
    })

    if (mode == "true") {
        document.querySelector("#follow").dataset.state = "false"
        document.querySelector("#follow").innerHTML = "Unfollow"
    } else {
        document.querySelector("#follow").dataset.state = "true"
        document.querySelector("#follow").innerHTML = "Follow"
    }
}

function changePage(mode) {
    document.querySelector('#posts').innerHTML = ''
    let page = document.querySelector('#page')
    let num = parseInt(page.innerHTML)

    if (mode == "next") {
        num = num + 1
    } else if (num > 0) {
        num = num - 1
    }
    page.innerHTML = num
    loadPost(window.loadMode, num)
}