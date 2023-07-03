let boxes = document.getElementsByClassName('check')
let allBox = document.getElementById('all')
/* view the checked class*/
for (let i in boxes){
    if(boxes[i].checked){
        let elements = document.getElementsByClassName(boxes[i].getAttribute('id'))
        for (let e in elements ){
            if(elements[e].innerHTML != undefined){
                elements[e].setAttribute('style' , 'display: block;')
            }
        }
    }

    /*checking and un unchecking*/
    boxes[i].onclick = ()=>{
        if(boxes[i].checked){
            boxes[i].setAttribute('checked' , 'checked')
        }else{
            boxes[i].removeAttribute('checked' , 'checked')
        }

        if(boxes[i].id !== 'all'){
            allBox.removeAttribute('checked')
        }

        /*reset*/

        let elements = document.getElementsByClassName(allBox.id)
        for(let e in elements){
            if(elements[e].innerHTML !== undefined){
                elements[e].setAttribute('style' , 'display: none;')
            }
        }




        /*add style*/



        for(let x in boxes){
            if(boxes[x].innerHTML !== undefined){
                if(boxes[x].checked){
                    let elements = document.getElementsByClassName(boxes[x].id)
                    for(let e in elements){
                        if(elements[e].innerHTML !== undefined){
                            elements[e].setAttribute('style' , 'display: block;')
                        }
                    }
                }
        }
    }
    }


    
}






/*logo click to home page*/


let logo = document.getElementById('imagelogo')

logo.onclick = ()=>{
    window.location.href = 'https://zeeeka.github.io/watch!/index.html' ;
}