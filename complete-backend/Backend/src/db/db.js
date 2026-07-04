const mongoose = require("mongoose");
const dns = require("dns");
require("dotenv").config();

function setupDns() {
    const current = dns.getServers();
    const isBroken = current.length === 0 || current.every(ip => ip === "127.0.0.1" || ip === "::1");

    if (process.platform === "win32" && isBroken) {
        dns.setServers(["8.8.8.8", "1.1.1.1"]);
        console.log("Patched DNS resolver (Windows loopback issue detected)");
    }
}

const MONGO_URI = process.env.MONGO_URI;

async function connectDB() {
    if (!MONGO_URI) {
        throw new Error("MONGO_URI is not defined in your .env file");
    }

    setupDns();

    try {
        await mongoose.connect(MONGO_URI);
        console.log("Connected to DB.");
    } catch (err) {
        console.error("MongoDB connection failed:", err.message);
        throw err;
    }
}

module.exports = connectDB;