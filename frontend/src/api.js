const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

export const sendMessageToAPI = async (message) => {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  return response.json();
};
