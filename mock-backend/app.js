const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');
const path = require('path');
const multer = require('multer');

const app = express();
const port = 3300;

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const uploadDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
}

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({ storage: storage });

let documents = [];
let chatHistory = [];

app.use('/uploads', express.static(uploadDir));

app.post('/auth/login', (req, res) => {
  const { email, password } = req.body;
  res.json({
    token: uuidv4(),
    user: { id: uuidv4(), email, name: email }
  });
});

app.get('/documents', (req, res) => {
  res.json(documents);
});

app.post('/documents/upload', upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  const id = uuidv4();
  const { originalname, filename, mimetype } = req.file;
  const newDoc = { 
    id, 
    name: originalname, 
    type: mimetype, 
    filePath: `/uploads/${filename}`
  };
  
  documents.push(newDoc);
  res.json(newDoc);
});
app.delete('/documents/:id', (req, res) => {
  const doc = documents.find(doc => doc.id === req.params.id);
  if (doc) {
    fs.unlinkSync(path.join(uploadDir, path.basename(doc.filePath)));
    documents = documents.filter(d => d.id !== req.params.id);
    res.sendStatus(200);
  } else {
    res.sendStatus(404);
  }
});

app.get('/documents/:id/content', (req, res) => {
  const doc = documents.find(doc => doc.id === req.params.id);
  if (doc) {
    res.sendFile(path.join(uploadDir, path.basename(doc.filePath)));
  } else {
    res.sendStatus(404);
  }
});

app.post('/chatbot/message', (req, res) => {
  const { message } = req.body;
  chatHistory.push({ content: message, isUser: true });
  const botReply = `AI response to: ${message}`;
  chatHistory.push({ content: botReply, isUser: false });
  res.json({ message: botReply });
});

app.get('/chatbot/history', (req, res) => {
  res.json(chatHistory);
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});