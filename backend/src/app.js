const express= require('express')
const noteModel= require('./models/note.model') 

const app= express()

app.use(express.json())


//Post  
app.post("/notes", async (req,res)=>{

    const data= req.body
    await noteModel.create(
        {
            "title" : data.title,
            "description" : data.description
        }
    )

    res.status(201).json({
        message: "Note created successfully",
        note: data
    })
})

//Get
app.get("/notes", async (req,res)=>{
    const notes= await noteModel.find()


    // const notes= await noteModel.findOne(
    //     {
    //         title: "test title"
    //     }
    // )
    res.status(200).json({
        notes: notes
    })
})

//Delete
app.delete("/notes/:id", async (req,res)=>{
    const id= req.params.id;
    await noteModel.findOneAndDelete(
        {
            _id: id
        }
    )

    res.status(200).json({
        message: "Note deleted successfully"
    })
})

module.exports= app