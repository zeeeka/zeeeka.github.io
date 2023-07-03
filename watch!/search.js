let search = document.getElementById('search')
let boxesSearch = document.getElementsByClassName('check')
let allBoxSearch = document.getElementById('all')
let titles = []
let searchedItems = []

/* on focus uncheck all filters*/

search.onfocus= () => {
    let elements = document.getElementsByClassName(allBoxSearch.id)
    for(let e in elements){
        if(elements[e].innerHTML !== undefined){
            elements[e].setAttribute('style' , 'display: none;')
        }
    }
    document.getElementsByClassName('filters')[0].style.display='none'
    document.getElementsByClassName('productstwo')[0].style.width='100%'
}
search.onblur= () => {
    let mediaQuery = window.matchMedia('(min-width: 871px)')
    if (mediaQuery.matches){
        document.getElementsByClassName('filters')[0].style.display='block'
    }
    let elements = document.getElementsByClassName(allBoxSearch.id)
    for(let e in elements){
        if(elements[e].innerHTML !== undefined){
            elements[e].setAttribute('style' , 'display: block;')
        }
    }
}





/*get input of search*/

search.oninput = ()=>{
    let elements = document.getElementsByClassName(allBoxSearch.id)
    for(let e in elements){
        if(elements[e].innerHTML !== undefined){
            elements[e].setAttribute('style' , 'display: none;')
        }
    }
    let searchValue = search.value.split('')
    if(searchValue.length == 0){
        searchedItems = []
        for(let e in elements){
            if(elements[e].innerHTML !== undefined){
                elements[e].setAttribute('style' , 'display: block;')
            }
        }
    }
    for(let i in titles){
        for(let x in searchValue){
            if(searchValue[x] == searchValue.slice(-1)){
                if(titles[i].indexOf(searchValue[x])==-1){
                    continue
                }else if (titles[i].indexOf(searchValue[x])==x) {
                    if(searchedItems.length == 0){
                        searchedItems.push(titles[i].join(''))
                    }else if (searchedItems.indexOf(titles[i].join('')) == -1 ){
                        searchedItems.push(titles[i].join(''))
                    }
                }
            }
            for(let si in searchedItems){
                if (searchedItems[si][x-1] !== undefined){
                    if (searchValue[x-1] !== searchedItems[si][x-1]){
                        searchedItems.pop(searchedItems[si])
                    }else if (searchValue[x] !== searchedItems[si][x]){
                        searchedItems.pop(searchedItems[si])
                }
                }
            }
        }
    }
    console.log(searchedItems)
    for(let z in searchedItems){
        let showElements = document.getElementById(searchedItems[z])
        showElements.setAttribute('style' , 'display: block;')
    }
}



/* separate all product names*/
let names = document.getElementsByClassName('producttitle')
for(let i in names){
    if(names[i].innerHTML !== undefined){
        titles.push(names[i].textContent.toLowerCase().split(''))
    }
}