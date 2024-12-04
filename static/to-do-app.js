function envio_post(destino, ...valores) {

    let objpost = {}
    valores.forEach((element, i) => {
        Object.assign(objpost, JSON.parse(`{ "${i}":"${element}" }`))
    });    

    fetch("/"+destino, {
            method: "POST",
            body: JSON.stringify(objpost),
            headers: {
            "Content-type": "application/json; charset=UTF-8"
            }
        })
        .then(response => response.json)
        .then(data => console.log(data))
        .catch(error => console.error(error))
        .finally(window.location.reload())
}

function mudar_pag(url) {
    location.href = url;
}