const image=document.querySelector("#upload-1")
const button = document.querySelector("[type=button]")
const body = document.querySelector("body")
button.addEventListener("click",async (e)=>{
    const formdata=new FormData()
    formdata.append("image",image.files[0])
    console.log(formdata)
    const response=await fetch("/registerFaces",{method:"POST",body:formdata,headers:{"Accept":"application/json"}})
    if(!response.ok)
        return
    body.innerHTML=""
    const data=await response.json()
    const img=document.createElement("img")
    img.src="./static/images/drawnImage.jpg"
    body.append(img)
    data["faceIds"].forEach((e,i)=>{
        const inp=document.createElement("input")
        const number = document.createElement("p")
        number.innerText=i
        inp.name="input"
        inp.id = data["faceIds"][i]
        inp.innerText=e
        body.append(number,inp)
    })
    const sendButton=document.createElement("button")
    sendButton.innerText="send"
    sendButton.addEventListener("click",async (e)=>{
        const inputs=document.querySelectorAll("input")
        const faceInfos = []
        inputs.forEach((e)=>{
            faceInfos.push({"name":e.value,"id":e.id})
        })
        const response=await fetch("/registerFaces",{body:JSON.stringify({"faceInfos":faceInfos}),method:"POST"})
        if(response.ok){
            alert("accepted !")
            window.location.pathname="/"
        }
    })
    body.append(sendButton)
})