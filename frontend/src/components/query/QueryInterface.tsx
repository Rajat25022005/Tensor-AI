import { useState, KeyboardEvent, useRef, useEffect } from "react";
import { useQueryStore } from "../../stores/queryStore";
import { Send, Loader2 } from "lucide-react";
import "./QueryInterface.css";

function QueryInterface() {
  const [query, setQuery] = useState("");
  const { submitQuery, isLoading } = useQueryStore();
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [query]);

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!query.trim() || isLoading) return;
    const question = query;
    setQuery("");
    await submitQuery(question);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <form className="query-interface glass" onSubmit={handleSubmit}>
      <div className="query-input-wrapper">
        <textarea
          ref={textareaRef}
          className="query-input"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything about your data... (Press Enter to submit)"
          disabled={isLoading}
          rows={1}
        />
        <button 
          type="submit" 
          className="query-submit-btn" 
          disabled={!query.trim() || isLoading}
          title="Send query"
        >
          {isLoading ? <Loader2 size={18} className="spin" /> : <Send size={18} />}
        </button>
      </div>
    </form>
  );
}

export default QueryInterface;
