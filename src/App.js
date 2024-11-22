import React, { useState } from "react";
import axios from "axios";
import { Container, Form, Button, Card } from "react-bootstrap";

const App = () => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [history, setHistory] = useState([]);

  const askQuestion = async () => {
    if (!question.trim()) return;

    try {
      const response = await axios.post("http://127.0.0.1:5000/query", { question });
      const botAnswer = response.data.answer;

      // Update conversation history
      setHistory([...history, { type: "user", text: question }, { type: "bot", text: botAnswer }]);
      setAnswer(botAnswer);
      setQuestion(""); // Clear the input
    } catch (error) {
      console.error(error);
      setAnswer("Error getting response from the server.");
    }
  };

  return (
    <Container className="mt-4">
      <Card>
        <Card.Header as="h5">PDF Chatbot</Card.Header>
        <Card.Body>
          <div style={{ maxHeight: "300px", overflowY: "auto" }}>
            {history.map((entry, index) => (
              <div
                key={index}
                className={`mb-2 p-2 rounded ${
                  entry.type === "user" ? "bg-primary text-white text-right" : "bg-light"
                }`}
              >
                {entry.text}
              </div>
            ))}
          </div>
          <Form className="mt-3">
            <Form.Group>
              <Form.Control
                type="text"
                placeholder="Ask a question..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
              />
            </Form.Group>
            <Button variant="primary" className="mt-2" onClick={askQuestion}>
              Ask
            </Button>
          </Form>
          <Card.Text className="mt-4">
            <strong>Answer:</strong> {answer}
          </Card.Text>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default App;
