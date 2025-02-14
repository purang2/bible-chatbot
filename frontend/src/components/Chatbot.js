// Chatbot.js
import React, { useState, useEffect, useRef } from "react";
import "./Chatbot.css";

const botProfile = process.env.PUBLIC_URL + "/bot-avatar.png";
const userProfile = process.env.PUBLIC_URL + "/user-avatar.png";
const BIBLE_VERSE_PATTERN =
  /\((\d+)\)\s*([가-힣]+\s*\d+:\d+)(?:\s*[-–]\s*["']([^"\']+)["\'])?(?:\s*[–-]\s*["']([^"\']+)["'])?/;

const categories = {
  relationships: {
    title: "인간관계",
    questions: [
      "가족과의 갈등을 어떻게 풀어야 할까요?",
      "친구관계에서 상처받았을 때는 어떻게 해야 할까요?",
      "대인관계가 어려울 때 어떻게 해야 할까요?",
      "용서하는 것이 어려울 때는 어떻게 해야 할까요?",
    ],
  },
  faith: {
    title: "신앙생활",
    questions: [
      "기도는 어떻게 하면 좋을까요?",
      "성경 읽기가 어려워요.",
      "예배생활이 게을러졌어요.",
      "하나님의 뜻을 어떻게 알 수 있을까요?",
    ],
  },
  life: {
    title: "일상과 결정",
    questions: [
      "중요한 결정을 앞두고 있어요.",
      "미래가 불안해요.",
      "습관을 바꾸고 싶어요.",
      "스트레스 관리가 필요해요.",
    ],
  },
};

const initialMessage = {
  id: "welcome",
  text: "안녕하세요! 성경과 삶에 대해 함께 이야기 나누어요. 어떤 주제에 관심이 있으신가요?",
  sender: "bot",
};

/*
const splitMessageAndVerses = (text) => {
  const parts = text.split("[추천 성경구절]");
  if (parts.length !== 2) return { message: text, verses: [] };

  const mainMessage = parts[0].trim();
  const versesText = parts[1].trim();

  const verses = [];
  let match;

  while ((match = BIBLE_VERSE_PATTERN.exec(versesText)) !== null) {
    verses.push({
      index: match[1],
      reference: match[2],
      content: match[4],
    });
  }

  return { message: mainMessage, verses };
}; */
const BibleVerse = ({ verse }) => {
  console.log("verse prop:", verse); // 구조 확인을 위해 추가

  const [showContext, setShowContext] = useState(false);
  const [contextData, setContextData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleVerseClick = async () => {
    try {
      if (!showContext) {
        setLoading(true);
        const [book, chapterVerse] = reference.split(" ");
        const [chapter, verseNum] = chapterVerse.split(":");

        // URL 인코딩 추가
        const encodedBook = encodeURIComponent(book);

        const response = await fetch(
          `/verse-context/${encodedBook}/${chapter}/${verseNum}`
        );

        if (!response.ok) throw new Error("구절을 가져오는데 실패했습니다");

        const data = await response.json();
        setContextData(data);
        setShowContext(true);
      }
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="message bot bible-verse">
      <div className="message-avatar">
        <img src={botProfile} alt="Bot Avatar" />
      </div>
      <div
        className="message-content bible-verse-content"
        onClick={handleVerseClick}
      >
        <span className="verse-reference">{verse.reference}</span>
        <p className="verse-text">{verse.text}</p>

        {loading && (
          <div className="context-loading">
            <div className="loading-spinner"></div>
          </div>
        )}

        {showContext && contextData && (
          <div className="verse-context" onClick={(e) => e.stopPropagation()}>
            <div className="context-header">
              <h4>
                {contextData.book} {contextData.chapter}장
              </h4>
              <button
                className="close-context"
                onClick={(e) => {
                  e.stopPropagation();
                  setShowContext(false);
                }}
              >
                ✕
              </button>
            </div>
            <div className="context-verses">
              {contextData.verses.map((v) => (
                <p
                  key={v.verse_number}
                  className={`context-verse ${v.is_target ? "highlight" : ""}`}
                >
                  <span className="verse-num">{v.verse_number}</span>
                  {v.text}
                </p>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const Chatbot = () => {
  const [messages, setMessages] = useState([initialMessage]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };
  /*
  const formatResponse = async (text) => {
    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ message: text }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "서버 오류가 발생했습니다.");
      }

      const data = await response.json();
      return data.message;
    } catch (error) {
      console.error("Error:", error);
      throw error;
    }
  };
  */
  const handleSend = async (text) => {
    if (!text.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: text,
      sender: "user",
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ message: text }),
      });

      if (!response.ok) throw new Error("서버 오류가 발생했습니다.");

      const data = await response.json();

      // 메인 메시지 추가
      const botMessage = {
        id: Date.now() + 1,
        text: data.main_message,
        sender: "bot",
      };

      // 성경 구절들을 별도의 메시지로 추가
      const verseMessages = data.verses.map((verse, index) => ({
        id: Date.now() + 2 + index,
        verse: {
          index: verse.index,
          reference: verse.reference,
          text: verse.text,
        },
        sender: "bot",
        type: "bible-verse",
      }));

      setMessages((prev) => [...prev, botMessage, ...verseMessages]);
    } catch (error) {
      console.error("Error:", error);
      const errorMessage = {
        id: Date.now() + 1,
        text: "죄송합니다. 응답을 생성하는 중에 문제가 발생했습니다. 다시 시도해 주세요.",
        sender: "bot",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCategorySelect = (category) => {
    setSelectedCategory(category);
    const message = {
      id: Date.now(),
      text: `${categories[category].title}에 대해 이야기 나누어 보아요.`,
      sender: "bot",
    };
    setMessages((prev) => [...prev, message]);
  };

  const renderMessage = (message) => {
    if (message.type === "bible-verse") {
      return <BibleVerse key={message.id} verse={message.verse} />;
    }

    const isBot = message.sender === "bot";
    return (
      <div key={message.id} className={`message ${message.sender}`}>
        <div className="message-avatar">
          <img
            src={isBot ? botProfile : userProfile}
            alt={`${isBot ? "Bot" : "User"} Avatar`}
          />
        </div>
        <div className="message-content">{message.text}</div>
      </div>
    );
  };

  const renderSuggestions = () => {
    if (selectedCategory) {
      return (
        <div className="question-suggestions">
          {categories[selectedCategory].questions.map((question, index) => (
            <button
              key={index}
              className="suggestion-button"
              onClick={() => handleSend(question)}
            >
              {question}
            </button>
          ))}
        </div>
      );
    }

    return (
      <div className="question-suggestions">
        {Object.entries(categories).map(([key, category]) => (
          <button
            key={key}
            className="suggestion-button"
            onClick={() => handleCategorySelect(key)}
          >
            {category.title}
          </button>
        ))}
      </div>
    );
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="header-profile">
          <img src={botProfile} alt="Bot Profile" />
        </div>
        <div className="header-text">
          <h1>성경 챗봇</h1>
          <p>환영하고 축복합니다. 성경과 삶의 이야기를 나눠요</p>
        </div>
      </div>

      <div className="chat-messages">
        {messages.map(renderMessage)}
        {renderSuggestions()}
        {isLoading && (
          <div className="loading-indicator">
            <span></span>
            <span style={{ animationDelay: "0.2s" }}></span>
            <span style={{ animationDelay: "0.4s" }}></span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <div className="chat-input-container">
        <input
          type="text"
          className="chat-input"
          placeholder="메시지를 입력하세요..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend(input);
            }
          }}
        />
        <button
          className="send-button"
          onClick={() => handleSend(input)}
          disabled={isLoading || !input.trim()}
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
