const mongoose= require("mongoose");
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI= os.getenv("MONGO_URI")

async function  connectDB() {
    
    await mongoose.connect(MONGO_URI)

    console.log("Connected to DB.")
}

module.exports = connectDB




