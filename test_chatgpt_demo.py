            if confirmation.get('additional_notes'):
                print(f"📝 ADDITIONAL NOTES:")
                print("-" * 20)
                print(confirmation.get('additional_notes'))
                print()
            
            # Sentiment Analysis Section
            if confirmation.get('sentiment_analysis'):
                sentiment = confirmation['sentiment_analysis']
                print(f"📊 COMPREHENSIVE SENTIMENT ANALYSIS")
                print("-" * 40)
                
                # Overall sentiment with visual indicators
                sentiment_emoji = {
                    'VERY_POSITIVE': "🚀",
                    'POSITIVE': "📈", 
                    'NEUTRAL': "➡️",
                    'NEGATIVE': "📉",
                    'VERY_NEGATIVE': "💥"
                }.get(sentiment.get('overall_sentiment', 'NEUTRAL'), "❓")
                
                sentiment_score = sentiment.get('sentiment_score', 0.5)
                score_emoji = "🟢" if sentiment_score >= 0.7 else "🟡" if sentiment_score >= 0.4 else "🔴"
                
                print(f"{sentiment_emoji} Overall Sentiment: {sentiment.get('overall_sentiment', 'NEUTRAL')}")
                print(f"{score_emoji} Sentiment Score: {sentiment_score:.1%}")
                print()
                
                print(f"🏢 Sector Analysis:")
                print(f"   {sentiment.get('sector_sentiment', 'N/A')}")
                print()
                
                print(f"📈 Market Mood:")
                print(f"   {sentiment.get('market_mood', 'N/A')}")
                print()
                
                print(f"📰 News & Events Impact:")
                print(f"   {sentiment.get('news_impact', 'N/A')}")
                print()
                
                print(f"🏛️ Economic Factors:")
                print(f"   {sentiment.get('economic_factors', 'N/A')}")
                print()
                
                print(f"🌍 Global Market Influence:")
                print(f"   {sentiment.get('global_influence', 'N/A')}")
                print()
                
                if sentiment.get('sentiment_reasoning'):
                    print(f"💭 Sentiment Reasoning:")
                    print(f"   {sentiment.get('sentiment_reasoning')}")
                    print()
            
            # Show if signal was filtered
            if signal_info.get('chatgpt_filtered', False):
                print(f"🚫 SIGNAL STATUS: FILTERED BY CHATGPT")
                print(f"   This signal was NOT sent to Telegram due to ChatGPT analysis")
            else:
                print(f"✅ SIGNAL STATUS: CONFIRMED AND SENT")
                print(f"   This signal was sent to Telegram with ChatGPT endorsement") 