let bars = document.getElementsByClassName ('bars')[0];
let sideList = document.getElementsByClassName('sidelist')[0];
let close = document.getElementsByClassName('closemenu')[0] ;
let transLayer = document.getElementsByClassName('transparent')[0];
let body = document.getElementById('body')
bars.onclick = function () {
    sideList.style.display='block';
    bars.style.display='none';
    transLayer.style.display='block';
    body.style.overflow = 'hidden' ;
    console.log(body)
}
close.onclick = function (){
    sideList.style.display='none';
    transLayer.style.display = "none" ;
    body.style.overflow='visible';
    if (window.matchMedia('(max-width : 540px)').matches){
        bars.style.display='flex';
    }else{
        bars.style.display='none';
    }
}
transLayer.onclick = function (){
    sideList.style.display='none';
    transLayer.style.display = "none" ;
    body.style.overflow='visible';
    if (window.matchMedia('(max-width : 540px)').matches){
        bars.style.display='flex';
    }else{
        bars.style.display='none';
    }
}
setInterval(function(){
    if (!window.matchMedia('(max-width : 540px)').matches ){
        bars.style.display='none';
    }else{
        bars.style.display='flex';
    }
} , 1000)

