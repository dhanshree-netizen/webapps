
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

const mongoURI = "mongodb+srv://dhanshree_db_user:dhanu666@cluster0.qp4k9nz.mongodb.net/webdemo?appName=Cluster0";

const Volunteer = mongoose.model("Volunteer", {
    name: {
        type: String,
        required: true,
        trim: true
    },
    city: {
        type: String,
        required: true,
        trim: true
    },
    experience: {
        type: String,
        required: true,
        trim: true
    }
});

app.get("/", function (req, res) {
    res.send("RescueConnect backend is running");
});

app.get("/status", function (req, res) {
    const connected = mongoose.connection.readyState === 1;

    res.json({
        mode: connected ? "MongoDB Atlas" : "MongoDB disconnected",
        atlasConnected: connected
    });
});

app.get("/volunteers", async function (req, res) {
    try {
        const volunteers = await Volunteer.find().sort({ _id: -1 });
        res.json(volunteers);
    } catch (err) {
        res.status(500).json({
            message: "Failed to fetch volunteers"
        });
    }
});

app.post("/volunteers", async function (req, res) {
    try {
        const name = (req.body.name || "").trim();
        const city = (req.body.city || "").trim();
        const experience = (req.body.experience || "").trim();

        if (!name || !city || !experience) {
            return res.status(400).json({
                message: "Please fill all fields"
            });
        }

        const volunteer = await Volunteer.create({
            name: name,
            city: city,
            experience: experience
        });

        res.status(201).json(volunteer);
    } catch (err) {
        res.status(400).json({
            message: "Failed to add volunteer"
        });
    }
});

app.put("/volunteers/:id", async function (req, res) {
    try {
        if (!mongoose.isValidObjectId(req.params.id)) {
            return res.status(400).json({
                message: "Invalid volunteer ID"
            });
        }

        const name = (req.body.name || "").trim();
        const city = (req.body.city || "").trim();
        const experience = (req.body.experience || "").trim();

        if (!name || !city || !experience) {
            return res.status(400).json({
                message: "Please fill all fields"
            });
        }

        const volunteer = await Volunteer.findByIdAndUpdate(
            req.params.id,
            {
                name: name,
                city: city,
                experience: experience
            },
            {
                new: true,
                runValidators: true
            }
        );

        if (!volunteer) {
            return res.status(404).json({
                message: "Volunteer not found"
            });
        }

        res.json(volunteer);
    } catch (err) {
        res.status(500).json({
            message: "Failed to update volunteer"
        });
    }
});

app.delete("/volunteers/:id", async function (req, res) {
    try {
        if (!mongoose.isValidObjectId(req.params.id)) {
            return res.status(400).json({
                message: "Invalid volunteer ID"
            });
        }

        const volunteer = await Volunteer.findByIdAndDelete(
            req.params.id
        );

        if (!volunteer) {
            return res.status(404).json({
                message: "Volunteer not found"
            });
        }

        res.json({
            message: "Volunteer deleted successfully"
        });
    } catch (err) {
        res.status(500).json({
            message: "Failed to delete volunteer"
        });
    }
});

async function startServer() {
    try {
        await mongoose.connect(mongoURI, {
            serverSelectionTimeoutMS: 10000
        });

        console.log("MongoDB Atlas connected");
        console.log("Database:", mongoose.connection.name);

        app.listen(5000, function () {
            console.log("Server running at http://localhost:5000");
        });
    } catch (err) {
        console.log("MongoDB connection failed:", err.message);
        console.log("Check your connection string and Atlas Network Access.");
        process.exit(1);
    }
}

startServer();
