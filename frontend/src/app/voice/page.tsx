'use client'

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { transcribeAudio, createEntry } from '@/lib/api';
import { Message } from '@/types';
import { generateId } from '@/lib/utils';

export default function VoicePage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [textInput, setTextInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const handleTextSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!textInput.trim()) return;

    const userMessage: Message = {
      id: generateId(),
      role: 'user',
      content: textInput,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setTextInput('');

    // Create entry from text
    try {
      await createEntry({
        type: 'text',
        content: textInput,
      });
    } catch (err) {
      console.error('Failed to create entry:', err);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        await transcribeAudioFile(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error('Failed to start recording:', err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const transcribeAudioFile = async (blob: Blob) => {
    setIsProcessing(true);

    const userMessage: Message = {
      id: generateId(),
      role: 'user',
      content: '[Voice Message]',
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMessage]);

    try {
      const file = new File([blob], 'recording.webm', { type: 'audio/webm' });
      const result = await transcribeAudio(file);

      // Create entry from voice
      await createEntry({
        type: 'voice',
        content: result.text,
        metadata: { source: 'voice_recording' },
      });
    } catch (err) {
      console.error('Transcription failed:', err);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Voice Input</h1>
          <Link href="/" className="text-blue-600 hover:underline">← Back</Link>
        </div>

        {/* Chat interface */}
        <div className="bg-white rounded-lg shadow-lg p-4 mb-6 h-96 overflow-y-auto">
          {messages.length === 0 ? (
            <p className="text-gray-400 text-center mt-20">
              Start a conversation by typing a message or recording your voice
            </p>
          ) : (
            messages.map(msg => (
              <div
                key={msg.id}
                className={`mb-4 p-3 rounded-lg ${
                  msg.role === 'user' ? 'bg-blue-100 ml-8' : 'bg-gray-100 mr-8'
                }`}
              >
                <p className="font-semibold text-xs text-gray-500 mb-1">
                  {msg.role === 'user' ? 'You' : 'System'}
                </p>
                <p>{msg.content}</p>
              </div>
            ))
          )}
          {isProcessing && (
            <div className="bg-gray-100 mr-8 p-3 rounded-lg">
              <p className="text-gray-500">Processing...</p>
            </div>
          )}
        </div>

        {/* Text input */}
        <form onSubmit={handleTextSubmit} className="flex gap-2 mb-4">
          <input
            type="text"
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Send
          </button>
        </form>

        {/* Voice recording */}
        <div className="flex justify-center">
          <button
            onClick={isRecording ? stopRecording : startRecording}
            className={`w-16 h-16 rounded-full flex items-center justify-center ${
              isRecording
                ? 'bg-red-500 animate-pulse'
                : 'bg-blue-600 hover:bg-blue-700'
            } text-white text-2xl`}
          >
            {isRecording ? '■' : '●'}
          </button>
        </div>
        <p className="text-center mt-2 text-gray-500">
          {isRecording ? 'Tap to stop recording' : 'Tap to record voice'}
        </p>
      </div>
    </main>
  );
}
