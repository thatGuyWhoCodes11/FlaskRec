const file=document.querySelector("#image")
const html=document.getElementsByTagName("html")
const body = document.querySelector("body")
const button = document.querySelector("[type=button]")

button.addEventListener("click",async (e)=>{
    const formdata=new FormData()
    formdata.append("image",file.files[0])
    const response=await fetch("/recognizeFaces",{method:"POST",body:formdata,headers:{"Accept":"application/json"}})
    if(!response.ok){
        return console.log("request failed")
    }
        const data=await response.json()
        const img=document.createElement("img")
        img.src="./static/images/drawnImage.jpg"
        body.innerHTML=""
        body.append(img)
        console.log( data["results"])
        for(const [index,result] of data["results"].entries()){
            const p=document.createElement("p")
            p.innerText=index+" "+result["name"]
            body.append(p)
        }
})