'use client';

import type React from 'react';
import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';

/**
 * Shape of a single chat message exchanged between the user
 * and the Digital Twin assistant.
 */
interface Message {
    id: string;                    // Unique identifier for the message (used as React key)
    role: 'user' | 'assistant';    // Message author role
    content: string;               // Text content of the message (may include Markdown)
    timestamp: Date;               // Timestamp when the message was created
}

/**
 * Digital Twin chat component.
 *
 * This component:
 * - Manages a simple chat history between the user and an AI assistant
 * - Sends user messages to the backend FastAPI `/chat` endpoint
 * - Displays responses from the AI Digital Twin
 * - Shows a typing/loading indicator while awaiting responses
 *
 * Notes:
 * - The backend maintains conversational memory via a session ID.
 * - Assistant responses may include light Markdown (headings, lists, bold, etc.),
 *   which is rendered using `react-markdown` with GitHub-flavoured Markdown support.
 */
export default function Twin() {
    // Store the ordered list of messages in the conversation
    const [messages, setMessages] = useState<Message[]>([]);
    // Store the current input text from the user
    const [input, setInput] = useState('');
    // Track whether a request is currently being processed
    const [isLoading, setIsLoading] = useState(false);
    // Persist a session ID to link multiple requests to the same session
    const [sessionId, setSessionId] = useState<string>('');
    // Reference to the bottom of the messages container for auto-scroll
    const messagesEndRef = useRef<HTMLDivElement>(null);

    /**
     * Scroll the chat view to the most recent message.
     */
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    /**
     * Whenever the messages array changes, scroll to the bottom so
     * the user always sees the latest message.
     */
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    /**
     * Send the current user input to the backend and append both the
     * user message and the assistant response to the conversation.
     */
    const sendMessage = async () => {
        // Do nothing if input is empty or a request is already in progress
        if (!input.trim() || isLoading) return;

        // Build the user message object
        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: input,
            timestamp: new Date(),
        };

        // Append the user message to the conversation
        setMessages(prev => [...prev, userMessage]);
        // Clear the input field
        setInput('');
        // Indicate that a request is in progress
        setIsLoading(true);

        try {
            // Send the chat request to the backend API
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: input,
                    session_id: sessionId || undefined, // Only include if already set
                }),
            });

            // Throw an error if the backend did not respond successfully
            if (!response.ok) throw new Error('Failed to send message');

            // Parse the JSON body from the backend response
            const data = await response.json();

            // If this is the first response, capture and store the session ID
            if (!sessionId) {
                setSessionId(data.session_id);
            }

            // Build the assistant's reply message
            const assistantMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: data.response, // May contain Markdown
                timestamp: new Date(),
            };

            // Append the assistant message to the conversation
            setMessages(prev => [...prev, assistantMessage]);
        } catch (error) {
            console.error('Error:', error);

            // Create a fallback error message from the assistant
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: 'Sorry, I encountered an error. Please try again.',
                timestamp: new Date(),
            };

            // Append the error message to the conversation
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            // Mark the request as complete (success or failure)
            setIsLoading(false);
        }
    };

    /**
     * Handle key press events in the input field.
     * Pressing Enter (without Shift) sends the message.
     */
    const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        // If Enter is pressed without Shift, prevent newline and send the message
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className="flex flex-col h-full bg-gray-50 rounded-lg shadow-lg">
            {/* Header */}
            <div className="bg-gradient-to-r from-slate-700 to-slate-800 text-white p-4 rounded-t-lg">
                <h2 className="text-xl font-semibold flex items-center gap-2">
                    {/* Bot icon in the header */}
                    <Bot className="w-6 h-6" />
                    AI Digital Twin
                </h2>
                <p className="text-sm text-slate-300 mt-1">Your AI course companion</p>
            </div>

            {/* Messages area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {/* Initial empty state when there are no messages */}
                {messages.length === 0 && (
                    <div className="text-center text-gray-500 mt-8">
                        <Bot className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                        <p>Hello! I&apos;m your Digital Twin.</p>
                        <p className="text-sm mt-2">Ask me anything about AI deployment!</p>
                    </div>
                )}

                {/* Render the list of messages */}
                {messages.map((message) => (
                    <div
                        key={message.id}
                        className={`flex gap-3 ${
                            message.role === 'user' ? 'justify-end' : 'justify-start'
                        }`}
                    >
                        {/* Assistant avatar on the left for assistant messages */}
                        {message.role === 'assistant' && (
                            <div className="flex-shrink-0">
                                <div className="w-8 h-8 bg-slate-700 rounded-full flex items-center justify-center">
                                    <Bot className="w-5 h-5 text-white" />
                                </div>
                            </div>
                        )}

                        {/* Message bubble */}
                        <div
                            className={`max-w-[70%] rounded-lg p-3 ${
                                message.role === 'user'
                                    ? 'bg-slate-700 text-white'
                                    : 'bg-white border border-gray-200 text-gray-800'
                            }`}
                        >
                            {/* Message content:
                               - Assistant: Markdown-rendered
                               - User: plain text (preserved line breaks) */}
                            {message.role === 'assistant' ? (
                                <div className="markdown-content prose prose-slate max-w-none">
                                    <ReactMarkdown
                                        remarkPlugins={[remarkGfm, remarkBreaks]}
                                    >
                                        {message.content}
                                    </ReactMarkdown>
                                </div>
                            ) : (
                                <p className="whitespace-pre-wrap">
                                    {message.content}
                                </p>
                            )}

                            {/* Timestamp below each message */}
                            <p
                                className={`text-xs mt-1 ${
                                    message.role === 'user' ? 'text-slate-300' : 'text-gray-500'
                                }`}
                            >
                                {message.timestamp.toLocaleTimeString()}
                            </p>
                        </div>

                        {/* User avatar on the right for user messages */}
                        {message.role === 'user' && (
                            <div className="flex-shrink-0">
                                <div className="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center">
                                    <User className="w-5 h-5 text-white" />
                                </div>
                            </div>
                        )}
                    </div>
                ))}

                {/* Loading indicator shown while waiting for a response */}
                {isLoading && (
                    <div className="flex gap-3 justify-start">
                        <div className="flex-shrink-0">
                            <div className="w-8 h-8 bg-slate-700 rounded-full flex items-center justify-center">
                                <Bot className="w-5 h-5 text-white" />
                            </div>
                        </div>
                        <div className="bg-white border border-gray-200 rounded-lg p-3">
                            <div className="flex space-x-2">
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
                            </div>
                        </div>
                    </div>
                )}

                {/* Invisible anchor used to scroll to the latest message */}
                <div ref={messagesEndRef} />
            </div>

            {/* Input area */}
            <div className="border-t border-gray-200 p-4 bg-white rounded-b-lg">
                <div className="flex gap-2">
                    {/* Text input for user message */}
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyPress}
                        placeholder="Type your message..."
                        className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-600 focus:border-transparent text-gray-800"
                        disabled={isLoading}
                    />
                    {/* Send button */}
                    <button
                        onClick={sendMessage}
                        disabled={!input.trim() || isLoading}
                        className="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </div>
            </div>
        </div>
    );
}
