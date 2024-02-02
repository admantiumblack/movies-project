function requestMovie(movieName='', movieId=''){
    url = "http://localhost:8000/movies?";
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