import React, { useState, useEffect } from "react";
import "./BotChat.css";

const BotChat = () => {
  const [open, setOpen] = useState(false);
  const toggle = () => {
    console.log('BotChat toggle clicked');
    setOpen(!open);
  };
  useEffect(() => {
    console.log('BotChat mounted, open state:', open);
  }, []);

  return (
    <>
      <button className="bot-toggle" onClick={toggle} aria-label="Chat with interview bot">
        {open ? "✕" : "💬"}
      </button>
      {open && (
        <iframe
          title="Interview Bot"
          src="https://cdn.botpress.cloud/webchat/v3.6/shareable.html?configUrl=https://files.bpcontent.cloud/2026/06/08/09/20260608093533-0CUGJ0LQ.json"
          className="bot-iframe"
          allow="microphone; camera"
        />
      )}
    </>
  );
};

export default BotChat;
