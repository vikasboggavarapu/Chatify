import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [uploading, setUploading] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const uploadPDF = async () => {
    if (!file) {
      setUploadMessage("Please select a PDF first.");
      return;
    }

    console.log("Selected file:", file);
    console.log("File name:", file.name);
    console.log("File type:", file.type);

    const formData = new FormData();

    formData.append("file", file);

    try {
      setUploading(true);
      setUploadMessage("");

      const response = await fetch(
        "http://127.0.0.1:8000/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      console.log("Status:", response.status);
      console.log("Backend response:", data);

      if (!response.ok) {
        setUploadMessage("Failed to upload PDF.");
        return;
      }

      setUploadMessage(data.message);

    } catch (error) {
      console.error("Upload error:", error);

      setUploadMessage("Failed to upload PDF.");

    } finally {
      setUploading(false);
    }
  };

  const askQuestion = async () => {
    if (!question.trim()) {
      return;
    }

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            question: question,
          }),
        }
      );

      const data = await response.json();

      console.log("Chat response:", data);

      setAnswer(data.answer);

    } catch (error) {
      console.error(error);

      setAnswer("Something went wrong.");
    }
  };


  return (
    <div className="container">

      <h1>💬 Chat with PDF</h1>

      <p>
        Upload a PDF file and ask questions.
      </p>


      {/* PDF Upload Section */}

      <div className="upload-section">

        <input
          type="file"
          accept=".pdf"
          disabled={uploading}
          onChange={(e) => {
            const selectedFile = e.target.files[0];

            console.log("File selected:", selectedFile);

            setFile(selectedFile);
          }}
        />

        <button
          onClick={uploadPDF}
          disabled={uploading}
        >
          {uploading ? "Processing..." : "Upload PDF"}
        </button>


        {/* Loading Spinner */}

        {uploading && (
          <div className="upload-status">

            <div className="spinner"></div>

            <span>
              Processing your PDF...
            </span>

          </div>
        )}


        {/* Upload Message */}

        {uploadMessage && (
          <p>{uploadMessage}</p>
        )}

      </div>


      {/* Chat Section */}

      <div className="chat-section">

        <h2>Ask your PDF</h2>

        <input
          type="text"
          placeholder="Ask a question about the PDF..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button onClick={askQuestion}>
          Ask
        </button>


        {/* LLM Answer */}

        {answer && (
          <div className="answer">

            <h3>Answer</h3>

            <p>{answer}</p>

          </div>
        )}

      </div>

    </div>
  );
}

export default App;
