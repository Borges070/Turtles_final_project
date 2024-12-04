const caixainput= document.getElementById("caixa-input")
        const lista = document.getElementById("lista")
        
        function addtarefa(){
        
            let li = document.createElement("li")
            li.innerHTML = caixainput.value
            lista.appendChild(li)
            
            let span = document.createElement("span")
            span.innerHTML = "\u00d7"
            li.appendChild(span)
            caixainput.value = ''
            savedata()
            
        }
        
        lista.addEventListener("click", function(riskrem){
            if(riskrem.target.tagName === "LI"){
                riskrem.target.classList.toggle("checked")
                savedata()
            }
            else if(riskrem.target.tagName === "SPAN"){
                riskrem.target.parentElement.remove()
                savedata()
            }
        })
        
        function savedata(){
            localStorage.setItem("data", lista.innerHTML)
        }
        function showdata(){
            lista.innerHTML = localStorage.getItem("data")
        }
        showdata()