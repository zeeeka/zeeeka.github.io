let listItem = document.getElementsByClassName('listitem')
let listIcon = document.getElementsByClassName ('dropicon')
let listTitle = document.getElementsByClassName ('droptitle')
let listP = document.getElementsByClassName ('dropp')
let listImg = document.getElementsByClassName('watchimg')


for (let i in listItem) {
    listItem[i].onclick = ()=> {
        /*icon rotate*/
        for(x=0;x<listIcon.length; x++){
            if(listIcon[x].getAttribute('style') == 'transform: rotate(90deg);'){
                listIcon[x].setAttribute('style','transform: rotate(0deg);')
            }
        }
        if(listIcon[i].getAttribute('style') == 'transform: rotate(0deg);'){
            listIcon[i].setAttribute('style' , 'transform: rotate(90deg);')
        }
        else {
            listIcon[i].setAttribute('style','transform: rotate(0deg);')
        }
        /*icon rotate*/
        /*paragraph display*/
        for(y=0;y<listP.length; y++){
            if(listP[y].getAttribute('style') == "display: block;"){
                listP[y].setAttribute('style',"display: none;")
            }
        }
        if(listP[i].getAttribute('style') == "display: none;"){
            listP[i].setAttribute('style' , "display: block;")
        }
        else {
            listP[i].setAttribute('style',"display: none;")
        }
        /*paragraph display*/
        /*change picture*/
        if(i == 0){
            listImg[0].setAttribute('src' , "images/watches/DreamShaper_v5_black_leather_braclet_white_hand_watch_preview_0.jpg")
            listImg[1].setAttribute('src' , "images/watches/DreamShaper_v5_black_leather_braclet_white_hand_watch_preview_3.jpg")
            listImg[2].setAttribute('src' , "images/watches/DreamShaper_v5_black_leather_braclet_white_hand_watch_preview_2.jpg")
            }else if (i==1){
                listImg[0].setAttribute('src' , "images/watches/DreamShaper_v5_hand_watch_preview_image_0.jpg")
                listImg[1].setAttribute('src' , "images/watches/DreamShaper_v5_hand_watch_preview_image_1.jpg")
                listImg[2].setAttribute('src' , "images/watches/last silver watch.jpg")
            }
            else if (i==2){
                listImg[0].setAttribute('src' , "images/watches/DreamShaper_v5_hand_watch_preview_4.jpg")
                listImg[1].setAttribute('src' , "images/watches/DreamShaper_v5_hand_watch_preview_0.jpg")
                listImg[2].setAttribute('src' , "images/watches/DreamShaper_v5_hand_watch_preview_5.jpg")
            }
            else if (i==3){
                listImg[0].setAttribute('src' , 'images/watches/vintage1.jpg')
                listImg[1].setAttribute('src' , 'images/watches/vintage2.jpg')
                listImg[2].setAttribute('src' , 'images/watches/vintage3.jpg')
            }
        /*change picture*/
    }
}