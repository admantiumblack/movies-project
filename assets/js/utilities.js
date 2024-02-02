function requestMovie(url, movieName='', movieId=''){
    url = url + "?"
    if(movieName != '' && movieId == ''){
        url += `name=${movieName}`;
    }else if(movieName == '' && movieId != ''){
        url += `id=${movieId}`;
    }
    const request = new XMLHttpRequest();
    request.open("GET", url, false);
    request.send(null);

    return JSON.parse(request.responseText)
}