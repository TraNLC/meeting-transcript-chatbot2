#!/usr/bin/env python
"""CLI interface for Meeting Analyzer."""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.data import TranscriptLoader, TranscriptPreprocessor
from src.llm import LLMManager
from src.rag import Chatbot
from src.config import Settings
from src.audio.stt_processor import STTProcessor
from src.audio.tts_processor import SimpleTTSProcessor


def analyze_transcript(args):
    """Analyze transcript file."""
    print(f"📄 Analyzing: {args.file}")
    
    # Load transcript
    loader = TranscriptLoader()
    transcript = loader.load_file(args.file)
    
    # Preprocess
    preprocessor = TranscriptPreprocessor()
    transcript = preprocessor.clean_text(transcript)
    transcript = preprocessor.truncate_text(transcript, max_length=15000)
    
    # Initialize LLM
    llm_manager = LLMManager(
        provider="gemini",
        model_name="gemini-2.5-flash",
        api_key=Settings.GEMINI_API_KEY
    )
    
    # Create chatbot
    chatbot = Chatbot(llm_manager=llm_manager, transcript=transcript, language=args.language)
    
    # Generate analysis
    print("\n📝 Generating summary...")
    summary = chatbot.generate_summary()
    print(f"\n{summary}\n")
    
    if args.topics:
        print("🎯 Extracting topics...")
        topics = chatbot.extract_topics()
        for i, topic in enumerate(topics, 1):
            print(f"{i}. {topic.get('topic')}: {topic.get('description')}")
        print()
    
    if args.actions:
        print("✅ Extracting action items...")
        actions = chatbot.extract_action_items_initially()
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action.get('task')} - {action.get('assignee')} ({action.get('deadline')})")
        print()
    
    if args.decisions:
        print("🎯 Extracting decisions...")
        decisions = chatbot.extract_decisions()
        for i, decision in enumerate(decisions, 1):
            print(f"{i}. {decision.get('decision')}")
        print()


def transcribe_audio(args):
    """Transcribe audio file."""
    print(f"🎙️ Transcribing: {args.audio}")
    
    stt = STTProcessor()
    result = stt.transcribe_audio(args.audio, language=args.language)
    
    if result.get("success"):
        print(f"\n✅ Transcription complete!")
        print(f"Language: {result.get('language')}")
        print(f"Duration: {result.get('duration')}s")
        print(f"\nText:\n{result.get('text')}")
        
        if args.output:
            stt.save_transcript(result.get('text'), args.output)
            print(f"\n💾 Saved to: {args.output}")
    else:
        print(f"\n❌ Error: {result.get('error')}")


def text_to_speech(args):
    """Convert text to speech."""
    print(f"🔊 Converting text to speech...")
    
    tts = SimpleTTSProcessor()
    
    # Read text from file or argument
    if args.text_file:
        with open(args.text_file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = args.text
    
    output_path = tts.text_to_speech(text, language=args.language, output_filename=args.output)
    print(f"\n✅ Audio generated: {output_path}")


def interactive_chat(args):
    """Interactive chat mode."""
    print("💬 Interactive Chat Mode")
    print("Type 'quit' or 'exit' to end\n")
    
    # Load transcript
    loader = TranscriptLoader()
    transcript = loader.load_file(args.file)
    
    # Initialize chatbot
    llm_manager = LLMManager(
        provider="gemini",
        model_name="gemini-2.5-flash",
        api_key=Settings.GEMINI_API_KEY
    )
    
    chatbot = Chatbot(llm_manager=llm_manager, transcript=transcript, language=args.language)
    
    while True:
        try:
            question = input("\n❓ You: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not question:
                continue
            
            result = chatbot.ask_question(question)
            print(f"\n🤖 AI: {result.get('answer')}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Meeting Analyzer CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze transcript
  python cli.py analyze transcript.txt --language vi --topics --actions
  
  # Transcribe audio
  python cli.py transcribe meeting.wav --language vi --output transcript.txt
  
  # Text to speech
  python cli.py tts --text "Hello world" --language en --output hello.mp3
  
  # Interactive chat
  python cli.py chat transcript.txt --language vi
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze transcript')
    analyze_parser.add_argument('file', help='Transcript file path')
    analyze_parser.add_argument('--language', '-l', default='vi', help='Output language')
    analyze_parser.add_argument('--topics', action='store_true', help='Extract topics')
    analyze_parser.add_argument('--actions', action='store_true', help='Extract action items')
    analyze_parser.add_argument('--decisions', action='store_true', help='Extract decisions')
    
    # Transcribe command
    transcribe_parser = subparsers.add_parser('transcribe', help='Transcribe audio')
    transcribe_parser.add_argument('audio', help='Audio file path')
    transcribe_parser.add_argument('--language', '-l', help='Audio language')
    transcribe_parser.add_argument('--output', '-o', help='Output transcript file')
    
    # TTS command
    tts_parser = subparsers.add_parser('tts', help='Text to speech')
    tts_parser.add_argument('--text', help='Text to convert')
    tts_parser.add_argument('--text-file', help='Text file to convert')
    tts_parser.add_argument('--language', '-l', default='en', help='Language')
    tts_parser.add_argument('--output', '-o', help='Output audio file')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Interactive chat')
    chat_parser.add_argument('file', help='Transcript file path')
    chat_parser.add_argument('--language', '-l', default='vi', help='Chat language')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    if args.command == 'analyze':
        analyze_transcript(args)
    elif args.command == 'transcribe':
        transcribe_audio(args)
    elif args.command == 'tts':
        text_to_speech(args)
    elif args.command == 'chat':
        interactive_chat(args)


if __name__ == "__main__":
    main()
